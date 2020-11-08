# zahra yousefi jamarani  97102717
# reza amini majd 97101275
input_file = ""
input_index = 0
lineno = 1  # represent line in code (will be ++ after \n)
symbol_table = ["if", "else", "void", "int", "while", "break", "switch",
                "default", "case", "return"]
key_words = ["if", "else", "void", "int", "while", "break", "switch",
             "default", "case", "return"]
simple_symbols = [";", ",", ":", "[", "]", "(", ")", "{", "}", "+", "-", "<"]
whitespaces = [' ', '\n', '\r', '\t', '\v', '\f']

parse_table = {
    ('Program', '$'): ["$"],
    ('Program', 'int'): ["DeclarationList"],
    ('Program', 'void'): ["DeclarationList"],

    ('DeclarationList', 'ε'): ["ε"],
    ('DeclarationList', 'int'): ["Declaration", "DeclarationList"],
    ('DeclarationList', 'void'): ["Declaration", "DeclarationList"],

    ('Declaration', 'int'): ["DeclarationInitial", "DeclarationPrime"],
    ('Declaration', 'void'): ["DeclarationInitial", "DeclarationPrime"],

    ('DeclarationInitial', 'int'): ["TypeSpecifier", "ID"],
    ('DeclarationInitial', 'void'): ["TypeSpecifier", "ID"],

    ('DeclarationPrime', '('): ["FunDeclarationPrime"],
    ('DeclarationPrime', ';'): ["VarDeclarationPrime"],
    ('DeclarationPrime', '['): ["VarDeclarationPrime"],

    ('VarDeclarationPrime', ';'): [";"],
    ('VarDeclarationPrime', '['): ["[", "NUM", "]", ";"],

    ('FunDeclarationPrime', '('): ["(", "Params", ")", "CompoundStmt"],

    ('TypeSpecifier', 'int'): ["int"],
    ('TypeSpecifier', 'void'): ["void"],

    ('Params', 'int'): ["int", "ID", "ParamPrime", "ParamList"],
    ('Params', 'void'): ["void", "ParamListVoidAbtar"],

    ('ParamListVoidAbtar', 'ID'): ["ID", "ParamPrime", "ParamList"],
    ('ParamListVoidAbtar', 'ε'): ["ε"],

    ('ParamList', ','): [",", "Param", "ParamList"],
    ('ParamList', 'ε'): ["ε"],

    ('Param', 'int'): ["DeclarationInitial", "ParamPrime"],
    ('Param', 'void'): ["DeclarationInitial", "ParamPrime"],

    ('ParamPrime', '['): ["[", "]"],
    ('ParamPrime', 'ε'): ["ε"],

    ('CompoundStmt', '{'): ["{", "DeclarationList", "StatementList", "}"],

    ('StatementList', 'ε'): ["ε"],
    ('StatementList', '{'): ["Statement", "StatementList"],
    ('StatementList', 'break'): ["Statement", "StatementList"],
    ('StatementList', ';'): ["Statement", "StatementList"],
    ('StatementList', 'if'): ["Statement", "StatementList"],
    ('StatementList', 'while'): ["Statement", "StatementList"],
    ('StatementList', 'return'): ["Statement", "StatementList"],
    ('StatementList', 'switch'): ["Statement", "StatementList"],
    ('StatementList', 'ID'): ["Statement", "StatementList"],
    ('StatementList', '+'): ["Statement", "StatementList"],
    ('StatementList', '-'): ["Statement", "StatementList"],
    ('StatementList', '('): ["Statement", "StatementList"],
    ('StatementList', 'NUM'): ["Statement", "StatementList"],

    ('Statement', '{'): ["CompoundStmt"],
    ('Statement', 'break'): ["ExpressionStmt"],
    ('Statement', ';'): ["ExpressionStmt"],
    ('Statement', 'if'): ["SelectionStmt"],
    ('Statement', 'while'): ["IterationStmt"],
    ('Statement', 'return'): ["ReturnStmt"],
    ('Statement', 'switch'): ["SwitchStmt"],
    ('Statement', 'ID'): ["ExpressionStmt"],
    ('Statement', '+'): ["ExpressionStmt"],
    ('Statement', '-'): ["ExpressionStmt"],
    ('Statement', '('): ["ExpressionStmt"],
    ('Statement', 'NUM'): ["ExpressionStmt"],

    ('ExpressionStmt', 'break'): ["break", ";"],
    ('ExpressionStmt', ';'): [";"],
    ('ExpressionStmt', 'ID'): ["Expression", ";"],
    ('ExpressionStmt', '+'): ["Expression", ";"],
    ('ExpressionStmt', '-'): ["Expression", ";"],
    ('ExpressionStmt', '('): ["Expression", ";"],
    ('ExpressionStmt', 'NUM'): ["Expression", ";"],

    ('SelectionStmt', 'if'): ["if", "(", "Expression", ")", "Statement",
                              "else", "Statement"],

    ('IterationStmt', 'while'): ["while", "(", "Expression", ")", "Statement"],

    ('ReturnStmt', 'return'): ["return", "ReturnStmtPrime"],

    ('ReturnStmtPrime', ';'): [";"],
    ('ReturnStmtPrime', 'ID'): ["Expression", ";"],
    ('ReturnStmtPrime', '+'): ["Expression", ";"],
    ('ReturnStmtPrime', '-'): ["Expression", ";"],
    ('ReturnStmtPrime', '('): ["Expression", ";"],
    ('ReturnStmtPrime', 'NUM'): ["Expression", ";"],

    ('SwitchStmt', 'switch'): ["switch", "(", "Expression", ")", "{",
                               "CaseStmts", "DefaultStmt", "}"],

    ('CaseStmts', 'ε'): ["ε"],
    ('CaseStmts', 'case'): ["CaseStmt", "CaseStmts"],

    ('CaseStmt', 'case'): ["case", "NUM", ":", "StatementList"],

    ('DefaultStmt', 'default'): ["default", ":", "StatementList"],
    ('DefaultStmt', 'ε'): ["ε"],

    ('Expression', 'ID'): ["ID", "B"],
    ('Expression', '+'): ["SimpleExpressionZegond"],
    ('Expression', '-'): ["SimpleExpressionZegond"],
    ('Expression', '('): ["SimpleExpressionZegond"],
    ('Expression', 'NUM'): ["SimpleExpressionZegond"],

    ('B', '='): ["=", "Expression"],
    ('B', '['): ["[", "Expression", "]", "H"],
    ('B', '('): ["SimpleExpressionPrime"],
    ('B', '*'): ["SimpleExpressionPrime"],
    ('B', '+'): ["SimpleExpressionPrime"],
    ('B', '-'): ["SimpleExpressionPrime"],
    ('B', '<'): ["SimpleExpressionPrime"],
    ('B', '=='): ["SimpleExpressionPrime"],
    ('B', 'ε'): ["SimpleExpressionPrime"],

    ('H', '='): ["=", "Expression"],
    ('H', '*'): ["G", "D", "C"],
    ('H', 'ε'): ["G", "D", "C"],
    ('H', '+'): ["G", "D", "C"],
    ('H', '-'): ["G", "D", "C"],
    ('H', '<'): ["G", "D", "C"],
    ('H', '=='): ["G", "D", "C"],

    ('SimpleExpressionZegond', '+'): ["AdditiveExpressionZegond", "C"],
    ('SimpleExpressionZegond', '-'): ["AdditiveExpressionZegond", "C"],
    ('SimpleExpressionZegond', '('): ["AdditiveExpressionZegond", "C"],
    ('SimpleExpressionZegond', 'NUM'): ["AdditiveExpressionZegond", "C"],

    ('SimpleExpressionPrime', '('): ["AdditiveExpressionPrime", "C"],
    ('SimpleExpressionPrime', '*'): ["AdditiveExpressionPrime", "C"],
    ('SimpleExpressionPrime', '+'): ["AdditiveExpressionPrime", "C"],
    ('SimpleExpressionPrime', '-'): ["AdditiveExpressionPrime", "C"],
    ('SimpleExpressionPrime', '<'): ["AdditiveExpressionPrime", "C"],
    ('SimpleExpressionPrime', '=='): ["AdditiveExpressionPrime", "C"],
    ('SimpleExpressionPrime', 'ε'): ["AdditiveExpressionPrime", "C"],

    ('C', 'ε'): ["ε"],
    ('C', '<'): ["Relop", "AdditiveExpression"],
    ('C', '=='): ["Relop", "AdditiveExpression"],

    ('Relop', '<'): ["<"],
    ('Relop', '=='): ["<"],

    ('AdditiveExpression', '+'): ["Term", "D"],
    ('AdditiveExpression', '-'): ["Term", "D"],
    ('AdditiveExpression', '('): ["Term", "D"],
    ('AdditiveExpression', 'ID'): ["Term", "D"],
    ('AdditiveExpression', 'NUM'): ["Term", "D"],

    ('AdditiveExpressionPrime', '('): ["TermPrime", "D"],
    ('AdditiveExpressionPrime', '*'): ["TermPrime", "D"],
    ('AdditiveExpressionPrime', '+'): ["TermPrime", "D"],
    ('AdditiveExpressionPrime', '-'): ["TermPrime", "D"],
    ('AdditiveExpressionPrime', 'ε'): ["TermPrime", "D"],

    ('AdditiveExpressionZegond', '+'): ["TermZegond", "D"],
    ('AdditiveExpressionZegond', '-'): ["TermZegond", "D"],
    ('AdditiveExpressionZegond', '('): ["TermZegond", "D"],
    ('AdditiveExpressionZegond', 'NUM'): ["TermZegond", "D"],

    ('D', 'ε'): ["ε"],
    ('D', '+'): ["Addop", "Term", "D"],
    ('D', '-'): ["Addop", "Term", "D"],

    ('Addop', '+'): ["+"],
    ('Addop', '-'): ["-"],

    ('Term', '+'): ["SignedFactor", "G"],
    ('Term', '-'): ["SignedFactor", "G"],
    ('Term', '('): ["SignedFactor", "G"],
    ('Term', 'ID'): ["SignedFactor", "G"],
    ('Term', 'NUM'): ["SignedFactor", "G"],

    ('TermPrime', '('): ["SignedFactorPrime", "G"],
    ('TermPrime', '*'): ["SignedFactorPrime", "G"],
    ('TermPrime', 'ε'): ["SignedFactorPrime", "G"],

    ('TermZegond', '+'): ["SignedFactorZegond", "G"],
    ('TermZegond', '-'): ["SignedFactorZegond", "G"],
    ('TermZegond', '('): ["SignedFactorZegond", "G"],
    ('TermZegond', 'NUM'): ["SignedFactorZegond", "G"],

    ('G', '*'): ["*", "SignedFactor", "G"],
    ('G', 'ε'): ["ε"],

    ('SignedFactor', '+'): ["+", "Factor"],
    ('SignedFactor', '-'): ["-", "Factor"],
    ('SignedFactor', '('): ["Factor"],
    ('SignedFactor', 'ID'): ["Factor"],
    ('SignedFactor', 'NUM'): ["Factor"],

    ('SignedFactorPrime', '('): ["FactorPrime"],
    ('SignedFactorPrime', 'ε'): ["FactorPrime"],

    ('SignedFactorZegond', '+'): ["+", "Factor"],
    ('SignedFactorZegond', '-'): ["-", "Factor"],
    ('SignedFactorZegond', '('): ["FactorZegond"],
    ('SignedFactorZegond', 'NUM'): ["FactorZegond"],

    ('Factor', '('): ["(", "Expression", ")"],
    ('Factor', 'ID'): ["ID", "VarCallPrime"],
    ('Factor', 'NUM'): ["NUM"],

    ('VarCallPrime', '('): ["(", "Args", ")"],
    ('VarCallPrime', '['): ["VarPrime"],
    ('VarCallPrime', 'ε'): ["VarPrime"],

    ('VarPrime', '['): ["[", "Expression", "]"],
    ('VarPrime', 'ε'): ["ε"],

    ('FactorPrime', '('): ["(", "Args", ")"],
    ('FactorPrime', 'ε'): ["ε"],

    ('FactorZegond', '('): ["(", "Args", ")"],
    ('FactorZegond', 'NUM'): ["NUM"],

    ('Args', 'ε'): ["ε"],
    ('Args', 'ID'): ["ArgList"],
    ('Args', '+'): ["ArgList"],
    ('Args', '-'): ["ArgList"],
    ('Args', '('): ["ArgList"],
    ('Args', 'NUM'): ["ArgList"],

    ('ArgList', 'ID'): ["Expression", "ArgListPrime"],
    ('ArgList', '+'): ["Expression", "ArgListPrime"],
    ('ArgList', '-'): ["Expression", "ArgListPrime"],
    ('ArgList', '('): ["Expression", "ArgListPrime"],
    ('ArgList', 'NUM'): ["Expression", "ArgListPrime"],

    ('ArgListPrime', ','): [",", "Expression", "ArgListPrime"],
    ('ArgListPrime', 'ε'): ["ε"]
}

