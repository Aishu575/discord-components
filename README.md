# discord.py-components
[![Build Status](https://travis-ci.com/kiki7000/discord.py-components.svg?branch=master)](https://travis-ci.com/kiki7000/discord.py-components)
[![PyPI version](https://badge.fury.io/py/discord-components.svg)](https://badge.fury.io/py/discord-components)
[![Documentation Status](https://readthedocs.org/projects/discord-components)](https://discord-components.readthedocs.io/)

unofficial library for discord components(on development)

## Install
```sh
pip install --upgrade discord-components
```

## Example
```python
from discord import Client
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

bot = Client()
ddb = DiscordComponents(bot)

@bot.event
async def on_message(msg):
    await msg.channel.send(
        "Content",
        components=[
            Button(style=ButtonStyle.blue, label="Blue"),
            Button(style=ButtonStyle.red, label="Red"),
            Button(style=ButtonStyle.URL, label="url", url="https://example.org"),
        ],
    )

    res = await ddb.wait_for_interact("button_click")
    if res.channel == msg.channel:
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f'{res.component.label} clicked'
        )


bot.run("token")
```

## Docs
[The docs](https://discord-components.readthedocs.io/) can contain lot of spelling mistakes, grammar errors so if there is a problem please create an issue!

## Features
+ Send, Edit discord components
+ Get components interact event!
+ Supports discord.ext.commands

## Helps
+ [Minibox](https://github.com/minibox24) - Button API explanation
+ [Lapis](https://github.com/Lapis0875) - Told me how to replace a property