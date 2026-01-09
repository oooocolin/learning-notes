---
title: 单例模式
tags:
  - common
  - design-pattern
  - singleton
---
## 概述
单例模式的核心目的是控制生命周期与共享边界，如果仅是为了方便访问或是为了全局唯一对象，那 90% 是误用。单例常见于一些资源不可复制 / 不应复制或是为了保持全局一致性的场景，比如数据源、线程池、本地注册表等。
## 实现
```java
public final class ConfigRegistry {
	
    private ConfigRegistry() {}
	
    private static final ConfigRegistry INSTANCE = new ConfigRegistry();
	
    public static ConfigRegistry getInstance() {
        return INSTANCE;
    }
}
```
这种实现保证线程安全，类加载期就完成初始化，无锁，无歧义。此外，Java 特有的枚举单例，在框架中更常使用。
```java
public enum MetricsRegistry {
    INSTANCE;

    public void record(...) { }
}
```
## 注意
### 懒加载式单例几乎是陷阱
```java
public class LazySingleton {
    private static LazySingleton instance;
	
    public static LazySingleton getInstance() {
        if (instance == null) {
            instance = new LazySingleton();
        }
        return instance;
    }
}
```
- 懒加载式单例在启动期创建一次和运行时创建一次，这在业务场景中成本无差别，这种形式往往只是看起来高级。
- 线程不安全。
### Spring 的 singleton 不等于 GoF 单例模式
- Spring 的 singleton 是容器作用域，表示在容器内只有一个实例，而不是指的是 JVM 级别的唯一。
- Spring Bean 是创建一次使用一次的全局对象，本身仍可以使用 `new` 创建对象，而经典单例是全局唯一的对象实例，两者存在本质不同。
- 所以在 Spring 框架内不需要自己写单例，全局唯一性由容器保证。
### 合理使用单例范围
#### (1). 合理使用
- 在不依赖 DI 容器，并对象且本身需要全局唯一，并且多次创建会出现问题时才使用单例，同时推荐使用类外统一管理实例 `DatabaseManager dbManager = DatabaseManager.getInstance();` ，而不是类本身控制。
- JVM 级注册表、底层工具库等。
#### (2). 不合理使用
- 服务对象做成单例。`UserService.getInstance()` 这样强耦合，难以测试，存在隐式依赖关系。
- 把单例当做全局变量，造成隐式上下文，不可预测副作用以及并发问题。
### 单例模式的退场
在现代语言大量支持类似 “模块” 的结构的情况下，“模块”是一等公民，语言提供了比设计模式更高层的抽象单元，所以在这些语言中更推荐使用模块的全局变量来代替单例设计模式，比如在 C# 、Kotlin 、TypeScript 等。而在 Java 也被吸收进入框架内，以容器的方式存在，成为更为复杂的实现。
