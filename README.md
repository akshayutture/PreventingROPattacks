# PreventingROPattacks
This is a compiler pass that runs on the Assembly code to prevent Return-oriented-programming attacks.


A] ABOUT

	This project looks at a Compiler pass that can be run after the Assembly code (.S file) has been generated, which helps prevent ROP attacks. The pass does not completely prevent ROP attacks, but reduces the number of gadgets that the attacker can possibly use. Read the report to get more details on why this pass works.

	There are 3 folders in this project
	a) ROPattack -> demonstrates a simple ROP attack with just 1 gadget.
	b) countingGadgets -> Contains 2 program to count gadgets. 1 works for a compilation without the ROP protection pass, and 1 with it
	c) protectionFromROPPass -> contains the pass to secure your C program against ROP attacks.
	
	Now we explain each section in further detail


B] ROP ATTACK

	This folder contains a file 'vulnerableCode.c' which is a simple program with a buffer overflow vulnerability. Also, the input to be provided in order to overflow the buffer, and call the 'not_called()' function in the program is provided in the 'attackInput' file. Do the following to run this part

	- Change your directory to that of this folder. 
	- Run "gcc -m32 -O0 -fno-stack-protector --static vulnerableCode.c"
	- Copy paste the entry from the 'attackInput' file into the terminal
	- If it worked, you will see the buffer overflow happen (ROP attack with single gadget).
	- In case it does not work, the address of the 'not_called()' function might be different.
	- Run "objdump --disassemble-all a.out > vulnerable.diss" to get the dissassembly of the executable. 
	- Now, look for the address of the 'not_called()' function, and replace it with the address given in the end of the 'attackInput' file. 
	- Make sure you use the Little-Endian format for the address.
	

C] COUNTING GADGETS

	This folder contains 2 programs to count gadgets. 1 works for a compilation without the ROP protection pass, and 1 with it. 

	a) The ROPGadget-master program is the one in "https://github.com/JonathanSalwan/ROPgadget", and it computes gadgets for the case when the pass is not there. Read the README located in the folder to know how to use it.
	b) The modifiedROPgadget program is a modification in the above program, where we tag each gadget with Valid or Invalid, indicating whether or not it will work with the new pass. It will also print how many gadgets are valid, and the total number of gadgets. It works exactly like the above program and the same README can be followed. It will be observed that the number of valid gadgets is very low.
	
	- Make sure to use the "-m32 -O0 -fno-stack-protector --static" options with "gcc" when generating the executable.
	- A sample vulnerable code file has also been provided 
	- Run "python modifiedROPgadget/ROPgadget.py --binary <binaryName>"
	
	
D] PROTECTION FROM ROP PASS

	- This contains the main compiler pass that protects your code from ROP attacks. The pass is implemented in Python, and is called ropProtectionPass.py.  You can run the script "sh gccWithRopProtection.sh <input-C-file>" or "./gccWithRopProtection.sh <input-C-file>" in order to compile the <input-C-file> file along with the ROP protection pass.

	- Now try to compile the 'vulnerableCode.c' file with this command, and attempt the Buffer overflow attack. The attack will be detected and execution will be stopped.
