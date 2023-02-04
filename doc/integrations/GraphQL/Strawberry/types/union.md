(Union types)=
# 联合类型

然而，联合（Union）类型与[接口](./interfaces)类似，而接口规定的字段必须对所有实现通用，而联合则不是。联合只表示允许的类型的选择，并且对这些类型没有要求。下面是用 GraphQL 模式定义语言([SDL](https://graphql.org/learn/schema/#type-language))表示的联合：

```
union MediaItem = Audio | Video | Image
```

每当在模式中返回 `MediaItem` 时，可能会得到 `Audio`、`Video` 或 `Image`。注意，联合类型的成员必须是具体的对象类型；不能在接口、其他联合或标量之外创建联合类型。

联合的一个很好的用例将出现在搜索字段中。例如：

```
searchMedia(term: "strawberry") {
  ... on Audio {
    duration
  }
  ... on Video {
    thumbnailUrl
  }
  ... on Image {
    src
  }
}
```

这里，`searchMedia` 字段返回 `[MediaItem!]!`，其中每个成员都是 `MediaItem` 联合的一部分。对于每个成员，希望选择不同的字段取决于成员是哪种类型的对象。可以通过使用[内联片段](https://graphql.org/learn/queries/#inline-fragments)来做到这一点。

## 定义联合

在 Strawberry 中有两种方式来定义联合：

你可以从 {mod}`typing` 模块中使用 `Union` 类型，它会根据 `Union` 成员的名字自动生成类型名：

```python
import strawberry

@strawberry.type
class Audio:
    duration: int

@strawberry.type
class Video:
    thumbnail_url: str

@strawberry.type
class Image:
    src: str

@strawberry.type
class Query:
    latest_media: Audio | Video | Image
```
```
union AudioVideoImage = Audio | Video | Image

type Query {
  latestMedia: AudioVideoImage!
}

type Audio {
  duration: Int!
}

type Video {
  thumbnailUrl: String!
}

type Image {
  src: String!
}
```

或者如果需要指定名称或描述，你可以使用 `strawberry.union` 函数：

```python
import strawberry

@strawberry.type
class Query:
    latest_media: strawberry.union("MediaItem", types=(Audio, Video, Image))
```
```
union MediaItem = Audio | Video | Image

type Query {
  latest_media: MediaItem!
}

type Audio {
  duration: Int!
}

type Video {
  thumbnailUrl: String!
}

type Image {
  src: String!
}
```

## 解析联合

当字段的返回类型是联合时，GraphQL 需要知道为返回值使用什么特定的对象类型。在上面的例子中，每个 `MediaItem` 必须被分类为 `Audio`、`Image` 或 `Video` 类型。要做到这一点，你需要总是从你的解析器返回对象类型的实例：

```python
from typing import Union
import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def latest_media(self) -> Union[Audio, Video, Image]:
        return Video(
            thumbnail_url="https://i.ytimg.com/vi/dQw4w9WgXcQ/hq720.jpg",
        )
```
