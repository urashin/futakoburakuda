入力されたSNS投稿を変換するAPI

# 環境構築
- googleのNatural Language APIから`secrets.json`を`textapi/`フォルダ直下に置く
- dockerイメージをビルドして実行する
```
$cd textapi/
$docker build -t textapi .
$docker run -d -p 8080:8080 textapi
```

# アクセス方法
- curlを使って以下のようにAPIを叩いてください．jqを使うとunicodeをデコードして見ることができます
```
$ curl -X POST -H "Content-Type:application/json" -d "{\"text\": \"今日はラーメンがとても美味しかった\", \"filterMode\": \"jk\"}" localhost:8080/transform
{"text":"\u30e9\u30fc\u30e1\u30f3\n\u3042\u3041\u3041\u3041\u2026\u2026(\u8a9e\u5f59\u529b)"}

$ curl -X POST -H "Content-Type:application/json" -d "{\"text\": \"今日はラーメンがとても美味しかった\", \"filterMode\": \"jk\"}" localhost:8080/transform | jq .
{
  "text": "ラーメン\nあぁぁぁ……(語彙力)"
} 
```