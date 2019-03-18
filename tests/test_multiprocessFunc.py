from multiprocess import multiprocess, Queue

def test_multiprocess_func():
  multiprocess(lambda: 1, [()])

def test_multiprocess_func_does_something():
  q = Queue()
  multiprocess(lambda q, x: q.push(x), [(q, 1), (q, 2)])
  arr = []
  while not q.empty():
    arr.append(q.pop())
  assert(set([1,2]) == set(arr))

