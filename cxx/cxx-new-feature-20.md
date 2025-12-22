---
title: C++ 20 新特性
tags:
  - cxx
  - language-feature
---
## 模板类型约束
### 概述
在 C++ 20 前，模板参数可以是任意类型，错误只在实例化时才报出，错误信息冗长，不容易对用户提供清晰的约束。此前使用 `enable_if` + SFINAE 解决，但是语法复杂，难以维护。C++ 20 引入 Concepts 为了提前约束模板类型，能清晰表达意图，可以在编译期检查，如果类型不满足要求，直接报错，并且改善错误信息。
### 实现
```cpp
#include <concepts>

template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
};
```
- `requires(T a, T b) { ... }`：要求类型 T 可以进行 `a + b` 操作。
- `-> std::same_as<T>`：要求结果类型与 T 相同。
- `Addable` 就是一个类型约束。
使用约束进行设置模板参数列表，这样 T 必须满足 `Addable` ，不满足就直接报错，错误信息清晰。以下是两种写法，语义一致，只是写法不同。
```cpp
template<Addable T>
T add(T a, T b) {
    return a + b;
}

template<typename T>
requires Addable<T>
T add(T a, T b) {
    return a + b;
}
```
以下这种写法，更为灵活，可针对函数重载使用不同约束。
```cpp
template<typename T>
T add(T a, T b) requires Addable<T> {
    return a + b;
}
```
### 标准库支持 Concepts
| Concept                         | 说明            |
| ------------------------------- | ------------- |
| `std::integral<T>`              | T 是整型         |
| `std::floating_point<T>`        | T 是浮点型        |
| `std::signed_integral<T>`       | 有符号整数         |
| `std::unsigned_integral<T>`     | 无符号整数         |
| `std::derived_from<T, U>`       | T 是 U 类或U类派生类 |
| `std::same_as<T, U>`            | T 与 U 类型相同    |
| `std::assignable_from<T, U>`    | 可以赋值          |
| `std::default_initializable<T>` | 可默认构造         |
| …                               | …             |
## Ranges
### 概述
此前，STL 的算法通常依赖迭代器区间。算法参数是迭代器，不直观，用户需要手动传入 `.begin()` / `.end()` ，进行链式操作很困难，且语义不够贴近 “集合/范围” 的概念。
```cpp
std::vector<int> v = {1,2,3,4,5};
std::sort(v.begin(), v.end());
auto it = std::find(v.begin(), v.end(), 3);
```
### 核心
#### (1). Range（范围）
范围相当于一对迭代器 + 边界，或者一个可迭代对象。本质上就是一个可迭代的集合。
```cpp
std::vector<int> v = {1,2,3};
auto r = v;  // v 本身就是 range
```
#### (2). View（视图）
视图是轻量、非拥有型范围，不拷贝底层数据，懒求值（按需计算）。其典型操作有 `filter` / `transform` / `take` / `drop` 。
```cpp
std::vector<int> v = {1,2,3,4,5};
auto evens = v | std::views::filter([](int x){ return x % 2 == 0; }); // {2, 4}
```
- `evens` 是视图，没有创建新容器。
- 底层直接引用 `v` 数据。
#### (3). Adapter（适配器）
Range 可以通过适配器组合操作，进行变换、筛选操作。
```cpp
auto r = v 
         | std::views::filter([](int x){ return x % 2 == 0; })
         | std::views::transform([](int x){ return x*x; });
```
- 链式调用，懒求值。
- 只有在遍历（`for` / `copy` / `accumulate`）时才真正计算。
### 使用
这样就不用分别传入迭代器，直接使用尤其是 STL 算法中，比如排序。
```cpp
std::ranges::sort(v);
```
## constexpr 再增强
C++ 20 支持在 constexpr 实现动态内存分配（`new/delete`），允许完整的 `try/catch`，允许虚函数，允许容器在编译期创建（元素是字面量类型），支持所有 STL 算法的执行。
```cpp
constexpr int* create_array(int n) {
    int* arr = new int[n];
    for (int i = 0; i < n; ++i) arr[i] = i;
    return arr;
}

constexpr auto arr = create_array(5);  // C++20 才允许
```
## 三路比较符（`<=>`）
### 概述
三路比较符 `<=>` ，用于提供一种方式，以要求编译器为某个类生成相一致的关系运算符，专用于类由编译器生成的运算符。此前的仅单独的进行操作符进行操作上的保证，如下。
```cpp
struct A {
    int x;
};

bool operator<(const A& a, const A& b) {
    return a.x < b.x;
}
```
虽然写了 `<` ，但实际上，`==` 、 `>` 、 `<=` 、`>=` 也要写，且一致性完全靠人为保证。现在可以使用三路比较符一次性确定，并且不再回答比较结果的真假，而是返回 “小于 / 大于 / 等于” 的比较结果对象。
### 比较结果对象
|类型|适用场景|说明|
|---|---|---|
|`std::strong_ordering`|整型、字符串|全序、等价即相等|
|`std::weak_ordering`|忽略某些字段的排序|等价 ≠ 相等|
|`std::partial_ordering`|浮点数|存在“不可比”（NaN）|
以上是标准定义的三种比较类别，以整型、字符串类别比较为例，其比较结果对象如下。
```cpp
std::strong_ordering::less
std::strong_ordering::equal
std::strong_ordering::greater
```
### 实现
一个最基本的 `<=>` 实现如下，这是使用编译器自动生成比较结果方法。
```cpp
#include <compare>

struct A {
    int x;
	
    auto operator<=>(const A&) const = default;
};
```
- 生成 `<` 、 `<=` 、 `>` 、 `>=` 、 `==` 、 `!=` 。
- 返回类型自动推导为 `std::strong_ordering` 。
也可以显式实现。
```cpp
struct A {
    int x;
	
    std::strong_ordering operator<=>(const A& other) const {
        if (x < other.x) return std::strong_ordering::less;
        if (x > other.x) return std::strong_ordering::greater;
        return std::strong_ordering::equal;
    }
};
```
**注意**：初期 C++ 20，只定义 `<=>` 的话，不会自动生成 `==` ，到了 C++ 20 最终标准中已经补齐了这一点，也可以通过三路比较符来进行生成。
## 模块化
C++ 20 更新的模块化是对 C++ 构建模型的结构性修复，目标是解决传统宏的 `#include` 导入方式的问题。传统 `#include` 并不是 “模块” ，而是简单的文本替换，没有语义边界，并且会造成宏污染、重复解析、头文件链极深等问题。模块使用 `export/import` 进行，语义导入，一次编译多次导入，并且在编译器就可被感知。
```cpp
// math.cppm
export module math;

export int add(int a, int b);
```

