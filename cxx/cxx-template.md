---
title: C++ 模板
tags:
  - cxx
  - template
---
## 概述
模板用于编写与数据类型无关的代码，是 C++ 中实现泛型的基础，避免方法因为类型而多次重载，提高代码复用率。模板的背后原理是通过编译器根据传入类型生成具体函数的版本，在调用时调用具体的实现。模板分为函数模板和类模板。
## 语法结构
函数模板：
```cpp
// 泛型函数模板
template <typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
    cout << add(2, 3) << endl;       // int
    cout << add(2.5, 3.7) << endl;   // double
}
```
类模板：
```cpp
template <typename T>
class Box {
    T value;
public:
    Box(T v) : value(v) {}
    T get() { return value; }
};

int main() {
    Box<int> intBox(10);      // T = int
    Box<double> doubleBox(3.14);  // T = double

    cout << intBox.get() << endl;
    cout << doubleBox.get() << endl;
}
```
## 特化及偏特化
模板函数和模板类需要对传入的不同类型进行不同的处理，是针对某些类型或是某些类型模式专门写一个实现。具体而言，有全特化和偏特化之分。  
- **全特化**：模板类型里的所有类型参数全部具体指明之后处理。`template<>` 中为空，代表所有类型都在下面特殊化处理。
- **偏特化**：模板类型里的局部类型参数进行具体指明，仍保留一部分泛化类型。
```cpp
// 全特化
template<>
struct A<int,int> {
	A(){ cout<<"int, int特化版本构造函数"<<endl; } 
	void func() { cout<<"int,int特化版本"<<endl; } 
};

// 对指针类型的偏特化
template <typename T>
struct TypeInfo<T*> {
    static void print() {
        cout << "指针类型" << endl;
    }
};
```
**注意**：
- 对于函数模板没有偏特化。因为模板会自动进行重载，这相当于语义上支持更特定版本，支持偏特化的话会与重载冲突。
- 模板特化与其他语言的泛型类型约束不同。模板本身不能限制类型，只能对特定类型进行特定逻辑的实现，而泛型类型约束可以约束实现的类型。若需要限制类型需要使用 C++ 11/17 以后的约束机制。
- 模板特化需要保留最通用的那个模板，因为特化本质上只是一种实现而已。
## 类型特征
类型特征是 C++ 中的一组模板类，用于获取类型的属性、行为或特性信息。它们位于 `<type_traits>` 头文件中，从 C++ 11 开始支持。通过使用类型特征，可以根据给定类型的属性调整代码，甚至可以在模板代码中强制类型参数具有特定属性。此前只能依靠宏、模板偏特化、编译器内建魔法实现。
### 本质
类型特征本质是返回编译期常量的模板结构体，其使用形式如下。这些值在编译期就已经确定，不会引入运行时开销。
```cpp
// 典型形式
std::is_integral<T>::value   // true / false

// C++ 17 后推荐形式
std::is_integral_v<T>        // true / false
```
类型特征总和 `static_assert` 一起出现，因为类型特征的结果是 “编译期常量” ，`static_assert` 的定义是在编译期断言一个常量表达式。没有 `static_assert` 的话会错误会出现在模板实例化深处，断言使得在最早最明确的地方提前失败。
### 类型特征的功能
#### (1). 类型判断
判断某个类型是否满足某种属性。
```cpp
// 常用示例
std::is_integral_v<int>        // true
std::is_floating_point_v<int> // false
std::is_pointer_v<int*>       // true
std::is_reference_v<int&>     // true
std::is_const_v<const int>    // true
std::is_array_v<int[10]>      // true
// 面向对象相关
std::is_class_v<T>
std::is_base_of_v<Base, Derived>
std::is_polymorphic_v<T>
std::is_abstract_v<T>
```
#### (2). 类型能力检测
判断可以不可以做某件事在，这是工程中最有价值的一类。
```cpp
// 能否用一个已有对象，构造一个新对象，即 T::T(const T&)
std::is_copy_constructible_v<T>
// 一个已经存在的对象，能否被另一个对象“赋值覆盖”，即 T& operator=(const T&)
std::is_copy_assignable_v<T>
// 能否转移另一个对象的资源来构造新对象，即 T::T(T&&)
std::is_move_constructible_v<T>
// 一个已经存在的对象，能否通过移动方式被另一个对象赋值，即 T& operator=(T&&)
std::is_move_assignable_v<T>
// 对象能否被安全销毁，即 ~T()
std::is_destructible_v<T>
```
智能指针、容器类型在这些测试判断中能全都通过，手写资源类，稍有遗漏就 fail 。这正是为什么现代 C++ 强调 Rule of Zero（零法则）。
#### (3). 类型变换
在编译期生成 “新类型” 。
```cpp
std::remove_reference<T>
std::remove_const<T>
std::add_const<T>
std::decay<T>
```
示例：
完美转发、泛型容器、函数包装器的基础。
```cpp
using U = std::remove_reference_t<T>;
```
### 使用场景
#### (1). 启用/禁用模板（SFINAE）
这样非整数类型会在编译期被排除。
```cpp
template<typename T>
std::enable_if_t<std::is_integral_v<T>, void>
foo(T) {
    // 只对整数类型有效
}
```
#### (2). `if constexpr`（C++17 起，强烈推荐）
```cpp
template<typename T>
void process(T&& x) {
    if constexpr (std::is_pointer_v<T>) {
        std::cout << "pointer\n";
    } else {
        std::cout << "not pointer\n";
    }
}
```
- 未选中的分支不会参与编译、
- 极大地简化了模板代码。
#### (3). 写 “零开销的泛型代码” 
```cpp
template<typename T>
void destroy(T* p) {
    if constexpr (!std::is_trivially_destructible_v<T>) {
        p->~T();
    }
}
```
编译器会：
- 对 trivial 类型直接删除整个分支。
- 对复杂类型生成析构代码。
#### (4). 决定拷贝 / 移动策略（性能关键）
```cpp
template<typename T>
void push(T&& value) {
    if constexpr (std::is_nothrow_move_constructible_v<T>) {
        data.emplace_back(std::move(value));
    } else {
        data.push_back(value);
    }
}
```
这是 STL 容器真实采用的策略之一。
#### (5). 编译期约束与错误提示
```cpp
template<typename T>
class MyContainer {
    static_assert(std::is_default_constructible_v<T>,
                  "T must be default constructible");
};
```
错误在模板实例化阶段给出，定位清晰。
### 类型特征与 Concepts（C++20）
C++20 Concepts 本质上是对类型特征的语法级封装。
```cpp
template<typename T>
concept Movable = std::is_move_constructible_v<T>;

template<Movable T>
void foo(T);
```
Concepts 让代码更可读、错误信息更友好、约束更直观。两者不是替代关系，而是分层关系。类型特征回答 “类型是什么” ，Concepts 回答 “模板要什么” 。Concepts 本质上是 “语法糖” ，其底层也是使用类型特征，把它们包装成了编译器能理解的“约束语言”。类型特征错误发生在函数体内，错误信息模板噪音大，语义是“事后检查”；Concepts 错误发生在模板匹配阶段，错误信息非常清楚，语义是“事前约束”。
## SFINAE
### 概述
SFINAE 即是 Substitution Failure Is Not An Error ，常译为：替换失败不是错误。其内容是在模板参数替换阶段，如果某个模板候选因为类型替换失败而不合法，编译器不会报错，而是简单地把这个候选从重载集中移除。可以用来自动忽略创造中不匹配的模板。
### 作用位置
在以下位置生效：
- 模板参数
- 返回类型
- 默认模板参数
- `decltype` / `sizeof` 等不求值上下文
不在函数体内生效，比如下面的情况会直接报错。
```cpp
template<typename T>
void bar(T t) {
    t.no_such_func();  // 这里不是 SFINAE，直接报错
}
```
### 应用
一般使用 `std::enable_if` 来进行对 SFINAE 机制的利用，`enable_if_t` 是 `typename enable_if<...>::type` 的现代简写，使得语法更为简单。`std::enable_if` 内部结构如下。
```cpp
template<bool B, typename T = void>
struct enable_if {};

template<typename T>
struct enable_if<true, T> {
    using type = T;
};
```
当 B == true → `enable_if<true, T>::type` 存在；当 B == false → `enable_if<false, T>::type` 根本不存在。而这正好触发了：模板参数替换失败 → SFINAE 生效 → 模板候选被移除。
### 与 Concepts 的关系
与 `static_assert` 、Concepts 都是进行模板类型检查，SFINAE将不满足的静默移除，`static_assert` 不满足编译错误，Concepts 形成了语言级语义，使得 IDE 在代码编写时期就能被感知。由于SFINAE 的问题，比如写法晦涩、错误信息差、可读性低、极易写错等问题，现在比较少写 SFINAE，更多写的是 Concepts。
## 注意
由于 C++ 模板是在编译器在编译期间静态创建模板实现的，所以模板不存在其他静态类型语言实现泛型的泛型擦除问题（由于 Java、C# 泛型是在编译期做类型检查，运行时将类型擦除为 Object 类型）。
