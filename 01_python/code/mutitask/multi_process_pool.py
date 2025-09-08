import multiprocessing

from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
from multi_process import multi_process, single_process, single_count
from ..util.perf_util import perf_count

iterations = 100000000


def multi_process_pool_by_multiprocessing():
    batch = 8
    step = iterations // batch
    params = []
    for start in range(1, iterations, step):
        params.append((start, start + step))

    with multiprocessing.Pool(batch) as pool:
        result = pool.starmap(single_count, params)

    return sum(result)


def single_count_wrapper(args):
    start, end = args
    return single_count(start, end)


def multi_threading_pool():
    batch = 8
    step = iterations // batch
    params = []
    for start in range(1, iterations, step):
        params.append((start, start + step))

    with ThreadPoolExecutor(max_workers=10) as pool:
        result = pool.map(lambda args: single_count(*args), params)

    return sum(result)


def multi_process_pool_by_concurrent_futures():
    batch = 8
    step = iterations // batch
    params = []
    for start in range(1, iterations, step):
        params.append((start, start + step))

    with ProcessPoolExecutor(max_workers=10) as pool:
        result = pool.map(single_count_wrapper, params)

    return sum(result)


if __name__ == '__main__':
    # perf_count(single_process)
    # perf_count(multi_process)
    # perf_count(multi_process_pool_by_multiprocessing())
    # perf_count(multi_threading_pool)
    # perf_count(multi_process_pool_by_concurrent_futures())
    print(single_process())
    print(multi_process())
    print(multi_process_pool_by_multiprocessing())
    print(multi_threading_pool())
    print(multi_process_pool_by_concurrent_futures())
