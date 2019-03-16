from MultiProcess import MultiProcess, Queue, MultiProcessException
import pytest

def test_empty_fn():
  def f():
    pass
  m = MultiProcess()
  m.add_tasks(f, [()])
  m.do_tasks()
  m.close()

def test_queue():
  q = Queue()
  m = MultiProcess()
  def f(q):
    q.push(1)
  m.add_tasks(f, [(q,)])
  m.do_tasks()
  m.close()
  assert(q.qsize() == 1)
  assert(q.pop() == 1)
  assert(q.qsize() == 0)

def test_fn_raises_exc_is_caught():
  m = MultiProcess()
  def f():
    raise ValueError('unique')
  m.add_tasks(f, [()])
  with pytest.raises(MultiProcessException) as excinfo:
    m.do_tasks()
  assert 'unique' in str(excinfo.value)
  m.close()

def test_lambda_pickling():
  f = lambda q: q.push(1)
  q = Queue()
  m = MultiProcess()
  m.add_tasks(f, [(q,)])
  m.do_tasks()
  m.close()
  assert(q.qsize() == 1)
  assert(q.pop() == 1)
  assert(q.qsize() == 0)

def test_multiple_tasks():
  def f(q, num):
    q.push(num)
  q = Queue()
  m = MultiProcess()
  arr = range(100)
  m.add_tasks(f, [(q, num,) for num in arr])
  m.do_tasks()
  m.close()
  assert(q.qsize() == len(arr))
  l = [q.pop() for v in range(q.qsize())]
  assert(set(l) == set(arr))

def test_close_does_calls_do_task():
  def f(q):
    q.push(1)
  q = Queue()
  m = MultiProcess()
  m.add_tasks(f, [(q,)])
  m.close()
  assert(q.qsize() == 1)
  assert(q.pop() == 1)
  assert(q.qsize() == 0)

def test_do_tasks_twice():
  def f(q):
    q.push(1)
  q = Queue()
  m = MultiProcess()
  m.add_tasks(f, [(q,)])
  m.do_tasks()
  assert(q.qsize() == 1)
  m.add_tasks(f, [(q,)])
  m.do_tasks()
  assert(q.qsize() == 2)

def test_close_twice_doesnt_raise_exc():
  m = MultiProcess()
  m.close()
  m.close()

def test_do_tasks_after_error_raises_exc():
  def f():
    raise ValueError('error')
  m = MultiProcess()
  m.add_tasks(f, [()])
  with pytest.raises(MultiProcessException):
    m.do_tasks()
  with pytest.raises(MultiProcessException):
    m.do_tasks()
  m.close()

def test_add_tasks_after_close_raises_exc():
  m = MultiProcess()
  m.close()
  f = lambda: 1
  with pytest.raises(MultiProcessException):
    m.add_tasks(f, [()])
  
def test_do_tasks_after_close_raises_exc():
  m = MultiProcess()
  f = lambda: 1
  m.add_tasks(f, [()])
  m.close()
  with pytest.raises(MultiProcessException):
    m.do_tasks()

