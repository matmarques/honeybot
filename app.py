import time
import discord
import json
import os
import sys


if not os.path.isfile("config.json"):
    sys.exit("{*} No 'config.json' found.")
try:
    with open("config.json") as config:
        config = json.load(config)
except json.decoder.JSONDecodeError as exc:
    sys.exit("{*} Invalid JSON syntax w/ traceback:\n%s" % exc)

default_channel = None

client = discord.Client()


@client.event
async def on_message(message):
    global default_channel

    server = message.server
    channel = message.channel
    author = message.author
    content = message.content

    if author == client.user or author.bot:
        return

    if default_channel is None:
        default_channel = client.get_channel(config['default_channel'])
    if default_channel is None:
        return

    caught = []

    for keyword in config['keywords']:
        if keyword in message.content:
            caught.append(keyword)
    if not caught:
        return

    await client.send_message(default_channel, """```css
User         %s <@%s>
Server      %s <@%s> 
Time         %s
Keyword  %s
--------------------------------------------------------

%s
```""" % (
        author.name + "#" + author.discriminator,
        author.id,

        server.name,
        server.id,
        time.asctime(),

        ", ".join(caught),
        
        content[:1000].replace('`', '')
        )
)


client.run(config['token'])
