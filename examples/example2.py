#!/usr/bin/env python3
"""This example shows multiple processes in action. Note the execution
time takes a total of 2 seconds, whereas the processes are paused for
over 4s in total"""
from time import sleep
from multiprocess import Multiprocess, Queue

def sleep_sort():
  """Sort numbers using `time.sleep`"""
  m = Multiprocess()
  q = Queue()
  def f(q, x):
    sleep(x)
    q.push(x)

  m.add_tasks(f, [(q, 1,), (q, 2,), (q, 1.5,)])
  m.do_tasks()
  m.close()
  print('SORTED')
  while not q.empty():
    print(q.pop())

sleep_sort()
