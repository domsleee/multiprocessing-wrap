#!/usr/bin/env python3
from multiprocess import Multiprocess

m = Multiprocess()
def f(x):
  raise ValueError('bad error')

m.add_tasks(f, [(1,)])
m.do_tasks()
m.close()