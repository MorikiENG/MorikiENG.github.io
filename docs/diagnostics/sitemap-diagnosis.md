# サイトマップ取得エラー診断

## 結論

検査時点で、リポジトリと公開応答に、Google Search Consoleの「サイトマップを読み込めませんでした」を説明できる不具合は検出されませんでした。サイトファイルの修正は行いません。Google側の一時的な取得失敗、以前の取得結果が残っている可能性、送信先プロパティ・入力URLの不一致などは候補ですが、今回の観測だけでは原因を確定できません。

- 観測開始（UTC）: 2026-10-15T05:43:02.038123+00:00
- 対象main: `bc1b3b66234231c0a9b45d1d8fe80064e166f88d`
- 観測経路: このクラウド環境のHTTPSプロキシ経由。実際のGoogleクローラーからの通信ではありません。
- HTTP応答・各URLのメタ情報・ハッシュの証拠: [sitemap-http-evidence.json](sitemap-http-evidence.json)

## サイトマップ

| 項目 | 結果 |
|---|---|
| URL | `https://morikieng.github.io/sitemap.xml` |
| GET応答 | HTTP 200 |
| 最終URL・リダイレクト | URL変更なし・0回 |
| Content-Type | `application/xml` |
| 内容 | 1,101バイト。HTMLのエラーページではない |
| XML宣言 | `<?xml version="1.0" encoding="UTF-8"?>` |
| エンコーディング | UTF-8として厳密にデコード成功 |
| BOM | なし（なおUTF-8のBOM自体が必ずエラー原因になるわけではない） |
| XML構文 | Python標準XMLパーサーで解析成功 |
| 名前空間 | `http://www.sitemaps.org/schemas/sitemap/0.9` |
| 要素 | urlset / url / locの通常のサイトマップ。全16件がHTTPSの同一ホストの絶対URL |
| URL数 | 日本語8・英語8、重複なし |
| 公開ファイルとmain | バイト単位で一致 |
| Cache-Control | `max-age=600`。検査応答のAgeは0 |
| SHA-256 | `5e6f690d3dd6e928955dfe2fa47694b918b71e967c0bc8e4e6fca2a2ef37519a` |

通常のUser-AgentとGooglebotを模したUser-Agentの2回のGETで同じXMLを取得しました。ただし、Googlebotの名前を付ける試験はGoogleのIP・ネットワーク・実クローラーによる取得を検証するものではありません。XMLパーサーによる構文検証と構造確認を行いましたが、Search Consoleの内部検証を代行したものではありません。

サイトマップ内にhreflang拡張はありませんが、通常のURL一覧として有効です。HTMLに設定されたhreflangが別途正しいことを確認しました。改行が少ないことや、lastmodがないことは修正が必要な不備ではありません。

## 全16ページの検証

canonicalは各行のURLと一致。リダイレクトは0回。noindexはmeta（robots/googlebot/bingbot）およびX-Robots-Tagを調査しました。全ページが公開mainとバイト単位で一致しています。

| URL（ホスト省略） | HTTP | 転送 | canonical | noindex | hreflang |
|---|---|---|---|---|---|
| `` | 200 | なし | 一致 | なし | 一致 |
| `3d-print.html` | 200 | なし | 一致 | なし | 一致 |
| `cad.html` | 200 | なし | 一致 | なし | 一致 |
| `engineering.html` | 200 | なし | 一致 | なし | 一致 |
| `software.html` | 200 | なし | 一致 | なし | 一致 |
| `works.html` | 200 | なし | 一致 | なし | 一致 |
| `company.html` | 200 | なし | 一致 | なし | 一致 |
| `contact.html` | 200 | なし | 一致 | なし | 一致 |
| `en/3d-print.html` | 200 | なし | 一致 | なし | 一致 |
| `en/cad.html` | 200 | なし | 一致 | なし | 一致 |
| `en/company.html` | 200 | なし | 一致 | なし | 一致 |
| `en/contact.html` | 200 | なし | 一致 | なし | 一致 |
| `en/engineering.html` | 200 | なし | 一致 | なし | 一致 |
| `en/` | 200 | なし | 一致 | なし | 一致 |
| `en/software.html` | 200 | なし | 一致 | なし | 一致 |
| `en/works.html` | 200 | なし | 一致 | なし | 一致 |

