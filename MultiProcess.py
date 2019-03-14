from tqdm import tqdm
import multiprocessing

MANAGER = multiprocessing.Manager()
# TODO error handling

class MultiProcess:
  def __init__(self, loading_bar=True):
    self.pool = multiprocessing.Pool()
    self.jobs = {}
    self.job_count = 0
    self.loading_bar = loading_bar

  def add_tasks(self, fn_name, arr_of_args):
    """add tasks to be done"""
    if not 'fn_name' in self.jobs:
      self.jobs[fn_name] = []
    self.jobs[fn_name] += arr_of_args
    self.job_count += len(arr_of_args)

  def do_tasks(self):
    """Block the thread and complete the tasks"""
    if self.loading_bar:
      pbar = tqdm(total=self.job_count)

    for job_fn, job_arr_of_args in self.jobs.items():
      if not self.loading_bar:
        self.pool.imap_unordered(job_fn, job_arr_of_args)
      else:
        for _ in enumerate(self.pool.imap_unordered(job_fn, job_arr_of_args)):
          pbar.update(1)
    
    pbar.close()
    self.jobs = {}
    self.job_count = 0
  
  def close(self):
    self.pool.close()


def my_worker(args):
  fn = args[0]
  errQ = args[1]
  remArgs = args[2:]
  try:
    fn(*remArgs)
  except Exception as e:
    errQ.push(e)


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
