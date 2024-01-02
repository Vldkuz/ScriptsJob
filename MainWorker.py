import asyncio
import datetime
import multiprocessing
import os

import discord

from DiscordWorker import DiscordWorker

std_branch = 'master'
std_doc_url = 'https://docs.ideco.dev'
std_url = 'https://github.com/ideco-team/docsUTM.git'

bot_config = DiscordWorker(os.getenv('DISCORD_TOKEN'), '/', discord.Intents.all())
bot = bot_config.get_bot()


@bot.event
async def on_ready():
    print('READY')


@bot.command(name='check_aliases')
async def check_aliases(message, version='v15', url=std_doc_url, url_repo=std_url, verbose=False, off=True):
    bot_config.check_web_aliases(version, url, url_repo, off, verbose)
    await message.channel.send(file=discord.File('aliases.txt'), content=f'Тест алиасов {datetime.datetime.now()}')
    os.remove('aliases.txt')


@bot.command(name='check_content_refs')
async def check_content_refs(message, version='v15', url=std_url, verbose=False):
    bot_config.check_content_refs(version, url, verbose)
    await message.channel.send(file=discord.File('content_refs.txt'),
                               content=f'Тест ссылок {datetime.datetime.now()}')
    os.remove('content_refs.txt')


bot.run(bot_config.token)
