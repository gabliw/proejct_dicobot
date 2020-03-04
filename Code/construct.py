# -*- coding:utf-8 -*-
import discord

# pip install --upgrade pip
# pip install discord
# discord.py documentation : https://discordpy.readthedocs.io/en/latest/index.html

# insert discord token
token = None

# Client API : https://discordpy.readthedocs.io/en/latest/api.html#client
client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!help'):
        msg = '!hello, !command'
        await client.send_message(message.channel, msg)

    await message.channel.send("react")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print("Bot Awaiting")
    print(client.user.name)
    print(client.user.id)

client.run(token)