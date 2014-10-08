#!/usr/bin/env python3

from pyrser.grammar import Grammar
from pyrser import meta, fmt
from cnorm import nodes
from cnorm.passes import to_c
import os
import KoocFile

class   Import(Grammar):
    entry = 'translation_unit'
    grammar = """
        import = [ @ignore("blanks") "@import" Import.Name:name #Imp(current_block, name) ]
        Name = [ '"'
                [ ['a'..'z'] | ['A'..'Z'] | '_' ]+
                ".kh" '"' ]
    """

class ImportNode(nodes.BlockStmt):
    """Import"""

    def __init__(self, name):
        self.name = name
        self.cut_header_name()
        body = nodes.Raw("")
        self.already_imported = KoocFile.is_file_imported(self.fileNameMacro)
        if not self.already_imported:
            self.ifndef = nodes.Raw("#ifndef " + self.fileNameMacro)
            self.define = nodes.Raw("# define " + self.fileNameMacro)
            self.endif = nodes.Raw("#endif /* " + self.fileNameMacro + " */")
            KoocFile.register_file(self.fileNameMacro)
            body = KoocFile.kooc_a_file(self.fileName + ".kh")
        super().__init__(body)

    def cut_header_name(self):
        self.name = KoocFile.includePath + "/" + self.name[1:]
        self.fileName, fileExtension = os.path.splitext(self.name)
        self.fileNameMacro = (self.fileName.upper() + "_H_").replace("\\", "_").replace(".", "_").replace("/", "_")

    def to_c(self):
        if self.already_imported:
            return fmt.sep("", [])
        lsbody = []
        lsbody.append(self.ifndef.to_c())
        lsbody.append(self.define.to_c()) 
        lsbody.append(self.body.to_c())
        lsbody.append(self.endif.to_c())
        return fmt.end("\n\n", fmt.tab(fmt.sep("\n", lsbody)))


@meta.hook(Import)
def Imp(self, ast, name):
    ast.ref.body.append(ImportNode(self.value(name)))
    return True
