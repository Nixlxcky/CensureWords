# CensureWords
## 🇷🇺 Русский

Telegram бот на базе aiogram, который автоматически фильтрует нецензурную лексику в чатах Telegram. Идеально подходит для админов чатов и каналов.

### 🔹 Возможности

* ✍️ У каждого пользователя своя личная база слов, которую можно редактировать.
* 🔄 Работает по ежемесячной подписке, оплата которой также произовдится через бота.
* ✅ Интерфейс админа чата, покупателя и обычного пользователя удобно разделен.
* ⚙️ Поддержка работы на двух языках: EN и RUS.

P.S _Пример работы смотрите [ТУТ](https://github.com/Nixlxcky/CensureWords/blob/master/videos/BotPrieviewrus.mp4)_

### 🧰 Технологии

`Python3.10`, `Aiogram2.21`, `PostgreSQL`, `asyncpg`, `stripe` 

### 🚀 Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Nixlxcky/CensureWords.git
cd CensureWords
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` со следующими переменными:

```
TOKEN=<ключ бота>
PAYMENT_TOKEN=<ключ stripe> # Платёжный токен Stripe, полученный через BotFather. В новых ботах больше не получить. Устаревший подход.
DATABASE_LINK =<ссылка PosgreSQL>
```

4. Запустите бот:

```bash
python main.py
```


## 🇬🇧 English

Telegram bot based on aiogram, which automatically filters swear words in Telegram chats. Ideal for chat and channel admins.

### 🔹 Features

* ✍️ Each user has their own personal word base, which can be edited.
* 🔄 Works on a monthly subscription, which is also paid for through the bot.
* ✅ The interface of the chat admin, buyer and regular user is conveniently separated.
* ⚙️ Support for working in two languages: EN and RUS.

P.S _See an example of the work [HERE](https://github.com/Nixlxcky/CensureWords/blob/master/videos/BotPrieviewen.mp4)_

### 🧰 Technologies

`Python3.10`, `Aiogram2.21`, `PostgreSQL`, `asyncpg`, `stripe` 

1. Clone the repository:

```bash
git clone https://github.com/Nixlxcky/CensureWords.git
cd CensureWords
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:

```
TOKEN=<bot key>
PAYMENT_TOKEN=<stripe key> # Stripe payment token received via BotFather. Cannot be obtained in new bots anymore. Deprecated approach.
DATABASE_LINK =<PosgreSQL link>
```

4. Run the bot:

```bash
python main.py
```


