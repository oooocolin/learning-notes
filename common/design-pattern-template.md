---
title: 模板方法模式
tags:
  - common
  - design-pattern
  - dp-template
---
## 概述
模板方法模式定义一个算法的骨架，将某些步骤延迟到子类中实现，使子类可以在不改变算法结构的情况下重定义某些步骤。这是一个以继承为核心的行为型模式。关键是骨架、步骤固定、局部可变。
## 实现
模板方法模式通过抽象类定义模板方法，定义若干抽象 / 钩子方法，让子类继承实现可变步骤。
```java
abstract class DataProcessor {
    // 模板方法
    public final void process() {
        readData();
        validate();
        save();
    }
	
    protected abstract void readData();
	
    protected void validate() {
        // 默认实现（Hook）
    }
	
    protected abstract void save();
}

class FileDataProcessor extends DataProcessor {
    protected void readData() {
        System.out.println("read from file");
    }
	
    protected void save() {
        System.out.println("save to db");
    }
}
```
其中非常关键的是 `process()` 是 final ，子类只能填空，不能改流程。
## 典型场景
模板方法模式是一个极度 “框架型” 的模式。可使用在以下场景中：
- 数据处理流程（read → validate → persist）。
- 网络请求处理流程。
- 测试框架（setup → test → teardown）。
- 批处理任务。
而更常见的是 Spring 中的模板方法，如 `JdbcTemplate`  、`AbstractController` 、`OncePerRequestFilter` 等。
```java
// JdbcTemplate
execute(ConnectionCallback<T> action)
```
其内部流程固定为获取连接，执行，释放资源。
## 现代实现
模板方法模式是最早期的 IoC 形态之一，调用顺序由父类决定，子类无法控制整体流程。在现代工程实践中，模板方法模式是一个没有淘汰，但已经高度退居幕后的模式。在业务代码中很少见到，在框架中非常多，形式已经被弱化。
### 语言机制层面
#### (1). Lambda / 回调
使用 Lambda / 回调符合组合由于继承的理念，而且实现更为轻量化，无需复杂结构。
```java
jdbcTemplate.execute(conn -> {
    // 只写变化部分
});
```
在这里模板方法依然存在，只是可变步骤不在通过子类实现，而是通过函数参数注入，其形式上有点类似于策略模式。
#### (2). 默认方法（Java Interface）
对于 Java 来说，还可以使用默认接口默认方法实现。这样继承层更轻。
```java
interface Processor {
    default void process() {
        step1();
        step2();
    }
    void step1();
    void step2();
}
```
### 框架层级
最典型的模板方法模式就是框架模板化
- Spring Template 系列
- Servlet Filter / Interceptor
- Test Framework（JUnit）
所以在使用的时候几乎不会自己再写模板方法类，而是使用别人的模板。
