---
title: 闭包
tags:
  - common
  - closure
---
## 一、概述
闭包是一种特殊类型的对象，它由一个函数以及创建该函数时存在的作用域中的变量组成。一个函数内部定义了另一个函数，内部函数引用了外部函数的局部变量，外部函数返回了内部函数，这时即使外部函数执行结束，它的局部变量仍然会被内部函数“捕获”并保留下来，这就形成了闭包。
## 二、代码框架
Python 和 JavaScript 都存在闭包的概念，其基本概念与代码框架是共通的。
```python
def outer(x):
    def inner(y):
        return x + y
    return inner

adder = outer(10)
print(adder(5))  # 输出 15
```

```js
function outer(x) {
  return function inner(y) {
    return x + y;
  };
}

const adder = outer(10);
console.log(adder(5)); // 输出 15
```
两者在使用场景上略有区别：
- Python：装饰器的实现、延迟计算、状态保存。
- JavaScript：模块封装、回调状态、异步逻辑。






