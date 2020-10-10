def check_file(file_name):
    file = open("a_" + file_name + str(n) + ".txt", "r")
    answer_lines = file.readlines()
    file = open(file_name + ".txt", "r")
    my_lines = file.readlines()
    if len(my_lines) != len(answer_lines):
        print("is false <" + file_name + ">")
    for j in range(0, len(answer_lines)):
        if answer_lines[j].strip() != my_lines[j].strip():
            print("is false <" + file_name + "> in line " + str(j))
            break
    print(file_name + "----" + "ok")


n = int(input())
check_file("tokens")
check_file("symbol_table")
check_file("lexical_errors")
