import time
from typing import Callable, Iterable

'''
        flatten?   mutable?          
list       no         yes
tuple      no         no
str        yes        yes
dict       no         yes
deque      no         yes
'''


def home_brew_map(func: Callable, iterable: Iterable):
  klass = iterable.__class__
  empty = klass()
  for item in iterable:
    empty += klass([func(item)])
  return empty


def timer(func):
  def inner(*args, **kwargs):
    start = time.time()
    ret = func(*args, **kwargs)
    elapsed = time.time() - start
    print(elapsed)
    return ret
  return inner


@timer
def long_run_func(*args, **kwargs):
  print(args)
  print(kwargs)
  time.sleep(1)


def main():
  long_run_func(1, 2, 3, arg1='foobar', arg2=1)
  print(home_brew_map(lambda x: x ** x, [1, 2, 3, 4, 5]))
  print(home_brew_map(lambda x: x ** x, (1, 2, 3, 4, 5)))


if __name__ == '__main__':
  main()