```cpp
// math.cpp
module math;

int add(int a, int b) {
    return a + b;
}
```

```cpp
import math;

int main() {
    return add(1, 2);
}
```
这样就不需要使用 `#include` ，也不需要有头文件，也没有宏泄漏。只是在一些官方库和第三方库支持还需后续支持，所以目前头文件的方式使用仍然广泛。但是目前也有了头单元，对现有头文件做了模块化封装，把现有的头文件当做模块导入，这样就不会重复解析整个头文件，比如 `import <vector>` 、`import <string>` 。
## 协程 Coroutines
### 概述
C++ 20 此前的仅能支持线程并行和 `future/promise` 的伪异步执行，但是其实并没有实现现代意义的异步，不是线程内挂起和恢复。C++ 20 支持的协程就能补足此前的缺陷。
### 核心结构
- `co_await`：暂停当前函数，等待一个 awaitable 对象完成，用于异步执行。
- `co_yield`：暂停当前函数，将一个值返回给调用者，用于生成器。
- `co_return`：协程完成时返回最终结果。
- 协程句柄（handle）：编译器生成一个对象保存状态机，用于 resume / destroy 协程。
### 语法示例
由于 C++ 官方只是提供了协程语言特性上的支持，但是生成器等需要自己实现或是第三方库实现，目前有开源库 `cppcoro` 提供 `generator<T>` 和 `task<T>` 以及 `folly` / `libunifex`是 Facebook 和 Microsoft 提供的更高级协程工具使用。简易的生成器实现思路如下。
```cpp
#include <coroutine>
#include <optional>
#include <iostream>

template<typename T>
struct Generator {
    struct promise_type {
        std::optional<T> current_value;
		
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
		
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
		
        std::suspend_always yield_value(T value) {
            current_value = value;
            return {};
        }
		
        void return_void() {}
        void unhandled_exception() { std::exit(1); }
    };
	
    std::coroutine_handle<promise_type> handle;
	
    Generator(std::coroutine_handle<promise_type> h) : handle(h) {}
    ~Generator() { if (handle) handle.destroy(); }
	
    bool next() {
        if (!handle.done()) {
            handle.resume();
        }
        return !handle.done();
    }
	
    T value() {
        return *handle.promise().current_value;
    }
};

// 使用示例
Generator<int> numbers(int n) {
    for (int i = 0; i < n; ++i) {
        co_yield i;
    }
}

int main() {
    auto gen = numbers(5);
    while (gen.next()) {
        std::cout << gen.value() << "\n";
    }
}
```
### 协程的底层机制
- 把函数拆成状态机，每个 `co_await` / `co_yield` 是一个挂起点，编译器生成隐藏成员变量存储局部变量和当前位置。
- 生成句柄 / promise_type ，用于控制 `resume` / `destroy` / 获取返回值，`promise_type` 定义协程生命周期和交互方式。
所以协程本质上就是由编译器生成状态机实现函数可暂停，句柄和 `promise_type` 提供接口实现外部控制协程。
## 强化 lambda