error_parse_table = {
    "DeclarationList": ['$', '{', 'break', ';', 'if', 'while', 'return',
                        'switch', 'ID', '+', '-', '(', 'NUM', '}'],
    "Declaration": ['int', 'void', '$', '{', 'break', ';', 'if', 'while',
                    'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}'],
    "DeclarationInitial": ['(', ';', '[', ',', ')'],
    "DeclarationPrime": ['int', 'void', '$', '{', 'break', ';', 'if', 'while',
                         'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}'],
    "VarDeclarationPrime": ['int', 'void', '$', '{', 'break', ';', 'if',
                            'while', 'return', 'switch', 'ID', '+', '-', '(',
                            'NUM', '}'],
    "FunDeclarationPrime": ['int', 'void', '$', '{', 'break', ';', 'if',
                            'while', 'return', 'switch', 'ID', '+', '-', '(',
                            'NUM', '}'],
    "TypeSpecifier": ["ID"],
    "Params": [')'],
    "ParamListVoidAbtar": [')'],
    "ParamList": [')'],
    "Param": [',', ')'],
    "ParamPrime": [',', ')'],
    "CompoundStmt": ['int', 'void', '$', '{', 'break', ';', 'if', 'while',
                     'return', 'switch', 'ID', '+', '-', '(', 'NUM', '}''else',
                     'case', 'default'],
    "StatementList": ['}', 'case', 'default'],
    "Statement": ['{', 'break', ';', 'if', 'while', 'return',
                  'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else',
                  'case', 'default'],
    "ExpressionStmt": ['{', 'break', ';', 'if', 'while', 'return',
                       'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else',
                       'case', 'default'],
    "SelectionStmt": ['{', 'break', ';', 'if', 'while', 'return',
                      'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else',
                      'case', 'default'],
    "IterationStmt": ['{', 'break', ';', 'if', 'while', 'return',
                      'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else',
                      'case', 'default'],
    "ReturnStmt": ['{', 'break', ';', 'if', 'while', 'return',
                   'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else',
                   'case', 'default'],
    "ReturnStmtPrime": ['{', 'break', ';', 'if', 'while', 'return',
                        'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else',
                        'case', 'default'],
    "SwitchStmt": ['{', 'break', ';', 'if', 'while', 'return',
                   'switch', 'ID', '+', '-', '(', 'NUM', '}', 'else',
                   'case', 'default'],
    "CaseStmts": ['}', 'default'],
    "CaseStmt": ['}', 'case', 'default'],
    "DefaultStmt": ['}'],
    "Expression": [';', ')', ']', ','],
    "B": [';', ')', ']', ','],
    "H": [';', ')', ']', ','],
    "SimpleExpressionZegond": [';', ')', ']', ','],
    "SimpleExpressionPrime": [';', ')', ']', ','],
    "C": [';', ')', ']', ','],
    "Relop": ['+', '-', '(', 'ID', 'NUM'],
    "AdditiveExpression": [';', ')', ']', ','],
    "AdditiveExpressionPrime": ['<', '==', ';', ')', ']', ','],
    "AdditiveExpressionZegond": ['<', '==', ';', ')', ']', ','],
    "D": ['<', '==', ';', ')', ']', ','],
    "Addop": ['+', '-', '(', 'ID', 'NUM'],
    "Term": ['+', '-', '<', '==', ';', ')', ']', ','],
    "TermPrime": ['+', '-', '<', '==', ';', ')', ']', ','],
    "TermZegond": ['+', '-', '<', '==', ';', ')', ']', ','],
    "G": ['+', '-', '<', '==', ';', ')', ']', ','],
    "SignedFactor": ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    "SignedFactorPrime": ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    "SignedFactorZegond": ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    "Factor": ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    "VarCallPrime": ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    "VarPrime": ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    "FactorPrime": ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    "FactorZegond": ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    "Args": [')'],
    "ArgList": [')'],
    "ArgListPrime": [')'],

}

