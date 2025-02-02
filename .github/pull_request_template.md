Please make sure you change the original .yaml fields in the accounts/, Collections/ or jettons/ directories and leave the auto-generated .json files in the repository root alone. Also please make sure that you do not use ton.api links in your pull request.
Example pull request:

```yaml
name: the name of your token
description: description of your token
image: "link to your token logo" !!! (don't use ton.api)!!!
address: Address of your token 
symbol: Symbol of your token
websites:
  - "link"
social:
  - "link"
```



Пожалуйста, убедитесь, что вы изменили исходные поля .yaml в каталогах account/, Collections/ или jettons/ и не трогаете автоматически сгенерированные файлы .json в корне репозитория. Так же, пожалуйста, убедитесь, что вы не используете ссылки ton.api в вашем пул реквесте.
Пример пул реквеста:

```yaml
name: имя вашего токена
description: описание вашего токена
image: "ссылка на лого вашего токена" !!! (не используйте ton.api)!!!
address: Адрес вашего токена 
symbol: Сивол вашего токена
websites:
  - "ссылка"
social:
  - "ссылка"
  ```
