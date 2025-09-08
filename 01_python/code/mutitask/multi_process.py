import multiprocessing
import threading

from ..util.perf_util import perf_count


def single_count(start, end):
    r = 0
    for i in range(start, end):
        r += i
    return r


iterations = 100000000


def single_process():
    return single_count(1, iterations + 1)


def threading_process():
    step = iterations // 5
    processes = []
    for start in range(1, iterations, step):
        p = threading.Thread(target=single_count, args=(start, start + step))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


def single_count_wrapper(value, start, end):
    r = 0
    for i in range(start, end):
        r += i
    value.value = r


def multi_process():
    step = iterations // 5
    processes = []
    for start in range(1, iterations, step):
        value = multiprocessing.Value("q")
        p = multiprocessing.Process(target=single_count_wrapper, args=(value, start, start + step))
        p.start()
        processes.append((p, value))

    result = 0
    for p, v in processes:
        p.join()
        result += v.value
    return result


def multi_process_pool():
    batch = 8
    step = iterations // batch
    params = []
    for start in range(1, iterations, step):
        params.append((start, start + step))

    with multiprocessing.Pool(batch) as pool:
        result = pool.starmap(single_count, params)

    return sum(result)


if __name__ == '__main__':
    # perf_count(single_process)
    # perf_count(threading_process)
    # perf_count(multi_process)
    print(single_process())
    print(multi_process())
