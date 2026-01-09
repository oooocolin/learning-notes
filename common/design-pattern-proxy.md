---
title: 代理模式
tags:
  - common
  - design-pattern
  - proxy
---
## 概述
代理模式的核心目的是为另一个对象提供一种代理以控制对它的访问。与装饰器模式不同的在于代理模式值进行控制访问、生命周期管理、缓存等，不增强行为，两者共同点就是接口层面保持一致。
## 实际场景
### 远程代理
```java
UserService proxy = (UserService) Proxy.newProxyInstance(
    classLoader,
    new Class[]{UserService.class},
    (obj, method, args) -> {
        // 前置控制
        checkPermission();
        Object result = remoteCall(method, args); // 远程调用
        // 后置处理
        log(result);
        return result;
    }
);
```
**特点**：
- 对客户端透明
- 控制访问 + 延迟加载
- 持有原对象引用（组合模式的体现）
### AOP
AOP 本身是装饰器思想的实现，但是在实现上往往都借助着代理模式实现。因为无法在运行时，把装饰器直接塞进一个已经被创建出来的对象里。Java 的限制决定了对象一旦创建，方法调用已经绑定，就无法在外部插入一层调用逻辑。于是只能退一步用一个代理对象，拦截调用，再转发给真实对象。代理在 AOP 中是手段而不是目的。
```
Client
  ↓
Proxy  ←—— AOP 生效点
  ↓
Target
```
## 现状
代理模式一般在业务层面几乎见不到，因为业务逻辑关心的是做什么，代理解决的是怎么被调用的问题，业务代码中显式写代理，往往是坏味道。而在框架中，代理是基础设施，用来承载横切能力。

