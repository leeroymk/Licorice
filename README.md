# Валютный мониторинг

Этот проект отслеживает курс валютных пар на нескольких биржах. При изменении курса на ≥0.03% отправляется уведомление на почту. Данные хранятся в базе данных и доступны через API с CRUD операциями.

### Установка

- Клонируйте репозиторий:

```
git clone https://github.com/leeroymk/Licorice
cd Licorice
```

- Установите зависимости:

```
pip install -r requirements.txt
```

### Настройка и запуск базы данных

Проект использует PostgreSQL, который разворачивается через Docker Compose.

-  Убедитесь, что Docker и Docker Compose установлены на вашем компьютере.
    Запустите команду для поднятия контейнера с PostgreSQL:

```
docker-compose up -d --build
```

- Настройка переменных окружения

Проект использует переменные окружения, которые берутся из файла .env. Пример файла уже предоставлен в репозитории — это файл .env.example.

Откройте файл .env и настройте переменные:
```
CMC_API_KEY=your_coinmarketcap_api_key

SMTP_HOST=your_smtp_host
SMTP_LOGIN=your_email
SMTP_PWD=your_password
SMTP_PORT=your_smtp_port
SMTP_RECIPIENT=recipient_email

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PWD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```

CMC_API_KEY — ключ API CoinMarketCap для получения курсов валют.
SMTP-переменные — настройки SMTP сервера для отправки уведомлений на почту.
DB-переменные — данные для подключения к базе данных PostgreSQL.

После настройки переменных окружения вы можете запускать проект и подключаться к базе данных и SMTP-серверу.
Теперь база данных готова для использования. После этого можно запускать приложение и выполнять CRUD-операции с валютными парами через API.


## Запуск проекта

- Запуск планировщика

Для запуска мониторинга курсов валют и отправки уведомлений выполните:

```
python -m app.main

```

Планировщик запустит проверку каждый час (интервал можно изменить в файле scheduler.py).

## Запуск API

API поддерживает операции по созданию, чтению, обновлению и удалению валютных пар.

- Запуск API:

```
python -m app.api.api
```

### API маршруты


    POST /currency_pairs/ — создание валютной пары.
    GET /currency_pairs/ — получение всех валютных пар.
    GET /currency_pairs/{pair_id} — получение валютной пары по ID.
    PUT /currency_pairs/{pair_id} — обновление валютной пары.
    DELETE /currency_pairs/{pair_id} — удаление валютной пары.

#### Примеры запросов к API

Ниже приведены примеры запросов для работы с валютными парами.

- Создание валютной пары

Метод: POST

URL: /currency_pairs/

Описание: Создаёт новую валютную пару.

Пример запроса:


```
curl -X POST http://localhost:8080/currency_pairs/ \
     -H "Content-Type: application/json" \
     -d '{
           "pair": "BTC/USDT",
           "exchange": "Binance",
           "price": 50000.00,
           "min_price": 49000.00,
           "max_price": 51000.00
         }'
```

- Получение всех валютных пар

Метод: GET

URL: /currency_pairs/

Описание: Возвращает список всех валютных пар.

Пример запроса:


```
curl -X GET http://localhost:8080/currency_pairs/
```

- Получение валютной пары по ID

Метод: GET

URL: /currency_pairs/{pair_id}

Описание: Возвращает информацию о конкретной валютной паре по ID.

Пример запроса:


```
curl -X GET http://localhost:8080/currency_pairs/1
```

- Обновление валютной пары

Метод: PUT

URL: /currency_pairs/{pair_id}

Описание: Обновляет данные о валютной паре.

Пример запроса:

```
curl -X PUT http://localhost:8080/currency_pairs/1 \
     -H "Content-Type: application/json" \
     -d '{
           "pair": "BTC/USDT",
           "exchange": "Binance",
           "price": 50500.00,
           "min_price": 49500.00,
           "max_price": 51500.00
         }'
```

- Удаление валютной пары

Метод: DELETE

URL: /currency_pairs/{pair_id}

Описание: Удаляет валютную пару по ID.

Пример запроса:

curl -X DELETE http://localhost:8080/currency_pairs/1
