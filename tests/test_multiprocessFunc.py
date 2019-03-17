from multiprocess import multiprocess

def test_multiprocess_func():
  multiprocess(lambda: 1, [()])
