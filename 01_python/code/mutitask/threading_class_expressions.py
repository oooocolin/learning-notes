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


def main():
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


if __name__ == "__main__":
    main()
