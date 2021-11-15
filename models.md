## Customer

| 和名            | 項目名          | タイプ  | 長さ       | 備考                             | 
| --------------- | --------------- | ------- | ---------- | -------------------------------- | 
| id              | id              | integer | INTEGER    |                                  | 
| customer_name   | 顧客名          | text    | TEXT       |                                  | 
| honorific_title | 敬称            | text    | TEXT       |                                  | 
| post_number     | 郵便番号        | string  | STRING(20) | ハイフンが入ると思ったのでstring | 
| address         | 住所            | text    | TEXT       |                                  | 
| tel_number      | 電話番号        | string  | STRING(30) | ハイフンが入ると思ったのでstring | 
| fax_number      | FAX番号         | string  | STRING(30) | ハイフンが入ると思ったのでstring | 
| url             | ホームページURL | text    | TEXT       |                                  | 
| email           | メールアドレス  | text    | TEXT       |                                  | 
| representative  | 代表者名        | text    | TEXT       |                                  | 
| memo            | メモ            | text    | TEXT       |                                  |
| create          | 作成日時        | date    | DATE       | 作成日時                          |
| update          | 更新日時        | date    | DATE       | 更新日時                          | 