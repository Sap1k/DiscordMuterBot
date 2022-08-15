# bot.py
import os
import random
from time import sleep

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG = True

intents = discord.Intents().all()
client = discord.Client(intents=intents)

list_already_muted = ['šaškuuu, už jsi mutnutej', 'vypoj si mikrofon gajdo', 'pomalu snejksi',
                      'kámo, to bych ti moc nepomohl']
list_already_unmuted = ['šaškuuu, už můžeš mluvit', 'zapoj si mikrofon gajdo', 'pomalu snejksi',
                        'kámo, to bych ti moc nepomohl']


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name="sussy bot | .mutehelp"))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    userid = message.author.id
    user_message = str(message.content)
    channel = str(message.channel.name)

    if message.author.voice:
        voice_channel = message.author.voice.channel
    else:
        voice_channel = None

    if DEBUG:
        print(f'{username} ({userid}): {user_message} ({channel}) ({voice_channel})')

    if user_message.lower() == '.mute' and message.author.guild_permissions.mute_members:
        response = f'hippity hoppity, lidé v kanálu "{voice_channel}" domluvili :)'

        if message.author.voice.mute or message.author.voice.self_mute:
            response = random.choice(list_already_muted)
            await message.channel.send(response, delete_after=5)
            # Bruh
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio("bruh.mp3"), after=lambda e: print(e))
            sleep(2)
            await vc.disconnect()
        else:
            for member in message.author.voice.channel.members:
                await member.edit(mute=True)
            await message.channel.send(response, delete_after=5)

    elif user_message.lower() == '.mute' and not message.author.guild_permissions.mute_members:
        response = f'hippity hoppity, {username} pro tuto operaci nemá oprávnění :('

        await message.channel.send(response, delete_after=5)

    if user_message.lower() == '.unmute' and message.author.guild_permissions.mute_members:
        response = f'hippity hoppity, lidé v kanálu "{voice_channel}" můžou mluvit :)'

        if not message.author.voice.mute or message.author.voice.self_mute:
            response = random.choice(list_already_unmuted)
            await message.channel.send(response, delete_after=5)
            # Bruh
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio("bruh.mp3"), after=lambda e: print(e))
            sleep(2)
            await vc.disconnect()

        else:
            for member in message.author.voice.channel.members:
                await member.edit(mute=False)
            await message.channel.send(response, delete_after=5)

    elif user_message.lower() == '.unmute' and not message.author.guild_permissions.mute_members:
        response = f'hippity hoppity, {username} pro tuto operaci nemá oprávnění :('

        await message.channel.send(response, delete_after=5)

    if user_message.lower() == '.mutehelp':
        response = '*.mute* - ztlumí všechny uživatele v kanále, ve kterém se právě nacházíte \n' \
                   '*.unmute* - nechá všechny uživatele v kanále ve kterém se právě nacházíte opět mluvit \n\n' \
                   '**!! Uživatel používající tyto příkazy musí mít právo pro ztlumení uživatelů !!**'

        await message.channel.send(response)


client.run(TOKEN)
