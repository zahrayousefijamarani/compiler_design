import compiler
def check_file(file_name, file_num):
    file = open(f"test/T{file_num}/" + file_name + ".txt", "r")
    answer_lines = file.readlines()
    file.close()
    file = open(file_name + ".txt", "r")
    my_lines = file.readlines()
    file.close()
    if len(my_lines) != len(answer_lines):
        print("is false <" + file_name + ">")
    for j in range(0, len(answer_lines)):
        if answer_lines[j].strip() != my_lines[j].strip():
            print("is false <" + file_name + "> in line " + str(j + 1))
            return
    print(file_name + "----" + "ok")


i = int(input())
file_number = str(i) if i > 9 else f'0{i}'
print(f"*** start Test {file_number} ***")
compiler.start_func(f"test/T{file_number}/input.txt")
# check_file("syntax_errors", file_number)
check_file("parse_tree", file_number)
