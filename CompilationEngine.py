"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


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
        self.const_indent = 0
        self.tokenizer = input_stream
        self.output_stream = output_stream

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.output_stream.write("<class>\n")
        self.const_indent += 2
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write class
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write className
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #wrie {
        self.tokenizer.advance()
        while self.tokenizer.get_current_token() != '}':
            if self.tokenizer.get_current_token() == 'static' or self.tokenizer.get_current_token() == 'field':
                self.compile_class_var_dec()
            elif self.tokenizer.get_current_token() == 'constructor' or self.tokenizer.get_current_token() == 'function' or self.tokenizer.get_current_token() == 'method':
                self.compile_subroutine()
            else:
                break
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write }
        self.tokenizer.advance()
        self.output_stream.write("</class>\n")
        self.const_indent -= 2
        print("Compilation complete!")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.output_stream.write(" " * self.const_indent + "<classVarDec>\n")
        self.const_indent += 2
        while self.tokenizer.get_current_token() != ';':
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
            self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</classVarDec>\n")
        self.tokenizer.advance()
        print("Class variable declaration complete!")




    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.output_stream.write(" " * self.const_indent + "<subroutineDec>\n")
        self.const_indent += 2
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write constructor/function/method
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write void/type
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write subroutineName
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
                "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write (
        self.tokenizer.advance()
        self.compile_parameter_list()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
                "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write )
        self.tokenizer.advance()
        if self.tokenizer.get_current_token() == '{':
            self.output_stream.write(" " * self.const_indent + "<subroutineBody>\n")
            self.const_indent += 2
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write(
                "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write {
            self.tokenizer.advance()
            while self.tokenizer.get_current_token() == "var":
                self.compile_var_dec()
            self.compile_statements()
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write }
            self.const_indent -= 2
            self.output_stream.write(" " * self.const_indent + "</subroutineBody>\n")
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</subroutineDec>\n")
        self.tokenizer.advance()
        print("Subroutine declaration complete!")


    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.output_stream.write(" " * self.const_indent + "<parameterList>\n")
        self.const_indent += 2
        while self.tokenizer.get_current_token() != ')':
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
            self.tokenizer.advance()
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</parameterList>\n")
        print("Parameter list complete!")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.output_stream.write(" " * self.const_indent + "<varDec>\n")
        self.const_indent += 2
        while self.tokenizer.get_current_token() != ';':
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
            self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write ;
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</varDec>\n")
        self.tokenizer.advance()
        print("Variable declaration complete!")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.output_stream.write(" " * self.const_indent + "<statements>\n")
        self.const_indent += 2
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
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</statements>\n")
        print("Statements complete!")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.output_stream.write(" " * self.const_indent + "<doStatement>\n")
        self.const_indent += 2
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write do
        self.tokenizer.advance()
        self.compile_subroutine_call() #subroutine call
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")  # write ;
        self.tokenizer.advance()
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</doStatement>\n")
        print("Do statement complete!")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.output_stream.write(" " * self.const_indent + "<letStatement>\n")
        self.const_indent += 2
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write let
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write varName
        self.tokenizer.advance()
        if self.tokenizer.get_current_token() == '[':
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write [
            self.tokenizer.advance()
            self.compile_expression()
            self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write ]
            self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write =
        self.tokenizer.advance()
        self.compile_expression()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write ;
        self.tokenizer.advance()
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</letStatement>\n")
        print("Let statement complete!")


    def compile_while(self) -> None:
        """Compiles a while statement."""
        print("ENTER WHILE STATEMENT!")
        self.output_stream.write(" " * self.const_indent + "<whileStatement>\n")
        self.const_indent += 2
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write while
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write (
        self.tokenizer.advance()
        print("first token og expression", self.tokenizer.get_current_token())
        self.compile_expression()
        print("token after expression", self.tokenizer.get_current_token())
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write )
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write {
        self.tokenizer.advance()
        print("first token in while statement", self.tokenizer.get_current_token())
        self.compile_statements()
        print("token after statements in while", self.tokenizer.get_current_token())
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n") #write }
        print("last token written in while statement", self.tokenizer.get_current_token())
        self.tokenizer.advance()
        print("token out of while statement", self.tokenizer.get_current_token())
        self.output_stream.write(" " * self.const_indent + "</whileStatement>\n")
        self.const_indent -= 2
        print("While statement complete!")


    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.output_stream.write(" " * self.const_indent + "<returnStatement>\n")
        self.const_indent += 2
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write return
        self.tokenizer.advance()
        if self.tokenizer.get_current_token() != ';':
            self.compile_expression()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
        self.tokenizer.advance()
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</returnStatement>\n")
        print("Return statement complete!")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.output_stream.write(" " * self.const_indent + "<ifStatement>\n")
        self.const_indent +=2
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
        self.tokenizer.advance()
        self.compile_expression()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
        self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
        self.tokenizer.advance()
        self.compile_statements()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
        self.tokenizer.advance()
        if self.tokenizer.get_current_token() == 'else':
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
            self.tokenizer.advance()
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write(
                "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
            self.tokenizer.advance()
            self.compile_statements()
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write(
                "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
            self.tokenizer.advance()
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</ifStatement>\n")
        print("If statement complete!")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        op = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=','^','#']
        self.output_stream.write(" " * self.const_indent + "<expression>\n")
        self.const_indent += 2
        self.compile_term()
        while self.tokenizer.get_current_token() in op:
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n") #write op
            self.tokenizer.advance()
            self.compile_term()
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</expression>\n")
        print("Expression complete!")

    def compile_term(self) -> None:
        self.output_stream.write(" " * self.const_indent + "<term>\n")
        self.const_indent += 2

        # Handle unary operators
        if self.tokenizer.get_current_token() in ['-', '~','^,#']:
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write(
                "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
            self.tokenizer.advance()
            self.compile_term()

        # Handle parentheses expression
        elif self.tokenizer.get_current_token() == '(':
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write(
                "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
            self.tokenizer.advance()
            self.compile_expression()
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write(
                "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
            self.tokenizer.advance()

        # Handle identifier cases (varName, array, subroutineCall)
        elif self.tokenizer.token_type() == "identifier":
            if self.tokenizer.get_next_token() in ['.', '(']:  # subroutineCall
                self.compile_subroutine_call()
            elif self.tokenizer.get_next_token() == '[':  # array
                self.output_stream.write(" " * self.const_indent)
                self.output_stream.write(
                    "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
                self.tokenizer.advance()
                self.output_stream.write(" " * self.const_indent)
                self.output_stream.write(
                    "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
                self.tokenizer.advance()
                self.compile_expression()
                self.output_stream.write(" " * self.const_indent)
                self.output_stream.write(
                    "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
                self.tokenizer.advance()
            else:  # varName
                self.output_stream.write(" " * self.const_indent)
                self.output_stream.write(
                    "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
                self.tokenizer.advance()

        # Handle constants
        else:
            self.output_stream.write(" " * self.const_indent)
            if self.tokenizer.token_type() == "stringConstant":
                self.output_stream.write(
                    "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token()[1:-1] + "  </" + self.tokenizer.token_type() + ">" + "\n")
            else:
                self.output_stream.write(
                    "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
            self.tokenizer.advance()

        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</term>\n")
        print("Term complete!")



    def compile_subroutine_call(self) -> None:
        """Compiles a subroutine call."""
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
        self.tokenizer.advance()
        if self.tokenizer.get_current_token() == '.':
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
            self.tokenizer.advance()
            self.output_stream.write(" " * self.const_indent)
            self.output_stream.write("<" + self.tokenizer.token_type() + ">  "+ self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() +">" + "\n")
            self.tokenizer.advance()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
        self.tokenizer.advance()
        self.compile_expression_list()
        self.output_stream.write(" " * self.const_indent)
        self.output_stream.write(
            "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
        self.tokenizer.advance()

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.output_stream.write(" " * self.const_indent + "<expressionList>\n")
        self.const_indent += 2
        if self.tokenizer.get_current_token() == ')':
            self.const_indent -= 2
            self.output_stream.write(" " * self.const_indent + "</expressionList>\n")
            return
        while True:
            self.compile_expression()
            if self.tokenizer.get_current_token() == ')':
                break
            if self.tokenizer.get_current_token() == ',':
                self.output_stream.write(" " * self.const_indent)
                self.output_stream.write(
                    "<" + self.tokenizer.token_type() + ">  " + self.tokenizer.get_current_token() + "  </" + self.tokenizer.token_type() + ">" + "\n")
                self.tokenizer.advance()
        self.const_indent -= 2
        self.output_stream.write(" " * self.const_indent + "</expressionList>\n")

