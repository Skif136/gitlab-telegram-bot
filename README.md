## Требования
[Создайте нового бота ](https://core.telegram.org/bots#create-a-new-bot)

## Переменные
- AUTHMSG - парольная фраза используется при авторизации в боте, для получения уведомлений
- TOKEN - токен бота

## Запуск
- Измененить значение переменных в файле "vars.py" 
p.s. значение {0}- {3} получаемые от json :
{0} - namespace (автор тэга)
{1} - ref (название тэга)
{2} - name (название проекта)
{3} - default_branch (ветка)
```yaml
token = 'XXX:XXX'
secret_message = 'XXX' # Парольная фраза
one_post = 'Hi !'
correct_key = 'Everything is fine !'
invalid_key = "I won't talk to you."
stop_bot = 'Ok, bye.'
message = "*{0} pushed new tag: '{1}' at project: '{2}' default_branch: '{3}' \n{4}/tree/{1}*"
```
- docker build -t bot .  
- docker run -d -p 10111:10111 --name bot bot
- Создайте Webhook в проекте gitlab, который указывает на http://ip:10111/
- Напишите боту в чате парольную фразу