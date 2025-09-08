---
title: Python的多任务处理
tags:
  - multitask
  - python
---
## 一、Python多任务处理的方法
`Python` 采用以下方法进行多任务的处理：
- 多线程
- 多进程
- 异步
## 二、Python 的多线程
### 1. `Python GIL`
`Python GIL(Global Interpreter Lock)` 是全局解释器锁，确保同一个进程任何时刻只能有一个线程执行。由于它的存在，使得对于无法实现真正的 `CPU` 并行操作，仅支持并发操作。  
`GIL` 问题只存在于 `CPython` 解释器中，对于 `JPython` 和 `PyPy` 解释器则不存在这个问题，但目前主流使用的还是 `CPython` 解释器（支持 `C` 语言生态，官方的主推版本等原因）。可以采用一些方法来规避这个问题：
- 多进程
- 使用其他解释器
- 使用 `C/C++` 代码实现，再在 `Python` 中调用
## 2. 多线程处理 `I/O` 密集型多任务
线程等待 `I/O` 时（系统调用），`CPython` 解释器会释放 `GIL` ，这样其他线程就可以在等待间隙执行代码。所以一般使用多线程来处理 `I/O` 密集型多任务，通常也一般结合异步来使用，可以缓解多线程切换的开销更进一步提高性能。  
`Python` 多线程使用 `threading` 模块实现，可以函数式调用或者继承式实现。
#### (1). 函数式（推荐）
使用 `threading.Thread` 来创建类对象，再使用 `start()` 方法启动执行。
```python
class threading.Thread(target=None, name=None, args=(), kwargs={}, *, daemon=None)
```
- `target`：线程执行的函数
- `name`：线程的名字
- `args`：执行函数的参数
- `kwargs`：关键字参数（指定参数名称，并与值对应）
- `*`：表示在此之后的参数必须为关键字参数
- `daemon`：设置是否将线程设置为守护线程（为主线程服务的线程，主线程销毁守护线程也被销毁）

**线程对象常用的方法**：

|        方法或属性         |     说明      |
|:--------------------:|:-----------:|
|        `name`        |    线程名称     |
|        ident         |  线程的唯一标识码   |
|        daemon        |   守护线程标志    |
|     `is_alive()`     | 查看线程是否还在执行  |
| `join(timeout=None)` | 阻塞线程，等待目标线程 |

示例：
```python
def task(name):
    print(f"Thread_{name}: starting")
    time.sleep(2)  # I/O操作  
    print(f"Thread_{name}: finished")


# 创建并启动线程  
threads = []
for i in range(5):
    t = threading.Thread(target=task, name=f'Thread_{i}', args=(i,))
    threads.append(t)
    t.start()

# 等待所有线程结束  
for t in threads:
    t.join()
print("All threads done")
```
#### (2). 继承式
继承 `threading.Thread` 类，实现 `run()` 方法，创建类对象，调用 `start()` 方法执行线程。

示例：
```python
class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(f"{self.name}: starting")
        time.sleep(2)  # I/O操作  
        print(f"{self.name}: finished")

# 创建并启动线程  
threads = []
for i in range(5):
    t = MyThread(name=f'Thread_{i}')
    threads.append(t)
    t.start()

# 等待所有线程结束  
for t in threads:
    t.join()
print("All threads done")
```
### 2. 多进程处理 `CPU` 密集型多任务
在面对 `CPU` 密集型多任务的情况下，使用多进程是更为有效的方案。`Python` 多进程使用 `multiprocessing` 模块实现。`multiprocessing` 模块使用多进程与多线程类似，入参及其含义也类似。