non_terminals = ['Program', 'DeclarationList', 'Declaration',
                 'DeclarationInitial', 'DeclarationPrime',
                 'VarDeclarationPrime', 'FunDeclarationPrime', 'TypeSpecifier',
                 'Params', 'ParamListVoidAbtar',
                 'ParamList', 'Param', 'ParamPrime', 'CompoundStmt',
                 'StatementList', 'Statement', 'ExpressionStmt',
                 'SelectionStmt', 'IterationStmt', 'ReturnStmt',
                 'ReturnStmtPrime', 'SwitchStmt', 'CaseStmts',
                 'CaseStmt', 'DefaultStmt', 'Expression', 'B', 'H',
                 'SimpleExpressionZegond', 'SimpleExpressionPrime',
                 'C', 'Relop', 'AdditiveExpression', 'AdditiveExpressionPrime',
                 'AdditiveExpressionZegond', 'D',
                 'Addop', 'Term', 'TermPrime', 'TermZegond', 'G',
                 'SignedFactor', 'SignedFactorPrime',
                 'SignedFactorZegond', 'Factor', 'VarCallPrime', 'VarPrime',
                 'FactorPrime', 'FactorZegond', 'Args',
                 'ArgList', 'ArgListPrime']
sync_table = {}


class ScannerErrorType:
    INVALID_INPUT = 'Invalid input'
    UNCLOSED_COMMENT = 'Unclosed comment'
    UN_MATCH_COMMENT = 'Unmatched comment'
    INVALID_NUMBER = 'Invalid number'


