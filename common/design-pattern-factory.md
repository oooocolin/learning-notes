---
title: 工厂模式
tags:
  - common
  - design-pattern
  - factory-method
  - abstract-factory
---
## 概述
工厂模式的核心是创建对象的逻辑封装起来，客户端不需要直接使用 `new` 创建对象，只需要告诉工厂需要什么类型，工厂返回相应的实例。其核心是把一类对象的创建综合起来，它们实现统一的抽象（接口 / 抽象类），从而保证上层依赖的接口不变。工厂模式内容不在于 Factory 类要怎么写，重点内容在于：
- 什么时候创建逻辑不该出现在调用方。
- 什么时候应该用数据 / 注册 / 配置替代 `if-else` 。
- 什么时候该停下，不要过度设计。
## 误区
- “保证上层依赖的接口不变” 这是工厂模式唯一稳定的价值点。它不意味着保证新增产品不改代码，以及不保证 “零入侵修改” ，不保证 “自动支持所有新类型” ，而是保证使用方只依赖抽象，不依赖具体实现。
- 以 `factory.create("A")` 或 `factory.create(ProductA.class)` 这样的形式，意味着客户端已经知道具体的类型，客户端已经参与了选择，那么这个工厂实质上就是把 `new` 挪了个位置，这种工厂价值有限，只剩下了集中创建逻辑这一好处（弱模式形态），但仍可用，也是日常中最常使用的工厂模式。工厂模式更大的价值形式是以 `factory.create()` 这种形式存在的，客户端不知道具体实现类，是以配置来调动需求的创建，结构复杂度决定了一般是以框架级开发使用场景使用更多。
## 三种 “工厂形态” 的层级区分
在实际场景使用工厂模式，不是一个形态，而是一个能力谱系，可依照不同的需求和场景使用不同抽象程度的工厂模式。
### 弱工厂
```java
factory.create("A")
```
本质是 `switch / if-else` 的集中，创建决策仍然在调用链路中，工厂只是替代 `new` 的地方。就导致不符合 OCP ，业务扩展时仍需修改工厂。但在业务系统中仍是可用的，因为在业务场景中，产品类型一般有限，变化的频率可预期，将其使用配置驱动反而降低可读性。而且弱工厂价值在于创建逻辑集中，生命周期、缓存、装配一致，可以营造干净统一的工程。但以下是一些不适合的危险信号，遇到则需要十分慎重。
- 分支在业务里反复出现。说明选择逻辑没有收敛。
- 产品类型被当做字符串到处传。说明系统没有清晰的产品模型，抽象层泄漏严重。
- 少量产品却只做 `new` 的集中这一件事，不对生命周期进行管理，没有创建前后的逻辑，使用并不频繁。这可能是多余的抽象。
### 半强工厂
```
factory.create(type)
→ Map<String, Supplier<T>>
```

```java
class PaymentFactory {
    private final Map<String, Supplier<Payment>> registry;
	
    Payment create(String type) {
        return registry.get(type).get();
    }
}
```
相比于弱工厂，半强工厂不再知道所有实现，实现类向工厂注册自己，创建逻辑从 `if/switch` 变为数据驱动。他满足了创建逻辑可扩展，工厂无需频繁修改，支持插件化 / 模块化，方便多团队协作，常用在需要一定扩展性但无需引入完整 IoC 的场景。是业务系统中可接受的上限。但也有一些危险使用的场景，如下。
- Key 只是没有约束的字符串而已。那相当于把 `switch` 换成了隐形的 `switch` 而已，应该使用枚举 / 值对象 / 明确的业务模型。
- 同一个 Key 在多个业务模块反复出现。说明选择职责没有收敛，工厂泄漏变化。
- 注册逻辑变得隐晦、不可追踪。例如在一些静态代码块、扫描时隐式注册等场景，使得维护成本远高于 `switch` 。
- Key 与实现语义缺乏约束。Key 没有抽象意义，那么只是类名别名，那实际上只是把类名字符串化，并没有真正解耦。
### 强工厂
```java
factory.create()
```
这样的工厂创建类型由上下文 / 配置 / 元数据 决定，调用方甚至不知道具体类型的概念。一般是框架能力，一般不在业务场景使用。Spring 框架实际上使用注册式 + 配置驱动工厂，所以一般在业务层感知不到具体的工厂实现。
## 实际场景
### 弱工厂
以导出文件模块为例。
```java
public interface Exporter {
    byte[] export(DataContext ctx);
}

class ExporterFactory {
    static Exporter create(ExportType type) {
        return switch (type) {
            case CSV -> new CsvExporter();
            case EXCEL -> new ExcelExporter();
            case PDF -> new PdfExporter();
        };
    }
}
```
这里 “不过度” 的详细原因：
- 类型枚举就是业务协议。
- 新增导出类型是需求级变更。
- 修改工厂是合理成本。
此时工厂存在是为了 “语义集中” ，不是为了 “抽象扩展” 。但仍需注意不能传字符串，`if/switch` 不能过长，构造不能复杂（不能承担 Builder 的职责）。
### 注册式工厂
核心动机是让新增实现不再修改工厂，是在业务中能用到的最强形态，有更多需求该上升到框架层级。需配合策略模式使用。以多种订单价格计算为例。
```java
public interface PricingStrategy {
    OrderType supportType();
    PricingResult calculate(PricingContext context);
}
```

