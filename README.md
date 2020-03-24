# 大阪府 新型コロナウイルス感染症対策サイト

![](https://github.com/codeforosaka/covid19/workflows/production%20deploy/badge.svg)

![大阪府 新型コロナウイルス感染症対策サイト](https://covid19-osaka.info/ogp.png)

## 貢献の仕方
Issues にあるいろいろな修正にご協力いただけると嬉しいです。

詳しくは[貢献の仕方](./.github/CONTRIBUTING.md)を御覧ください。

## 行動原則
詳しくは[サイト構築にあたっての行動原則](./.github/CODE_OF_CONDUCT.md)を御覧ください。

## ライセンス
本ソフトウェアは、[MITライセンス](./LICENSE.txt)の元提供されています。

## このサイトの大元

### 東京都 新型コロナウイルス感染症対策サイト
[サイトへのリンク](https://stopcovid19.metro.tokyo.lg.jp/)

[Githubへのリンク](https://github.com/tokyo-metropolitan-gov/covid19)

## 開発者向け情報

### data.jsonの説明
* JSON形式のデータです
* 今は手作業で修正しています（大阪府の方がプルリクを投げてくれることが多いです）

#### patients
* 感染者数
* date：最終更新日
* data -> リリース日：発表された日（最後の`T08:00:00.000Z`は固定）
* data -> 曜日：他の行と同じでOK
* data -> 居住地：市区町村まで
* data -> 年代：〜〜代まで
* data -> 性別：男性 or 女性
* data -> 退院：退院してたら「○」、死亡した場合は「死亡」、それ以外は「（空白）」
* data -> date：上のリリース日と同じでOK（フォーマットは違うけど）

#### patients_summary
* 日毎の感染者数
* date：最終更新日
* data -> 日付：発表された日（最後の`T08:00:00.000Z`は固定）
* data -> 小計：その日の感染者数（累計じゃないので注意）

#### inspections_summary
* 日毎の検査件数
* date：最終更新日
* data -> 日付：発表された日（最後の`T08:00:00.000Z`は固定）
* data -> 小計：その日の検査件数（累計じゃないので注意）

#### contacts1_summary
* 府民向け相談窓口への相談件数
* date：最終更新日
* data -> 日付：発表された日（最後の`T08:00:00.000Z`は固定）
* data -> 小計：その日の検査件数（累計じゃないので注意）

#### contacts2_summary
* 新型コロナ受診相談センターへの相談件数
* date：最終更新日
* data -> 府管轄保健所：日毎の府管轄保健所での相談件数（累計じゃないので注意）
* data -> 政令中核市保健所：日毎の政令中核市保健所での相談件数（累計じゃないので注意）
* labels：日付

#### treated_summary
* 陰性確認済（退院者累計）
* date：最終更新日
* data -> 退院した日（最後の`T08:00:00.000Z`は固定）
* data -> 小計：その日の退院件数（累計じゃないので注意）

#### main_summary
* 状況サマリー
* http://www.pref.osaka.lg.jp/iryo/osakakansensho/corona.html
* 上記ページの数字と合わせる（手作業）

### 環境構築の手順

- 必要となるNode.jsのバージョン: 10.19.0以上

**yarn を使う場合**
``` bash
# install dependencies
$ yarn install

# serve with hot reload at localhost:3000
$ yarn dev
```

**docker compose を使う場合**
```bash
# serve with hot reload at localhost:3000
$ docker-compose up --build
```

### `Cannot find module ****` と怒られた時

**yarn を使う場合**
```
$ yarn install
```

**docker compose を使う場合**
```bash
$ docker-compose run --rm app yarn install
```

### ステージング・本番環境への反映

`master` ブランチがアップデートされると、自動的に `production` ブランチにHTML類がbuildされます。そして、本番サイト https://covid19-osaka.info/ が更新されます。

`staging` ブランチは大阪では運用しません。developからmasterにプルリクを投げてください

`development` ブランチがアップデートされると、自動的に `dev-pages` ブランチにHTML類がbuildされます。そして、開発用サイト https://dev-covid19-osaka.netlify.com/ が更新されます。
