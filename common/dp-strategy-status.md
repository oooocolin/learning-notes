---
title: 策略模式和状态模式
tags:
  - common
  - design-pattern
  - strategy
  - status
---
## 概述
策略模式和状态模式面对同一个问题，就是同一个对象，在不同条件下，行为不一样，而且这种差异会持续演化。这一般场景是使用 `if/switch` 进行分支判断，但是当分支判断结构越来越长之后，就需要策略模式 / 状态模式进行优化了。策略模式偏向将行为提取出来抽象为可替换对象，关注点是行为差异、算法替换、调用方的主动选择；状态模式偏向将状态对象中，并允许状态在内部自动切换。
## 模式介绍
### 策略模式
策略模式把算法或行为抽象成可替换的对象。通过注入不同的接口实现来实现不同的策略。策略模式常用于以下场景：
- 行为差异并列。
- 彼此无状态依赖。
- 切换逻辑在调用方。
```java
interface PricingStrategy {
    BigDecimal calculate(Order order);
}

class NormalPricing implements PricingStrategy { ... }
class VipPricing implements PricingStrategy { ... }
class PromotionPricing implements PricingStrategy { ... }

class OrderService {
    private final PricingStrategy strategy;
	
    OrderService(PricingStrategy strategy) {
        this.strategy = strategy;
    }
	
    BigDecimal price(Order order) {
        return strategy.calculate(order);
    }
}
```
这里演示的是不可变策略的情况，若需进行可切换设计则可以不使用 `final` 关键字。这样的形式没有使用 if 并且决策权在外部。
### 状态模式
状态模式把对象在不同状态下的行为封装到状态对象中，并允许状态在内部自动切换。状态对象自己决定是否切换，并且行为 + 状态迁移绑在一起。
```java
// 状态接口
public interface OrderState {
    void pay(OrderContext ctx);
    void ship(OrderContext ctx);
    void cancel(OrderContext ctx);
}

// 定义上下文
public class OrderContext {
    private OrderState state;
	
    public OrderContext() {
        this.state = new CreatedState(); // 初始状态
    }
	
    public void setState(OrderState state) {
        this.state = state;
    }
	
    // 调用行为，由当前状态对象决定执行逻辑
    public void pay() {
        state.pay(this);
    }
	
    public void ship() {
        state.ship(this);
    }
	
    public void cancel() {
        state.cancel(this);
    }
}

// 初始状态
public class CreatedState implements OrderState {
    @Override
    public void pay(OrderContext ctx) {
        System.out.println("支付成功，订单进入已支付状态");
        ctx.setState(new PaidState());
    }
	
    @Override
    public void ship(OrderContext ctx) {
        System.out.println("订单未支付，无法发货");
    }
	
    @Override
    public void cancel(OrderContext ctx) {
        System.out.println("订单取消成功");
        ctx.setState(new CancelledState());
    }
}

// 已支付状态
public class PaidState implements OrderState {
    @Override
    public void pay(OrderContext ctx) {
        System.out.println("订单已支付，不可重复支付");
    }
	
    @Override
    public void ship(OrderContext ctx) {
        System.out.println("订单发货成功");
        ctx.setState(new ShippedState());
    }
	
    @Override
    public void cancel(OrderContext ctx) {
        System.out.println("订单已支付，无法取消");
    }
}

// 已发货状态
public class ShippedState implements OrderState {
    @Override
    public void pay(OrderContext ctx) {
        System.out.println("订单已发货，不可支付");
    }
	
    @Override
    public void ship(OrderContext ctx) {
        System.out.println("订单已发货，无法重复发货");
    }
	
    @Override
    public void cancel(OrderContext ctx) {
        System.out.println("订单已发货，无法取消");
    }
}

// 已取消状态
public class CancelledState implements OrderState {
    @Override
    public void pay(OrderContext ctx) {
        System.out.println("订单已取消，无法支付");
    }
	
    @Override
    public void ship(OrderContext ctx) {
        System.out.println("订单已取消，无法发货");
    }
	
    @Override
    public void cancel(OrderContext ctx) {
        System.out.println("订单已取消，无需重复操作");
    }
}

// 使用
public class Main {
    public static void main(String[] args) {
        OrderContext order = new OrderContext();
		
        order.ship();   // "订单未支付，无法发货"
        order.pay();    // "支付成功，订单进入已支付状态"
        order.pay();    // "订单已支付，不可重复支付"
        order.ship();   // "订单发货成功"
        order.cancel();// "订单已发货，无法取消"
    }
}
```
这样客户端无需关心状态切换逻辑，只调用 `OrderContext.pay()` / `ship()` / `cancel()` 即可。但是由此可见，状态模式的这种实现方式，类膨胀问题十分严重，并且每个接口为了适配每一种状态操作也是臃肿不堪，那些没有使用需求的方法在实现中也要编写空方法或是抛出异常，而且有着很深的嵌套关系，类结构难以维护。
### 总结
整体上策略模式要比状态模式更加简明易懂，应用场景更广，在大型项目中的应用也随处可见。状态模式把行为的差异定义在不同的状态中，但是由于其统一的结构造成的一系列问题，导致状态模式在日常使用中没有用武之地。
## 现代实现
在现代工程中，两者都是使用 Enum + Map 的结构或是类似结构实现的，达到其轻量化、方便取用的目的。Enum 限定状态空间或是策略类型；Map 保存其对应的行为，作为一个执行表进行，内部通过函数式参数或是对象保存行为。这样对于策略模式而言，这样行为动态可配置且规则清晰，而对于状态模式，Map 消解了上下文的存在，不需要通过持有上下文这个冗余结构来实现状态切换信息。这种形式对状态模式而言算是一种 “擦边球” ，相当于使用策略模式形式维护表的维护方式来帮进行轻量化操作，但在语义上仍是状态模式的。这样两种模式在实现层面完成某种程度上的融合。
### 策略模式
```java
// 现代编程的标准形态
enum PricingStrategy {
    NORMAL(order -> ...),
    VIP(order -> ...),
    PROMOTION(order -> ...);
	
    final Function<Order, BigDecimal> calculator;
}

// 规则驱动
Map<Type, Function<Order, BigDecimal>> strategies;
```
### 状态模式
状态模式也可以以状态机的形式存在。
```java
enum OrderState {
    CREATED {
        void pay(Context c) { c.state = PAID; }
    },
    PAID {
        void ship(Context c) { c.state = SHIPPED; }
    }
}
```