```java
public class PromotionPricing implements PricingStrategy {
	
    @Override
    public OrderType supportType() {
        return OrderType.PROMOTION;
    }
	
    @Override
    public PricingResult calculate(PricingContext context) {
        // 活动价逻辑
    }
}
```

```java
public class PricingRegistryFactory {
	
    private final Map<OrderType, PricingStrategy> registry;
	
    public PricingRegistryFactory(List<PricingStrategy> strategies) {
        this.registry = strategies.stream()
                .collect(Collectors.toMap(
                        PricingStrategy::supportType,
                        Function.identity()
                ));
    }
	
    public PricingStrategy getStrategy(OrderType type) {
        PricingStrategy strategy = registry.get(type);
        if (strategy == null) {
            throw new IllegalStateException("No pricing strategy for type: " + type);
        }
        return strategy;
    }
}
```

```java
public class Application {
	
    public static void main(String[] args) {
        List<PricingStrategy> strategies = List.of(
            new NormalPricing(),
            new PromotionPricing(),
            new CrossBorderPricing()
        );
		
        PricingRegistryFactory factory =
            new PricingRegistryFactory(strategies);
		
        OrderService orderService = new OrderService(factory);
    }
}
```
注意：
- 策略不是传 type 进来判断，而是策略声明自己支持什么，这是注册式的关键。
- 如果这个结构在 Spring 框架内使用那么就将会退化为业务级策略选择器，因为在 Spring 中 BeanFactory 已经十分强大，无需自己实现工厂模式。这也是弱工厂在实际使用中更为常见的原因。
## 抽象工厂模式
### 概述
抽象工厂是简单工厂的延伸，与简单工厂不同抽象工厂在同一个工厂会创建多种抽象角色，这些角色构成一个产品族，混用会导致语义错误或运行错误。
```java
interface RpcComponentFactory {
    Transport createTransport();
    Encoder createEncoder();
    Decoder createDecoder();
}
```
这必然依靠强关联才能达到语义聚合的效果，所以业务对象很少使用抽象工厂。而且抽象工厂假设协议长期稳定，而业务协议经常变，经常拆，经常重组。所以几乎不应该自己实现抽象工厂模式，除非是在写框架、中间件、通用 SDK 等这些大型组件的时候。BeanFactory 的概念更为广泛，是超集型、框架级的抽象工厂 + 注册表 + 生命周期管理器。
### 反例
订单子系统抽象工厂，实现 OnlineOrderFactory 、OfflineOrderFactory 。
```java
interface OrderFactory {
    Order createOrder();
    Invoice createInvoice();
    Shipment createShipment();
}
```
表面看起来很像抽象工厂，有多个 create ，成套对象，Factory 实例决定族。但其实这是反模式的，体现在业务对象之间没有协议级强绑定，有的订单不需要发票，有的订单没有物流，有的发票来自第三方，所以这是强行成套，是人为制造约束，这时抽象工厂反而成了业务演进的结构性阻碍。这就是抽象工厂在业务中必然失败的原因。
