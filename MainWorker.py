import asyncio
import datetime
import os
import shutil
import discord
from DiscordWorker import DiscordWorker

std_path = os.getcwd()
std_branch = 'master'
std_doc_url = 'https://docs.ideco.dev'
std_url = 'https://github.com/ideco-team/docsUTM.git'

bot_config = DiscordWorker(os.getenv('DISCORD_TOKEN'), '/', discord.Intents.all())
bot = bot_config.get_bot()


@bot.event
async def on_ready():
    print('READY')


async def check_aliases(message, version='v15', url=std_doc_url, url_repo=std_url, verbose=False, off=True):
    await message.channel.send('Checking aliases...')
    directory = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    create_dir(directory)
    bot_config.check_web_aliases(version, url, url_repo, off, verbose)
    await message.channel.send(file=discord.File('aliases.txt'),
                               content=f'Тест алиасов {datetime.datetime.now().strftime("%Y%m%d%")}')
    os.remove('aliases.txt')
    delete_dir(directory)


async def check_content_refs(message, version='v15', url=std_url, verbose=False):
    await message.channel.send('Тестим')
    directory = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    create_dir(directory)
    bot_config.check_content_refs(version, url, verbose)
    await message.channel.send(file=discord.File('content_refs.txt'),
                               content=f'Тест ссылок {datetime.datetime.now().strftime("%Y/%m/%d")}')
    os.remove('content_refs.txt')
    delete_dir(directory)


def create_dir(name):
    os.makedirs(name, exist_ok=True)
    os.chdir(name)


def delete_dir(name):
    print(os.getcwd())
    os.chdir('..')
    shutil.rmtree(name)


@bot.command(name='check_aliases')
async def wrapper_check_aliases(message, version='v15', url=std_doc_url, url_repo=std_url, verbose=False, off=True):
    task = asyncio.create_task(check_aliases(message, version, url, url_repo, verbose, off))
    await message.channel.send("Тест алиасов запущен")


@bot.command(name='check_content_refs')
async def wrapper_check_content_refs(message, version='v15', url=std_url, verbose=False):
    task = asyncio.create_task(check_content_refs(message, version, url, verbose))
    await message.channel.send("Тест ссылок запущен")


asyncio.run(bot.start(bot_config.token))
