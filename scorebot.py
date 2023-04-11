import discord
from discord.ext import commands
import requests

description = '''A bot to show you the leaderboards of PAUL'''
paul_endpoint = "https://web.physcorp.com/paul/endpoint.php"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

valid_games = ['Puzzle', 'Snake', 'Asteroids', 'PAULatformer', 'Tetris']

paul = commands.Bot(command_prefix='!', description=description, intents=intents)
@paul.event
async def on_ready():
    await paul.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name= 'All things'))
    print(f'Logged in as {paul.user} (ID: {paul.user.id})')
    print('------')

@paul.command()
async def leaderboards(ctx):
    await ctx.send("Which game would you like to see the leaderboard for?\nFor Puzzle enter !puzz\nFor Snake enter !snake\nFor Asteroids enter !ast\nFor PAULatformer enter !plat\nFor Tetris enter !tet")

@paul.command()
async def puzz(ctx):
    game_name = "Puzzle"
    r = requests.get(paul_endpoint)
    if r.status_code != 200:
        await ctx.send(f"[I have died, rip me. Error code {r.status_code}] {r.text}")
    else:
        game_dict = r.json()
        game = game_dict[game_name]
        # If game is empty, no scores
        if game == "":
            await ctx.send(f"No scores for {game_name} yet!")
        else:
            # Split scores into list
            scores = game.split(",")
            # Compile scores into a string separated by newlines
            scores_str = ""
            for score in scores:
                formatted_score = score.replace(":::", " - ")
                scores_str += f"{formatted_score}\n"
            await ctx.send(f"=== Puzzle Scoreboard ===\n{scores_str}")

@paul.command()
async def snake(ctx):
    game_name = "Snake"
    r = requests.get(paul_endpoint)
    if r.status_code != 200:
        await ctx.send(f"[I have died, rip me. Error code {r.status_code}] {r.text}")
    else:
        game_dict = r.json()
        game = game_dict[game_name]
        # If game is empty, no scores
        if game == "":
            await ctx.send(f"No scores for {game_name} yet!")
        else:
            # Split scores into list
            scores = game.split(",")
            # Compile scores into a string separated by newlines
            scores_str = ""
            for score in scores:
                formatted_score = score.replace(":::", " - ")
                scores_str += f"{formatted_score}\n"
            await ctx.send(f"=== Snake Scoreboard ===\n{scores_str}")

@paul.command()
async def ast(ctx):
    game_name = "Asteroids"
    r = requests.get(paul_endpoint)
    if r.status_code != 200:
        await ctx.send(f"[I have died, rip me. Error code {r.status_code}] {r.text}")
    else:
        game_dict = r.json()
        game = game_dict[game_name]
        # If game is empty, no scores
        if game == "":
            await ctx.send(f"No scores for {game_name} yet!")
        else:
            # Split scores into list
            scores = game.split(",")
            # Compile scores into a string separated by newlines
            scores_str = ""
            for score in scores:
                formatted_score = score.replace(":::", " - ")
                scores_str += f"{formatted_score}\n"
            await ctx.send(f"=== Asteroids Scoreboard ===\n{scores_str}")

@paul.command()
async def plat(ctx):
    game_name = "PAULatformer"
    r = requests.get(paul_endpoint)
    if r.status_code != 200:
        await ctx.send(f"[I have died, rip me. Error code {r.status_code}] {r.text}")
    else:
        game_dict = r.json()
        game = game_dict[game_name]
        # If game is empty, no scores
        if game == "":
            await ctx.send(f"No scores for {game_name} yet!")
        else:
            # Split scores into list
            scores = game.split(",")
            # Compile scores into a string separated by newlines
            scores_str = ""
            for score in scores:
                formatted_score = score.replace(":::", " - ")
                scores_str += f"{formatted_score}\n"
            await ctx.send(f"=== PAULatformer Scoreboard ===\n{scores_str}")

@paul.command()
async def tet(ctx):
    game_name = "Tetris"
    r = requests.get(paul_endpoint)
    if r.status_code != 200:
        await ctx.send(f"[I have died, rip me. Error code {r.status_code}] {r.text}")
    else:
        game_dict = r.json()
        game = game_dict[game_name]
        # If game is empty, no scores
        if game == "":
            await ctx.send(f"No scores for {game_name} yet!")
        else:
            # Split scores into list
            scores = game.split(",")
            # Compile scores into a string separated by newlines
            scores_str = ""
            for score in scores:
                formatted_score = score.replace(":::", " - ")
                scores_str += f"{formatted_score}\n"
            await ctx.send(f"=== Tetris Scoreboard ===\n{scores_str}")

paul.run('MTA4NjY1NzE1NzM2NzM1MzQ0Nw.GU-OBu.64MXE9ImHTbZCChiajTGXnPdLJ9wlaThFaT3Zg')
