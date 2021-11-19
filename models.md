## Customers

| 項目名           | 和名           | タイプ      |  備考                             | 
| --------------- | --------------- | -------    |  -------------------------------- | 
| id              | id              | integer    |                                   | 
| customerName    | 得意先名         | text       |                                   | 
| honorificTitle  | 敬称            | text       |                                   | 
| postNumber      | 郵便番号        | string(20) |  ハイフンが入ると思ったのでstring | 
| address         | 住所            | text       |                                   | 
| telNumber       | 電話番号         | string(30) |  ハイフンが入ると思ったのでstring | 
| faxNumber       | FAX番号         | string(30) |  ハイフンが入ると思ったのでstring | 
| url             | ホームページURL  | text       |                                   | 
| email           | メールアドレス   | text       |                                   | 
| manager         | 担当者          | text       |                                   |
| representative  | 代表者名        | text       |                                   | 
| memo            | メモ            | text       |                                   |
| createdAt       | 作成日時        | datetime   |  作成日時                          |
| updatedAt       | 更新日時        | datetime   |  更新日時                          | 

<br>

## Items

| 項目名    | 和名     | タイプ     |  備考                                                                                       | 
| -------- | -------- | --------  |  ------------------------------------------------------------------------------------------ | 
| id       | id       | integer   |                                                                                             | 
| itemName | 商品名   | text      |                                                                                             | 
| unit     | 単位     | text      |  単位はユーザーが追加できるように単位テーブルを作成し、単位追加ページを作成した方が良いかも         | 
| price    | 単価     | integer   |                                                                                             | 
| cost     | 原価     | integer   |                                                                                             | 
| costRate | 原価率   | float     |                                                                                             | 
| memo     | メモ     | text      |                                                                                             | 
| createdAt| 作成日時 | datetime  |                                                                                             | 
| updatedAt| 更新日時 | datetime  |                                                                                             |

<br>

## Invoices

| 項目名       | 和名           | タイプ    |  備考                                                     | 
| ----------- | -------------- | -------- |  -------------------------------------------------------- | 
| id          | id             | integer  |                                                           | 
| customerId  | 得意先ID       | integer  |  フォーリンキー。                                         | 
| applyNumber | 請求番号       | integer  |  作成時にインクリメント。他の請求書と被らないようにする。 | 
| applyDate   | 日付           | datetime |  請求書作成日                                             | 
| expiry      | 請求書有効期限  | datetime |                                                           | 
| title       | 件名           | text     |                                                           | 
| memo        | メモ           | text     |  アプリ利用者に見えるもの                                 | 
| remarks     | 備考           | text     |  印刷時に表示されるもの                                   |
| isTaxExp    | 内税・外税     | boolean   |  内税・外税のチェック                                      | 
| createdAt   | 作成日時       | datetime  |                                                           | 
| updatedAt   | 更新日時       | datetime  |                                                           | 

<br>

## Invoice_Items

| 項目名      | 和名     | タイプ    |  備考                   | 
| ---------- | -------- | -------- |  ---------------------- | 
| id         | id       | integer  |                         | 
| invoiceId  | 請求書ID | integer  |  請求書テーブルと紐づく | 
| itemId     | 商品ID   | integer  |  商品テーブルと紐づく   | 
| count      | 個数     | integer  |                         | 
| createdAt  | 作成日時 | datetime |                         | 
| updatedAt  | 更新日時 | datetime |                         | 

<br>

## Quotaions

| 項目名       | 和名           | タイプ    |  備考                                                     | 
| ----------- | -------------- | -------- | -------------------------------------------------------- | 
| id          | id             | integer  |                                                          | 
| customerId  | 得意先ID       | integer  | フォーリンキー。                                         | 
| applyNumber | 見積番号       | integer  | 作成時にインクリメント。他の見積書と被らないようにする。 | 
| applyDate   | 日付           | datetime | 見積書作成日                                             | 
| expiry      | 見積書有効期限  | datetime |                                                          | 
| title       | 件名           | text     |                                                          | 
| memo        | メモ           | text     | アプリ利用者に見えるもの                                 | 
| remarks     | 備考           | text     | 印刷時に表示されるもの                                   | 
| isTaxExp    | 内税・外税      | boolean  | 内税・外税のチェック                                     | 
| createdAt   | 作成日時       | datetime |                                                          | 
| updatedAt   | 更新日時       | datetime |                                                          | 

<br>

## Quotaion_Items

| 項目名       | 和名     | タイプ    |  備考                   | 
| ----------  | -------- | -------- |  ---------------------- | 
| id          | id       | integer  |                         | 
| quotaionId  | 見積書ID | integer  |  見積書テーブルと紐づく | 
| itemId      | 商品ID   | integer  |  商品テーブルと紐づく   | 
| count       | 個数     | integer  |                         | 
| createdAt   | 作成日時 | datetime |                         | 
| updatedAt   | 更新日時 | datetime |                         | 

<br>

## Memos

| 項目名    | 和名     | タイプ   | 備考 | 
| --------- | -------- | -------- | ---- | 
| id        | id       | integer  |      | 
| title     | 件名     | text     |      | 
| content   | 内容     | text     |      | 
| createdAt | 作成日時 | datetime |      | 
| updatedAt | 更新日時 | datetime |      | 

<br>

## Units

| 項目名    | 和名     | タイプ    |  備考 | 
| -------- | -------- | -------- |  ---- | 
| id       | id       | integer  |       | 
| unitName | 単位名   | text     |       | 
| createdAt| 作成日時 | datetime |       | 
| updatedAt| 更新日時 | datetime |       | 

<br>

## Setting

| 項目名                   | 和名             | タイプ       | 備考                     | 
| ----------------------- | ---------------- | --------    | ------------------------ | 
| companyName             | 会社名           | text        |                          | 
| representative          | 代表者名         | text        |                          | 
| postNumber              | 郵便番号         | string(20)  |                          | 
| address                 | 住所             | text        |                          | 
| telNumber               | 電話番号         | string(30)  |                          | 
| faxNumber               | FAX番号          | string(30)  |                          | 
| url                     | ホームページURL  | text        |                          | 
| email                   | メールアドレス   | text        |                          | 
| logoFilePath            | ロゴファイルパス | text        |                          | 
| stampFilePath           | 印鑑ファイルパス | text        |                          | 
| isDisplayQuotationLogo  | ロゴ見積書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayInvoiceLogo    | ロゴ請求書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayDeliveryLogo   | ロゴ納品書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayQuotationStamp | 印鑑見積書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayInvoiceStamp   | 印鑑請求書表示   | boolean     | 印刷時に表示するかどうか | 
| isDisplayDeliveryStamp  | 印鑑納品書表示   | boolean     | 印刷時に表示するかどうか | 
| updatedAt               | 更新日時         | datetime    |                          | 