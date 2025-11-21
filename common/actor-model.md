---
title: Actor 模型
tags:
  - common
  - concurrency
  - actor-model
---
## 概述
Actor 模型以一个 Actor 为单元，每个 Actor 拥有自己的邮箱（Mailbox），Actor 之间不共享内存，其他线程通过异步通信发消息到邮箱，Actor 通过收到的消息改变自己的状态。Actor 实际执行中有三个核心部件：`ActorSystem` （管理所有 Actor ，提供调度器和消息路由）、`Dispatcher` 调度器（负责从 `mailbox` 中取出消息并调用 Actor 的逻辑）、`Mailbox` 邮箱（队列，用于存储待处理的消息）。
## Actor 模型的简易实现


