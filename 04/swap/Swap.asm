// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

@i
M=0        // initialize index loop to 0
@R14
D=M
@mini
M=D        // initialize min index to the first index
@maxi
M=D        // initialize max index to the first index
@R14
A=M
D=M
@min 
M=D        // initialize min to the first element
@max
M=D        // initialize max to the first element

(LOOP)
@i
D=M
@R15
D=M-D      // check if reached end of array
@SWAP 
D;JEQ

// Get current array value for min comparison
@R14
D=M
@i
A=D+M
D=M        // get current array value
@min
D=D-M      // compare with min
@MIN 
D;JLT

// Get current array value again for max comparison
@R14
D=M
@i
A=D+M
D=M        // get current array value
@max
D=D-M      // compare with max
@MAX 
D;JGT

@CONTINUE
0;JMP

(MIN)
@R14
D=M
@i
A=D+M
D=M        // get current array value
@min
M=D        // store as new minimum
@R14
D=M
@i
D=D+M      // calculate current array position
@mini
M=D        // store the index where minimum was found
@CONTINUE
0;JMP

(MAX)
@R14
D=M
@i
A=D+M
D=M        // get current array value
@max
M=D        // store as new maximum
@R14
D=M
@i
D=D+M      // calculate current array position
@maxi
M=D        // store the index where maximum was found
@CONTINUE
0;JMP

(CONTINUE)
@i
M=M+1      // increment loop counter
@LOOP
0;JMP

(SWAP)
@max
D=M        // get max value
@mini
A=M
M=D        // put max value at min index
@min
D=M        // get min value
@maxi
A=M
M=D        // put min value at max index

(END)
@END
0;JMP