class ParserErrorType:
    MISSING = 'Missing'
    ILLEGAL = 'Illegal'


class ErrorHandler:
    def __init__(self, scanner, parser):
        self.lexical_errors_file = open("syntax_errors.txt", "w+")
        self.no_error_message = 'There is no syntax error.'
        self.is_exist_error = False
        self.last_line = 0
        self.scanner = scanner
        self.parser = parser

    def close_file(self):
        if not self.is_exist_error:
            self.lexical_errors_file.write(self.no_error_message)
        self.lexical_errors_file.close()

    def handle_scanner_error(self, line_number, error_type, problematic_word):
        global input_index
        if self.scanner:
            self.is_exist_error = True
            if self.last_line != line_number:
                if self.last_line != 0:
                    self.lexical_errors_file.write('\n')
                self.last_line = line_number
                self.lexical_errors_file.write(str(
                    line_number) + ".	(" + problematic_word + ", " + error_type + ")")
            else:
                self.lexical_errors_file.write(
                    " (" + problematic_word + ", " + error_type + ")")
            input_index += 1

    def handle_parser_error(self, line_number, error_type=None, character=None,
                            message=None):
        if self.parser:
            self.is_exist_error = True
            error_message = message
            if error_message is None:
                error_message = f"{error_type} {character}"
            self.lexical_errors_file.write(
                f"#{line_number} : Syntax Error, {error_message}"
            )
            self.lexical_errors_file.write('\n')


