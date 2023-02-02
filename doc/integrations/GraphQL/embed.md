# Sphinx 嵌入 GraphiQL 视图

参考：[embed-graphiql](https://dls-controls.github.io/sphinx-graphql/master/how-to/embed-graphiql.html)

安装：

```bash
pip install sphinx-graphql
```

Sphinx 配置：

```bash
extensions = [
    # <Preexisting config>
    ...,

    # Directive for embedding GraphiQL view in documentation
    "sphinx_graphql.graphiql",
]
```

## GraphiQL 视图

`graphiql` 指令允许在文档中嵌入 GraphiQL 视图，如果服务器可用，可以选择使其实时编辑。

### 静态嵌入式视图

```
.. graphiql::
  :query:
    {
      country(code: "BR") {
        name
        native
        capital
        emoji
        currency
        languages {
          code
          name
        }
      }
    }
  :response:
    {
      "data": {
        "country": {
          "name": "Brazil",
          "native": "Brasil",
          "capital": "Brasília",
          "emoji": "🇧🇷",
          "currency": "BRL",
          "languages": [
            {
              "code": "pt",
              "name": "Portuguese"
            }
          ]
        }
      }
    }
```

渲染：

```{eval-rst}
.. graphiql::
  :query:
    {
      country(code: "BR") {
        name
        native
        capital
        emoji
        currency
        languages {
          code
          name
        }
      }
    }
  :response:
    {
      "data": {
        "country": {
          "name": "Brazil",
          "native": "Brasil",
          "capital": "Brasília",
          "emoji": "🇧🇷",
          "currency": "BRL",
          "languages": [
            {
              "code": "pt",
              "name": "Portuguese"
            }
          ]
        }
      }
    }
```

### 实时，可编辑的视图

如果具有 GraphQL API 的服务器可用，则可以配置 Sphinx 视图来使用它。在这种情况下，它变成可编辑的：

```
.. graphiql:: https://countries.trevorblades.com/
    :query:
      {
        country(code: "BR") {
          name
          native
          capital
          emoji
          currency
          languages {
            code
            name
          }
        }
      }
    :response:
      {
        "data": {
          "country": {
            "name": "Brazil",
            "native": "Brasil",
            "capital": "Brasília",
            "emoji": "🇧🇷",
            "currency": "BRL",
            "languages": [
              {
                "code": "pt",
                "name": "Portuguese"
              }
            ]
          }
        }
      }
```

渲染：

```{eval-rst}
.. graphiql:: https://countries.trevorblades.com/
    :query:
      {
        country(code: "BR") {
          name
          native
          capital
          emoji
          currency
          languages {
            code
            name
          }
        }
      }
    :response:
      {
        "data": {
          "country": {
            "name": "Brazil",
            "native": "Brasil",
            "capital": "Brasília",
            "emoji": "🇧🇷",
            "currency": "BRL",
            "languages": [
              {
                "code": "pt",
                "name": "Portuguese"
              }
            ]
          }
        }
      }
```

```{note}
如果 `https://countries.trevorblades.com/` 不可用，视图将恢复到静态情况。
```
