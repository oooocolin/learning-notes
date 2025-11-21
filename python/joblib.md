---
title: joblib库
tags:
  - python
  - multitask
  - joblib
---
## 概述
`joblib` 库是用于高效并行计算的库，其提供了许多简单易用的计算工具等。主要功能有：
- 缓存计算结果，下次计算时直接调用减小重复计算；
- 高效的序列化，对 `Numpy` 数组等大型的数据对象进行优化，加快序列化和反序列化的速度；
- 使用并行计算，将任务拆分到多个进程或线程中执行，技术计算过程。
## 缓存功能
### `Memory` 类
`Memory` 类将函数计算结果存储起来，以便在下次使用的时候直接调用。这有利于加速计算过程，节约资源。
```python
class joblib.Memory(location=None, backend='local', mmap_mode=None, compress=False, verbose=1, bytes_limit=None, backend_options=None)
```
- `location`：文件缓存的存放位置。若设置为 `None`，则只缓存在内存，不保存在磁盘。
- `backend`：缓存的后端存储方式。默认是 `'local'`，表示使用本地文件系统；`'cloudpickle'`，是使用 `cloudpickle` 序列化结果，可以支持更多的对象（如 `lambda` 、闭包），但是一般速度会慢一些。
- `mmap_mode`：表示内存映射文件的模式（`None`, `'r+'` ,  `'r'` ,  `'w+'` , `'c'`）。如果缓存结果是很大的 `numpy` 数组，可以通过 `mmap` 避免一次性加载进内存，实现按需访问。
- `compress`：表示是否压缩缓存文件。压缩可以节省磁盘空间，但会增加 I/O 操作的时间。压缩默认使用 `zlib` ，也可以指定其他压缩算法（需安装）。
- `verbose`：一个整数，表示日志的详细程度。`0` 表示没有输出，`1` 表示只输出警告，`2` 表示输出信息，`3` 表示输出调试信息。
- `bytes_limit`：表示缓存使用的字节数限制。如果缓存超过了这个限制，最旧的缓存文件将被删除。
- `backend_options`：传递给缓存后端的选项。一般不常用，一般用在 `backend` 支持的一些额外特性，通过此参数传入细节配置。
### 缓存的使用
```python
memory = joblib.Memory("cache", verbose=0)  
  
iterations = 100000000  
  
  
@memory.cache  
def single_count(start, end):  
    r = 0  
    for i in range(start, end):  
        r += i  
    return r

single_count(1, iterations)
single_count(1, iterations)
```
### 清除缓存
```python
memory.clear(warn=True)
```
这会将 `memory` 绑定的地址中的缓存被清除，注意文件夹内部不要存储其他内容以及文件。
## 高效序列化
`joblib.dump()` 和 `joblib.load()` 提供了一种替代 `pickle` 库的方法，可以高效地序列化处理包含大量数据的任意 `Python` 对象，特别是大型的 `NumPy` 数组。尤其是 `pickle` 库无法直接序列化 `Numpy` 对象。
```python
# 序列化数据
# 注意 joblib.dump() 只能保存为 .pkl 文件和 .joblib 文件
joblib.dump(dist_persist, filename)    # filename 保存的路径及文件名

# 读取数据
joblib.dump('dist_persist.joblib')
```
## 并行计算
### `Parallel` 类
`Joblib` 库的 `Parallel` 类用于简单快速将任务分解为多个子任务，并分配到不同的CPU核心或机器上执行，从而显著提高程序的运行效率。
```python
class joblib.Parallel(n_jobs=None, backend=None, return_as='list', verbose=0, timeout=None, batch_size='auto', pre_dispatch='2 * n_jobs', temp_folder=None, max_nbytes='1M', require=None)
```
- `n_jobs`：指定并行任务的数量，为 `-1` 的时候表示所有CPU可用的核心，为 `None` 是表示单个进程。
- `backend`：指定并行化的后端，
    - `'loky'`：使用 `joblib` 自己专门开发的一个稳定的进程池实现，比 `Python` 自带的更为健壮（默认）；
    - `'threading'`：基于 `Python` 自带的 `threading` 库实现多线程；
    - `'multiprocessing'`：基于 `Python` 自带的 `multiprocessing` 库实现多进程。
- `return_as`：返回结果的格式，可选项：
    - `'list'`：列表。
    - `'generator'`：按照任务提交顺序生成结果的生成器。
    - `'generator_unordered'`：按照执行结果完成先后顺序的生成器。
- `verbose`：表示日志的详细程度，`0` 表示不输出，`1` 表示只输出警告，`2` 表示输出信息，`3` 表示输出调试信息。
- `timeout`：表示单个任务最大运行时长，超时将报 `TimeOutError` 错误。（仅适用于不为单线程场景）
- `batch_size`：指定进行一次批处理中包含的任务数，若为 `'auto'` 则为 `joblib` 自动调整（过程更为复杂，但是对于不知道取什么批次的任务更为适合）。
- `pre_dispatch`：用来决定在并行计算开始之前，每个批次有多少个任务会被预先准备好并等待被分配给单个工作进程。默认值为 `'2*n_jobs'` ，表示并行计算时可以使用2倍工作进程的任务数量。
- `temp_folder`：指定临时文件的存储路径。（这并非使用 `joblib.Memory` 类实现，无法避免重复计算，只是避免大数据量在管道通信中爆内存或太慢）
- `max_nbytes`：传递给工作程序的数组大小的阈值。（决定将数据存储到 `temp_folder` 内的阈值）
- `require`：对运行任务的要求，可选 `None` 和 `sharedmem` 。`sharedmem` 表示将使用共享内存来执行并行任务，但会影响计算性能。
### `delayed`
`Parallel` 类创建时不能直接接收执行函数和参数，而 `delayed` 专门用于把函数调用封装成可延迟执行的任务对象。其基本形式为 `delayed(func)(*args)` ，这相当于 `lambda` 表达式 `lambda: func(*args)` 该形式的简化。
```python
# 单参数函数
delayed(square)(i) for i in range(10)

# 多参数函数
delayed(slow_add)(a, b) for a, b in pairs
delayed(slow_add)(*i) for i in pairs    # 解包元组作为入参
```
### 执行并行计算
```python
def multi_process_pool_by_joblib():  
    batch = 8  
    step = iterations // batch  
		  
    with joblib.Parallel(batch) as parallel:  
        result = parallel(joblib.delayed(single_count)(start, start + step) for start in range(1, iterations, step))  
		  
    return sum(result)
```




