# 为什么要创造 Strawberry？

Strawberry 的灵感来自于 dataclasses[^1]，它的目标之一是为 GraphQL 初学者和高级用户提供良好的开发体验。

除此之外，我们真的想创建和培养友好的、受欢迎的社区，让人们在 Python 中使用 GraphQL。

## 为什么要使用 Strawberry？

````{note}
目前 Strawberry 仍处于早期开发阶段，所以有可能会突然发生变化，但希望公共 API 足够稳定。
````

多亏了类型提示和数据类启发的装饰器语法，Strawberry 提供了很好的开发体验，这将有助于编写更好的 GraphQL API，同时也有助于在使用像 myypy 这样的类型检查器时发现错误。

下面是类型的基本示例，以及它与 GraphQL 中的等效类型的比较:

```python
@strawberry.type
class User:
    id: strawberry.ID
    name: str
```

```
type User {
  id: ID!
  name: String!
}
```

如您所见，该代码与使用 GraphQL SDL 编写的代码非常相似。正因为如此，我们认为 Strawberry 在代码优先和模式优先之间找到了完美的中间地带。

还将提供有用的功能和集成；例如，支持 Apollo Federation，文件上传，权限和集成流行的框架，如 Django,  ASGI 和 Flask。

最后，尝试修复错误，并通过 GitHub 或 [Discord 服务器](http://strawberry.rocks/discord) 提供帮助，所以如果有任何问题，请随意删除问题或在 Discord 上询问。

[^1]:
    更具体地说
    [talk on dataclasses](https://www.youtube.com/watch?v=epKegvx_Jws)
