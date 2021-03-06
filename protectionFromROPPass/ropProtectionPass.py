import sys
import re

#main function
def main():
	'''INITIALIZATION AND FILE READING'''
	#initialization
	codeToBeInstrumentedFile = "codeToBeInstrumented"
	inputFileStringArray = []
	outputFileStringArray = []
	codeToBeInstrumentedStringArray = []

	#Read the command line arguments for input and output assembly code file names, and the code to be instrumented
	inputFile = sys.argv[1]
	outputFile = sys.argv[2]

	#Read the input file into the inputFileStringArray
	with open(inputFile,"r") as f:
		lines = f.readlines()

	for line in lines: 
		inputFileStringArray.append(line)

	
	
	'''
	INSTRUMENTING THE CODE
	'''
	retCount = 0
	#Loop through the input file to find the 'ret' instructions
	for inputLine in inputFileStringArray:
		#Remove white spaces and non ascii characters from the input line
		x = inputLine
		re.sub(r'[^\x00-\x7F]+','', x)
		x = ''.join([i if ord(i) < 128 else '' for i in x])
		x = ''.join(x.split())
		#If the input line is a 'ret' instruction, add the code to be instrumented
		if x=="ret":
			retCount = retCount + 1
			outputFileStringArray.append(getCodeToBeInstrumented(retCount))
		#Add the input line to the output string
		outputFileStringArray.append(inputLine)

	'''
	WRITING INSTRUMENTED CODE TO THE OUTPUT
	'''
	with open(outputFile, 'w') as f:
		for line in outputFileStringArray:
			f.write(line)
		
	
#Fetches the code string to be instrumented. Modifies the string based on the input index variable
#The reason for this modification is that every instrumentation needs to have unique labels. The index makes the label unique
def getCodeToBeInstrumented(index):		
	codeToBeInstrumented = """		
	/* CODE INSTRUMENTATION START */
	/*if (int)(*(ptr-3))==232 (checking for e8 opcode at 3 bytes behind)*/
		movl	(%esp), %eax
		subl	$3, %eax
		movzbl	(%eax), %eax
		cmpb	$232, %al
		je	.LRopProtPass7i""" + str(index) + """
	/*if (int)(*(ptr-5))==232  (checking for e8 opcode at 5 bytes behind)*/
		movl	(%esp), %eax
		subl	$5, %eax
		movzbl	(%eax), %eax
		cmpb	$232, %al
		je	.LRopProtPass7i""" + str(index) + """
	/*if (int)(*(ptr-2))==255 (checking for ff opcode at 2 bytes behind)*/
		movl	(%esp), %eax
		subl	$2, %eax
		movzbl	(%eax), %eax
		cmpb	$255, %al
		jne	.LRopProtPass4i""" + str(index) + """
	/*if (((int)(*(ptr-1)))/8)%8==2 (checking for ff opcode at 2 bytes behind - making the additional check of the \2 in the opcode)*/
		movl	(%esp), %eax
		subl	$1, %eax
		movzbl	(%eax), %eax
		leal	7(%eax), %edx
		testb	%al, %al
		cmovs	%edx, %eax
		sarb	$3, %al
		movl	%eax, %edx
		sarb	$7, %dl
		shrb	$5, %dl
		addl	%edx, %eax
		andl	$7, %eax
		subl	%edx, %eax
		cmpb	$2, %al
		je	.LRopProtPass7i""" + str(index) + """
.LRopProtPass4i""" + str(index) + """:
	/*if (int)(*(ptr-4))==255 (checking for ff opcode at 4 bytes behind)*/
		movl	(%esp), %eax
		subl	$4, %eax
		movzbl	(%eax), %eax
		cmpb	$255, %al
		jne	.LRopProtPass5i""" + str(index) + """
	/*if (((int)(*(ptr-3)))/8)%8==2 (checking for ff opcode at 4 bytes behind - making the additional check of the \2 in the opcode)*/
		movl	(%esp), %eax
		subl	$3, %eax
		movzbl	(%eax), %eax
		leal	7(%eax), %edx
		testb	%al, %al
		cmovs	%edx, %eax
		sarb	$3, %al
		movl	%eax, %edx
		sarb	$7, %dl
		shrb	$5, %dl
		addl	%edx, %eax
		andl	$7, %eax
		subl	%edx, %eax
		cmpb	$2, %al
		je	.LRopProtPass7i""" + str(index) + """
	.LRopProtPass5i""" + str(index) + """:
	/*if (int)(*(ptr-4))==255 (checking for ff opcode at 6 bytes behind)*/
		movl	(%esp), %eax
		subl	$6, %eax
		movzbl	(%eax), %eax
		cmpb	$255, %al
		jne	.LRopProtPass6i""" + str(index) + """
	/*if (((int)(*(ptr-5)))/8)%8==2 (checking for ff opcode at 6 bytes behind - making the additional check of the \2 in the opcode)*/
		movl	(%esp), %eax
		subl	$5, %eax
		movzbl	(%eax), %eax
		leal	7(%eax), %edx
		testb	%al, %al
		cmovs	%edx, %eax
		sarb	$3, %al
		movl	%eax, %edx
		sarb	$7, %dl
		shrb	$5, %dl
		addl	%edx, %eax
		andl	$7, %eax
		subl	%edx, %eax
		cmpb	$2, %al
		je	.LRopProtPass7i""" + str(index) + """
	.LRopProtPass6i""" + str(index) + """:
	/*If you reached this point, you did not find any call instruction behind the return address. Exit*/
		movl	$.LCRopProtPassStri""" + str(index) + """, (%esp)
		call	puts
		movl	$1, (%esp)
		call	exit
	.LCRopProtPassStri""" + str(index) + """:
		.string	\"----ROP-PROTECTOR:Buffer Overflow attack attempted. Terminating Program -----\"
	.LRopProtPass7i""" + str(index) + """:

	/* CODE INSTRUMENTATION END */
	"""
	return codeToBeInstrumented

#Execution starts here	
if __name__ == '__main__':
    main()
