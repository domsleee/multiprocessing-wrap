import pytest
from multiprocess import Multiprocess, Queue, MultiprocessException


def test_stdout(capsys):
  m = Multiprocess()
  m.add_tasks(lambda: 1, [()])
  m.do_tasks()
  m.close()
  out, err = capsys.readouterr()
  assert (out == '')
  spl = [v.split('\r')[-1] for v in err.split('\n')]
  assert (len(spl) == 2)
  assert (spl[0].startswith('100%'))
  assert (spl[1] == '')


def test_disable_load_bar_works(capsys):
  m = Multiprocess(show_loading_bar=False)
  m.add_tasks(lambda: 1, [()])
  m.close()
  out, err = capsys.readouterr()
  assert (out == '')
  assert (err == '')
