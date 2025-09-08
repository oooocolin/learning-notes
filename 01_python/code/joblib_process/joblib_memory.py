import joblib
from perf_util import perf_count

memory = joblib.Memory("cache", verbose=0)

iterations = 100000000


@memory.cache
def single_count(start, end):
    r = 0
    for i in range(start, end):
        r += i
    return r


if __name__ == "__main__":
    perf_count(single_count, *(1, iterations))
    perf_count(single_count, *(1, iterations))
