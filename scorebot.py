import discord
from discord.ext import commands
from discord.ext import tasks
import requests
import json

description = '''A bot to show you the leaderboards of PAUL'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
txt = open('PAULTOken.txt','r')
token = txt.read()
txt.close()


paul = commands.Bot(command_prefix='!', description=description, intents=intents)
@paul.event
async def on_ready():
    await paul.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name= 'All things'))
    print(f'Logged in as {paul.user} (ID: {paul.user.id})')
    print('------')

@paul.command()
async def leaderboards(ctx):
    await ctx.send("Which game would you like to see the leaderboard for:\nFor hangman enter !hang\nFor number-guessing game enter !num\nFor Slide Puzzle enter !puzz\nFor Snake enter !Snake\nFor asteroids enter !ast\nFor Tetris enter !Tet")

@paul.command()
async def hang(ctx):
    await ctx.send("hangman scoreboard")

@paul.command()
async def num(ctx):
    await ctx.send("Number-guessing game scoreboard")

@paul.command()
async def puzz(ctx):
    await ctx.send("Slide puzzle socreboard")

@paul.command()
async def snake(ctx):
    await ctx.send("snake game scoreboard")

@paul.command()
async def ast(ctx):
    await ctx.send("Asteroids game scoreboard")

@paul.command()
async def Tet(ctx):
    await ctx.send("Tetris game scoreboard")

paul.run(BOT_TOKEN)
