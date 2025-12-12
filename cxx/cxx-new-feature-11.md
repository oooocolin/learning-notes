---
title: C++ 11 新特性
tags:
  - cxx
  - language-feature
---
## 基于范围的 `for` 循环
是一种简化循环书写的语法糖，其结构为 `for (decl : range) statement;` 相当于一种容器的遍历。
```cpp
std::vector<int> v = {1, 2, 3, 4};

for (int x : v) {
    std::cout << x << " ";
}
```
相当于
```cpp
for (auto it = v.begin(); it != v.end(); ++it) {
    int x = *it;
    std::cout << x << " ";
}
```
## 自动类型推断
### 简介
`auto` 让编译器根据初始化表达式的类型自动推导变量类型，但它并不是“动态类型”，而是编译期静态类型推导。
```cpp
auto x = 10;        // x 是 int  相当于 int x = 10;
auto y = 3.14;      // y 是 double  相当于double y = 3.14;
auto s = "hello";   // s 是 const char*  相当于const char* s = "hello";
```
### 推导规则
| 表达式形式      | 推导结果                | 示例                                        |
| :--------- | :------------------ | ----------------------------------------- |
| 普通值        | 去掉引用和cv修饰           | `const int x=1; auto a=x; // a是int`       |
| 引用         | 保留实际类型，不自动添加引用      | `int &r=i; auto a=r; // a是int`            |
| 指针         | 保留指针                | `int *p; auto a=p; // a是int*`             |
| const指针    | const属性保留在指针上，不在值上  | `const int *p; auto a=p; // a是const int*` |
| 初始化为引用或右值  | 推导成值类型（除非用 `auto&`） | `auto a = getInt(); // 值拷贝`               |
| 使用 `auto&` | 保留引用关系              | `auto& r = i;`                            |
### 与基于范围的 `for` 循环结合
一般在使用 `for` 循环的遍历对象尤其是容器时比较常见 `auto&` 与 `const` 的集合，因为这个这既保证了不参与拷贝，降低了拷贝的性能开销，`const` 又保证了元素不被修改，是在循环遍历中常见的结构。
```cpp
for (const auto& item : vec) {
    // 安全，不拷贝
}
```
## Lambda 表达式
### 简介
Lambda 是一种匿名函数对象（functor），可以在定义的同时使用。其基本格式为 `[捕获列表](参数列表) -> 返回类型 { 函数体 }` 。
```cpp
auto f = [](int x, int y) { return x + y; };
std::cout << f(2, 3);  // 输出 5
```
- `[]`：捕获外部变量，可以捕获具体的变量，或是根据捕获规则按需捕获。
- `(int x, int y)` → 参数列表
- `{ return x + y; }` → 函数体
### 捕获规则
- `[=]`：值捕获。拷贝外部变量到 lambda 内部，但内部不可修改外部变量（除非用 `mutable`并且只会在内部生效，不影响外部）。
```cpp
int x = 10;
auto f = [=]() mutable { x += 1; return x; }; // x 在 lambda 内可改，但外部 x 不变
f();  // 内部 x = 11
```
- `[&]`：引用捕获。捕获外部变量的引用，lambda 内修改会影响外部变量。
```cpp
int x = 10;
auto f = [&]() { x += 1; };
f();  // 外部 x = 11
```
- `[x, &y]`：混合捕获。可以对不同变量选择值捕获或引用捕获。
### 注意
- 在 C++ 11 中如果返回值类型不一致时需要指定返回值类型，但在 C++ 14 中改善了这个问题，可以不用指定返回值了。
```cpp
auto f = [](bool b) -> double { 
    if (b) return 1; 
    else return 2.0; 
};
```
- C++ 11 书写函数以及 lambda 表达式返回 lambda 表达式 不支持 `auto` 类型，这要在 C++ 14 改善。
- C++ 11 只支持捕获普通变量、指针、容器、`this` 指针，之后版本将支持更多，比如初始化捕获（C++ 14）、`*this` （C++ 17）、泛型类型约束（C++ 20）等。
## 列表初始化
列表初始化（List Initialization），也叫统一初始化（Uniform Initialization），这是现代 C++ 很重要的语法糖之一。提升了可读性，也减少了类型歧义和隐式转换问题。C++11 引入了 `{}` 花括号来初始化变量，相比传统初始化，`{}` 是统一的初始化语法，所有类型都可以使用，避免了 C++98/03 多种写法的混乱。
```cpp
int x{5};                        // x = 5
std::vector<int> v{1,2,3,4,5};
std::string s{"hello"};          // s = "hello"
Student{1, "LiHua"};             // 初始化类对象
```
但也得注意分别一些特殊情况：
- 注意数组与容器语法的区别。
```cpp
std::vector<int> v1{10}; // 1个元素 10
std::vector<int> v2(10); // 10个默认元素 0
```
- 列表初始化可以进行嵌套初始化。
```cpp
struct Rect {
    Point topLeft;
    Point bottomRight;
};

Rect r{{0,0}, {10,10}}; // 嵌套列表初始化
```
## 移动语义
### 简介
传统 C++ 对象拷贝都是 深拷贝（Copy），这对小对象无妨，但对大对象，比如容器、字符串、文件句柄等，复制成本很高。移动语义优化的目标是将临时对象或即将被销毁的对象，不必再做昂贵的拷贝，直接搬走资源（之后原对象置空），避免内存拷贝。具体而言，移动语义专门针对右值（临时对象，反之左值是有名字可寻址的对象）。在 C++ 11 中新增 `T&&` 类型用于表示右值引用。
### 转换左值
C++ 11 新支持的 `std::move` 可以将左值强制转换为右值，之后在构造/赋值过程中实现移动语义。
```cpp
std::vector<int> v1 = {1,2,3};
std::vector<int> v2 = std::move(v1);
```
## 智能指针
### 概述
此前对于堆内存必须手动使用 `new` / `delete` 进行管理，但容易出现忘记释放、重复释放以及异常中途返回导致内存泄漏。C++ 11 引入智能指针，希望让堆内存自动释放像栈对象一样安全的管理生命周期。智能指针其实是一个类模板，内部保存了一个普通指针，并在析构时自动释放资源，而且在异常时也会自动释放资源。
### 三种智能指针
#### (1). 独占式指针（最轻量）
独占式指针 `std::unique_ptr<T>` ，同一时刻只能有一个指针指向同一个对象。该指针不能复制，只能移动（使用 `std::move` 移动），离开作用域自动销毁。
```cpp
#include <memory>

std::unique_ptr<A> p1 = std::make_unique<A>();
// std::unique_ptr<A> p2 = p1; // 错误，不能拷贝
std::unique_ptr<A> p3 = std::move(p1); // 移动所有权
```
**使用场景**：局部对象、树结构、资源独占管理等。
#### (2). 共享式指针
共享式指针 `std::shared_ptr<T>` ，同一时刻可以有多个指针指向同一个对象。该指针内部维护一个引用计数，最后一个离开作用域时自动销毁资源。
```cpp
#include <memory>

auto p1 = std::make_shared<A>();
auto p2 = p1;  // 引用计数 +1
p1.reset();    // 引用计数 -1，资源仍存活
p2.reset();    // 最后一个销毁，delete 资源
```
**注意**：共享式指针也可在函数结束后自动释放，`reset()` 是程序员可选在作用域内提前释放资源。
**缺点**：
- 额外的引用计数内存和原子操作成本。
- 可能产生循环引用（如果两个 `shared_ptr` 互相引用，就永远不会释放。需要 `weak_ptr` 解决）。
**使用场景**：共享资源、异步任务。
#### (3). 弱引用
弱引用 `std::weak_ptr<T>` 不参与引用计数，用于安全观察 `shared_ptr` 管理对象，解决 `shared_ptr` 相互引用导致的死锁问题（实质上还是需要根据使用场景正确使用智能指针）。
```cpp
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev; // 防止循环引用
};
```
## constexpr
### 概述
constexpr 用于在编译期对变量、函数、构造函数进行求值，可以提高性能。并且可用于数组大小、模板参数等需要编译期常量的地方。
### constexpr 变量
```cpp
constexpr int max_value = 100;
int arr[max_value]; // 可以用作数组大小
```
- 必须初始化。
- 值必须在编译期已知。
- 只允许字面量类型（如 int、float、指针、数组、栈上对象）。
### constexpr 函数
```cpp
constexpr int square(int x) {
    return x * x;
}

constexpr int y = square(5); // 编译期求值
```
- 函数体只能有一条 return 语句。
- 不允许循环、`if/else` 分支判断。
- 函数参数和返回类型必须是字面量类型。
## nullptr 关键字
C++ 11 新增支持使用 nullptr 关键字，用于表示空指针，比使用字面值 “0” 或 “NULL” 更具类型安全性。nullptr 的类型是 `std::nullptr_t` ，`nullptr` 是语言字面量，可以直接使用。
```cpp
int *ptr = nullptr;
```
## 线程与并发
### 概述
从 C++ 11 开始，标准库引入线程与并发支持。此前是由各平台单独维护，无法写跨平台的代码，没有语言级的内存模型，而 C++ 11 开始正式支持。
### 核心组成
#### (1). 语言级内存模型
C++11 定义了线程、原子操作、数据竞争等语义，规定编译器和 CPU 的指令重排规则，保障多线程语义可预测，得以安全地实现并发机制。之后的所有库都基于此设计。
#### (2). 线程与并发运行时库
##### (i). `std::thread` 
`std::thread` 用于创建线程，线程对象支持 `join()` 进行阻塞等待，`detach()` 后台运行等功能。
```cpp
void work() {}

int main() {
    std::thread t(work);
    t.join(); // 等待线程执行结束
}
```
##### (ii). `std::mutex` / `std::lock_guard` / `std::unique_lock` 
`std::mutex` 是互斥量，是最基础的锁。需要手动上锁和解锁。配合 `std::lock_guard` 和 `std::unique_lock` 可对互斥量进行管理不用手动上锁和解锁。
```cpp
std::mutex m;

void f() {
    std::lock_guard<std::mutex> lg(m); // 自动上锁/释放
    // 临界区
}
```
##### (iii). `std::condition_variable` 
`std::condition_variable` 是条件变量，用于线程等待事件，让线程在满足某个条件之前处于阻塞状态。
```cpp
std::mutex m;
std::condition_variable cv;
bool ready = false;

void f() {
    std::unique_lock<std::mutex> lk(m);
    cv.wait(lk, []{ return ready; });
}
```
##### (iv). `std::future` / `std::promise` / `std::async` 
`std::async` 用于启动异步任务，进行简化多线程编程，使得不用手动管理线程的创建、同步等细节。具体来说，`std::async` 会在后台启动一个线程来执行一个函数，并允许你在未来某个时刻获取它的结果。
```cpp
std::future<T> std::async(std::launch::policy, callable&& f, Args&&... args);
```
- `std::launch::policy`：指定异步执行策略的枚举，常见的有：
    - `std::launch::async`：强制在新的线程中异步执行。
    - `std::launch::deferred`：延迟执行，直到调用 `get()` 或 `wait()` 时才会执行任务。此时任务将在当前线程中执行。
    - `std::launch::async | std::launch::deferred`：系统决定任务应该在哪个线程中执行。
- `callable`：希望异步执行的可调用对象（比如函数指针、lambda 表达式等）。
- `args` 是传递给 `callable` 的参数。
**说明**：虽说在名称上是异步，但是这并不是现代意义上的 async/await 型异步。`launch::async` 实际上就是创建新线程并行执行，而 `launch::deferred` 是使用延迟执行的伪异步，并不具备并发性。也就是说此异步只是语义上的 `std::future` 并不是非阻塞 IO / 事件驱动协作式异步。直到 C++ 20 增加了协程机制，才带来了真正的语言级异步机制，才能实现现代意义上的异步。但是截止 C++ 23 仍未提供官方的异步 API ，目前仍是第三方实现。`std::async` 更像一个“轻量级的、不可调优的、实现自带的小线程池或线程管理器”，而不是现代意义上的异步系统。
#### (3). 原子操作
C++11 标准化了 CPU 层级的 无锁原子操作。支持原子读写，原子加减/交换，内存序语义，lock-free 判断。atomic 是现代高性能并发（lock-free / wait-free）的基础。
```cpp
std::atomic<int> counter{0};

void f() {
    counter.fetch_add(1);
}
```