```python
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
```
**注意**：由于多进程本身有开销，并且拥有独立内存空间，所以在上下文切换时的开销往往比多线程还要大很多，所以需要哟足够的计算量才能对性能优化有一定作用。   
在面对加法这种简易操作由于 `GIL` 的存在，使用多线程效果和直接循环求值的效果差不多，有时还会因为多线程本身的开销以及频繁切换上下文，导致性能反而变差；当面对乘法运算，尤其是涉及到远超 `CPU` 原生的64位加法器范围的大数乘法的计算，`CPython` 解释器就会主动释放 `GIL` 实现有限度的并行，在大数累乘方面多线程的性能将会有所提高。
### 3. 线程池与进程池
使用线程池和进程池可以避免重复创建和销毁进程或线程的开销，从而提高性能，并且使用线程池和进程池可以更为方便的管理线程和进程的信息、执行状态等。  
在使用线程池或进程池结束的时候需要将资源释放，不然易造成内存泄漏、僵尸进程等问题，可以调用对应的关闭方法实现，或是使用 `with ... as ...` 帮你自动关闭。
#### (1). 使用 `multiprocessing.Pool` 实现进程池
`multiprocessing.Pool` 是 `multiprocessing` 模块提供的一个类，用于创建进程池。它的构造函数接受一个可选的参数 `processes`，用于指定进程池中的进程数量。如果不指定，默认会使用 `os.cpu_count()` 返回的 CPU 核心数量。
```python  
def multi_process_pool_by_multiprocessing():
    batch = 8
    step = iterations // batch
    params = []
    for start in range(1, iterations, step):
        params.append((start, start + step))
    with multiprocessing.Pool(batch) as pool:
        result = pool.starmap(single_count, params)
    return sum(result)    
```  
原本若要获取进程的结果需要自己实现的过程很复杂，并且还有 `Value` 类对象必须事先指定映射的 `C` 语言类型以及使用 `Manager` 本身开销巨大等问题。而使用改方法，以及后续演示的其他进程池和线程池的调用都不需要自己实现结果的记录，而是直接调用相关的方法。
#### (2). 使用 `concurrent.futures` 实现线程池与进程池
`concurrent.futures` 模块提供了 `ThreadPoolExecutor` 和 `ProcessPoolExecutor` 两个类，用于创建线程池和进程池。它们的构造函数接受一个可选的参数 `max_workers`，用于指定线程池或进程池中的线程或进程数量。如果不指定，默认会使用 `os.cpu_count()` 返回的 CPU 核心数量。
```python
# 实现线程池
def multi_threading_pool():
    batch = 8
    step = iterations // batch
    params = []
    for start in range(1, iterations, step):
        params.append((start, start + step))
    with ThreadPoolExecutor(max_workers=10) as pool:
        result = pool.map(lambda args: single_count(*args), params)
    return sum(result)


# 实现进程池
def multi_process_pool_by_concurrent_futures():  
    batch = 8  
    step = iterations // batch  
    params = []  
    for start in range(1, iterations, step):  
        params.append((start, start + step))  
		
    with ProcessPoolExecutor(max_workers=10) as pool:  
        result = pool.map(single_count_wrapper, params)  
		
    return sum(result)
```
以 `ProcessPoolExecutor` 为例，介绍常用的方法。`ProcessPoolExecutor` 继承自 `Executor` 类，在调用一些执行方法后返回 `Future` 对象。  
`ProcessPoolExecutor` 给了两种方法来执行进程：
- `submit()`：将一个进程需要执行的函数及其参数输入，返回一个 `Future` 对象等待执行结果。
- `map()`：创造进程批量执行函数，参数以列表逐个传入，等待全部执行完成返回一个迭代器，里面存储着结果。相当于是一个 `submit()` + 收集 `f.result()` 简化的语法糖。
`Future` 对象的常用方法：
- `result()`：用于获取计算的结果。
- `running()`：用于获取该进程是否正在执行。
- `cancelled()`：用于获取该进程是否在执行前被取消。
- `cancel()`：用于使该进程在执行前被取消，若已经开始执行则无法取消。
- `done()`：用于获取该进程是否完成或是取消。
#### (3). 使用 `joblib` 库加速计算

