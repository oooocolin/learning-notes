import time


def perf_count(fn, *args):
    start = time.perf_counter() * 1000
    fn(*args)
    print("cost time: ", round(time.perf_counter() * 1000 - start, 2), " ms")
