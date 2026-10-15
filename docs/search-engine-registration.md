# 検索エンジン登録と公開後の確認

この変更は技術的SEOの整備です。検索順位・インデックス登録・検索結果のタイトルや説明文を保証するものではありません。日本語・英語の本文と既存URLは維持しています。

## 公開前

- 作業ブランチの変更をレビューし、公開を別途承認する。このPRの作成・pushだけでは公開されません。
- Google Search Consoleで、URLプレフィックスプロパティ `https://morikieng.github.io/` を追加する。これは `/en/` も含みます。
- 所有権確認はHTMLファイル方式を選び、Googleが発行するファイルをそのまま取得する。秘密情報や任意の確認コードを作成しない。
- 発行された `google…html` をリポジトリ直下へ置く。現在のルートHTMLはGitHub Pagesからそのまま配信される構成です。既存ファイルとの重複がないことを確認し、内容・ファイル名を変えずにコミットして、承認後に公開する。
- 確認ファイルはコンテンツページではないため、ナビゲーション・サイトマップ・言語切り替えの対象にしない。所有権維持のため、確認後も削除しない。
- この変更には未発行の確認ファイルや確認用metaタグは含めていません。代替のHTMLタグ方式を使う場合は、Search Consoleが発行するタグをトップページのheadへ追加し、公開後に確認する。

## 公開後（アカウント所有者が実施）

1. GitHub Pagesのデプロイ完了を確認する。`https://morikieng.github.io/` と `/en/`、`/robots.txt`、`/sitemap.xml`、`/app-ads.txt` が正常に取得できることを確認する。
2. `https://morikieng.github.io/google…html` が発行された確認内容をHTTP 200で返すことを確認し、Search Consoleの「確認」を押す。
3. 「サイトマップ」で `sitemap.xml` を送信し、取得結果と検出URLを確認する。このサイトマップは日英16ページを含む。
4. URL検査で日本語トップ `/`、英語トップ `/en/`、CAD・3Dプリントの各言語ページを検査する。必要に応じてライブテスト後にインデックス登録をリクエストする。
5. ページのインデックス登録レポートで、クロールエラー、noindex、canonicalの選択、サイトマップの処理状況を確認する。登録リクエストは登録を保証しない。
6. 検索パフォーマンスで「森樹エンジニアリング」「Moriki Engineering」、サービス関連の検索語、表示回数・クリック数を確認する。反映には時間がかかる場合がある。

## URLの重複について

- トップページの正規URLは `/` と `/en/`。`/index.html` と `/en/index.html` も既存互換のためアクセス可能だが、canonicalとサイトマップはディレクトリURLを指定している。
- 既存リンクやURLは変更しない。GitHub Pagesには任意のサーバー側リダイレクト設定がないため、今回JavaScript転送や別サービスは追加しない。
- 日英は別URLとして相互hreflangを設定し、x-defaultは対応する日本語ページを指定する。

## Yahoo! JAPAN

Yahoo! JAPANへの独立したサイト登録を今回実施したとは扱わない。Googleでの所有権確認・サイトマップ送信と、公開サイトのクロール可能性を整備したうえで、Yahoo! JAPANの検索結果も確認する。Google Search Consoleの操作だけでYahoo! JAPANへの掲載・順位が保証されるわけではない。検索サービスの現行の案内に従う。

## 構造化データと保護対象

日英トップに同一IDのOrganizationを掲載。確認済みのブランド名・英語名・URL・既存ロゴ・公開メールのみを使う。法人登記・住所・設立日・評価・実績・アプリ公開状況は追加しない。会社概要は法人設立準備中のまま。

`app-ads.txt`、アプリ紹介ページの本文、既存の外部問い合わせリンク、CSS・JavaScript・画像は維持する。新たにアプリサポートページやプライバシーポリシーが追加された場合は、公開対象を再調査してからサイトマップへの追加可否を判断する。

## 実行できるチェック

リポジトリ直下で `python3 -m unittest discover -s tests -v` を実行。標準ライブラリのみで、メタ情報、canonical・hreflang、サイトマップ、robots、ローカルリンク、構造化データの整合性を検証する。これらは検索サービスによる登録結果やリッチリザルト表示を保証しない。

公式の案内：
- [Search Consoleの所有権確認](https://support.google.com/webmasters/answer/9008080?hl=ja)
- [サイトマップの構築と送信](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=ja)
- [多言語ページの指定](https://developers.google.com/search/docs/specialty/international/localized-versions?hl=ja)
