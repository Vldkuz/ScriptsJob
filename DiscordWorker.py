import asyncio
import datetime
import multiprocessing
import os
import shutil

import discord
from discord.ext import commands
from CheckRefsWorker import CheckRefsWorker


class DiscordWorker:
    def __init__(self, token, com_prefix, intents):
        self.token = token
        self.bot = commands.Bot(command_prefix=com_prefix, intents=intents)

    def get_bot(self):
        return self.bot

    async def start_bot(self):
        await asyncio.create_task(self.bot.run(self.token))

    @staticmethod
    def check_content_refs(branch, url_repo, verbose):
        with open('content_refs.txt', 'w') as file:
            checker = CheckRefsWorker(out_stream=file, verbose=verbose, directory=os.getcwd())
            checker.check_content_refs(url_repo,branch)



    @staticmethod
    def check_web_aliases(branch, url, url_repo, off, verbose):
        with open('aliases.txt', 'w') as file:
            checker = CheckRefsWorker(out_stream=file, verbose=verbose, directory=os.getcwd())
            checker.check_web_aliases(url, url_repo, branch, off)


