import datetime
import os

import discord
from discord.ext import commands
import test_aliases as checker

bot = commands.Bot("/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Ready to WORK)')
@bot.command(name='check_alias')
async def check_alias(message, version:str):
    fd = open("tmp_file1.txt", "w")
    file_aliases = f'.gitbook.yaml'
    version_doc = version
    try:
        await message.send("Проверка алиасов запущена ;)")
        checker.check_aliases(file_aliases,version_doc, fd)
        fd.close()
    except BaseException as e:
        fd.close()
        await message.send("Че там с версиями ?")
    await message.send(file=discord.File('tmp_file1.txt'), content = f'Тест алиасов {datetime.datetime.now()}')
    os.remove("tmp_file1.txt")
@bot.command(name="check_all_refs")
async def check_all_refs(message):
    fd = open("tmp_file2.txt", "w")
    dir = f'..{os.sep}docsUTM'
    await message.send("Проверка ссылок запущена")
    checker.check_all_refs(dir, fd)
    fd.close()
    await (message.send(file=discord.File("tmp_file2.txt"), content = f'Тест ссылок {datetime.datetime.now()}'))
    os.remove("tmp_file2.txt")

token_discord = os.getenv('DISCORD_TOKEN')
bot.run(token_discord)