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
- 使用原生 `C/C++` 代码，再在 `Python` 中调用
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
| :------------------: | :---------: |
|        `name`        |    线程名称     |
|        ident         |  线程的唯一标识码   |
|        daemon        |   守护线程标志    |
|     `is_alive()`     | 查看线程是否还在执行  |
| `join(timeout=None)` | 阻塞线程，等待目标线程 |

示例：
```python
import threading
import time

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
import threading
import time

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


