from collections import deque

stack = deque()

# stack.append(')')
# stack.pop()


evaluation = '(1+2) * [4 - 1] + \'ale o co chodzi?\'((([[[""" '


def check(f_name):
    first = True
    with open(f_name, "r") as f:
        for line in f:
            for ch in line:
                if (ch == '(' or ch == '['):
                    stack.append(ch)
                    continue
                if (ch == '"' and (first is True)):
                    stack.append(ch)
                    first = False
                    continue
                if (ch == ')' or ch == ']' or (ch =='"' and first is False)):
                    p = stack.pop()
                    print("Popped: ", p, first)
                    if (ch == '"'):
                        first = True

check("test.txt")
print(stack)

