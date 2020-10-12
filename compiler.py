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


class ErrorType:
    INVALID_INPUT = 'Invalid input'
    UNCLOSED_COMMENT = 'Unclosed comment'
    UN_MATCH_STAR_BACK_SLASH = 'Unmatched */'
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
        print(problematic_word)
        self.is_exist_error = True
        if self.last_line != line_number:
            if self.last_line != 0:
                self.lexical_errors_file.write('\n')
            self.last_line = line_number
            self.lexical_errors_file.write(str(line_number) + ".	(" + problematic_word + ", " + error_type + ")")
        else:
            self.lexical_errors_file.write(" (" + problematic_word + ", " + error_type + ")")
        input_index += 1


error_handler = ErrorHandler()


def get_next_token():
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
        if input_file[input_index] != "/":
            return "SYMBOL", "*"
        else:
            error_handler.handle_error(
                lineno,
                ErrorType.UN_MATCH_STAR_BACK_SLASH,
                '*/'
            )
            return

    elif input_file[input_index] == "=":
        input_index += 1
        if input_index < len(input_file) and input_file[input_index] == "=":
            input_index += 1
            return "SYMBOL", "=="
        return "SYMBOL", "="

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


def start_func():
    global input_file, lineno
    try:
        file = open("input.txt", "r")
        input_file = file.read()
    except FileNotFoundError:
        print("input file not found!")
        end_func()
        return
    file.close()
    tokens_file = open("tokens.txt", "w+")
    seen_next_line = True
    first_token = True
    while input_index < len(input_file):
        token_result = get_next_token()
        if token_result is not None:
            # print(token_result)
            # print(lineno)
            # print(input_index)
            number_of_next_line = token_result[1].count('\n')
            for i in range(number_of_next_line):
                seen_next_line = True
                # tokens_file.write('\n')
                lineno += 1
            if token_result[0] != "WHITESPACE" and token_result[0] != "COMMENT":
                if seen_next_line:
                    seen_next_line = False
                    if not first_token:
                        tokens_file.write('\n')
                    tokens_file.write(str(lineno) + ".	")
                first_token = False
                tokens_file.write(
                    "(" + token_result[0] + ", " + token_result[1] + ") ")

    tokens_file.close()
    end_func()


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
