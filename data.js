// ALL SITE CONTENT LIVES HERE. Edit in VS Code, save, then commit and push.
// Per project: "image" = cover photo (optional). "files" = items shown on the Files page:
//   {name:"Final report", kind:"doc",   path:"docs/tap-report.pdf"}
//   {name:"Circuit photo", kind:"image", path:"images/tap-circuit.jpg"}
//   {name:"Demo video",   kind:"video", path:"videos/tap-demo.mp4"}   (or kind:"link" with a YouTube/Drive URL)
// Example: add  files:[{name:"Final report",kind:"doc",path:"docs/tap-report.pdf"}]  to any project below.
const PROJECTS=[
 {title:"Two-Office Network Simulation",type:"Networking",icon:"🌐",tone:"q",image:"images/packet-tracer-network.png",desc:"Cisco Packet Tracer design linking two offices through routers and switches, with DHCP, DNS and HTTP servers, PCs and IP phones.",files:[{name:"Network demo video",kind:"video",path:"videos/packet-tracer-demo.mp4"},{name:"Packet Tracer network topology",kind:"image",path:"images/packet-tracer-network.png"}],tags:["Packet Tracer","DHCP / DNS / HTTP","Routing"]},
 {title:"BCD Adder with Overflow Detection",type:"Electronics",icon:"🔢",tone:"r",desc:"CUMEM220 digital logic design: adds two BCD digits with gates only, flags sums above 9 and drives a seven-segment display, simulated in Proteus.",files:[{name:"BCD adder: report and Proteus files",kind:"doc",path:"docs/bcd_adder.rar"}],tags:["Logic gates","BCD","Proteus"]},
 {title:"Touchless Tap & Soap Dispenser",type:"Robotics",icon:"🚰",tone:"r",desc:"Two-phase CUT Robotics Group build: an IR-sensor tap, then a 3-in-1 system with soap, hold-to-run water and a temperature lever.",files:[],tags:["Arduino","ATmega328P","Proteus"]},
 {title:"MPI Wildlife Migration Simulation",type:"Software",icon:"🐘",tone:"q",image:"images/elephant-simulation.png",desc:"Open MPI simulation in C of elephant herds moving across terrain zones using collective communication.",files:[{name:"Source code (C, Open MPI)",kind:"doc",path:"docs/wildlife_migration.rar"},{name:"Simulation output: 4 herds, 13 days",kind:"image",path:"images/elephant-simulation.png"}],tags:["C","Open MPI","Parallel"]},
 {title:"Expression Evaluator GUI",type:"Software",icon:"🧮",tone:"s",image:"images/stack-calculator.png",desc:"Stack-based calculator built with the Shunting-Yard algorithm, with a Tkinter interface and full report.",files:[{name:"Source code (Python)",kind:"doc",path:"docs/stack_based_calculator.rar"},{name:"Stack calculator screenshot",kind:"image",path:"images/stack-calculator.png"}],tags:["Python","Tkinter","Algorithms"]},
 {title:"Campus Internet Connectivity Study",type:"Research",icon:"📡",tone:"q",desc:"Survey-based report on internet connectivity at CUT, using a structured six-step problem-solving model.",files:[],tags:["Survey","Analysis","Report"]},
 {title:"Correlation Analysis Presentation",type:"Research",icon:"📈",tone:"r",desc:"Slides and written report on correlation, supported by matplotlib charts.",files:[],tags:["Statistics","Matplotlib"]},
 {title:"OpenMP Environment Setup Guide",type:"Software",icon:"⚙️",tone:"s",desc:"Presentation walking through setting up and running OpenMP programs.",files:[],tags:["OpenMP","C","Slides"]}
];
const SKILLS=["C","Python","Arduino","ATmega328P","Proteus","MPI & OpenMP","Data structures","Statistics","Technical writing","Printing & design"];
const TOOLS=[
 {name:"VS Code",icon:"💻"},{name:"Git & GitHub",icon:"🐙"},{name:"PyCharm",icon:"🐍"},
 {name:"Proteus",icon:"🔌"},{name:"Arduino",icon:"🧰"},{name:"Open MPI",icon:"🧵"},
 {name:"OpenMP",icon:"⚙️"},{name:"Matplotlib",icon:"📊"},{name:"Word",icon:"📝"},{name:"PowerPoint",icon:"📽️"},
 {name:"MATLAB",icon:"🧮"},{name:"IntelliJ IDEA",icon:"🧠"},{name:"Notepad++",icon:"📄"},
 {name:"Cisco Packet Tracer",icon:"🌐"}
];
