# StickyCamプライバシーポリシー：暫定版・リリース前レビュー

作成日: 2026-11-27。対象はWebページのみ。アプリ本体のソースは変更しない。

## 作業範囲と公開ゲート

- ローカルブランチ: `feat/stickycam-privacy`
- ローカルコミットまでが承認済み。GitHubへのPush・GitHub Pages公開は別途ユーザー承認が必要。
- 既存チェックアウトを使用。追加のリポジトリ複製・worktree・バックアップフォルダは作らない。
- アプリ側の変更やアプリ内リンク組み込みはこの作業に含めない。
- 適法性・規約への完全準拠、Apple/Googleの審査通過を断定しない。

## ページと管理方法

既存のQuick2Dは `quick2d-viewer/privacy.html` と `en/quick2d-viewer/privacy.html` を管理している。同じ静的HTMLの配置を優先する。Quick3Dと画像圧縮くんは別の `moriki-apps` 配下に個別ポリシーがあり、既存URLを移動・変更しない。

| 役割 | 公開予定URL | ファイル |
| --- | --- | --- |
| 共通・ブラウザー言語選択 | https://morikieng.github.io/stickycam/privacy/ | `stickycam/privacy/index.html` |
| 日本語 | https://morikieng.github.io/stickycam/privacy.html | `stickycam/privacy.html` |
| English | https://morikieng.github.io/en/stickycam/privacy.html | `en/stickycam/privacy.html` |

共通入口だけが `navigator.languages` の最初の対応言語（ja/en）を選び、どちらもなければ日本語へ移動する。言語別ページには自動転送を設けないので手動選択は保持される。Cookie・localStorageは使わない。JavaScript無効時は共通入口の実リンクから本文を開け、各本文は完全な静的HTMLとして閲覧できる。

専用のCSSを用い、白・黒・グレーとパステルイエロー `#FFF2B3` を使用。外部フォント・外部ライブラリなし。`prefers-color-scheme` によるライト/ダーク対応。既存サイトのCSS・JSやフッターを変更しない。sitemap.xmlでは既存URLを保持して3URLを追加する。

日英は同じ12節・同じ段落構成・同じ外部参照先でレビューした。今後も片方だけ更新せず、対応節を同時に修正する。12節: 運営者/暫定版、権限、写真とメモ、履歴、キャプション、広告、同意、保持削除、第三者/Webページ、権利/子ども、問い合わせ、変更日。

## 確認したソースと根拠

確認対象: `MorikiENG/StickyCam`、`main`、コミット `a8ee9708cc99f94396f852e75564bbd1783f3105`。接続済みGitHubから読み取り専用で参照した。Macの未コミット変更や実際のリリースバイナリは確認していない。アプリのチェックアウトを新たに複製せず、本体ファイルは編集していない。

| 説明 | 根拠 |
| --- | --- |
| 撮影用カメラ権限 | `StickyCam/Camera/Camera.swift`: `AVCaptureDevice.requestAccess(for: .video)` |
| 追加専用の写真保存 | `StickyCam/Imaging/PhotoPipeline.swift`: `PHPhotoLibrary.requestAuthorization(for: .addOnly)`、`PHAssetCreationRequest` |
| 端末内メモ合成 | 同ファイルの `render` / `NoteLayout`。ネットワーク送信処理なし |
| 履歴最大50件・個別/一括削除 | `StickyCam/App/MemoSettings.swift`: `record` の `prefix(50)`、`remove`、`clear`、`MemoHistoryView` |
| 履歴と設定の保存 | 履歴JSONとUserDefaults。履歴フォルダはバックアップ対象外。保存失敗フラグ・再試行UIあり |
| キャプションは開発版に存在 | `PhotoPipeline.save` / `requestedCaption`、設定の `autoCaption` とOS条件付きToggle。既定値trueだが正式採用前なのでリリース仕様を断定しない |
| 保存成功時の履歴登録 | `StickyCam/App/StickyCamApp.swift`: `PhotoPipeline.save` 後の `settings.record` |
| 既存検証状況 | `Docs/Phase1-Device-Validation.md`: Phase 1～3。実機のキャプションON/OFF確認はあるが、検索・共有後保持など未確認事項あり |
| Privacy Manifest | `StickyCam/Resources/PrivacyInfo.xcprivacy`: UserDefaultsのRequired Reason APIの宣言。広告SDKを統合した完成版の申告ではない |
| 広告/ATT/UMP | 現在の参照ツリーではSDK依存・実装なし。Phase 4の予定と区別 |
| 価格・登録・独自サーバー | ユーザー仕様: 無料、登録不要、独自サーバーなし |
| 開発者・問い合わせ | 既存公式サイト `contact.html`: 森樹エンジニアリング、`moriki.engineering@gmail.com`。法人格を加えない |

