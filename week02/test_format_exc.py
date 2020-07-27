from traceback import format_exc

try:
    1/0
except ZeroDivisionError as e:
    print(format_exc())

