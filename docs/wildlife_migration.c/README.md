# README.md

## Zimbabwe National Parks Wildlife Migration Simulation using Open MPI

### Project Overview

This parallel simulation models elephant herds migrating 200 km from Hwange National Park to the Victoria Falls watering hole across various terrain types (Hwange Plains, Deti Vlei, Victoria Falls). Each herd acts as an independent MPI process, synchronizing daily progress using collective communication primitives (`MPI_Allgather` and `MPI_Bcast`).

### Prerequisites (Windows)

1. **MinGW-w64 (GCC Compiler)** installed and added to your system `PATH`.
2. **Microsoft MPI (MS-MPI v10.0+)** SDK and Redistributable installed.

### File Structure

* **`wildlife_migration.c`**: Primary C source code containing MPI simulation logic, terrain algorithms, collective communication, error handling, and report generation.


* **`README.md`**: Compilation and execution instructions for Windows Command Prompt (`cmd`).

### Step 1: Open Command Prompt

1. Press `Win + R`, type **`cmd`**, and press **Enter**.
2. Navigate to your project folder:
```cmd
cd C:\Users\YourName\Documents\Wildlife_Migration

```
### Step 2: Compilation Instructions (Windows CMD)

Compile the C source file using `gcc` while pointing directly to your MS-MPI include and library directories:

```cmd
gcc wildlife_migration.c -o wildlife_migration.exe -I"C:\Program Files (x86)\Microsoft SDKs\MPI\Include" -L"C:\Program Files (x86)\Microsoft SDKs\MPI\Lib\x64" -lmsmpi

```
### Step 3: Execution Instructions (Windows CMD)

Run the executable using `mpiexec` with your chosen number of parallel processes (elephant herds):

```cmd
mpiexec -n 4 wildlife_migration.exe

```
*(Replace `4` with any desired number of herd processes, e.g., `-n 6`).*

### Technical Implementation Details

* **`MPI_Init` & `MPI_Finalize**`: Initializes and terminates the parallel execution environment.
* **`check_mpi` Function**: Custom error-handling wrapper to check return codes and safely call `MPI_Abort` upon failure.
* **`MPI_Comm_rank` & `MPI_Comm_size**`: Identifies individual process ranks (Herd IDs) and total process count.
* **`MPI_Allgather`**: Gathers floating-point position data from all herds to Process 0 for synchronized daily console logging.
* **`MPI_Bcast`**: Broadcasts the winning herd rank from Process 0 to all other processes to trigger parallel termination.