キャプションの具体的なOS条件は現時点の開発コードに存在するが、正式版で再確認するため公開本文では未確定の対応OSを固定していない。Debug専用のIPTC/キーワード試験を一般向け確定機能としない。

## Phase 4：広告実装時の必須確認

- [ ] 実際に導入するGoogle Mobile Ads SDK、UMP、メディエーション/追加SDKの名前とバージョンを記録。
- [ ] SDKの通信、取得データ、用途、第三者受領者、パーソナライズ/非パーソナライズの実際の設定を確認。
- [ ] 写真・メモ・キャプション・履歴を広告リクエストや解析へ渡していないことを確認。
- [ ] ATTの要否・プロンプト・拒否時挙動を実装とAppleの最新要件で判定。別の同意でATT拒否を迂回しない。
- [ ] UMPの要否、起動時更新、広告要求条件、必要な地域・状態での同意変更入口を確認。
- [ ] トラッキング拒否でも撮影・合成・保存等の基本機能が使えることを確認。
- [ ] 年齢区分・子ども向け設定を決定し、実装/配信設定に合わせる。
- [ ] 保持・削除の説明をGoogleの最新資料と最終SDKに合わせる。未実装の広告設定UIを利用可能と書かない。
- [ ] 日英の広告・同意・第三者サービス各節を同時に更新する。

## Phase 5：リリース前の必須確認

- [ ] 実際のReleaseビルドとこのポリシーを再照合する。Mac等にしかない最新差分を含める。
- [ ] App Store ConnectのApp Privacy申告をSDKを含む実際のデータ処理と一致させる。
- [ ] アプリと全SDKのPrivacy Manifest、Required Reason API、トラッキングドメイン等をXcodeのレポートと照合。
- [ ] キャプションの正式採用、対応OS、既定値、自動登録OFF、再試行条件、エラー表示を確定。
- [ ] 標準写真アプリでのキャプション、共有先へのメモ/メタデータ、履歴削除後の写真残存を実機確認。
- [ ] カメラ・写真追加の権限拒否/再許可、履歴50件、個別/一括削除、保存エラー、アプリ削除、OSバックアップの説明を再確認。
- [ ] GoogleとAppleの最新要件を再読し、ポリシーと実装・申告の差分を解消。
- [ ] 制定日・最終更新日、暫定版ラベルを正式版へ更新する。確認前に「準拠済み」「審査承認済み」と表明しない。
- [ ] Push/公開のユーザー承認を取得し、GitHub Pages公開後に3URLのHTTPS・ログイン不要・日英切替・JS無効を確認。
- [ ] App Store Connect/AdMobへ登録するURLは、公開が完了したものを用いる。現時点では公開予定URLにすぎない。

## 公式資料（2026-11-27確認）

Google:
- https://policies.google.com/privacy
- https://policies.google.com/technologies/partner-sites
- https://developers.google.com/admob/ios/privacy/data-disclosure （参照時は13.12.0の一般的なSDK説明。StickyCamへ導入済みという意味ではない）
- https://developers.google.com/admob/ios/privacy
- https://support.google.com/admob/answer/7676680

