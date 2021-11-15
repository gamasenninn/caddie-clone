## Customers

| 項目名           | 和名           | タイプ  | 長さ       | 備考                             | 
| --------------- | --------------- | ------- | ---------- | -------------------------------- | 
| id              | id              | integer | INTEGER    |                                  | 
| customerName    | 顧客名          | text    | TEXT       |                                  | 
| honorificTitle  | 敬称            | text    | TEXT       |                                  | 
| postNumber      | 郵便番号        | string  | STRING(20) | ハイフンが入ると思ったのでstring | 
| address         | 住所            | text    | TEXT       |                                  | 
| telNumber       | 電話番号        | string  | STRING(30) | ハイフンが入ると思ったのでstring | 
| faxNumber       | FAX番号         | string  | STRING(30) | ハイフンが入ると思ったのでstring | 
| url             | ホームページURL | text    | TEXT       |                                  | 
| email           | メールアドレス  | text    | TEXT       |                                  | 
| manager         | 担当者          | text    | TEXT       |                                  |
| representative  | 代表者名        | text    | TEXT       |                                  | 
| memo            | メモ            | text    | TEXT       |                                  |
| createAt        | 作成日時        | datetime| DATETIME   | 作成日時                          |
| updateAt        | 更新日時        | datetime| DATETIME   | 更新日時                          | 

<br>

## Items

| 項目名   | 和名     | タイプ   | 長さ     | 備考                                                                                       | 
| -------- | -------- | -------- | -------- | ------------------------------------------------------------------------------------------ | 
| id       | id       | integer  | INTEGER  |                                                                                            | 
| itemName | 商品名   | text     | TEXT     |                                                                                            | 
| unit     | 単位     | text     | TEXT     | 単位はユーザーが追加できるように単位テーブルを作成し、単位追加ページを作成した方が良いかも         | 
| price    | 単価     | integer  | INTEGER  |                                                                                            | 
| cost     | 原価     | integer  | INTEGER  |                                                                                            | 
| costRate | 原価率   | float    | FLOAT    |                                                                                            | 
| memo     | メモ     | text     | TEXT     |                                                                                            | 
| createAt | 作成日時 | datetime | DATETIME |                                                                                            | 
| updateAt | 更新日時 | datetime | DATETIME |                                                                                            |

<br>

## Invoices

| 項目名      | 和名           | タイプ   | 長さ     | 備考                                                     | 
| ----------- | -------------- | -------- | -------- | -------------------------------------------------------- | 
| id          | id             | integer  | INTEGER  |                                                          | 
| customerId  | 得意先ID       | integer  | INTEGER  | フォーリンキー。                                         | 
| applyNumber | 請求番号       | integer  | INTEGER  | 作成時にインクリメント。他の請求書と被らないようにする。 | 
| applyDate   | 日付           | datetime | DATETIME | 請求書作成日                                             | 
| expiry      | 請求書有効期限 | datetime | DATETIME |                                                          | 
| title       | 件名           | text     | TEXT     |                                                          | 
| memo        | メモ           | text     | TEXT     | アプリ利用者に見えるもの                                 | 
| remarks     | 備考           | text     | TEXT     | 印刷時に表示されるもの                                   |
| isTaxExp    | 内税・外税     | boolean  | BOOLEAN  | 内税・外税のチェック                                      | 
| createAt    | 作成日時       | datetime | DATETIME |                                                          | 
| updateAt    | 更新日時       | datetime | DATETIME |                                                          | 

<br>

## Invoice_Items

| 項目名     | 和名     | タイプ   | 長さ     | 備考                   | 
| ---------- | -------- | -------- | -------- | ---------------------- | 
| id         | id       | integer  | INTEGER  |                        | 
| invoicesId | 請求書ID | integer  | INTEGER  | 請求書テーブルと紐づく | 
| itemsId    | 商品ID   | integer  | INTEGER  | 商品テーブルと紐づく   | 
| count      | 個数     | integer  | INTEGER  |                        | 
| createAt   | 作成日時 | datetime | DATETIME |                        | 
| updateAt   | 更新日時 | datetime | DATETIME |                        | 

