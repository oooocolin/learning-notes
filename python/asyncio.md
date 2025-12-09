---
title: asyncio模块
tags:
  - python
  - asynchrony
---
## 概述
`asyncio` 是 Python 标准库中的一个模块，用于编写异步 I/O 操作的代码。`asyncio` 适合在一些 I/O 密集型场景使用，如网络请求、文件读写，使单线程中处理多个任务。
## 核心构成
### 协程
协程是 `asyncio` 的核心概念之一。它是一个特殊的函数，可以在执行过程中暂停，并在稍后恢复执行。协程通过 `async def` 关键字定义，并通过 `await` 关键字暂停执行，等待异步操作完成。更多协程内容，关联 [协程](../common/concurrency-model.md#) 链接
```python
​async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")
```
### 事件循环（Event Loop）
事件循环是 `asyncio` 的核心组件，负责调度和执行协程。它不断地检查是否有任务需要执行，并在任务完成后调用相应的回调函数。
```python
async def main():
    await say_hello()

asyncio.run(main())
```
### 任务（Task）
任务是对协程的封装，表示一个正在执行或将要执行的协程。可以通过 `asyncio.create_task()` 函数创建任务，并将其添加到事件循环中。
```python
async def main():
    task = asyncio.create_task(say_hello())
    await task
```
### Future
`Future` 是一个表示异步操作结果的对象。它通常用于底层 API，表示一个尚未完成的操作。你可以通过 `await` 关键字等待 `Future` 完成。
```python
async def main():
    future = asyncio.Future()
    await future
```
## 基本用法
### 执行任务
```python
async def task1():
    await asyncio.sleep(1)

async def task2():
    await asyncio.sleep(2)

async def main():
    await asyncio.gather(task1(), task2())

# 创建一个事件循环，运行协程
asyncio.run(task1())
# 并发执行多个任务
asyncio.run(main())
```
### 超时控制
可使用 `asyncio.wait_for()` 函数设置协程超时时间，如果在指定时间未完成，将引发 `asyncio.TimeoutError` 异常。
```python
async def long_task():
    await asyncio.sleep(5)

async def main():
    try:
        await asyncio.wait_for(long_task(), timeout=5)
    except asyncio.TimeoutError:
        print("Task timed out")

asyncio.run(main())
```
## 使用场景与说明
异步操作适合集中式的 I/O 操作，如网络请求、文件 I/O、数据库异步访问、实时消息队列处理。但是面对一些含有 CPU 计算场景或是一些混合场景，比如 I/O-计算-I/O 的典型流水线场景就不如多线程，尽管瓶颈在 I/O 上面，除非计算的耗时极低（≈0）。
