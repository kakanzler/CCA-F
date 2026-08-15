# [Structured data](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287732)

## Summary

- *問題*
  - Claudeは出力に` ```json ～ ``` `や、` - aaa, -bbb `などのmarkdownの説明的な文字をつかうことがあるがこういったものを排除しrawデータが欲しい場合の対処方法

- *対処方法*
  - 以下の2点を実施する。
    1. **Prefilling**: Claudeにメッセージを送付する際に`"role" : "user"`のメッセージに追加した後、さらに、 `"role" : "assistant"`を追加し、そのメッセージに` ```json `のように先にClaudeが出力してくれそうな説明的な文字を入力しておく。
    2. **Stop Sequence**: `client.mesasges.create()`の引数に`stop_sequences=["```"]`といれる。

- *Key*
  - Claudeが構造データを包みがちなラッパーを見極め、その開始側を`Prefilling`に、終了側を`Stop Sequence`に指定すること。コードならmarkdownのコードフェンス、箇条書きなら番号や改行など、対象によってラッパーは変わる。

### Note/Tips

- jsonとして出力してもらったものはpythonのbuilt-inライブラリの`json`などで整形して次プロセスに渡すとよい。

- このテクニックはjsonのみならず、pythonなどのコードブロックやCSVなどにも有効。

## Supplement

- これもUXを低くさせてしまう原因を排除しようというテクニック。
- Claudeへ送信するassistant messageに ````json`と記載することでClaudeはjsonブロックを出力すればいいんだ、と解釈してくれる。

- Prefillに入れた文字列（` ```json ` など）はAPIのレスポンスには含まれない。返ってくるのは「その続き」だけなので、そのままパースに回せる。
- Stop Sequenceで停止した場合、`stop_reason`は`"end_turn"`ではなく`"stop_sequence"`になり、ヒットした文字列自体も出力には含まれない。
- Prefillの直後は改行が入りやすいため、パース前に`text.strip()`を挟むのが定石（origin.mdも`json.loads(text.strip())`としている）。

## Reference

```python
messages = []
add_user_message(
    messages=messages,
    text="もっとも簡単な構成のmcp_server.pyのコードを教えて"
)
add_assistant_message(messages,text="```python")
answer_python = client.messages.create(
    messages=messages,
    max_tokens=1000,
    model=model,
    stop_sequences=["```"]
)
# output : answer_python.content[0].text.replace('\n', '')
# 'import jsonimport sysfrom typing import Anydef process_request(request: dict) -> dict:    """MCPリクエストを処理"""    method = request.get("method")        if method == "initialize":        return {            "protocolVersion": "2024-11",            "capabilities": {},            "serverInfo": {                "name": "simple-mcp-server",                "version": "1.0.0"            }        }        elif method == "resources/list":        return {            "resources": []        }        elif method == "tools/list":        return {            "tools": [                {                    "name": "hello",                    "description": "あいさつ",                    "inputSchema": {                        "type": "object",                        "properties": {                            "name": {"type": "string"}                        }                    }                }            ]        }        elif method == "tools/call":        tool_name = request.get("params", {}).get("name")        if tool_name == "hello":            name = request.get("params", {}).get("arguments", {}).get("name", "World")            return {                "content": [                    {                        "type": "text",                        "text": f"Hello, {name}!"                    }                ]            }        return {"error": "Unknown method"}def main():    while True:        try:            line = sys.stdin.readline()            if not line:                break                        request = json.loads(line)            response = process_request(request)            print(json.dumps(response))            sys.stdout.flush()                except Exception as e:            error_response = {"error": str(e)}            print(json.dumps(error_response))            sys.stdout.flush()if __name__ == "__main__":    main()'

messages = []
add_user_message(
    messages=messages,
    text="スピーキングに必要なことを3点箇条書きで教えて"
)

add_assistant_message(messages, text="1.")
answer_list = client.messages.create(
    messages=messages,
    max_tokens=1000,
    model=model,
    stop_sequences=["\\n"]
)
# output : answer_list.content[0].text
# 1. 語彙や文法の基礎知識
#     - 実際に使える単語や表現を身につけておくこと
# 2. 継続的な発話練習
#     - 実際に声に出す、独り言、会話練習など繰り返すこと
# 3. 聴く力（リスニング）
#     - 他者の発話を理解し、自然な流れで応答すること

```