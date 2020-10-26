# zahra yousefi jamarani  97102717
# reza amini majd 97101275
input_file = ""
lexical_errors_file = open("lexical_errors.txt", "w+")
input_index = 0
lineno = 1  # represent line in code (will be ++ after \n)
symbol_table = ["if", "else", "void", "int", "while", "break", "switch",
                "default", "case", "return"]
key_words = ["if", "else", "void", "int", "while", "break", "switch",
             "default", "case", "return"]
simple_symbols = [";", ",", ":", "[", "]", "(", ")", "{", "}", "+", "-", "<"]
whitespaces = [' ', '\n', '\r', '\t', '\v', '\f']

parse_table = {
    "Program": ["$", "int", "void"],
    "DeclarationList": ["ε", "int", "void"],
    "Declaration": ["int", "void"],
    "DeclarationInitial": ["int", "void"],
    "DeclarationPrime": ["(", ";", "["],
    "VarDeclarationPrime": [";", "["],
    "FunDeclarationPrime": ["("],
    "TypeSpecifier": ["int", "void"],
    "Params": ["int", "void"],
    "ParamListVoidAbtar": ["ID", "ε"],
    "ParamList": [",", "ε"],
    "Param": ["int", "void"],
    "ParamPrime": ["[", "ε"],
    "CompoundStmt": ["{"],
    "StatementList": ["ε", "{", "break", ";", "if", "while", "return", "switch", "ID", "+", "-", "(", "NUM"],
    "Statement": ["{", "break", ";", "if", "while", "return", "switch", "ID", "+", "-", "(", "NUM"],
    "ExpressionStmt": ["break", ";", "ID", "+", "-", "(", "NUM"],
    "SelectionStmt": ["if"],
    "IterationStmt": ["while"],
    "ReturnStmt": ["return"],
    "ReturnStmtPrime": [";", "ID", "+", "-", "(", "NUM"],
    "SwitchStmt": ["switch"],
    "CaseStmts": ["ε", "case"],
    "CaseStmt": ["case"],
    "DefaultStmt": ["default", "ε"],
    "Expression": ["ID", "+", "-", "(", "NUM"],
    "B": ["=", "[", "(", "*", "+", "-", "<", "==", "ε"],
    "H": ["=", "*", "ε", "+", "-", "<", "=="],
    "SimpleExpressionZegond": ["+", "-", "(", "NUM"],
    "SimpleExpressionPrime": ["(", "*", "+", "-", "<", "==", "ε"],
    "C": ["ε", "<", "=="],
    "Relop": ["<", "=="],
    "AdditiveExpression": ["+", "-", "(", "ID", "NUM"],
    "AdditiveExpressionPrime": ["(", "*", "+", "-", "ε"],
    "AdditiveExpressionZegond": ["+", "-", "(", "NUM"],
    "D": ["ε", "+", "-"],
    "Addop": ["+", "-"],
    "Term": ["+", "-", "(", "ID", "NUM"],
    "TermPrime": ["(", "*", "ε"],
    "TermZegond": ["+", "-", "(", "NUM"],
    "G": ["*", "ε"],
    "SignedFactor": ["+", "-", "(", "ID", "NUM"],
    "SignedFactorPrime": ["(", "ε"],
    "SignedFactorZegond": ["+", "-", "(", "NUM"],
    "Factor": ["(", "ID", "NUM"],
    "VarCallPrime": ["(", "[", "ε"],
    "VarPrime": ["[", "ε"],
    "FactorPrime": ["(", "ε"],
    "FactorZegond": ["(", "NUM"],
    "Args": ["ε", "ID", "+", "-", "(", "NUM"],
    "ArgList": ["ID", "+", "-", "(", "NUM"],
    "ArgListPrime": [",", "ε"]
}


class ErrorType:
    INVALID_INPUT = 'Invalid input'
    UNCLOSED_COMMENT = 'Unclosed comment'
    UN_MATCH_COMMENT = 'Unmatched comment'
    INVALID_NUMBER = 'Invalid number'


