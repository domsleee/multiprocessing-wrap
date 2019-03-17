# multiprocess

A simple interface for writing concurrent scripts.

## Installation

To install using pip:

~~~bash
pip install multiprocess
~~~

## Usage

A simple example that prints out three `1`s:

~~~python
from multiprocess import Multiprocess

m = Multiprocess(show_loading_bar=False)
def f():
  print(1)
m.add_tasks(f, [(), (), ()])
m.do_tasks()
m.close()
~~~

A more involved example of sorting numbers using `sleep`. Note that you only have as many workers as you have threads, so if you have 4 threads you will only be able to sort up to 4 numbers with this approach:
~~~python
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
    print(q.pop())

sleep_sort()
~~~


## Error handling
Errors from within a process are propagated back to the parent with stack information. For example

~~~python
from multiprocess import Multiprocess

m = Multiprocess()
def f(x):
  raise ValueError('bad error')

m.add_tasks(f, [(1,)])
m.do_tasks()
m.close()
~~~

Outputs:

~~~bash
Traceback (most recent call last):
  File "./example3.py", line 9, in <module>
    m.do_tasks()
  File "/Users/dom/Documents/git/Multiprocess/src/multiprocess.py", line 53, in do_tasks
    self._check_for_exceptions()
  File "/Users/dom/Documents/git/Multiprocess/src/multiprocess.py", line 71, in _check_for_exceptions
    "\n".join(['ERROR: ' + str(e) for e in exceptions]))
multiprocess.MultiprocessException: 1 errors occurred:
ERROR: Error in function call "f((1,))"
Traceback (most recent call last):
  File "/Users/dom/Documents/git/Multiprocess/src/multiprocess.py", line 85, in my_worker
    fn(*rem_args)
  File "./example3.py", line 6, in f
    raise ValueError('bad error')
ValueError: bad error
~~~

