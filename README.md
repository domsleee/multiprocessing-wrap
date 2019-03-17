# multiprocess

A simple interface for writing concurrent scripts.

## Installation

To install using pip:

~~~bash
pip install multiprocess
~~~

## Usage

This library uses `tqdm` loading bars by default. For example:

~~~python
from multiprocess import Multiprocess
from time import sleep

m = Multiprocess(show_loading_bar=false)
def f(x):
  time.sleep(2)

m.add_tasks(f, [(1,), (2,), (1.5,)])
m.do_tasks()
m.close()
~~~

Outputs:


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


