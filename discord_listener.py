import asyncio
import datetime
import functools
import os
import shutil
import subprocess
import typing

import discord
from discord.ext import commands
import test_aliases as checker

url = "https://github.com/ideco-team/docsUTM.git"
dir = url[url.rfind('/') + 1:-4]

bot = commands.Bot("/", intents=discord.Intents.all())

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

def prepare_repo(url, branch):
    try:
        subprocess.run(['git', 'clone', f'{url}'])
        os.chdir(dir)
        subprocess.run(['git', 'checkout', branch])
        os.chdir("..")
        return True
    except BaseException:
        return False


def delete_repo(direct):
    shutil.rmtree(direct)



@bot.event
async def on_ready():
    print("READY TO WORK")

@to_thread
@bot.command(name='check_aliases')
async def check_aliases(message, version: str, verbose = False):
    await message.send("Проверка алиасов запущена ;)")

    if prepare_repo(url, version):
        os.chdir(dir)
        fd = open("tmp_file1.txt", "w")
        file_aliases = f'.gitbook.yaml'
        version_doc = version
        checker.check_refs_yaml(file_aliases, fd)
        checker.check_aliases(file_aliases, version_doc, fd, verbose)
        fd.close()
        await message.send(file=discord.File('tmp_file1.txt'), content=f'Тест алиасов {datetime.datetime.now()}')
        os.remove("tmp_file1.txt")
    else:
        await (message.send("Проблема при переключении ветви или вытягивании репозитория"))
    delete_repo(dir)


@to_thread
@bot.command(name="check_all_refs")
async def check_all_refs(message, branch: str, verbose=False):
    await message.send("Проверка ссылок запущена")

    if prepare_repo(url, branch):
        fd = open("tmp_file2.txt", "w")
        checker.check_all_refs(dir, fd, verbose)
        fd.close()
        await message.send(file=discord.File("tmp_file2.txt"), content=f'Тест ссылок {datetime.datetime.now()}')
        os.remove("tmp_file2.txt")
    else:
        await (message.send("Проблема при переключении ветви или вытягивании репозитория"))
    delete_repo(dir)


token_discord = os.getenv('DISCORD_TOKEN')
bot.run(token_discord)

