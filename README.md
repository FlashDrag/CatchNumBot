[<img src="https://img.shields.io/badge/Telegram-%40CatchNumBot-blue">](https://t.me/CatchNumBot)

### This is a Python Telegram bot GAME created with the Aiogram v2.2 framework and using Binary search algorithm

#### Game Rules 
The bot sets the range of numbers from 1 to 10 and sets a random number, and the player needs to guess it in 4 attempts. If the user guessed the number, then the difficulty is increased by increasing the range of numbers. The number of attempts is calculated automatically by the algorithm and is different for different ranges of numbers, but the minimum possible so that the player can guess correctly.

>
#### Data
The rating of players, game  progress and some actions of each user, as well as losses and winnings, are stored in a remote database PostgreSQL. Every user can view or reset his progress in the bot menu. 

>
The rest of the data is available only to the admin in the admin menu to which users have no access, since the command input is checked by the isadmin filter.
> The bot is still under development. Next step is international localization.

>
> The current game language is ukrainian