<br>

## Quotaions

| 項目名      | 和名           | タイプ   | 長さ     | 備考                                                     | 
| ----------- | -------------- | -------- | -------- | -------------------------------------------------------- | 
| id          | id             | integer  | INTEGER  |                                                          | 
| customerId  | 得意先ID       | integer  | INTEGER  | フォーリンキー。                                         | 
| applyNumber | 見積番号       | integer  | INTEGER  | 作成時にインクリメント。他の見積書と被らないようにする。 | 
| applyDate   | 日付           | datetime | DATETIME | 見積書作成日                                             | 
| expiry      | 見積書有効期限 | datetime | DATETIME |                                                          | 
| title       | 件名           | text     | TEXT     |                                                          | 
| memo        | メモ           | text     | TEXT     | アプリ利用者に見えるもの                                 | 
| remarks     | 備考           | text     | TEXT     | 印刷時に表示されるもの                                   | 
| isTaxExp    | 内税・外税     | boolean  | BOOLEAN  | 内税・外税のチェック                                     | 
| createAt    | 作成日時       | datetime | DATETIME |                                                          | 
| updateAt    | 更新日時       | datetime | DATETIME |                                                          | 

<br>

## Quotaion_Items

| 項目名      | 和名     | タイプ   | 長さ     | 備考                   | 
| ----------  | -------- | -------- | -------- | ---------------------- | 
| id          | id       | integer  | INTEGER  |                        | 
| quotaionsId | 見積書ID | integer  | INTEGER  | 見積書テーブルと紐づく | 
| itemsId     | 商品ID   | integer  | INTEGER  | 商品テーブルと紐づく   | 
| count       | 個数     | integer  | INTEGER  |                        | 
| createAt    | 作成日時 | datetime | DATETIME |                        | 
| updateAt    | 更新日時 | datetime | DATETIME |                        | 

<br>

## Units

| 項目名   | 和名     | タイプ   | 長さ     | 備考 | 
| -------- | -------- | -------- | -------- | ---- | 
| id       | id       | integer  | integer  |      | 
| unitName | 単位名   | text     | TEXT     |      | 
| createAt | 作成日時 | datetime | DATETIME |      | 
| updateAt | 更新日時 | datetime | DATETIME |      | 

<br>

## Setting

| 項目名                  | 和名             | タイプ   | 長さ       | 備考                     | 
| ----------------------- | ---------------- | -------- | ---------- | ------------------------ | 
| companyName             | 会社名           | text     | TEXT       |                          | 
| representative          | 代表者名         | text     | TEXT       |                          | 
| postNumber              | 郵便番号         | string   | STRING(20) |                          | 
| address                 | 住所             | text     | TEXT       |                          | 
| telNumber               | 電話番号         | string   | STRING(30) |                          | 
| faxNumber               | FAX番号          | string   | STRING(30) |                          | 
| url                     | ホームページURL  | text     | TEXT       |                          | 
| email                   | メールアドレス   | text     | TEXT       |                          | 
| logoFilePath            | ロゴファイルパス | text     | TEXT       |                          | 
| stampFilePath           | 印鑑ファイルパス | text     | TEXT       |                          | 
| isDisplayQuotationLogo  | ロゴ見積書表示   | boolean  | BOOLEAN    | 印刷時に表示するかどうか | 
| isDisplayInvoiceLogo    | ロゴ請求書表示   | boolean  | BOOLEAN    | 印刷時に表示するかどうか | 
| isDisplayDeliveryLogo   | ロゴ納品書表示   | boolean  | BOOLEAN    | 印刷時に表示するかどうか | 
| isDisplayQuotationStamp | 印鑑見積書表示   | boolean  | BOOLEAN    | 印刷時に表示するかどうか | 
| isDisplayInvoiceStamp   | 印鑑請求書表示   | boolean  | BOOLEAN    | 印刷時に表示するかどうか | 
| isDisplayDeliveryStamp  | 印鑑納品書表示   | boolean  | BOOLEAN    | 印刷時に表示するかどうか | 
| updateAt                | 更新日時         | datetime | DATETIME   |                          | 