class ErrorHandler:
    def __init__(self):
        self.lexical_errors_file = open("lexical_errors.txt", "w+")
        self.no_error_message = 'There is no lexical error.'
        self.is_exist_error = False
        self.last_line = 0

    def close_file(self):
        if not self.is_exist_error:
            self.lexical_errors_file.write(self.no_error_message)
        self.lexical_errors_file.close()

    def handle_error(self, line_number, error_type, problematic_word):
        global input_index
        # print(problematic_word)
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


error_handler = ErrorHandler()


def get_next_token_func():
    global input_index, input_file
    # ------------------- recognizing SYMBOL
    # -------------------------------------------
    if input_file[input_index] in simple_symbols:
        token = input_file[input_index]
        input_index += 1
        return "SYMBOL", token
    if input_file[input_index] == "*":
        input_index += 1
        if input_index >= len(input_file):
            return "SYMBOL", "*"
        if not is_in_language(input_file[input_index]):
            error_handler.handle_error(
                lineno,
                ErrorType.INVALID_INPUT,
                "*" + input_file[input_index]
            )
            return
        if input_file[input_index] != "/":
            return "SYMBOL", "*"
        else:
            error_handler.handle_error(
                lineno,
                ErrorType.UN_MATCH_COMMENT,
                '*/'
            )
            return

    elif input_file[input_index] == "=":
        input_index += 1
        if input_index < len(input_file) and input_file[input_index] == "=":
            input_index += 1
            return "SYMBOL", "=="
        if is_in_language(input_file[input_index]):
            return "SYMBOL", "="
        else:
            error_handler.handle_error(
                lineno,
                ErrorType.INVALID_INPUT,
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
            error_handler.handle_error(
                lineno,
                ErrorType.INVALID_NUMBER,
                token + input_file[input_index]
            )
            return
        if not is_letter(input_file[input_index]):
            return "NUM", token
        else:
            error_handler.handle_error(
                lineno,
                ErrorType.INVALID_NUMBER,
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
                error_handler.handle_error(
                    lineno,
                    ErrorType.INVALID_INPUT,
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
                                error_handler.handle_error(
                                    lineno,
                                    ErrorType.UNCLOSED_COMMENT,
                                    token[:7] + '...'
                                )
                                return  # return error
                        while input_file[input_index] == "*":
                            seen_star = True
                            token += input_file[input_index]
                            input_index += 1
                            if input_index >= len(input_file):
                                error_handler.handle_error(
                                    lineno,
                                    ErrorType.UNCLOSED_COMMENT,
                                    token[:7] + '...'
                                )
                                return  # return error
                else:
                    error_handler.handle_error(
                        lineno,
                        ErrorType.UNCLOSED_COMMENT,
                        token[:7] + '...'
                    )
                    return  # return error
            elif input_file[input_index] == '\n':
                input_index -= 1
    error_handler.handle_error(
        lineno,
        ErrorType.INVALID_INPUT,
        input_file[input_index]
    )


def return_keyword_id(token):
    if token in key_words:
        return "KEYWORD", token
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
            if token_result[0] != "WHITESPACE" and token_result[0] != "COMMENT":
                return token_result
    else:
        return "$", "$"


def start_func(input_file_name="input.txt"):
    global input_file, lineno
    try:
        file = open(input_file_name, "r")
        input_file = file.read()
    except FileNotFoundError:
        # print("input file not found!")
        end_func()
        return
    file.close()

    token = get_next_token()
    while token is None:
        token = get_next_token()
    if token[0] == "$":
        end_func()
        return
        # use token


def end_func():
    symbol_file = open("symbol_table.txt", "w+")
    for i in range(0, len(symbol_table)):
        symbol_file.write(str(i + 1) + ".	" + symbol_table[i])
        if i != len(symbol_table) - 1:
            symbol_file.write("\n")
    symbol_file.close()
    error_handler.close_file()
    return


start_func()