※ 空パスは日本語トップ `/` です。hreflangの「一致」は、ja・enが対応ページを、x-defaultが対応する日本語ページを指すことを示します。日英間の相互参照と全対象URLの存在を確認しました。日本語lang=ja、英語lang=enです。

`/index.html`・`/en/index.html` は既存の別名URLですが、正規URLを `/`・`/en/` に指定し、サイトマップには正規URLだけを掲載しています。この既知の別名はサイトマップ取得失敗の証拠ではありません。今回、既存リンクやURLを変更していません。

## robots・公開設定・保護対象

robots.txtはHTTP 200、リダイレクトなし、公開mainと一致。内容は以下のとおりで、Googlebotの全16URLへのアクセスを許可しています。

```text
User-agent: *
Allow: /
Sitemap: https://morikieng.github.io/sitemap.xml
```

GitHub APIで確認したPages設定は、公開元 `main` の `/`、build_type=legacy、HTTPS強制あり、公開URL `https://morikieng.github.io/`。最新ビルドはmainの上記SHAに対してbuilt、エラーメッセージなしでした。

所有権確認用 `googled86428f90575e69a.html` と `app-ads.txt` もHTTP 200で、mainの内容と一致しています。削除・変更していません。既存のHTML・CSS・JS・画像・ページ構成も変更していません。

以前のSEO改善PR #3はOPENのままで、公開mainには未反映です。現在の公開サイトマップ自体は有効で、PR #3のマージを今回のエラー解消条件にはしません。

## 可能性と未検証範囲

1. **Google側の一時的な取得・処理エラー／過去の取得結果**：今回の正常応答とは両立する可能性があります。ただしGoogleの取得時刻と詳細エラーを確認できておらず、確定ではありません。
2. **送信先プロパティや送信URLの相違**：`https://morikieng.github.io/` のプロパティに正確なURLを送っているか、Search Console内の実際の値は未確認です。
3. **過去のデプロイ中・CDNや経路の一時的不調**：検査時は正常ですが、問題発生時の応答履歴やGoogleアクセスログは取得できません。現在のCache-Controlだけで原因を断定できません。
4. **Googleからの取得だけが失敗**：ローカルのHTTPS応答や模擬User-Agentでは否定できません。実Googlebotからの接続・TLS・DNS・CDN経路は未検証です。

Search Consoleへのログイン操作、エラー詳細、最終読み込み日時、実クローラーのログ、過去のHTTP応答は確認していません。両トップのURL検査成功は利用者提供情報であり、この診断からSearch Console内で再確認したものではありません。URL検査成功は、サイトマップ処理の成功を直接意味しません。

## Search Consoleで行うこと

1. URLプレフィックスプロパティが `https://morikieng.github.io/` であることを確認する。
2. 「サイトマップ」で失敗した送信行を開き、登録済みURL、詳細エラー、最終読み込み日時、表示される場合はHTTPエラーを記録する。
3. 正しい送信先は `https://morikieng.github.io/sitemap.xml`。入力欄にホストが補完される場合は `sitemap.xml` だけを入力し、ホストの二重入力や誤った `/en/sitemap.xml` がないことを確認する。
4. 同じ正しいURLを再送信できる場合は一度再送信する。不要なファイル名変更・クエリ追加・連続再送信は行わない。削除・再登録自体が必須の修復方法ではない。
5. 処理後に状態と最終読み込み日時を確認する。再取得までの時間は保証できない。失敗が継続する場合は詳細エラーと日時を共有し、その時点の公開HTTP応答と照合する。
6. 所有権確認ファイルはそのまま保持する。登録・順位を保証するものではなく、現段階でサイトの作り直しや本番の設定変更は不要。

公式参考: [サイトマップの管理](https://support.google.com/webmasters/answer/7451001?hl=ja)、[サイトマップの作成と送信](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=ja)。

## 今回の変更と再検証

追加はこのレポートとHTTP診断証拠JSONの2ファイルのみ。サイトマップを含む既存ファイルの修正はありません。全16URL、XML解析、HTTP応答、canonical・hreflang・robots・noindex、公開main一致のチェックは全件成功しました。「修正後」の検証対象となるサイト修正はありません。mainへのマージ・本番公開は行いません。
