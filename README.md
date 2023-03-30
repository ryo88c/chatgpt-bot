# What is this

メンションを飛ばすと OpenAI の API を使って返信をしてくれる Slack ボットの最小サンプルです。
Slack からの HTTP リクエストは3秒以内にレスポンスしなければなりませんが、OpenAI の API はレスポンスが返ってくるまで数十秒かかることもあります。
そのため、Slack からのリクエストボディは Redis に保存してすぐに `200 OK` を返しています。
`reply.py` を実行することで Redis に保存されているメッセージを OpenAI に送信し、レスポンスをスレッドに返信します。

# Sequence

```plantuml
@startuml
group Catch a mention by __init__.py
    Slack -> App: Mention
    App -> Redis: Set mention
    App -> Slack: 200 OK
end
group Ask OpenAI by reply.py
    App -> Redis: Pop mentions
    Redis -> App: Mentions
    loop All mentions
        App -> "OpenAI API": Chat by the mention
        "OpenAI API" -> App: Answer
        App -> Slack: Reply on a thread
    end
end
@enduml
```