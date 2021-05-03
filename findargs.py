import re

pat_boolean = "--([\w]*).*store_true"
pat_other = "--([\w]*).*type=([\w]*), default=(\"?[\w]*\"?)"


def parseFromSuiteName(input):
    text = input.read()
    boolean_list = re.findall(pat_boolean, text)
    print(boolean_list)
    fancy_list = re.findall(pat_other, text)
    for item in fancy_list:
        print(f"name={item[0]}, type={item[1]}, value={item[2]}")


input = open("suitename-args.txt")
parseFromSuiteName(input)


