#!/usr/bin/env python3
"""This example demonstrates the propagation of the value error
raised by `f`"""
from multiprocess import Multiprocess

m = Multiprocess()
def f(x):
  raise ValueError('bad error')
m.add_tasks(f, [(1, )])
m.do_tasks()
m.close()
