"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import SymbolTable
import VMWriter


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.output_stream = output_stream
        self.symbol_table = SymbolTable.SymbolTable()
        self.vm_writer = VMWriter.VMWriter(output_stream)
        self.current_name = ""
        self.current_kind = ""
        self.current_type = ""
        self.label_counter = 0

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.label_counter = 0
        self.symbol_table = SymbolTable.SymbolTable()
        self.tokenizer.advance() #skip class
        self.current_class = self.tokenizer.get_current_token()
        self.tokenizer.advance() #skip class name
        self.tokenizer.advance() #skip {
        while self.tokenizer.get_current_token() != '}':
            if self.tokenizer.get_current_token() == 'static' or self.tokenizer.get_current_token() == 'field':
                self.compile_class_var_dec()
            elif self.tokenizer.get_current_token() == 'constructor' or self.tokenizer.get_current_token() == 'function' or self.tokenizer.get_current_token() == 'method':
                self.compile_subroutine()
            else:
                break
        self.tokenizer.advance() #skip }
        print("Compilation complete!")

    def compile_class_var_dec(self) -> None:
        kind = self.tokenizer.get_current_token()
        kind = kind.upper()
        self.tokenizer.advance()
        type = self.tokenizer.get_current_token()
        self.tokenizer.advance()

        while self.tokenizer.get_current_token() != ';':
            var_name = self.tokenizer.get_current_token()
            self.symbol_table.define(var_name, type, kind)
            self.tokenizer.advance()
            if self.tokenizer.get_current_token() == ',':
                self.tokenizer.advance()
        self.tokenizer.advance()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.label_counter = 0
        self.symbol_table.start_subroutine()
        self.current_kind = self.tokenizer.get_current_token()
        self.tokenizer.advance() #skip constructor/function/method
        self.current_type = self.tokenizer.get_current_token()
        self.tokenizer.advance() #skip void/int/char/boolean/className
        self.current_name = self.tokenizer.get_current_token()
        self.tokenizer.advance() #skip subroutine name
        self.tokenizer.advance() #skip (
        # expecting to see parameter list
        self.compile_parameter_list()
        self.tokenizer.advance() #skip )
        if self.tokenizer.get_current_token() == '{':
            self.tokenizer.advance() #skip {
            n_locals = 0
            while self.tokenizer.get_current_token() == "var":
                vars_in_dec = self.compile_var_dec()
                n_locals += vars_in_dec
            self.vm_writer.write_function(f"{self.current_class}.{self.current_name}", n_locals)

            # If it's a method, set up 'this'
            if self.current_kind == 'method':
                self.vm_writer.write_push('argument', 0)
                self.vm_writer.write_pop('pointer', 0)
            # If it's a constructor, allocate memory
            elif self.current_kind == 'constructor':
                fields_count = self.symbol_table.var_count('FIELD')
                self.vm_writer.write_push('constant', fields_count)
                self.vm_writer.write_call('Memory.alloc', 1)
                self.vm_writer.write_pop('pointer', 0)
            self.compile_statements()
        self.tokenizer.advance() #skip }

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        if self.current_kind == 'method':
            self.symbol_table.define("this", self.current_class, "ARG")
        while self.tokenizer.get_current_token() != ')':
            self.current_type = self.tokenizer.get_current_token()
            self.tokenizer.advance()  # skip type
            var_name = self.tokenizer.get_current_token()
            self.symbol_table.define(var_name, self.current_type, "ARG")
            self.tokenizer.advance()  # skip argName
            if self.tokenizer.get_current_token() == ',':
                self.tokenizer.advance()  # skip ,

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.tokenizer.advance()  # skip var
        self.current_type = self.tokenizer.get_current_token()
        self.tokenizer.advance()  # skip type
        n_locals = 0
        while self.tokenizer.get_current_token() != ';':
            n_locals += 1
            var_name = self.tokenizer.get_current_token()
            self.symbol_table.define(var_name, self.current_type, "VAR")
            self.tokenizer.advance()  # skip varName
            if self.tokenizer.get_current_token() == ',':
                self.tokenizer.advance()  # skip ,
        self.tokenizer.advance()  # skip ;
        return n_locals

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        while self.tokenizer.token_type() == 'keyword':
            if self.tokenizer.get_current_token() == 'let':
                self.compile_let()
            elif self.tokenizer.get_current_token() == 'if':
                self.compile_if()
            elif self.tokenizer.get_current_token() == 'while':
                self.compile_while()
            elif self.tokenizer.get_current_token() == 'do':
                self.compile_do()
            elif self.tokenizer.get_current_token() == 'return':
                self.compile_return()

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.tokenizer.advance() #skip do
        self.compile_subroutine_call() #subroutine call
        self.vm_writer.write_pop("temp", 0)
        self.tokenizer.advance() #skip ;

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.tokenizer.advance() #skip let
        var_name = self.tokenizer.get_current_token()
        self.tokenizer.advance() #skip varName
        kind = self.symbol_table.kind_of(var_name)
        index = self.symbol_table.index_of(var_name)
        vm_segment = self.get_vm_segment(kind)
        if self.tokenizer.get_current_token() == '[':
            self.vm_writer.write_push(vm_segment, index)
            self.tokenizer.advance() #skip [
            self.compile_expression() #expression
            self.vm_writer.write_arithmetic('add')
            self.tokenizer.advance() #skip ]
            self.tokenizer.advance() #skip =
            self.compile_expression() #expression
            self.vm_writer.write_pop('temp', 0)
            self.vm_writer.write_pop('pointer', 1)
            self.vm_writer.write_push('temp', 0)
            self.vm_writer.write_pop('that', 0)
        else:
            self.tokenizer.advance() #skip =
            self.compile_expression()
            self.vm_writer.write_pop(vm_segment, index)
        self.tokenizer.advance() #skip ;

    def compile_while(self) -> None:
        """Compiles a while statement."""
        label_exp = f"WHILE_EXP{self.label_counter}"
        label_end = f"WHILE_END{self.label_counter}"
        self.label_counter += 1

        self.vm_writer.write_label(label_exp)

        self.tokenizer.advance()  # skip while
        self.tokenizer.advance()  # skip (
        self.compile_expression()
        self.vm_writer.write_arithmetic('not')  # negate condition
        self.vm_writer.write_if(label_end)

        self.tokenizer.advance()  # skip )
        self.tokenizer.advance()  # skip {
        self.compile_statements()

        self.vm_writer.write_goto(label_exp)
        self.vm_writer.write_label(label_end)

        self.tokenizer.advance()  # skip }


    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.tokenizer.advance() #skip return
        if self.tokenizer.get_current_token() == ';':
            self.vm_writer.write_push('constant', 0)
        else:
            self.compile_expression()
        self.tokenizer.advance() #skip ;
        self.vm_writer.write_return()

    def compile_if(self) -> None:
        """Compiles a if statement."""
        label_true = f"IF_TRUE{self.label_counter}"
        label_false = f"IF_FALSE{self.label_counter}"
        label_end = f"IF_END{self.label_counter}"
        self.label_counter += 1

        self.tokenizer.advance()  # skip if
        self.tokenizer.advance()  # skip (
        self.compile_expression()

        self.vm_writer.write_if(label_true)
        self.vm_writer.write_goto(label_false)
        self.vm_writer.write_label(label_true)

        self.tokenizer.advance()  # skip )
        self.tokenizer.advance()  # skip {
        self.compile_statements()
        self.tokenizer.advance()  # skip }

        self.vm_writer.write_goto(label_end)
        self.vm_writer.write_label(label_false)

        if self.tokenizer.get_current_token() == 'else':
            self.tokenizer.advance()  # skip else
            self.tokenizer.advance()  # skip {
            self.compile_statements()
            self.tokenizer.advance()  # skip }

        self.vm_writer.write_label(label_end)


    def compile_expression(self) -> None:
        """Compiles an expression."""
        op = {'+':'add', '-':'sub', '*':
        'call Math.multiply 2', '/':'call Math.divide 2', '&amp;': 'and', '|':'or', '&lt;':'lt', '&gt;':'gt', '=':'eq','^':'shift left','#':'shift right'}
        self.compile_term()
        while self.tokenizer.get_current_token() in op:
            command = op[self.tokenizer.get_current_token()]
            self.tokenizer.advance() #skip operator
            self.compile_term()
            if command.startswith('call'):
                self.vm_writer.write_call(command.split()[1], int(command.split()[2])) #call Math.multiply 2
            else:
                self.vm_writer.write_arithmetic(command)

    def compile_term(self) -> None:
        # Handle unary operators
        if self.tokenizer.get_current_token() in ['-', '~', '^', '#']:
            command = self.tokenizer.get_current_token()
            self.tokenizer.advance()  # skip unary operator
            self.compile_term()
            if command == '-':
                self.vm_writer.write_arithmetic('neg')
            elif command == '~':
                self.vm_writer.write_arithmetic('not')
            elif command == '^':
                self.vm_writer.write_arithmetic('shift left')
            elif command == '#':
                self.vm_writer.write_arithmetic('shift right')

        # Handle parentheses expression
        elif self.tokenizer.get_current_token() == '(':
            self.tokenizer.advance()  # skip (
            self.compile_expression()
            self.tokenizer.advance()  # skip )

        # Handle identifier cases (varName, array, subroutineCall)
        elif self.tokenizer.token_type() == "identifier":
            if self.tokenizer.get_next_token() in ['.', '(']:  # subroutineCall
                self.compile_subroutine_call()
            elif self.tokenizer.get_next_token() == '[':  # array
                kind = self.symbol_table.kind_of(self.tokenizer.get_current_token())
                kind = self.get_vm_segment(kind)
                index = self.symbol_table.index_of(self.tokenizer.get_current_token())
                self.vm_writer.write_push(kind, index)
                self.tokenizer.advance()  # skip ArrayName
                self.tokenizer.advance()  # skip [
                self.compile_expression()
                self.vm_writer.write_arithmetic('add')
                self.vm_writer.write_pop('pointer', 1)
                self.vm_writer.write_push('that', 0)
                self.tokenizer.advance()  # skip ]
            else:  # varName
                kind = self.symbol_table.kind_of(self.tokenizer.get_current_token())
                kind = self.get_vm_segment(kind)
                index = self.symbol_table.index_of(self.tokenizer.get_current_token())
                self.vm_writer.write_push(kind, index)
                self.tokenizer.advance()  # skip varName

        # Handle constants
        else:
            if self.tokenizer.token_type() == "integerConstant":
                self.vm_writer.write_push('constant', int(self.tokenizer.get_current_token()))
            elif self.tokenizer.token_type() == "stringConstant":
                string = self.tokenizer.get_current_token().strip('"')
                self.vm_writer.write_push('constant', len(string))
                self.vm_writer.write_call('String.new', 1)
                for char in string:
                    self.vm_writer.write_push('constant', ord(char))
                    self.vm_writer.write_call('String.appendChar', 2)
            elif self.tokenizer.get_current_token() == 'true':
                self.vm_writer.write_push('constant', 0)
                self.vm_writer.write_arithmetic('not')
            elif self.tokenizer.get_current_token() == 'false' or self.tokenizer.get_current_token() == 'null':
                self.vm_writer.write_push('constant', 0)
            elif self.tokenizer.get_current_token() == 'this':
                self.vm_writer.write_push('pointer', 0)
            self.tokenizer.advance()

    def compile_subroutine_call(self) -> None:
        """Compiles a subroutine call."""
        n_args = 0

        if self.tokenizer.get_next_token() == '.':  # className.subroutineName or varName.methodName
            class_name = self.tokenizer.get_current_token()
            var_type = self.symbol_table.type_of(class_name)

            if var_type:  # Method call on object (like game.run())
                kind = self.get_vm_segment(self.symbol_table.kind_of(class_name))
                self.vm_writer.write_push(kind, self.symbol_table.index_of(class_name))
                class_name = var_type
                n_args = 1  # Count 'this'
            self.tokenizer.advance()  # skip className/varName
            self.tokenizer.advance()  # skip .
            subroutine_name = self.tokenizer.get_current_token()
            self.tokenizer.advance()  # skip subroutineName
        else:  # Method call in same class (like draw())
            self.vm_writer.write_push("pointer", 0)  # push this
            class_name = self.current_class
            subroutine_name = self.tokenizer.get_current_token()
            self.tokenizer.advance()  # skip subroutineName
            n_args = 1  # Count 'this'

        self.tokenizer.advance()  # skip (
        n_args += self.compile_expression_list()  # Add normal arguments
        self.vm_writer.write_call(f"{class_name}.{subroutine_name}", n_args)
        self.tokenizer.advance()  # skip )

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        n_args = 0
        if self.tokenizer.get_current_token() == ')':
            return n_args
        while True:
            self.compile_expression()
            n_args += 1
            if self.tokenizer.get_current_token() == ')':
                break
            if self.tokenizer.get_current_token() == ',':
                self.tokenizer.advance() #skip ,
        return n_args

    def get_vm_segment(self, kind: str) -> str:
        """
        Converts symbol table kinds to VM segments.
        """
        # Handle empty string or None case
        if not kind:  # This catches both None and empty string
            return "this"  # Default to 'this' for field access

        segment_map = {
            "VAR": "local",
            "ARG": "argument",
            "FIELD": "this",
            "STATIC": "static"
        }

        # Convert to uppercase and map
        kind_upper = kind.upper()
        result = segment_map.get(kind_upper)

        if result is None:
            return kind.lower()

        return result
