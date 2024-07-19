import discord_bot
from discord.ext import commands

class HelloCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='hello') # 그룹 명령어는 단독으로 호출할 수 없습니다.
    async def hello_group(self, ctx: discord_bot.ext.commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('그룹 명령어는 단독으로 실행될 수 없습니다.')

    @hello_group.command(name='korean')
    async def hello_korean(self, ctx):
        # !hello korean 명령어에 대한 응답을 처리합니다.
        await ctx.send('안녕하세요.')