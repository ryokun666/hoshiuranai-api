
# 星占い API

このプロジェクトは、Flask を使用して構築されたシンプルな占い API です。指定されたパラメータに基づいて、12 星座の占い結果を返します。

**注意**: このAPIは日付ベースの乱数を使用して占い結果を生成しているため、占い結果の信ぴょう性はありません。

## セットアップ

### 必要なソフトウェア

- Python 3.x
- pip (Python のパッケージ管理システム)

### 仮想環境の作成と依存関係のインストール

1. プロジェクトのルートディレクトリに移動します。

   ```bash
   cd project_root
   ```

2. 仮想環境を作成します。

   ```bash
   python3 -m venv venv
   ```

3. 仮想環境をアクティブにします。

   ```bash
   source venv/bin/activate
   ```

4. 必要な依存関係をインストールします。

   ```bash
   pip install Flask
   ```

## アプリケーションの実行

1. 仮想環境をアクティブにしていることを確認します。
2. アプリケーションを実行します。

   ```bash
   python run.py
   ```

3. ブラウザで以下の URL にアクセスして、API をテストします。

   ```
   http://127.0.0.1:5000/?userid=test&date=20240101&birth=0401&resulttype=json
   ```

## API の使用方法

### リクエスト形式

URI 形式:

```
http://[サーバードメイン]/?userid=[ユーザID]&date=[指定日]&birth=[生年月日]&resulttype=[結果形式]
```

#### パラメータ

- `userid`: ユーザ ID。今回は`test`を使用します。
- `date`: 指定日。形式は`yyyymmdd` (例: `20240101`)。
- `birth`: 生年月日。形式は`yyyymmdd`、`mmdd`、または`mdd` (例: `20200401`, `0401`, `401`)。
- `resulttype`: 結果形式。`xml`または`json`を指定。

### レスポンス形式

#### XML 形式

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<announce lastAnnounce="2024-01-02 13:34:47" astroDate="2024-01-01">
  <astro code="0" name="牡羊座" datefrom="03-21" dateto="04-19">
      <astrotext_s>...</astrotext_s>
      <astrotext_m>...</astrotext_m>
      <astrotext_l>...</astrotext_l>
  </astro>
  <!-- 他の星座のデータも続く -->
</announce>
```

#### JSON 形式

```json
{
  "announce": {
    "lastAnnounce": "2024-01-02 13:47:54",
    "fortuneDate": "2024-01-01",
    "astro": [
      {
        "code": "0",
        "name": "牡羊座",
        "datefrom": "03-21",
        "dateto": "04-19",
        "astrotext_s": "...",
        "astrotext_m": "...",
        "astrotext_l": "..."
      }
      // 他の星座のデータも続く
    ]
  }
}
```

### 複数リクエストのサポート

このAPIは、複数のリクエストパラメータを受け取ることができます。それぞれのリクエストパラメータに対して、占い結果が配列で返されます。

#### リクエスト形式

URI形式:

```
http://[サーバードメイン]/?userid=[ユーザID]&date=[指定日]&birth=[生年月日]&userid=[ユーザID]&date=[指定日]&birth=[生年月日]&resulttype=[結果形式]
```

#### 複数リクエスト例

```bash
curl "http://127.0.0.1:5000/?userid=test1&date=20240712&birth=19970606&userid=test2&date=20240713&birth=19880515&resulttype=json"
```

このリクエストは、2つのユーザーID（`test1`と`test2`）、2つの日付（`20240712`と`20240713`）、およびそれぞれの誕生日に対する占い結果を要求します。レスポンスは、配列形式のJSONで返されます。

### レスポンス形式

#### JSON 形式

```json
[
  {
    "userid": "test1",
    "announce": {
      "lastAnnounce": "2024-07-12 14:41:29",
      "fortuneDate": "20240712",
      "astro": {
        "code": "0",
        "name": "牡羊座",
        "datefrom": "03-21",
        "dateto": "04-19",
        "astrotext_s": "...",
        "astrotext_m": "...",
        "astrotext_l": "..."
      }
    }
  },
  {
    "userid": "test2",
    "announce": {
      "lastAnnounce": "2024-07-12 14:41:29",
      "fortuneDate": "20240713",
      "astro": {
        "code": "1",
        "name": "牡牛座",
        "datefrom": "04-20",
        "dateto": "05-20",
        "astrotext_s": "...",
        "astrotext_m": "...",
        "astrotext_l": "..."
      }
    }
  }
]
```

## テストの実行

1. 仮想環境をアクティブにしていることを確認します。
2. テストを実行します。

   ```bash
   python -m unittest discover tests
   ```

## ディレクトリ構成

```
project_root/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── utils.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── horoscopes.py
│   │   ├── zodiac_signs.py
│   └── templates/
│       └── index.html
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   ├── test_utils.py
├── venv/
├── .gitignore
├── README.md
└── run.py
```

各ファイルとディレクトリの説明:

- `app/`: アプリケーションのメインディレクトリ。

  - `__init__.py`: Flask アプリケーションの初期化。
  - `routes.py`: API のルート定義。
  - `utils.py`: 補助関数。
  - `data/`: データを格納。
    - `horoscopes.py`: 占い文章のデータ。
    - `zodiac_signs.py`: 星座のデータ。
  - `templates/`: HTML テンプレート。
    - `index.html`: ホームページのテンプレート。

- `tests/`: テストコード。

  - `__init__.py`: テストモジュールの初期化。
  - `test_routes.py`: ルートのテスト。
  - `test_utils.py`: 補助関数のテスト。

- `venv/`: Python 仮想環境。

- `.gitignore`: Git で無視するファイルやディレクトリ。

- `README.md`: プロジェクトの概要と説明。

- `run.py`: アプリケーションを実行するスクリプト。
