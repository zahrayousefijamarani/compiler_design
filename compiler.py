input_file = ""
input_index = 0
lineno = 1  # represent line in code (will be ++ after \n)
symbol_table = {"if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"}
key_words = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]
simple_symbols = [";", ":", "[", "]", "(", ")", "{", "}", "+", "-", "<"]
whitespaces = [' ', '\n', '\r', '\t', '\v', '\f']


def get_next_token():
    global input_index, input_file
    token = ""
    while True:
        # todo check character be in language
        # ------------------- recognizing SYMBOL -------------------------------------------
        if input_file[input_index] in simple_symbols:
            token = input_file[input_index]
            input_index += 1
            return "SYMBOL", token
        if input_file[input_index] == "*":
            input_index += 1
            if input_file[input_index] != "/":
                return "SYMBOL", "*"
            # todo else lexical error

        elif input_file[input_index] == "=":
            input_index += 1
            if input_index < len(input_file) and input_file[input_index] == "=":
                input_index += 1
                return "SYMBOL", "=="
            return "SYMBOL", "="

        # ------------------- recognizing NUM -------------------------------------------
        elif is_digit(input_file[input_index]):
            token += input_file[input_index]
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
            # todo else:   lexical error like 123d

        # ------------------- recognizing ID AND KEYWORD -------------------------------------------
        elif is_letter(input_file[input_index]):
            token += input_file[input_index]
            input_index += 1
            if input_index < len(input_file):
                while is_letter(input_file[input_index]) or is_digit(input_file[input_index]):
                    token += input_file[input_index]
                    input_index += 1
                    if input_index >= len(input_file):
                        break
            return return_keyword_id(token)

        # ------------------- recognizing WHITESPACE -------------------------------------------
        elif input_file[input_index] in whitespaces:
            token += input_file[input_index]
            input_index += 1
            if input_index < len(input_file):
                while input_file[input_index] in whitespaces:
                    token += input_file[input_index]
                    input_index += 1
                    if input_index >= len(input_file):
                        break
            return "WHITESPACE", token

        # ------------------- recognizing COMMENT -------------------------------------------
        elif input_file[input_index] == "/":
            token += input_file[input_index]
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
                        while True:
                            while input_file[input_index] != "*":
                                token += input_file[input_index]
                                input_index += 1
                                if input_index >= len(input_file):
                                    break  # todo return error
                            while input_file[input_index] == "*" or input_file[input_index] == "/":
                                token += input_file[input_index]
                                if input_file[input_index] == "/":
                                    input_index += 1
                                    return "COMMENT", token
                                input_index += 1
                                if input_index >= len(input_file):
                                    break  # todo return error

            # todo else lexical error


def return_keyword_id(token):
    if token in key_words:
        return "KEYWORD", token
    else:
        symbol_table.add(token)
        return "ID", token


def is_digit(character):
    return 0 <= ord(character) - ord('0') <= 9


def is_letter(character):
    return ord('a') <= ord(character) <= ord('z') or ord('A') <= ord(character) <= ord('Z')


def start_func():
    global input_file, lineno
    try:
        file = open("input.txt", "r")
        input_file = file.read()
    except:  # if input.txt does not found
        end_func()
        return
    file.close()
    tokens_file = open("tokens.txt", "w+")

    while input_index < len(input_file):
        token_result = get_next_token()
        if token_result[0] != "WHITESPACE" and token_result[0] != "COMMENT":
            tokens_file.write("(" + token_result[0] + "," + token_result[1] + ")")
        number_of_next_line = token_result[1].count('\n')
        for i in range(0, number_of_next_line):
            tokens_file.write('\n')
            lineno += 1

    tokens_file.close()
    end_func()


def end_func():
    symbol_file = open("symbol_table.txt", "w+")
    symbol_list = list(symbol_table)
    for i in range(0, len(symbol_list)):
        symbol_file.write(symbol_list[i])
        if i != len(symbol_list) - 1:
            symbol_file.write("\n")
    symbol_file.close()
    return


start_func()
