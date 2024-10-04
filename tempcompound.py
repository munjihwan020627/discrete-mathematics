def NOT(a):
    return "F" if a == "T" else "T"


def OP(a, b, op):
    if op == "^":
        return "T" if a == "T" and b == "T" else "F"
    elif op == "v":
        return "T" if a == "T" or b == "T" else "F"
    elif op == "+":
        return "T" if a != b else "F"
    elif op == "->":
        return "F" if a == "T" and b == "F" else "T"


def cal(a):
    while '~' in a:
        i = a.index('~')
        a[i + 1] = NOT(a[i + 1])
        a.pop(i)

    while '^' in a or 'v' in a or '+' in a or '->' in a:
        for op in ['^', 'v', '+', '->']:
            while op in a:
                i = a.index(op)
                a[i - 1] = OP(a[i - 1], a[i + 1], a[i])
                a.pop(i + 1)
                a.pop(i)

    return a[0]


def MakeResult(cols, rows):
    return [["" for _ in range(cols)] for _ in range(rows)]


def initialize_table(formula, operator):
    variables = []
    table = []

    for i in formula:
        if i not in operator and i not in variables:
            variables.append(i)

    for var in variables:
        table.append(var)

    return table


def process_formula(formula, operator, table):
    for j in operator:
        if j == '~':
            for i in range(len(formula)):
                if formula[i] == '~':
                    table.append(formula[i] + " " + formula[i + 1])
                    formula[i + 1] = formula[i] + " " + formula[i + 1]
                    del formula[i]
                    formula.append('.')
        else:
            for i in range(len(formula)):
                if formula[i] == j:
                    table.append(formula[i - 1] + " " + formula[i] + " " + formula[i + 1])
                    formula[i + 1] = formula[i - 1] + " " + formula[i] + " " + formula[i + 1]
                    del formula[i]
                    formula.append('.')
                    del formula[i - 1]
                    formula.append('.')

        for i in range(len(formula)):
            if formula[i] == '.':
                del formula[i:]
                break

    return table


def calculate_truth_table(table, num):
    result = MakeResult(len(table), 2 ** num + 1)

    if num == 1:
        for i in range(len(table)):
            result[0][i] = table[i]
        result[1][0] = 'T'
        result[2][0] = 'F'
    elif num == 2:
        for i in range(len(table)):
            result[0][i] = table[i]
        result[1][0], result[1][1] = 'T', 'T'
        result[2][0], result[2][1] = 'T', 'F'
        result[3][0], result[3][1] = 'F', 'T'
        result[4][0], result[4][1] = 'F', 'F'
    elif num == 3:
        for i in range(len(table)):
            result[0][i] = table[i]
        result[1][0], result[1][1], result[1][2] = 'T', 'T', 'T'
        result[2][0], result[2][1], result[2][2] = 'T', 'T', 'F'
        result[3][0], result[3][1], result[3][2] = 'T', 'F', 'T'
        result[4][0], result[4][1], result[4][2] = 'T', 'F', 'F'
        result[5][0], result[5][1], result[5][2] = 'F', 'T', 'T'
        result[6][0], result[6][1], result[6][2] = 'F', 'T', 'F'
        result[7][0], result[7][1], result[7][2] = 'F', 'F', 'T'
        result[8][0], result[8][1], result[8][2] = 'F', 'F', 'F'

    return result


def print_result(result, num):
    for i in range(2 ** num + 1):
        for j in range(len(result[0])):
            for k in range((15 - len(result[i][j])) // 2):
                print(" ", end="")
            print(result[i][j], end=" ")
            for k in range((15 - len(result[i][j])) // 2):
                print(" ", end="")
        print("")


def main():
    print("not : ~, and : v, or : ^, xor : +, conditional proposition : ->")

    while True:
        formula = input("Enter a formula or type 'exit' to quit: ").split()

        if "exit" in formula:
            break

        operator = ['~', 'v', '^', '+', '->']

        table = initialize_table(formula, operator)
        table = process_formula(formula, operator, table)

        num = 0
        for i in table:
            if len(i) == 1:
                num += 1

        result = calculate_truth_table(table, num)

        for i in range(num, len(result[0])):
            a = result[0][i].split()
            for j in range(1, 2 ** num + 1):
                b = []
                for k in range(len(a)):
                    for l in range(num):
                        if a[k] == result[0][l]:
                            b.append(result[j][l])
                    if k == len(b) - 1:
                        continue
                    else:
                        b.append(a[k])
                result[j][i] = cal(b)

        print_result(result, num)


if __name__ == "__main__":
    main()
