---
title: 建造者模式
tags:
  - common
  - design-pattern
  - builder
---
## 概述
建造者模式面向那些对象构造参数多、可选项多、组合复杂时，避免构造函数爆炸，通过拆解构造的步骤。关键不是创建，而是可读性、约束性以及构造过程清晰。该模式在现代工程仍然常见。在工程中常用于以下场景。
- 复杂参数组合 + 强可读性要求。
```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(uri)
    .timeout(Duration.ofSeconds(2))
    .header("X-Auth", token)
    .build();
```
- 构建过程有顺序 / 状态约束。如果 `setUrl` 未调用，`build()` 直接非法。
```java
builder
  .setUrl(...)
  .setMethod(...)
  .setBody(...)
  .build();
```
- 希望调用代码像语言一样读，构建行为比结果更重要。如一些 SQL 语句，工作流定义，规则引擎等。
```java
query
  .select("id", "name")
  .where("age > 18")
  .orderBy("name")
  .limit(10);
```
- 不可变对象。
```java
const newConfig = config
  .toBuilder()
  .timeout(5000)
  .build();
```
- 跨语言 / SDK API 设计。
## 替代
在一些语言中，使用命名参数、对象字面量、默认值等机制直接消化了 Builder 。在一些普通配置更倾向使用这些机制。Builder 建议在一些 SDK 开发、流式 API 或是需要强步骤约束的场景使用。
```ts
createUser({
  name: "Tom",
  age: 18,
  email: "a@b.com"
});
```
在框架层面也可以使用 DSL 、JSON / YAML 配置、Fluent API 实现类似机制，但已成为 API 设计风格，不再是模式本身。
## 实现
```java
public class Product {
	
    private String partA;
    private String partB;
    private String partC;
	
    private Product() {
        // 禁止外部直接 new
    }
	
    // 仅提供 getter（推荐）
    public String getPartA() {
        return partA;
    }
	
    public String getPartB() {
        return partB;
    }
	
    public String getPartC() {
        return partC;
    }
	
    // Builder 作为内部静态类（常见做法）
    public static class Builder {
		
        private Product product = new Product();
		
        public Builder partA(String value) {
            product.partA = value;
            return this; // 关键：返回自身，实现链式调用
        }
		
        public Builder partB(String value) {
            product.partB = value;
            return this;
        }
		
        public Builder partC(String value) {
            product.partC = value;
            return this;
        }
		
        public Product build() {
            // 这里可以做参数校验
            return product;
        }
    }
}
```
