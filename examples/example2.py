#!/usr/bin/env python3
from multiprocess import Multiprocess, Queue
from time import sleep

def sleep_sort():
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
    print(q.top())

sleep_sort()