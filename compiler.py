# zahra yousefi jamarani  97102717
# reza amini majd 97101275

input_file = ""
input_index = 0
lineno = 1  # represent line in code (will be ++ after \n)
symbol_table = ["if", "else", "void", "int", "while", "break", "switch",
                "default", "case", "return"]
symbol_table = {(token, 0): {'token': token, 'address': 0, 'scope': 0} for token in
                symbol_table}
declaration = []
key_words = ["if", "else", "void", "int", "while", "break", "switch",
             "default", "case", "return"]
simple_symbols = [";", ",", ":", "[", "]", "(", ")", "{", "}", "+", "-", "<"]
whitespaces = [' ', '\n', '\r', '\t', '\v', '\f']
scope = 0
function_names = []
data_index = 100
temp_index = 1008
main_faction_name = "main"

parse_table = {
    ('Program', '$'): ["$"],
    ('Program', 'int'): ["DeclarationList"],
    ('Program', 'void'): ["DeclarationList"],

    ('DeclarationList', 'ε'): ["ε"],
    ('DeclarationList', 'int'): ["Declaration", "DeclarationList"],
    ('DeclarationList', 'void'): ["Declaration", "DeclarationList"],

    ('Declaration', 'int'): ["DeclarationInitial", "DeclarationPrime"],
    ('Declaration', 'void'): ["DeclarationInitial", "DeclarationPrime"],

    ('DeclarationInitial', 'int'): ["TypeSpecifier", "#set_dec_flag", "#pid", "ID"],
    ('DeclarationInitial', 'void'): ["TypeSpecifier", "#set_dec_flag", "#pid", "ID"],

    ('DeclarationPrime', '('): ["#function_dec", "FunDeclarationPrime"],
    ('DeclarationPrime', ';'): ["VarDeclarationPrime"],
    ('DeclarationPrime', '['): ["VarDeclarationPrime"],

    ('VarDeclarationPrime', ';'): [";", "#var_dec"],
    ('VarDeclarationPrime', '['): ["[", "#pnum", "NUM", "]", ";", "#array_dec"],

    ('FunDeclarationPrime', '('): ["(", "Params", ")", "CompoundStmt", "#function_return"],

    ('TypeSpecifier', 'int'): ["int", "#push_plus"],
    ('TypeSpecifier', 'void'): ["void", "#push_minus"],

    ('Params', 'int'): ["int", "#set_dec_flag", "#pid", "ID", "#int_input_var", "ParamPrime", "ParamList"],
    ('Params', 'void'): ["void", "ParamListVoidAbtar"],

    ('ParamListVoidAbtar', 'ID'): ["#set_dec_flag", "#pid", "ID", "#void_input_var", "ParamPrime", "ParamList"],
    ('ParamListVoidAbtar', 'ε'): ["ε"],

    ('ParamList', ','): [",", "Param", "ParamList"],
    ('ParamList', 'ε'): ["ε"],

    ('Param', 'int'): ["DeclarationInitial", "#int_input_var", "ParamPrime"],
    ('Param', 'void'): ["DeclarationInitial", "#void_input_var", "ParamPrime"],

    ('ParamPrime', '['): ["[", "]", "#set_as_array"],
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

    ('ExpressionStmt', 'break'): ["break", "#jp_break", ";"],
    ('ExpressionStmt', ';'): [";"],
    ('ExpressionStmt', 'ID'): ["Expression", "#pop", ";"],
    ('ExpressionStmt', '+'): ["Expression", "#pop", ";"],
    ('ExpressionStmt', '-'): ["Expression", "#pop", ";"],
    ('ExpressionStmt', '('): ["Expression", "#pop", ";"],
    ('ExpressionStmt', 'NUM'): ["Expression", "#pop", ";"],

    ('SelectionStmt', 'if'): ["if", "(", "Expression", "#save", ")",
                              "Statement", "#jpf_save", "else", "Statement", "#jp"],

    ('IterationStmt', 'while'): ["while", "(", "#label", "Expression", "#save",
                                 ")", "Statement", "#while_sym"],

    ('ReturnStmt', 'return'): ["return", "ReturnStmtPrime", "#function_return"],

    ('ReturnStmtPrime', ';'): [";"],
    ('ReturnStmtPrime', 'ID'): ["Expression", "#return_val", ";"],
    ('ReturnStmtPrime', '+'): ["Expression", "#return_val", ";"],
    ('ReturnStmtPrime', '-'): ["Expression", "#return_val", ";"],
    ('ReturnStmtPrime', '('): ["Expression", "#return_val", ";"],
    ('ReturnStmtPrime', 'NUM'): ["Expression", "#save_temp", "#return_val", ";"],

    ('SwitchStmt', 'switch'): ["switch", "#tmp_save", "(", "Expression", ")", "{",
                               "CaseStmts", "DefaultStmt", "#jp_switch", "}"],

    ('CaseStmts', 'ε'): ["ε"],
    ('CaseStmts', 'case'): ["CaseStmt", "CaseStmts"],

    ('CaseStmt', 'case'): ["case", "#pnum", "NUM", "#cmp_save", ":", "StatementList", "#jpf"],

    ('DefaultStmt', 'default'): ["default", ":", "StatementList"],
    ('DefaultStmt', 'ε'): ["ε"],

    ('Expression', 'ID'): ["#pid", "ID", "B"],
    ('Expression', '+'): ["SimpleExpressionZegond"],
    ('Expression', '-'): ["SimpleExpressionZegond"],
    ('Expression', '('): ["SimpleExpressionZegond"],
    ('Expression', 'NUM'): ["SimpleExpressionZegond"],

    ('B', '='): ["=", "Expression", "#assign"],
    ('B', '['): ["[", "Expression", "]", "#fix_address_of_array", "H"],
    ('B', '('): ["SimpleExpressionPrime"],
    ('B', '*'): ["SimpleExpressionPrime"],
    ('B', '+'): ["SimpleExpressionPrime"],
    ('B', '-'): ["SimpleExpressionPrime"],
    ('B', '<'): ["SimpleExpressionPrime"],
    ('B', '=='): ["SimpleExpressionPrime"],
    ('B', 'ε'): ["SimpleExpressionPrime"],

    ('H', '='): ["=", "Expression", "#assign"],
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
    ('C', '<'): ["Relop", "AdditiveExpression", "#compare"],
    ('C', '=='): ["Relop", "AdditiveExpression", "#compare"],

    ('Relop', '<'): ["<", "#push_plus"],
    ('Relop', '=='): ["==", "#push_minus"],

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
    ('D', '+'): ["Addop", "Term", "#add", "D"],
    ('D', '-'): ["Addop", "Term", "#add", "D"],

    ('Addop', '+'): ["+", "#push_plus"],
    ('Addop', '-'): ["-", "#push_minus"],

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

    ('G', '*'): ["*", "SignedFactor", "#multiply", "G"],
    ('G', 'ε'): ["ε"],

    ('SignedFactor', '+'): ["+", "Factor"],
    ('SignedFactor', '-'): ["-", "Factor", "#negative"],
    ('SignedFactor', '('): ["Factor"],
    ('SignedFactor', 'ID'): ["Factor"],
    ('SignedFactor', 'NUM'): ["Factor"],

    ('SignedFactorPrime', '('): ["FactorPrime"],
    ('SignedFactorPrime', 'ε'): ["FactorPrime"],

    ('SignedFactorZegond', '+'): ["+", "Factor"],
    ('SignedFactorZegond', '-'): ["-", "Factor", "#negative"],
    ('SignedFactorZegond', '('): ["FactorZegond"],
    ('SignedFactorZegond', 'NUM'): ["FactorZegond"],

    ('Factor', '('): ["(", "Expression", ")"],
    ('Factor', 'ID'): ["#pid", "ID", "VarCallPrime"],
    ('Factor', 'NUM'): ["#pnum", "NUM"],

    ('VarCallPrime', '('): ["(", "#push_func_sign", "Args", ")", "#function_call"],
    ('VarCallPrime', '['): ["VarPrime"],
    ('VarCallPrime', 'ε'): ["VarPrime"],

    ('VarPrime', '['): ["[", "Expression", "]", "#fix_address_of_array"],
    ('VarPrime', 'ε'): ["ε"],

    ('FactorPrime', '('): ["(", "#push_func_sign", "Args", ")", "#function_call"],
    ('FactorPrime', 'ε'): ["ε"],

    ('FactorZegond', '('): ["(", "Expression", ")"],
    ('FactorZegond', 'NUM'): ["#pnum", "NUM"],

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


class ScannerErrorType:
    INVALID_INPUT = 'Invalid input'
    UNCLOSED_COMMENT = 'Unclosed comment'
    UN_MATCH_COMMENT = 'Unmatched comment'
    INVALID_NUMBER = 'Invalid number'


class ParserErrorType:
    MISSING = 'Missing'
    ILLEGAL = 'Illegal'


class ErrorHandler:
    def __init__(self):
        self.lexical_errors_file = open("lexical_errors.txt", "w+")
        self.syntax_errors_file = open("syntax_errors.txt", "w+")
        self.no_error_message = 'There is no syntax error.'
        self.is_exist_lexical_error = False
        self.is_exist_syntax_error = False
        self.last_line = 0

    def close_file(self):
        if not self.is_exist_lexical_error:
            self.lexical_errors_file.write(self.no_error_message)
        self.lexical_errors_file.close()
        if not self.is_exist_syntax_error:
            self.syntax_errors_file.write(self.no_error_message)
        self.syntax_errors_file.close()

    def handle_scanner_error(self, line_number, error_type, problematic_word):
        global input_index
        self.is_exist_lexical_error = True
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
        self.is_exist_syntax_error = True
        error_message = message
        if error_message is None:
            error_message = f"{error_type} {character}"
        self.syntax_errors_file.write(
            f"#{line_number} : Syntax Error, {error_message}\n"
        )


error_handler = ErrorHandler()


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
    global data_index

    if token in key_words:
        return token, "KEYWORD"
    else:
        if (token, scope) not in symbol_table:
            symbol_table[(token, scope)] = {'token': token, 'address': data_index, 'scope': scope}
            data_index += 4
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


def get_temp_var():
    global temp_index

    temp_index += 4
    return temp_index


def findadrr(var_name):
    # print(var_name)
    a = symbol_table.get((var_name, scope))['address']  # local
    if (var_name, scope) in declaration:
        return a
    if (var_name, 0) in symbol_table:
        return symbol_table.get((var_name, 0))['address']  # global
    return a


ra = []


class ReturnClass:
    def __init__(self, return_value, return_address):
        self.return_value = return_value
        self.return_address = return_address


class FunctionDec:
    def __init__(self, name, address, return_val, start):
        self.name = name
        self.address = address
        self.return_val = return_val
        self.scope = scope
        self.param_list = []
        self.return_val_add = None
        self.start = start

    def add_param(self, param):
        self.param_list.append(param)

    def set_return_val_add(self, address):
        self.return_val_add = address


class SemanticStack:

    def __init__(self):
        self.stack = []

    def pop(self, count=1):
        for i in range(count):
            self.stack.pop()

    def push(self, element):
        self.stack.append(element)

    def top(self, count=1):
        return self.stack[len(self.stack) - count]


class CodeGen:
    def __init__(self):
        self.pb = [''] * 10000
        self.i = 1
        self.ss = SemanticStack()

    def generate(self, action, input_var):
        return getattr(self, action)(input_var)

    def pid(self, var):
        p = findadrr(var)
        self.ss.push(p)

    def set_dec_flag(self, var):
        declaration.append((var, scope))

    def push_func_sign(self, *args):
        self.ss.push("f")

    def function_return(self, *args):
        if function_names[-1].name != "main":
            self.pb[self.i] = f'(JP, @1000, ,)'
            self.i += 1

    def function_call(self, *args):
        i = 1
        param_list = []
        while self.ss.top(i) != "f":
            param_list.insert(0, self.ss.top(i))
            i += 1
        self.ss.pop(i)

        address = self.ss.top()
        values = list(symbol_table.values())
        name = ""
        for i in range(0, len(values)):
            if address == values[i]['address']:
                name = values[i]['token']
                break

        if name == "output":
            self.ss.push(param_list[0])
            self.output()
            return

        self.ss.pop()
        called_function = None
        for func in function_names:
            if func.name == name:
                called_function = func

        param_size = len(param_list)
        for index in range(0, param_size):
            self.ss.push(called_function.param_list[index][0])
            self.ss.push(str(param_list[index]))
            self.assign()
            self.ss.pop()

        self.pb[self.i] = f'(ASSIGN, #{self.i + 2}, 1000,)'
        self.i += 1
        ra.append(ReturnClass(0, self.i + 1))
        self.pb[self.i] = f'(JP, {called_function.start}, ,)'
        self.i += 1
        t1 = get_temp_var()
        self.pb[self.i] = f'(ASSIGN, 1004, {t1},)'
        self.i += 1
        if 2 <= len(ra):
            ra.pop()
            val = ra.pop()
            self.pb[self.i] = f'(ASSIGN, #{val[1]}, 1000,)'
            self.i += 1
        elif len(ra) == 1:
            ra.pop()
        self.ss.push(t1)

    def var_dec(self, *args):
        self.pb[self.i] = f'(ASSIGN, #0, {self.ss.top()},)'
        self.i += 1
        self.ss.pop(2)

    def pnum(self, var, *args):
        self.ss.push(f'#{var}')

    def save_temp(self, *args):
        t = get_temp_var()
        self.pb[self.i] = f'(ASSIGN, {self.ss.top()}, {t},)'
        self.i += 1
        self.ss.pop(1)
        self.ss.push(t)

    def array_dec(self, *args):
        global data_index
        s = self.ss.top()
        if '#' in s:
            s = int(s[1:])
            
        self.pb[self.i] = f'(ASSIGN, #{self.ss.top(2) + 4}, {self.ss.top(2)})' 
        self.i += 1
        for i in range(int(s)):
            self.pb[self.i] = f'(ASSIGN, #0, {self.ss.top(2) + (i+1) * 4})'  # !!!size of word
            self.i += 1
        data_index += (s) * 4
        self.ss.pop(3)  # todo

    def push_plus(self, *args):
        self.ss.push(1)

    def push_minus(self, *args):
        self.ss.push(2)

    def push_int(self, var, *args):
        self.ss.push(f'#{var}')

    def save(self, *args):
        self.ss.push(self.i)
        self.i += 1

    def jpf_save(self, *args):
        self.pb[self.ss.top()] = f'(JPF, {self.ss.top(2)}, {self.i + 1},)'
        self.ss.pop(2)
        self.ss.push(self.i)
        self.i += 1

    def label(self, *args):
        self.ss.push(self.i)

    def while_sym(self, *args):
        self.pb[self.ss.top()] = f'(JPF, {self.ss.top(2)}, {self.i + 1},)'
        self.pb[self.i] = f'(JP, {self.ss.top(3)}, ,)'
        self.i += 1
        self.ss.pop(3)

    def jp(self, *args):
        self.pb[self.ss.top()] = f'(JP, {self.i}, ,)'
        self.ss.pop()

    def pop(self, *args):
        self.ss.pop()

    def assign(self, *args):
        self.pb[self.i] = f'(ASSIGN, {self.ss.top()}, {self.ss.top(2)},)'
        self.ss.pop()
        self.i += 1

    def fix_address_of_array(self, *args):
        t = get_temp_var()
        self.pb[self.i] = f'(ADD, #{self.ss.top(2)}, {self.ss.top()}, {t})'
        self.i += 1
        self.ss.pop(2)
        self.ss.push(f'@{t}')

    def compare(self, *args):
        t = get_temp_var()
        if self.ss.top(2) == 1:
            self.pb[
                self.i] = f'(LT, {self.ss.top(3)}, {self.ss.top()}, {t})'
            self.i += 1
            self.ss.pop(3)
        else:
            self.pb[
                self.i] = f'(EQ, {self.ss.top()}, {self.ss.top(3)}, {t})'
            self.i += 1
            self.ss.pop(3)
        self.ss.push(t)

    def add(self, *args):
        t = get_temp_var()
        if self.ss.top(2) == 2:
            self.pb[
                self.i] = f'(SUB, {self.ss.top(3)}, {self.ss.top()}, {t})'
            self.i += 1
            self.ss.pop(3)
        else:
            self.pb[
                self.i] = f'(ADD, {self.ss.top(3)}, {self.ss.top()}, {t})'
            self.i += 1
            self.ss.pop(3)
        self.ss.push(t)

    def multiply(self, *args):
        t = get_temp_var()
        self.pb[
            self.i] = f'(MULT, {self.ss.top(2)}, {self.ss.top()}, {t})'
        self.i += 1
        self.ss.pop(2)
        self.ss.push(t)

    def negative(self, *args):
        t = get_temp_var()
        self.pb[self.i] = f'(SUB, #0, {self.ss.top()}, {t})'
        self.i += 1
        self.ss.pop()
        self.ss.push(t)

    def tmp_save(self, *args):
        self.pb[self.i] = f'(JP, {self.i + 2}, , )'
        self.i += 1
        self.ss.push(self.i)
        self.i += 1

    def jp_switch(self, *args):
        self.ss.pop()
        self.pb[self.ss.top()] = f'(JP, {self.i}, , )'
        self.ss.pop()

    def cmp_save(self, *args):
        t = get_temp_var()
        self.pb[self.i] = f'(EQ, {self.ss.top()}, {self.ss.top(2)}, {t})'
        self.i += 1
        self.ss.pop(1)
        self.ss.push(t)
        self.ss.push(self.i)
        self.i += 1

    def jpf(self, *args):
        self.pb[self.ss.top()] = f'(JPF, {self.ss.top(2)}, {self.i}, )'
        self.ss.pop(2)

    def jp_break(self, *args):
        self.pb[self.i] = f'(JP, {self.ss.top(3)}, , )'
        self.i += 1

    def function_dec(self, *args):
        global scope
        address = self.ss.top()
        values = list(symbol_table.values())
        name = ""
        for i in range(0, len(values)):
            if address == values[i]['address']:
                name = values[i]['token']
                break
        return_val = "void"
        if self.ss.top(2) == 1:
            return_val = "int"

        if name == main_faction_name:
            self.pb[0] = f'(JP, {self.i}, ,)'

        f = FunctionDec(name, address, return_val, self.i)
        self.ss.pop(2)
        function_names.append(f)
        scope += 1

    def void_input_var(self, *args):
        function_names[-1].add_param((self.ss.top(), "void"))
        self.ss.pop(1)

    def int_input_var(self, *args):
        function_names[-1].add_param((self.ss.top(), "int"))
        self.ss.pop(1)

    def set_as_array(self, *args):
        function_names[-1].param_list[-1] = (function_names[-1].param_list[-1][0], 'array')

    def return_val(self, *args):
        a = self.ss.top()
        function_names[-1].set_return_val_add(a)
        self.ss.pop(1)  # todo
        self.pb[self.i] = f'(ASSIGN, {a}, 1004,)'
        self.i += 1

    def output(self, *args):
        self.pb[self.i] = f'(PRINT, {self.ss.top()}, ,)'
        self.ss.pop()
        self.i += 1
        print(self.ss.stack)
        for i in function_names:
            print(i.name)


code_gen = CodeGen()


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

        if '#' in top_stack[1]:
            code_gen.generate(top_stack[1][1:], token[1])

        if top_stack[1] == "$":
            if token[0] == "$":
                add_to_parse_table(top_stack, parse_file)
            else:
                error_handler.handle_parser_error(lineno,
                                                  message="unexpected EOF")
            break

        if top_stack[1] in non_terminals:
            if token[0] == "$" and (
                    not (token[0] in error_parse_table[top_stack[1]])):
                error_handler.handle_parser_error(lineno,
                                                  message="unexpected EOF")
                break
            if (top_stack[1], token[0]) in parse_table or (
                    ((top_stack[1], "ε") in parse_table) and (
                    token[0] in error_parse_table[top_stack[1]])):
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
                    grammar_stack.append(top_stack)
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
                    ParserErrorType.MISSING,
                    top_stack[1]
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
    for i in range(0, len(symbol_table.keys())):
        symbol_file.write(str(i + 1) + ".	" + list(symbol_table.keys())[i][0])
        if i != len(symbol_table.keys()) - 1:
            symbol_file.write("\n")
    symbol_file.close()
    error_handler.close_file()
    return


start_func()

with open('output.txt', 'w') as f:
    for i, code in enumerate(code_gen.pb):
        if code:
            f.write(f'{i}\t{code}\n')
