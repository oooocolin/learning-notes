import threading
import time


def task(name):
    print(f"Thread_{name}: starting")
    time.sleep(2)  # I/O操作
    print(f"Thread_{name}: finished")


def main():
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


if __name__ == "__main__":
    main()
