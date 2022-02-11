This script has dependenciec: `BeautifulSoup4`, `discord.py`, and `requests`.

This script requires you to make another file `secrets.py`:

```py
# secrets.py

USERNAME = "123456"
PASSWORD = "Password"
DISCORD_TOKEN = "xxxxxx..."
```
Create `constants.py`:
```py
# constants.py

LOGIN_URL = "your.moodle.url/login_page"
```


This [How to Make a Discord Bot](https://realpython.com/how-to-make-a-discord-bot-python/#creating-a-discord-connection) has everything you need to know on discord bots in python.  


Example output:
```sh
upel-webscrap> python discord_main.py

Connected with:  ['Teleinfa', 'TestServer']
kkw#1124: -followed
running command:  -followed
kkw#1124: -follow 7838
running command:  -follow 7838
Users being followed:  ['John Krasinski : 5 hours 49 mins']
kkw#1124: -follow 9014
running command:  -follow 9014
Users being followed:  ['Lisa Armstrong : 5 hours 49 mins', 'Jerry Montenegro : 1 day 6 hours']
```

When bot is running you can get the below help by `-help` command:  

You can follow UPEL users to be notified on this chat/channel when they become online / offline.
Do this by entering a command: `-follow wxyz` where `wxyz` is the `...profile.php?id=wxyz` in url in the UPEL profile page.
To unfollow execute command: `-unfollow wxyz`
To find out about followed users and ther last time online: `-followed`.

You also can get your grades from UPEL, your username and password will not be saved, only kept in RAM, you can allways delete them by executing: `-logout`.
But first to log in execute command: `-login <UPEL_LOGIN> <UPEL_PASSWORD>`
_WARNING!!! LOG IN BY SENDING A PRIVATE MESSAGE TO THE BOT!!! DO NOT EXPOSE YOUR CREDENTIALS!_

If you see a message indicating success then you can proceed with the next step:
`-getgrades <anal/alg/wdsi/pt/ask>` example: `-getgrades pt`.
or `-getgrades wxyz` example: `-getgrades 1477` beacuse 1477 is the course id of Podstawy Telekomunikacji.
The id can be found in the URL the same way as id of UPEL profile id.
