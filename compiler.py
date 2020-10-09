input_file = ""
input_index = 0
lineno = 1  # represent line in code (will be ++ after \n)
symbol_table = {"if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"}
key_words = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]
simple_symbols = [";","," ,":", "[", "]", "(", ")", "{", "}", "+", "-", "<"]
whitespaces = [' ', '\n', '\r', '\t', '\v', '\f']


def get_next_token():
    global input_index, input_file
    # ------------------- recognizing SYMBOL -------------------------------------------
    if input_file[input_index] in simple_symbols:
        token = input_file[input_index]
        input_index += 1
        return "SYMBOL", token
    if input_file[input_index] == "*":
        input_index += 1
        if input_index >= len(input_file) or (
                input_file[input_index] != "/" and is_in_language(input_file[input_index])):
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
        token = input_file[input_index]
        input_index += 1
        if input_index >= len(input_file):
            return "NUM", token
        while is_digit(input_file[input_index]):
            token += input_file[input_index]
            input_index += 1
            if input_index >= len(input_file):
                return "NUM", token
        if not is_letter(input_file[input_index]) and is_in_language(input_file[input_index]):
            return "NUM", token
        # todo else:   lexical error like 123d

    # ------------------- recognizing ID AND KEYWORD -------------------------------------------
    elif is_letter(input_file[input_index]):
        token = input_file[input_index]
        input_index += 1
        if input_index < len(input_file):
            while is_letter(input_file[input_index]) or is_digit(input_file[input_index]):
                token += input_file[input_index]
                input_index += 1
                if input_index >= len(input_file):
                    return return_keyword_id(token)
        if is_in_language(input_file[input_index]):
            return return_keyword_id(token)
        # todo else lexical error

    # ------------------- recognizing WHITESPACE -------------------------------------------
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

    # ------------------- recognizing COMMENT -------------------------------------------
    elif input_file[input_index] == "/":
        # todo - comment can contain any character??????
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
                            return "COMMENT", token
                        while input_file[input_index] != "*":
                            seen_star = False
                            token += input_file[input_index]
                            input_index += 1
                            if input_index >= len(input_file):
                                return  # todo return error
                        while input_file[input_index] == "*":
                            seen_star = True
                            token += input_file[input_index]
                            input_index += 1
                            if input_index >= len(input_file):
                                return  # todo return error

        # todo else lexical error


def return_keyword_id(token):
    if token in key_words:
        return "KEYWORD", token
    else:
        symbol_table.add(token)
        return "ID", token


def is_in_language(character):
    if is_digit(character) or is_letter(character) or\
            (character in simple_symbols) or (character in ["=","*","/"])\
            or (character in whitespaces):
        return True
    return False


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
    seen_next_line = True
    while input_index < len(input_file):
        token_result = get_next_token()
        if token_result is not None:

            number_of_next_line = token_result[1].count('\n')
            for i in range(0, number_of_next_line):
                seen_next_line = True
                # tokens_file.write('\n')
                lineno += 1

            if token_result[0] != "WHITESPACE" and token_result[0] != "COMMENT":
                if seen_next_line:
                    seen_next_line = False
                    if lineno != 1:
                        tokens_file.write('\n')
                    tokens_file.write(str(lineno) + ".	")
                tokens_file.write("(" + token_result[0] + ", " + token_result[1] + ")")

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
