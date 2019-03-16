from tqdm import tqdm
import multiprocessing
import traceback
import dill

MANAGER = multiprocessing.Manager()

class MultiProcessException(Exception):
  pass

class MultiProcess:
  def __init__(self, show_loading_bar=True):
    self.pool = multiprocessing.Pool()
    self.jobs = []
    self.show_loading_bar = show_loading_bar
    self.errQ = Queue()
    self.alive = True

  def _reset(self):
    while not self.errQ.empty():
      self.errQ.pop()
    self.jobs = []

  def add_tasks(self, fn, arr_of_args):
    """add tasks to be done"""
    if not self.alive:
      raise MultiProcessException("CLOSED, refusing to add tasks")
    arr = [dill.dumps((fn, self.errQ) + (args)) for args in arr_of_args]
    self.jobs += arr

  def do_tasks(self, called_from_close=False):
    """Block the thread and complete the tasks"""
    if not self.alive:
      if called_from_close:
        return
      else:
        raise MultiProcessException('CLOSED, refusing to do tasks')
    job_count = len(self.jobs)
    if self.show_loading_bar:
      pbar = tqdm(total=job_count)

    if not self.show_loading_bar:
      self.pool.imap_unordered(my_worker, self.jobs)
    else:
      for _ in enumerate(self.pool.imap_unordered(my_worker, self.jobs)):
        self._check_for_exceptions()
        pbar.update(1)
    
    # Raise exceptions, if there were any
    self._check_for_exceptions()
    pbar.close()
    self._reset() 
  
  def _check_for_exceptions(self):
    if not self.errQ.empty():
      exceptions = []
      while not self.errQ.empty():
        exceptions.append(self.errQ.pop())
      self._reset()
      self.close()
      raise MultiProcessException('%s errors occurred:\n' % len(exceptions) + "\n".join(['ERROR: ' + str(e) for e in exceptions]))

  def close(self):
    self.do_tasks(True)
    self.alive = False
    self.pool.close()


def my_worker(args):
  args = dill.loads(args)
  fn = args[0]
  errQ = args[1]
  remArgs = args[2:]
  try:
    fn(*remArgs)
  except Exception:
    errQ.push('Error in function call "%s(%s)"\n%s' % (fn.__name__, remArgs, traceback.format_exc()))


"""A lightweight wrapper for multiprocess.manager.Queue()"""
class Queue:
  def __init__(self):
    self.q = MANAGER.Queue()
    #for method in dir(self.q):
    #  if method[0] != '_':
    #    setattr(self, method, getattr(self.q, method]))
  
  def get(self):
    return self.q.get()
  
  def put(self, v):
    self.q.put(v)

  def pop(self):
    return self.get()
  
  def push(self, v):
    self.q.put(v)
  
  def empty(self):
    return self.q.empty()
  
  def qsize(self):
    return self.q.qsize()
  
