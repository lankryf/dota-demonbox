# DOTA2 DemonBox
## Preparing
So to use dota-demonbox just clone it to your linunx machine using
```
git clone https://github.com/lankryf/dota-demonbox.git && cd dota-demonbox
```

Then you need to make config in folder "configs" using
```
cp configs/config.ini.example configs/config.ini
```
You have the ability to modify the configuration according to your specific setup.

Then you can run `main.py` in repo folder to init dota-demonbox
```
python main.py
```

## Commands
There are some commands you can use:
* `greatload` is used to load all matches into the database. It will be done faster if you add proxy links as a strings to the `web.json` file in the `config` folder.

* `web:proxycheck` to check if proxies are working.
  * flag `-f` to fix the proxies' list.

* `refresh` is used to refresh the database after `greatload`.
  * flag `-b` to make a backup before.

* `backup` to make backup of your database.
  * flag `-c` to clear after backup.
  * flag `-m` flag to mark a backup as important.

* `inspect` to inspect for errors in the database.
  * flag `-b` to make a backup before.
  * flag `-f` to fix errors.

* `load:demon` to load the trained demon model.

* `predict` to open the prediction menu.

* `clear` to clear the terminal.

* `getinfo` to retrieve information about database and demon.
* `getinfo:char <character name>` to retrieve information about a character based on their name.
* `getinfo:team <team name>` to retrieve information about a team based on its name.
* `getinfo:match <match ID>` to retrieve information match a team based on its ID.

* `fusion:char <character name 1> <character name 2>` to make fusion of character's attributes. You can use it if in the database you have different names of a same character.
* `fusion:team <team name 1> <team name 2>` same as `fusion:char`, but for a team.

* `fit <games' count from the end>` to train the demon.
  * `-b` to make `<games' count from the beginning>`.
  * `-p` to poweroff your machine after the training.

* `fit:workbook` to utilize the algorithm from the workbook for training the demon.

* 'tasks' to view current tasks, in case greatload hasn't been completed yet.
  * flag `-c` lo clear tasks.

* `source` to load the last important databace backup.
* `source:from <path>` to load the database using a specified path.

* `exit` to exit dota-demonbox.
