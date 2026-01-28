---
title: C++ 惯用法
tags:
  - cxx
---
## 概述
C++ 惯用法是指在 C++ 编程中常用的成熟模式或技巧，用于实现特定目标。它们有助于提高代码效率、可维护性和减少错误。常见的有 RAII 、零三五法则、PImpl 惯用法、NVI 等。
## RAII（资源获取即初始化）
RAII 是 C++ 中一种流行的资源管理惯用法，它强调利用对象的生命周期来管理资源。RAII 鼓励将资源的生命周期绑定到相应对象的作用域，以便在对象创建时自动获取资源，并在对象销毁时自动释放资源（也就是不在额外的函数进行获取资源和释放资源，只在构造函数和析构函数获取和释放资源）。这有助于简化代码、避免内存泄漏并高效地管理资源。
```cpp
class ManagedArray {
public:
    ManagedArray(size_t size) : size_(size), data_(new int[size]) {
    }
	
    ~ManagedArray() {
        delete[] data_;
    }
	
    // Access function
    int& operator [](size_t i) {
        return data_[i];
    }
	
private:
    size_t size_;
    int* data_;
};
```
使用：
```cpp
ManagedArray arr(10);
arr[0] = 42;

// 后续无需自己释放资源，在离开作用域后自动释放
```
## 零三五法则
详见 [C++ 类零三五法则](class.md#零三五法则) 。
## PImpl（指向实现的指针）惯用法
### 概述
这种惯用法将类的实现细节与其接口分离，从而加快编译速度，并允许在不影响客户端的情况下更改实现。PImpl 在工程上是为了解决头文件依赖，避免任何改变都导致级联重编译。
### 示例
原写法如下：
```cpp
// foo.h
#include <vector>
#include <string>
#include "big_dependency.h"

class Foo {
    std::vector<std::string> data;
    BigType impl;
};
```
PImpl 实现：
```cpp
// foo.h
#include <memory>

class Foo {
public:
    Foo();
    ~Foo();              // 必须在 cpp 中定义
    Foo(Foo&&) noexcept; // 可移动
    Foo& operator=(Foo&&) noexcept;

private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};
```

```cpp
// foo.cpp
#include "foo.h"
#include <vector>

struct Foo::Impl {
    std::vector<int> v;
};

Foo::Foo() : impl_(std::make_unique<Impl>()) {}
Foo::~Foo() = default;
Foo::Foo(Foo&&) noexcept = default;
Foo& Foo::operator=(Foo&&) noexcept = default;
```
### 适用场景
Pimpl 是库作者的工具，不是应用开发者的默认模式，它是为了解决特定工程问题而牺牲简洁性的权衡方案。常用于以下场景：
- 对外发布的库（尤其是动态库）。
- ABI 必须稳定；头文件依赖极重。
- 构建时间是主要成本。
- 实现经常变，但接口稳定。
而在以下场景就不值得使用了：
- 内部模块。
- 模板类。
- header-only。
- 性能关键路径。
- 生命周期简单的 value type。
## 不可复制惯用法
不可复制惯用法是 C++ 中的一种设计模式，它防止对象被复制或赋值。它通常应用于管理资源的类，例如文件句柄或网络套接字，因为复制这些对象可能会导致资源泄漏或重复删除等问题。要使一个类不可复制，需要删除复制构造函数和复制赋值运算符。这可以在类声明中显式完成，从而明确告知其他程序员不允许复制。
```cpp
class NonCopyable {
protected:
  NonCopyable() = default;
  ~NonCopyable() = default;

  NonCopyable(const NonCopyable&) = delete;
  NonCopyable& operator=(const NonCopyable&) = delete;
};
```
要使用这种惯用法，只需继承该类即可 `NonCopyable` ：
```cpp
class MyClass : private NonCopyable {、
};
```
## Erase-remove（擦除-删除）惯用法
擦除删除惯用法是一种常见的 C++ 技术，用于高效地从容器中删除元素，特别是从标准序列容器（如 `std::vector` 、`std::list` 和 `std:::deque` ）中删除元素。具体而言是使用标准库算法 `std::remove` 以及容器的 `erase()` 方法。相关信息 [STL 算法修饰序列](standard-library.md#修饰序列) 。
```cpp
std::vector<int> numbers = {1, 3, 2, 4, 3, 5, 3};

// Remove all occurrences of 3 from the vector.
auto it = std::remove(numbers.begin(), numbers.end(), 3);
numbers.erase(it, numbers.end());
```
## 复制和交换惯用法
复制交换是 C++ 中的一种惯用法，它利用复制构造函数和交换函数来创建一个赋值运算符。它遵循一个简单而强大的范式：创建一个右侧对象的临时副本，并将其内容与左侧对象交换。进行以下具体流程。
- 复制：创建右侧对象的本地副本。该副本可能通过复制构造或移动构造生成。
- 交换：将左侧对象的内容与临时副本交换。此过程通常是常数时间操作。
- 销毁：临时副本在作用域结束时析构，从而释放原对象的旧资源。
这种结构能够提供强异常安全保证，即如果构造临时对象失败，当前对象保持原状。
```cpp
class T {
public:
    T(const T& other): data(new int(*other.data)) {}
	
    ~T() { delete data; }
	
    void swap(T& other) noexcept {
        std::swap(data, other.data);
    }
	
    T& operator=(T other) {  // 注意：按值传参
        swap(other);
        return *this;
    }
	
private:
    int* data;
};
```
在 C++11 之后，按值参数 `T other` 可能通过复制构造，也可能通过移动构造生成，从而自然支持移动语义。在现代 C++ 中，复制-交换惯用法依然存在，但其工程地位发生了变化。主要原因包括：
- 该赋值运算符无法声明为 `noexcept`，因为按值构造参数本身可能抛出异常。
- 标准容器（如 `std::vector`）在重新分配元素时，优先选择 `noexcept` 的移动操作，否则会退化为复制。
- 对于资源管理类型，直接实现 `T& operator=(T&&) noexcept` 通常更加高效、语义清晰，并且对容器更友好。
因此，在现代 C++ 工程中，复制-交换更多用于教学示例和需要强异常安全但性能不敏感的场景。而在性能敏感或容器友好的类型中，通常推荐显式实现 `noexcept` 的移动赋值运算符。
## 写时复制惯用法
Copy-Write（写时复制）惯用法，有时也称为 Copy-on-Write (CoW) 或 “惰性复制” 惯用法，使多个对象共享同一份数据，只有当某个对象尝试修改数据时，才真正拷贝一份私有数据，从而最大限度地减少复制大型对象的开销。使用场景在字符串类（如 `std::string` 早期实现）、图像 / 缓冲区对象、共享数据结构。  
但由于存在线程安全问题，且复杂性高，现代 STL 已经放弃 CoW 。在C++ 11 之后不推荐使用，使用移动语义和 `noexcept` 构造可以提供零开销拷贝。引用计数智能指针 `std::shared_ptr` 本质上也可以实现 CoW。
