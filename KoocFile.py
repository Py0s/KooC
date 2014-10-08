
from KoocGrammar import KoocG

includePath = "./"

importedFileNames = []
modules = []
classes = []

# modules = [ module = [ symbol, ... ], ...]

def kooc_a_file(koocFileName):
    cparse = KoocG()
    ast = cparse.parse_file(koocFileName)
    return ast

def register_file(fileName):
    importedFileNames.append(fileName)
def register_class(className):
    classes.append(className)
def register_module(moduleName):
    modules.append(moduleName)

def register_class_function(className, mangledFunctionName):
    classes[className].append(mangledFunctionName)
def register_module_function(moduleName, mangledFunctionName):
    modules[moduleName].append(mangledFunctionName)

def is_file_imported(fileName):
    return fileName in importedFileNames
def is_module_function(mangledFunctionName):
    for module in modules:
        for symbol in module:
            if symbol == mangledFunctionName:
                return True
    return False
def is_class_function(mangledFunctionName):
    for classe in classes:
        for symbol in classe:
            if symbol == mangledFunctionName:
                return True
    return False