error_handler = ErrorHandler(False, True)


def get_next_token_func():
    global input_index, input_file
    # ------------------- recognizing SYMBOL
    # -------------------------------------------
    if input_file[input_index] in simple_symbols:
        token = input_file[input_index]
        input_index += 1
        return token, "SYMBOL"
    if input_file[input_index] == "*":
        input_index += 1
        if input_index >= len(input_file):
            return "*", "SYMBOL"
        if not is_in_language(input_file[input_index]):
            error_handler.handle_scanner_error(
                lineno,
                ScannerErrorType.INVALID_INPUT,
                "*" + input_file[input_index]
            )
            return
        if input_file[input_index] != "/":
            return "*", "SYMBOL"
        else:
            error_handler.handle_scanner_error(
                lineno,
                ScannerErrorType.UN_MATCH_COMMENT,
                '*/'
            )
            return

    elif input_file[input_index] == "=":
        input_index += 1
        if input_index < len(input_file) and input_file[input_index] == "=":
            input_index += 1
            return "==", "SYMBOL"
        if is_in_language(input_file[input_index]):
            return "=", "SYMBOL"
        else:
            error_handler.handle_scanner_error(
                lineno,
                ScannerErrorType.INVALID_INPUT,
                "=" + input_file[input_index]
            )
            return

    # ------------------- recognizing NUM
    # -------------------------------------------
    elif is_digit(input_file[input_index]):
        token = input_file[input_index]
        input_index += 1
        if input_index >= len(input_file):
            return "NUM", token
        while is_digit(input_file[input_index]):
            token += input_file[input_index]
            input_index += 1
            if input_index >= len(input_file):
                return "NUM", token
        if not is_in_language(input_file[input_index]):
            error_handler.handle_scanner_error(
                lineno,
                ScannerErrorType.INVALID_NUMBER,
                token + input_file[input_index]
            )
            return
        if not is_letter(input_file[input_index]):
            return "NUM", token
        else:
            error_handler.handle_scanner_error(
                lineno,
                ScannerErrorType.INVALID_NUMBER,
                token + input_file[input_index]
            )
            return  # lexical error like 123d

    # ------------------- recognizing ID AND KEYWORD
    # -------------------------------------------
    elif is_letter(input_file[input_index]):
        token = input_file[input_index]
        input_index += 1
        if input_index < len(input_file):
            while is_letter(input_file[input_index]) or is_digit(
                    input_file[input_index]):
                token += input_file[input_index]
                input_index += 1
                if input_index >= len(input_file):
                    return return_keyword_id(token)
            if is_in_language(input_file[input_index]):
                return return_keyword_id(token)
            else:
                error_handler.handle_scanner_error(
                    lineno,
                    ScannerErrorType.INVALID_INPUT,
                    token + input_file[input_index]
                )
                return  # lexical error
        else:
            return return_keyword_id(token)

    # ------------------- recognizing WHITESPACE
    # -------------------------------------------
    elif input_file[input_index] in whitespaces:
        token = input_file[input_index]
        input_index += 1
        if input_index < len(input_file):
            while input_file[input_index] in whitespaces:
                token += input_file[input_index]
                input_index += 1
                if input_index >= len(input_file):
                    break
        return "WHITESPACE", token

    # ------------------- recognizing COMMENT
    # -------------------------------------------
    elif input_file[input_index] == "/":
        token = input_file[input_index]
        input_index += 1
        if input_index < len(input_file):
            if input_file[input_index] == "/":  # // comment
                token += input_file[input_index]
                input_index += 1
                if input_index < len(input_file):
                    while input_file[input_index] != '\n':
                        token += input_file[input_index]
                        input_index += 1
                        if input_index >= len(input_file):
                            break
                return "COMMENT", token
            elif input_file[input_index] == "*":  # /* */ comment
                token += input_file[input_index]
                input_index += 1
                if input_index < len(input_file):
                    seen_star = False
                    while True:
                        if seen_star and input_file[input_index] == "/":
                            input_index += 1
                            token += "/"
                            return "COMMENT", token
                        while input_file[input_index] != "*":
                            seen_star = False
                            token += input_file[input_index]
                            input_index += 1
                            if input_index >= len(input_file):
                                error_handler.handle_scanner_error(
                                    lineno,
                                    ScannerErrorType.UNCLOSED_COMMENT,
                                    token[:7] + '...'
                                )
                                return  # return error
                        while input_file[input_index] == "*":
                            seen_star = True
                            token += input_file[input_index]
                            input_index += 1
                            if input_index >= len(input_file):
                                error_handler.handle_scanner_error(
                                    lineno,
                                    ScannerErrorType.UNCLOSED_COMMENT,
                                    token[:7] + '...'
                                )
                                return  # return error
                else:
                    error_handler.handle_scanner_error(
                        lineno,
                        ScannerErrorType.UNCLOSED_COMMENT,
                        token[:7] + '...'
                    )
                    return  # return error
            elif input_file[input_index] == '\n':
                input_index -= 1
        input_index -= 1
    error_handler.handle_scanner_error(
        lineno,
        ScannerErrorType.INVALID_INPUT,
        input_file[input_index]
    )


