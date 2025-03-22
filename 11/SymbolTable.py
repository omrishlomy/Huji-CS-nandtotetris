"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self.subroutine_table = {"name":[], "type":[], "kind":[], "index":[]}
        self.class_table = {"name":[], "type":[], "kind":[], "index":[]}

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self.subroutine_table = {"name":[], "type":[], "kind":[], "index":[]}

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope,
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind in ["STATIC", "FIELD"]:
            cur_index = self.var_count(kind)  # Get count before adding
            self.class_table["name"].append(name)
            self.class_table["type"].append(type)
            self.class_table["kind"].append(kind)
            self.class_table["index"].append(cur_index)
        else:
            cur_index = self.var_count(kind)  # Get count before adding
            self.subroutine_table["name"].append(name)
            self.subroutine_table["type"].append(type)
            self.subroutine_table["kind"].append(kind)
            self.subroutine_table["index"].append(cur_index)
    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        if kind in ["STATIC", "FIELD"]:
            return len([k for k in self.class_table["kind"] if k == kind])
        else:
            return len([k for k in self.subroutine_table["kind"] if k == kind])

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """

        if name in self.subroutine_table["name"]:
            return self.subroutine_table["kind"][self.subroutine_table["name"].index(name)]
        elif name in self.class_table["name"]:
            return self.class_table["kind"][self.class_table["name"].index(name)]
        else:
            print(f"Warning: Identifier '{name}' not found in symbol table")
            return "FIELD"  # Default to FIELD for class members

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self.subroutine_table["name"]:
            return self.subroutine_table["type"][self.subroutine_table["name"].index(name)]
        elif name in self.class_table["name"]:
            return self.class_table["type"][self.class_table["name"].index(name)]
        else:
            return ""

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self.subroutine_table["name"]:
            return self.subroutine_table["index"][self.subroutine_table["name"].index(name)]
        elif name in self.class_table["name"]:
            return self.class_table["index"][self.class_table["name"].index(name)]
        else:
            print(f"Warning: Identifier '{name}' not found in symbol table")
            return None
