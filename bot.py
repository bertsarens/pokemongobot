# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
from discord.ext import commands
from datetime import datetime
from datetime import date
import os

class Quest:
    def __init__(self, stop: str, task: str, reward: str):
      self.stop=stop
      self.reportDate=date.today()
      self.task=task
      self.reward=reward    

activeQuests = []

def addQuest(newQuest: Quest):
  isNew = True
  for quest in activeQuests:
    if (quest.stop==newQuest.stop):
      isNew = False
  if (isNew):
    activeQuests.append(newQuest)

def cleanQuests():
  for quest in list(activeQuests):
    if (quest.reportDate != date.today()):
      activeQuests.remove(quest)

def removeQuest(stop: str):
  for quest in list(activeQuests):
    if (quest.stop == stop):
      activeQuests.remove(quest)

TOKEN = os.environ.get('TOKEN') 

bot = commands.Bot(command_prefix='!', description='A bot for managing quests and raids in pokemonGo')

@bot.command()
async def addquest(ctx, stop:str,reward:str,*tasks):
    task = ""
    for s in tasks:
      task=task+" "+s
    addQuest(Quest(stop,task,reward))
    await ctx.send("quest added")

@bot.command()
async def quests(ctx):
    cleanQuests()
    embed = discord.Embed(color=0xeee657)
    if (len(activeQuests)!=0):
      for quest in activeQuests:
        embed.add_field(name=str(quest.reportDate)+"  "+quest.stop, value=quest.task+" ==> "+quest.reward,inline=False)
    else:
      embed.add_field(name="no quests", value="no quests reported today",inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def removequest(ctx, stop:str):
    removeQuest(stop)
    await ctx.send("quest removed")

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Quest en raid bot", description="Commandos:", color=0xeee657)

    embed.add_field(name="!addquest stop reward taak om te doen", value="Voegt een quest toe aan de lijst", inline=False)
    embed.add_field(name="!removequest stop", value="Verwijderd de quest voor een stop uit de lijst", inline=False)
    embed.add_field(name="!quests", value="Geeft een lijst met quests terug", inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)