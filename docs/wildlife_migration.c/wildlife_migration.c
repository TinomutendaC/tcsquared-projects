/**
 *CHISHAMBA_TINOMUTENDA_C
 *C24158396F -- BECE5
 * Assignment 1: Elephant Simulation using Open MPI
 * File: wildlife_migration.c
 * Description: Parallel simulation of elephant herd migration between Hwange 
 *              National Park and Victoria Falls across variable terrain.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <mpi.h>

#define WATERING_HOLE 200.0f
#define MAX_DAYS 1000

// Helper function for safe MPI error handling 
void check_mpi(int err, const char *msg) {
    if (err != MPI_SUCCESS) {
        fprintf(stderr, "MPI Error in %s: Code %d\n", msg, err);
        MPI_Abort(MPI_COMM_WORLD, err);
    }
}

int main(int argc, char *argv[]) {
    int rank, size, err;

    // 1. MPI Initialization 
    err = MPI_Init(&argc, &argv);
    check_mpi(err, "MPI_Init");

    err = MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    check_mpi(err, "MPI_Comm_rank");

    err = MPI_Comm_size(MPI_COMM_WORLD, &size);
    check_mpi(err, "MPI_Comm_size");

    // Movement Logic: Seeded random number generator using rank and time
    srand((unsigned int)(time(NULL) + rank * 1337));

    // Simulation state variables
    float position = 0.0f;
    int day = 0;
    int winning_rank = -1; // -1 indicates active simulation; non-negative means a herd won

    // Buffer to store gathered positions of all herds
    float *all_positions = (float *)malloc(size * sizeof(float));
    if (all_positions == NULL) {
        fprintf(stderr, "Rank %d: Memory allocation failed for all_positions buffer.\n", rank);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    // 2. Main Simulation Loop
    while (winning_rank == -1 && day < MAX_DAYS) {
        day++;

        // Base Movement Logic: Random float distance between 5 and 25 km (15 Marks)
        float base_move = (float)(5 + rand() % 21);
        float terrain_modifier = 0.0f;

        // 3. Terrain Implementation 
        if (position < 80.0f) {
            // Hwange Region (0-80 km): Open plains -> bonus +0 to +5 km
            terrain_modifier = (float)(rand() % 6);
        } else if (position >= 80.0f && position < 150.0f) {
            // Deti Vlei (81-150 km): Marshy areas -> penalty 0 to 8 km
            terrain_modifier = -(float)(rand() % 9);
        } else {
            // Victoria Falls Region (151-200+ km): Dense bush -> normal movement
            terrain_modifier = 0.0f;
        }

        float actual_move = base_move + terrain_modifier;
        
        // Strict Boundary Constraints: Movement must stay between 2 km minimum and 25 km maximum per day
        if (actual_move < 2.0f) {
            actual_move = 2.0f;
        }
        if (actual_move > 25.0f) {
            actual_move = 25.0f;
        }

        // Advance herd position
        position += actual_move;

        // 4. Collective Communication: Share positions among all processes 
        err = MPI_Allgather(&position, 1, MPI_FLOAT, all_positions, 1, MPI_FLOAT, MPI_COMM_WORLD);
        check_mpi(err, "MPI_Allgather");

        // Output Formatting: Synchronized daily status printed by Rank 0 
        if (rank == 0) {
            for (int i = 0; i < size; i++) {
                const char *terrain_desc = "";
                if (all_positions[i] < 80.0f) {
                    terrain_desc = "(Hwange Plains - Fast terrain)";
                } else if (all_positions[i] >= 80.0f && all_positions[i] < 150.0f) {
                    terrain_desc = "(Deti Vlei - Slow terrain)";
                } else {
                    terrain_desc = "(Victoria Falls Region - Dense bush)";
                }

                printf("Herd %d: Day %d - Position: %.1f km %s\n", i, day, all_positions[i], terrain_desc);
            }
            printf("----------------------------------------\n");
        }

        // 5. Termination Logic: Rank 0 checks if any herd reached/surpassed 200 km 
        if (rank == 0) {
            for (int i = 0; i < size; i++) {
                if (all_positions[i] >= WATERING_HOLE) {
                    winning_rank = i;
                    break; // Select lowest rank herd reaching the goal first
                }
            }
        }

        // 4. Collective Communication: Broadcast winning status using MPI_Bcast 
        err = MPI_Bcast(&winning_rank, 1, MPI_INT, 0, MPI_COMM_WORLD);
        check_mpi(err, "MPI_Bcast");
    }

    // 6. Winner Announcement & Summary Table 
    if (rank == 0) {
        printf("\n🏆 WINNER! Herd %d reached the watering hole at Victoria Falls in %d days!\n\n", winning_rank, day);
        
        printf("--- FINAL SUMMARY ---\n");
        for (int i = 0; i < size; i++) {
            if (i == winning_rank) {
                printf("Herd %d: Position %.1f km (WINNER - %d days)\n", i, all_positions[i], day);
            } else if (all_positions[i] >= WATERING_HOLE) {
                printf("Herd %d: Position %.1f km (Also reached but came second)\n", i, all_positions[i]);
            } else if (WATERING_HOLE - all_positions[i] <= 5.0f) {
                printf("Herd %d: Position %.1f km (Just short!)\n", i, all_positions[i]);
            } else {
                printf("Herd %d: Position %.1f km\n", i, all_positions[i]);
            }
        }

        // 7. BONUS: Conservation Status Report 
        printf("\n==============================================\n");
        printf("   CONSERVATION STATUS REPORT (ZIMPARKS)      \n");
        printf("==============================================\n");
        
        printf("1. Average Speed Per Herd:\n");
        for (int i = 0; i < size; i++) {
            float avg_speed = all_positions[i] / (float)day;
            printf("   - Herd %d: %.2f km/day\n", i, avg_speed);
        }

        printf("\n2. Terrain Delay Analysis:\n");
        printf("   - Deti Vlei Marshlands (positions 81-150 km) caused the most significant movement delays\n");
        printf("     due to negative terrain penalties (up to -8 km/day).\n");

        printf("\n3. Recommended Migration Route Strategy:\n");
        printf("   - Maintain protected corridors along Hwange Open Plains to maximize movement momentum\n");
        printf("     and establish a strong lead before encountering the Deti Vlei marsh bottleneck.\n");
        printf("==============================================\n\n");
    }

    // Resource Cleanup & MPI Finalization
    free(all_positions);
    err = MPI_Finalize();
    check_mpi(err, "MPI_Finalize");

    return 0;
}