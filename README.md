# Matt-bot
Dumb discord bot I use for learning and testing stuff.
Currently has a few cool features, like image search, some image manipulation (for making caption and demotivational poster memes), a (sorta) coinflip, an autoreact for the word "Ratio", the infamous "Hi xyz, I'm Dad!" joke, and most recently, some cool Wiki commands.

[![Link For Invitation](https://img.shields.io/badge/Invite%20to%20Your%20server-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/api/oauth2/authorize?client_id=837011037894737951&permissions=414464732224&scope=applications.commands%20bot)

Optionally, you could try cloning the bot and adding the following .env variables:
```
DISCORD_TOKEN
GOOGLE_CUSTOM_SEARCH_API_TOKEN
SEARCH_ENGINE_ID
WIKIPEDIA_SEARCH_ENGINE_ID
WOOKIEEPEDIA_SEARCH_ENGINE_ID
BOT_USER_ID
```
(The search engine IDs are google custom search engine IDs, with the latter two searching wikipedia.org and wookieepedia exclusively, respectively.)
(There's also a "SQUILL_USER_ID" env variable. Add that and use your own discord user ID as the value.)

## I'm a beginner, so the code is trash

Suggest changes if you want to, or not.

Also, the bot is written in nextcord, a fork of discord.py.

***
**if you wanna get the code for this feature, it's in ```cogs/ImageCommands.py```, under the djtj function**

<img src = "https://github.com/Bezbakri/Matt-bot/blob/main/assets/trump_tweet_example.png?raw=true" alt = "trump tweet example">

[The file in question](cogs/ImageCommands.py#L296) (go to line 296)