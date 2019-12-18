HackDay2019に出場して、SNSを薄めるChrome Extensionを作成してプレゼンをしたのですが、裏の仕組みはどうなっているのか聞きたい、という意見をちらほら頂けたので、振り返りの意味も込めてQiitaに投稿していきたいと思います。

## つくったもの

Facebookの投稿を薄める拡張機能を作りました。
友達が投稿したテキストの内容をいい感じに一言で表現して、さらに投稿された画像も抽象度の高い画像に変換して表示してくれます。
どういう背景で作成したかは以下のスライドを見てもらえるとわかりやすいと思います。

// TODO プレゼンのスライドのリンクを入れたい

## 全体構成
今回作成したプロダクトの全体構成は以下の図のような感じです。

![全体構成.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/160829/5f7ce087-12ad-2248-908f-a922372c8a64.png)

主な構成要素は以下の5つです。
- Chrome Extension
- 文章変換API
- 画像生成/配信API
- 文章変換ライブラリ
- 画像生成ライブラリ

ここからはそれぞれの要素について解説していきたいと思います。
## Chrome extension
Chrome Extensionでは以下を行います。
- Facebookの友達が投稿したテキストと画像情報をDOMから取得する
- パースした情報をテキスト変換API, 画像生成/配信APIに渡す
- 変換前のテキストを変換後のテキストに書き換える
- 画像生成APIを叩いて生成された画像の特徴タグと画像のパスを受け取る
- 変換前の画像のパスを生成した画像のパスに置き換える

## 文章変換API
文章変換APIでは、以下を行います。

- 友達が投稿した文章データを文章変換ライブラリを使って変換する
- 変換後の文章データをレスポンスとして返す

## 画像生成/配信API
画像生成/配信APIでは以下を行います。

### 画像生成
- 画像の特徴タグの文字列を受け取り、画像生成モジュールに渡すパラメータに変換する
- 画像生成モジュールにパラメータを渡し、画像をローカルに生成する
- 変換対象の画像のパスをハッシュにかけてユニークなファイル名を生成し、レスポンスとして返す

### 画像配信
- パスパラメータで指定されたファイル名と一致するファイルを返す

## 文章変換ライブラリ
// TODO 文章変換ライブラリの説明
## 画像生成ライブラリ 
// TODO 画像生成ライブラリの説明