Apple:
- https://developer.apple.com/documentation/avfoundation/requesting-authorization-to-capture-and-save-media （公式Markdownでも内容確認）
- https://developer.apple.com/app-store/user-privacy-and-data-use/
- https://developer.apple.com/app-store/app-privacy-details/
- https://developer.apple.com/documentation/bundleresources/privacy-manifest-files （公式Markdownでも内容確認）

Web配信:
- https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement

PhotoKitのadd-only個別ページはWeb取得ツールでは到達できなかった。追加専用の実装は上記ソースとAppleの撮影・保存認可資料を根拠にした。上記の本文掲載リンク3件とその他の主要資料はHTTP 200を確認した。

## 検証とスクリーンショット

- HTMLのタグ対応・一意なID・言語属性・canonical/hreflang・実リンク/アンカーを確認。
- 日英12節の順序、段落数、外部参照先、履歴上限50件が一致することを確認。
- 新規5リソース（HTML3/CSS/JS）のローカルHTTP 200を確認。既存のサイトマップURL24件をすべて保持し、新規3URLだけを追加。
- Chromiumで320/390/834/1440px、日英、ライト/ダーク、JavaScript有効/無効の32通りを検証。
- JS有効16通りで横はみ出しなし、本文の計算上の色コントラスト4.5:1以上を確認。32通りで本文・言語リンクが閲覧可能。
- 手動切替リンクの解決先を確認。共通入口の実スクリプトを日本語、英語、未対応言語、混在言語、空の候補でテストし、意図するページを選ぶことを確認。
- JavaScript無効の共通入口には言語リンクとnoscript案内がある。本文ページはJavaScriptに依存しない。
- 本文ページのレンダリング中に外部リソース要求なし。スクリプトにはCookie/localStorage書き込み処理なし。
- 環境の制限で、ChromiumがローカルHTTP URLへ直接遷移するとERR_ABORTEDになる。そのためHTTP応答を別に確認し、同じHTML/CSSを直接読み込んで表示を検証した。実URLでのブラウザー往復遷移は、Push/公開承認後に再確認する。遷移先のテストをブラウザーでの往復操作成功とは扱わない。
- アプリの実機テストやiOSビルドはこのWeb作業では実施していない。

実ページの全長スクリーンショット（PNG）:

| 言語 | PCライト | PCダーク | スマートフォンライト | スマートフォンダーク |
| --- | --- | --- | --- | --- |
| 日本語 | [画像](stickycam-privacy/screenshots/ja-desktop-light.png) | [画像](stickycam-privacy/screenshots/ja-desktop-dark.png) | [画像](stickycam-privacy/screenshots/ja-mobile-light.png) | [画像](stickycam-privacy/screenshots/ja-mobile-dark.png) |
| English | [Image](stickycam-privacy/screenshots/en-desktop-light.png) | [Image](stickycam-privacy/screenshots/en-desktop-dark.png) | [Image](stickycam-privacy/screenshots/en-mobile-light.png) | [Image](stickycam-privacy/screenshots/en-mobile-dark.png) |

PCは1440×1000、スマートフォンは390×844のviewportから全長を撮影した。アプリ画面の仮画像ではなく、今回のポリシーページそのものの実キャプチャ。

## ローカルレビュー手順

GitHub Pagesへ公開せず、リポジトリで空きポートを確認して `python3 -m http.server 3000 --bind 127.0.0.1` を起動する。通常のローカルブラウザーで `/stickycam/privacy/`、`/stickycam/privacy.html`、`/en/stickycam/privacy.html` を開く。上記の管理ブラウザー制限がある環境では別途表示手段が必要。検証後は自分で開始したサーバーだけを停止する。

Push/公開はユーザー承認まで実行しない。既存ページへの新しいフッターリンクやアプリ紹介カードは追加していない。
