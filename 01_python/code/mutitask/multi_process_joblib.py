import joblib

from perf_util import perf_count
from multi_process import multi_process, single_process, single_count

iterations = 100000000


def multi_process_pool_by_joblib():
    batch = 8
    step = iterations // batch

    with joblib.Parallel(batch) as parallel:
        result = parallel(joblib.delayed(single_count)(start, start + step) for start in range(1, iterations, step))

    return sum(result)


if __name__ == "__main__":
    perf_count(single_process)
    perf_count(multi_process)
    perf_count(multi_process_pool_by_joblib)
    print(single_process())
    print(multi_process())
    print(multi_process_pool_by_joblib())
