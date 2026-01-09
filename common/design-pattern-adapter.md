---
title: 适配器模式
tags:
  - common
  - design-pattern
  - adapter
---
## 概述
适配器模式解决的核心问题是接口不兼容，但你又不能（或不该）改原有实现。这是个现实世界问题，不是来源于语言能力不足，所以至今仍然活跃。因为历史包袱（旧接口）、第三方库（你不能改）、边界系统（协议不同）这三者是长期存在的是架构边界的常见问题。  
一般来说对接口进行二次封装或是框架化都用到了这一思想，比如在 Java 中一般的 ORM ，其实都是对 JDBC 的适配封装，都使用到了这一思想。从模式来看，这些 ORM 更为好用是受适配器的影响，强大需要其他模式的配合，比如装饰器、代理、策略等。  
对于适配器模式的替代一般是在轻量的机制方面，对于一些存在函数或是 Lambda 机制存在的，且适配器本身修改不多只需 1~2 个地方的场景，使用函数式的修改是更为轻量化的选择，而面对更为重大或是关联性较强的转换方法仍应该使用类结构。
## 实际场景
### 统一支付接口
已有第三方 SDK ：
```java
class AliPayClient {
    void pay(String orderNo, BigDecimal amount) {}
}
```
希望统一接口如下：
```java
interface PaymentService {
    void pay(PaymentRequest request);
}
```
适配器：
```java
class AliPayAdapter implements PaymentService {
    private final AliPayClient client;
	
    AliPayAdapter(AliPayClient client) {
        this.client = client;
    }
	
    @Override
    public void pay(PaymentRequest request) {
        client.pay(request.orderNo(), request.amount());
    }
}
```
### Spring 的适配器设计
框架中的适配器，通常不是一个类，而是一组协作结构，通常是 “接口 + 注册表 + 路由逻辑” ，并且适配发生在运行时，而不是编译期，适配对象往往是 “不可控的外部类型” 。典型例子就是 `HandlerAdapter` 。Spring MVC 支持多种 Controller 形式，如下。
- `Controller` 接口
- `@Controller` 注解方法
- `HttpRequestHandler` 
- 函数式 Handler 
它们的接口完全不同，解决方就是每种 Controller 类型，对应一个 Adapter，建立起一个重型适配器体系（一个统一框架中，支持完全不同的编程模型），包含 `SimpleControllerHandlerAdapter` 、`RequestMappingHandlerAdapter` 、`HttpRequestHandlerAdapter` 等。执行流程如下。
```
DispatcherServlet
   ↓
找到 handler
   ↓
遍历 HandlerAdapter
   ↓
supports(handler) ?
   ↓
用对应 Adapter 执行
```
## 与装饰器模式辨析
适配器模式与装饰器模式是 GoF 设计模式中最容易混淆的模式。两者的结构上有某些场景是一样的，但是两者的意图不同，也就决定了两者不同的模式存在。
- 适配器模式偏向处理外部的无法使用或是使用不友好的进行内部的转换诉求，而装饰器则是偏向在内外部可用的情况下，是否进行增强功能的这一诉求。
- 在实际工程中，适配器已经主要用于边界、遗留系统、第三方 SDK 的改造，而不是作为内部演进。因为这会导致内部结构更为臃肿，难以为继。在迭代版本的演进中，内部代码应该通过重构演进而不是嵌套的方式。装饰器在内部结构相对合理，因为装饰器不改变接口，不改变调用方认知，可以叠加和撤销，但更适合扩展同样不是代码演进。
