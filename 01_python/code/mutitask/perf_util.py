import time


def perf_count(fn):
    start = time.perf_counter() * 1000
    fn()
    print("cost time: ", round(time.perf_counter() * 1000 - start, 2), " ms")
