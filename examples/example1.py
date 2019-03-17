#!/usr/bin/env python3
from multiprocess import Multiprocess

m = Multiprocess(show_loading_bar=False)
f = lambda: 1
m.add_tasks(f, [()])
m.do_tasks()
m.close()