def return_keyword_id(token):
    if token in key_words:
        return token, "KEYWORD"
    else:
        if token not in symbol_table:
            symbol_table.append(token)
        return "ID", token


def is_in_language(character):
    if is_digit(character) or is_letter(character) or \
            (character in simple_symbols) or (character in ["=", "*", "/"]) \
            or (character in whitespaces):
        return True
    return False


def is_digit(character):
    return 0 <= ord(character) - ord('0') <= 9


def is_letter(character):
    return ord('a') <= ord(character) <= ord('z') or ord('A') <= ord(
        character) <= ord('Z')


def get_next_token():
    global lineno
    if input_index < len(input_file):
        token_result = get_next_token_func()
        if token_result is not None:
            number_of_next_line = token_result[1].count('\n')
            for i in range(number_of_next_line):
                lineno += 1
            if token_result[0] != "WHITESPACE" and token_result[
                0] != "COMMENT":
                return token_result
    else:
        return "$", "$"


def start_func(input_file_name="input.txt"):
    global input_file, lineno
    try:
        file = open(input_file_name, "r")
        input_file = file.read()
    except FileNotFoundError:
        end_func()
        return
    file.close()
    parse_file = open("parse_tree.txt", "w+")
    grammar_stack = [(0, "$"), (0, "Program")]
    token = get_next_token()
    while token is None:
        token = get_next_token()
    while len(grammar_stack) != 0:
        top_stack = grammar_stack.pop()
        if top_stack[1] == "$":
            if token[0] == "$":
                add_to_parse_table(top_stack, parse_file)
            # else:
            #     error_handler.handle_parser_error(lineno, "unexpected EOF")  # todo
            break

        if top_stack[1] in non_terminals:
            if (top_stack[1], token[0]) in parse_table or (
                    (top_stack[1], "ε") in parse_table):
                depth = top_stack[0] + 1
                if (top_stack[1], token[0]) in parse_table:
                    l = parse_table[(top_stack[1], token[0])]
                else:
                    l = parse_table[(top_stack[1], "ε")]
                for j in range(len(l) - 1, -1, -1):
                    grammar_stack.append((depth, l[j]))
                add_to_parse_table(top_stack, parse_file)
                depth += 1
                continue
            else:
                if token[0] in error_parse_table[top_stack[1]]:  # synch
                    error_handler.handle_parser_error(
                        lineno,
                        ParserErrorType.MISSING,  # todo
                        top_stack[1]  # todo
                    )
                else:  # illegal
                    error_handler.handle_parser_error(
                        lineno,
                        ParserErrorType.ILLEGAL,  # todo
                        token[0]  # todo
                    )
                    token = get_next_token()
                    while token is None:
                        token = get_next_token()
                    continue

        else:  # it is terminal
            if token[0] == top_stack[1]:
                if token[0] == "ID" or token[0] == "NUM":
                    add_to_parse_table(
                        (top_stack[0], '(' + token[0] + " ," + token[1] + ')'),
                        parse_file)
                else:
                    add_to_parse_table(
                        (top_stack[0], '(' + token[1] + ", " + token[0] + ')'),
                        parse_file)
                token = get_next_token()
                while token is None:
                    token = get_next_token()
                continue
            elif top_stack[1] == "ε":
                add_to_parse_table((top_stack[0], "epsilon"), parse_file)
                continue
            else:
                error_handler.handle_parser_error(
                    lineno,
                    ParserErrorType.MISSING,  # todo
                    top_stack[1]  # todo
                )
    parse_file.close()
    end_func()


def add_to_parse_table(grammar, file):
    for i in range(0, grammar[0]):
        file.write('|\t')
    file.write(str(grammar[1]))
    file.write('\n')
    return


def end_func():
    symbol_file = open("symbol_table.txt", "w+")
    for i in range(0, len(symbol_table)):
        symbol_file.write(str(i + 1) + ".	" + symbol_table[i])
        if i != len(symbol_table) - 1:
            symbol_file.write("\n")
    symbol_file.close()
    error_handler.close_file()
    return

# start_func()
