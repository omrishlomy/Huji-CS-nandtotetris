"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing



class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    label_counter = 0
    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.file_name = ""

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        self.file_name = filename
    def write_add(self)->None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("A=A-1\n")
        self.output_stream.write("M=D+M\n")
    def write_sub(self)->None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("A=A-1\n")
        self.output_stream.write("M=M-D\n")
    def write_and(self)->None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("A=A-1\n")
        self.output_stream.write("M=D&M\n")
    def write_or(self)->None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("A=A-1\n")
        self.output_stream.write("M=D|M\n")
    def write_eq(self)->None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("A=A-1\n")
        self.output_stream.write("D=M-D\n")
        self.output_stream.write("@TRUE_" + str(CodeWriter.label_counter) +"\n")
        self.output_stream.write("D;JEQ\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=0\n")
        self.output_stream.write("@END_" + str(CodeWriter.label_counter) + "\n")
        self.output_stream.write("0;JMP\n")
        self.output_stream.write("(TRUE_" + str(CodeWriter.label_counter) +")" + "\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=-1\n")
        self.output_stream.write("(END_" + str(CodeWriter.label_counter) +")" + "\n")
        CodeWriter.label_counter += 1

    def write_gt(self) -> None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")  # D = y
        self.output_stream.write("@R13\n")  # R13 = y
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("D=M\n")  # D = x
        self.output_stream.write("@R14\n")  # R14 = x
        self.output_stream.write("M=D\n")
        # Check x sign
        self.output_stream.write("@CHECK_Y_" + str(self.label_counter) + "\n")
        self.output_stream.write("D;JLT\n")  # if x < 0 goto CHECK_Y
        # x >= 0
        self.output_stream.write("@R13\n")
        self.output_stream.write("D=M\n")  # D = y
        self.output_stream.write("@SAME_SIGN_" + str(self.label_counter) + "\n")
        self.output_stream.write("D;JGE\n")  # if y >= 0 goto SAME_SIGN
        self.output_stream.write("@TRUE_" + str(self.label_counter) + "\n")
        self.output_stream.write("0;JMP\n")  # x >= 0, y < 0 -> true
        # Check y when x < 0
        self.output_stream.write("(CHECK_Y_" + str(self.label_counter) + ")\n")
        self.output_stream.write("@R13\n")
        self.output_stream.write("D=M\n")  # D = y
        self.output_stream.write("@SAME_SIGN_" + str(self.label_counter) + "\n")
        self.output_stream.write("D;JLT\n")  # if y < 0 goto SAME_SIGN
        self.output_stream.write("@FALSE_" + str(self.label_counter) + "\n")
        self.output_stream.write("0;JMP\n")  # x < 0, y >= 0 -> false
        # Same sign comparison
        self.output_stream.write("(SAME_SIGN_" + str(self.label_counter) + ")\n")
        self.output_stream.write("@R13\n")  # D = y
        self.output_stream.write("D=M\n")
        self.output_stream.write("@R14\n")  # D = x - y
        self.output_stream.write("D=M-D\n")
        self.output_stream.write("@TRUE_" + str(self.label_counter) + "\n")
        self.output_stream.write("D;JGT\n")
        # False case
        self.output_stream.write("(FALSE_" + str(self.label_counter) + ")\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=0\n")
        self.output_stream.write("@END_" + str(self.label_counter) + "\n")
        self.output_stream.write("0;JMP\n")
        # True case
        self.output_stream.write("(TRUE_" + str(self.label_counter) + ")\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=-1\n")
        self.output_stream.write("(END_" + str(self.label_counter) + ")\n")
        self.label_counter += 1

    def write_lt(self) -> None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")  # D = y
        self.output_stream.write("@R13\n")  # R13 = y
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("D=M\n")  # D = x
        self.output_stream.write("@R14\n")  # R14 = x
        self.output_stream.write("M=D\n")
        # Check x sign
        self.output_stream.write("@CHECK_Y_" + str(self.label_counter) + "\n")
        self.output_stream.write("D;JLT\n")  # if x < 0 goto CHECK_Y
        # x >= 0
        self.output_stream.write("@R13\n")
        self.output_stream.write("D=M\n")  # D = y
        self.output_stream.write("@SAME_SIGN_" + str(self.label_counter) + "\n")
        self.output_stream.write("D;JGE\n")  # if y >= 0 goto SAME_SIGN
        self.output_stream.write("@FALSE_" + str(self.label_counter) + "\n")
        self.output_stream.write("0;JMP\n")  # x >= 0, y < 0 -> false
        # Check y when x < 0
        self.output_stream.write("(CHECK_Y_" + str(self.label_counter) + ")\n")
        self.output_stream.write("@R13\n")
        self.output_stream.write("D=M\n")  # D = y
        self.output_stream.write("@SAME_SIGN_" + str(self.label_counter) + "\n")
        self.output_stream.write("D;JLT\n")  # if y < 0 goto SAME_SIGN
        self.output_stream.write("@TRUE_" + str(self.label_counter) + "\n")
        self.output_stream.write("0;JMP\n")  # x < 0, y >= 0 -> true
        # Same sign comparison
        self.output_stream.write("(SAME_SIGN_" + str(self.label_counter) + ")\n")
        self.output_stream.write("@R13\n")  # D = y
        self.output_stream.write("D=M\n")
        self.output_stream.write("@R14\n")  # D = x - y
        self.output_stream.write("D=M-D\n")
        self.output_stream.write("@TRUE_" + str(self.label_counter) + "\n")
        self.output_stream.write("D;JLT\n")
        # False case
        self.output_stream.write("(FALSE_" + str(self.label_counter) + ")\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=0\n")
        self.output_stream.write("@END_" + str(self.label_counter) + "\n")
        self.output_stream.write("0;JMP\n")
        # True case
        self.output_stream.write("(TRUE_" + str(self.label_counter) + ")\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=-1\n")
        self.output_stream.write("(END_" + str(self.label_counter) + ")\n")
        self.label_counter += 1
    def write_neg(self)->None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=-M\n")
    def write_not(self)->None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M-1\n")
        self.output_stream.write("M=!M\n")
    def write_shift_left(self)->None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("A=A-1\n")
        self.output_stream.write("M=M<<D\n")
    def write_shift_right(self)->None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("A=A-1\n")
        self.output_stream.write("M=M>>D\n")
    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        if command == "add":
            self.write_add()
        elif command == "sub":
            self.write_sub()
        elif command == "and":
            self.write_and()
        elif command == "or":
            self.write_or()
        elif command == "eq":
            self.write_eq()
        elif command == "gt":
            self.write_gt()
        elif command == "lt":
            self.write_lt()
        elif command == "neg":
            self.write_neg()
        elif command == "not":
            self.write_not()
        elif command == "shiftleft":
            self.write_shift_left()
        elif command == "shiftright":
            self.write_shift_right()
    def write_push(self, segment: str, index: int) -> None:
        self.output_stream.write("@" + str(index) + "\n")
        self.output_stream.write("D=A\n")
        self.output_stream.write("@" +segment + "\n")
        self.output_stream.write("A=M+D\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")
    def write_pop(self, segment: str, index: int) -> None:
        self.output_stream.write("@" + segment + "\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@" + str(index) + "\n")
        self.output_stream.write("D=D+A\n")
        self.output_stream.write("@R13\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@R13\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
    def write_static_push(self, index: int) -> None:
        self.output_stream.write("@" + self.file_name + "." + str(index) + "\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")
    def write_static_pop(self, index: int) -> None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@" + self.file_name + "." + str(index) + "\n")
        self.output_stream.write("M=D\n")
    def write_tmp_push(self, index: int) -> None:
        self.output_stream.write("@" + str(5 + index) + "\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")
    def write_tmp_pop(self,index:int)->None:
        self.output_stream.write("@" + str(5+index) + "\n")
        self.output_stream.write("D=A\n")
        self.output_stream.write("@R13\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@R13\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")

    def write_pointer_push(self, index: int) -> None:
        self.output_stream.write("@" + str(3 + index) + "\n")  # THIS/THAT address
        self.output_stream.write("D=M\n")  # D = THIS/THAT value
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")  # Store value in stack
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")  # Increment SP
    def write_pointer_pop(self, index: int) -> None:
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n") #decrement the stack pointer
        self.output_stream.write("D=M\n") # D = value in the stack
        self.output_stream.write("@" + str(3 + index) + "\n") # THIS/THAT address
        self.output_stream.write("M=D\n") # store the value in THIS/THAT
    def write_push_constant(self, index: int) -> None:
        self.output_stream.write("@" + str(index) + "\n")
        self.output_stream.write("D=A\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")
    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.
        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        segment_map = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
        if segment == 'static':
            if command == 'C_PUSH':
                self.write_static_push(index)
            else:
                self.write_static_pop(index)
        elif segment == 'temp':
            if command == 'C_PUSH':
                self.write_tmp_push(index)
            else:
                self.write_tmp_pop(index)
        elif segment == 'pointer':
            if command == 'C_PUSH':
                self.write_pointer_push(index)
            else:
                self.write_pointer_pop(index)
        elif segment == 'constant':
            if command == 'C_PUSH':
                self.write_push_constant(index)
        elif segment in segment_map:
            base = segment_map[segment]
            if command == "C_PUSH":
                self.write_push(base, index)
            else:
                self.write_pop(base, index)

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        self.output_stream.write("(" + label + ")\n")
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write("@" + label + "\n")
        self.output_stream.write("0;JMP\n")
    
    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@" + label + "\n")
        self.output_stream.write("D;JNE\n")


    def write_branching(self, command: str, label: str) -> None:
        """Writes assembly code that is the translation of the given
        branching command.

        Args:
            command (str): "label", "goto", or "if-goto".
            label (str): the label to write.
        """
        if command == "C_LABEL":
            self.write_label(label)
        elif command == "C_GOTO":
            self.write_goto(label)
        elif command == "C_IF-GOTO":
            self.write_if(label)
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0

        self.output_stream.write("(" + function_name + ")\n")
        for i in range(n_vars):
            self.write_push_constant(0)
        self.output_stream.write("@SP\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@14\n")
        self.output_stream.write("M=D\n")
    
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        self.output_stream.write("@SP\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@debug_sp_before_call\n")
        self.output_stream.write("M=D\n")

        # push return_address // generates a label and pushes it to the stack
        self.output_stream.write("@return_address" + str(CodeWriter.label_counter) + "\n")
        self.output_stream.write("D=A\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")
        # push LCL // saves LCL of the caller
        self.output_stream.write("@LCL\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")
        # push ARG // saves ARG of the caller
        self.output_stream.write("@ARG\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")
        # push THIS // saves THIS of the caller
        self.output_stream.write("@THIS\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")
        # push THAT // saves THAT of the caller
        self.output_stream.write("@THAT\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=M+1\n")
        # ARG = SP-5-n_args // repositions ARG
        self.output_stream.write("@SP\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@5\n")
        self.output_stream.write("D=D-A\n")
        self.output_stream.write("@" + str(n_args) + "\n")
        self.output_stream.write("D=D-A\n") # D = SP-5-n_args
        self.output_stream.write("@ARG\n")
        self.output_stream.write("M=D\n")
        # LCL = SP // repositions LCL
        self.output_stream.write("@SP\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@LCL\n")
        self.output_stream.write("M=D\n")
        # goto function_name // transfers control to the callee
        self.output_stream.write("@" + function_name + "\n")
        self.output_stream.write("0;JMP\n")
        # (return_address) // injects the return address label into the code
        self.output_stream.write("(return_address" + str(CodeWriter.label_counter) + ")\n")
        CodeWriter.label_counter += 1


    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        self.output_stream.write("@SP\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@15\n")
        self.output_stream.write("M=D\n")
        # endframe = LCL // endframe is a temporary variable
        self.output_stream.write("@LCL\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@R13\n")
        self.output_stream.write("M=D\n")
        # return_address = *(endframe-5) // puts the return address in a temp var
        self.output_stream.write("@5\n")
        self.output_stream.write("A=D-A\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@R14\n")
        self.output_stream.write("M=D\n")
        # *ARG = pop() // repositions the return value for the caller
        self.output_stream.write("@SP\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@ARG\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("M=D\n")
        # SP = ARG + 1 // repositions SP for the caller
        self.output_stream.write("@ARG\n")
        self.output_stream.write("D=M+1\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=D\n")
        # THAT = *(endframe-1) // restores THAT for the caller
        self.output_stream.write("@R13\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@THAT\n")
        self.output_stream.write("M=D\n")
        # THIS = *(endframe-2) // restores THIS for the caller
        self.output_stream.write("@R13\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@THIS\n")
        self.output_stream.write("M=D\n")
        # ARG = *(endframe-3) // restores ARG for the caller
        self.output_stream.write("@R13\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@ARG\n")
        self.output_stream.write("M=D\n")
        # LCL = *(endframe-4) // restores LCL for the caller
        self.output_stream.write("@R13\n")
        self.output_stream.write("AM=M-1\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@LCL\n")
        self.output_stream.write("M=D\n")
        # goto return_address // go to the return address
        self.output_stream.write("@R14\n")
        self.output_stream.write("A=M\n")
        self.output_stream.write("0;JMP\n")

        self.output_stream.write("@SP\n")
        self.output_stream.write("D=M\n")
        self.output_stream.write("@debug_sp_final\n")
        self.output_stream.write("M=D\n")
    def function_commands(self,command:str,function_name:str,n_args:int)->None:
        if command == "C_FUNCTION":
            self.write_function(function_name,n_args)
        elif command == "C_CALL":
            self.write_call(function_name,n_args)
        elif command == "C_RETURN":
            self.write_return()
    def close(self) -> None:
        """Closes the output file."""
        self.output_stream.close()
