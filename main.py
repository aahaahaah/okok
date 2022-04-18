import discord
from discord.ext import commands
import os
import asyncio
import colorama
import datetime
from urllib import parse, request
import re
import time
import pymongo
from colorama import Fore, Style 
import io
import csv
import random
import aiohttp
import json
import asyncio
import random
from random import choice
from discord.ext.commands import has_permissions, MissingPermissions, Greedy
from typing import Union
import datetime
import urllib.parse
import requests



data = pymongo.MongoClient("mongodb+srv://cheemsgay:imimokok@cluster0.jqdu0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = data.get_database("cheemsgay").get_collection("okgandu")
dbb = data.get_database("cheemsgay").get_collection("okbro")

determine_flip = [1, 0]
CSV_NAME = "guild-album-mapping.csv"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("_"), intents=intents, case_insensitive=True)
bot.remove_command('help')



@bot.command()
async def help(ctx):
 embed=discord.Embed(title="GREED COMMAND MENU", 
 url="https://discord.com/api/oauth2/authorize?client_id=804663463842283562&permissions=8&scope=bot%20applications.commands") 
 embed.add_field(name=" UTILITY ⚙️",value="`ping`,`calculate`,`geticon`,`seticon`,`getbanner`,`setbanner`,`dm`,`addemoji`,`membercount`,`snipe`", inline=False)
 embed.add_field(name="FUN :game_die:",value="`roll`,`coinflip`,`clone`", inline=False)
 embed.add_field(name="MODERATION :tools:",value="`ban`,`unban`,`mute`,`unmute`,`lock`,`unlock`,`purge`", inline=False)

 await ctx.reply(embed=embed, mention_author=False)



@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.reply(f"Muted {member.mention} for reason {reason}", mention_author=False)
   



@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(mutedRole)
    await ctx.reply(f"Unmuted {member.mention} ", mention_author=False)


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User):
    guild = ctx.guild
    if ctx.author.guild_permissions.ban_members:
      await ctx.reply(f"{user} was unbanned!", mention_author=False)
      await guild.unban (user=user)

@bot.command(name = 'snipe')
async def snipe(ctx):
    channel = ctx.channel
    try: 
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}.")
        await ctx.reply(embed = em, mention_author=False)
    except: 
        await ctx.reply(f"There are no recently deleted messages in #{channel.name}", mention_author=False)




  
@bot.command(helpinfo='Clone your words - like echo')
async def clone(ctx, user: discord.Member , *,message):
    '''
    Creates a webhook, that says what you say. Like echo.
    '''
    pfp = requests.get(user.avatar_url_as(format='png', size=256)).content
    hook = await ctx.channel.create_webhook(name=user.display_name,
                                            avatar=pfp)
    await hook.send(message)
    await hook.delete()
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.reply(f"{member} has been banned.", mention_author=False)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.reply(f"{member} has been kicked.", mention_author=False)







@bot.command(aliases=['clean','cls','sweep'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=10):
        await ctx.channel.purge(limit=amount+1)
        

@bot.event
async def on_ready():
    print('Potato Cat is ready :D')

    servers = len(bot.guilds)
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1

    await bot.change_presence(activity = discord.Activity(
        type = discord.ActivityType.watching,
        name = f'{servers} servers and {members} members'))



  






  
  
  
@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def roll(ctx, info=None):
   async with ctx.typing():
    await asyncio.sleep(1)
   if info is None:
    embed = discord.Embed(title="Invalid Choice ❎", color=0x2f3136, description="Correct usage example: **`p!roll 2d100`** to roll 2 dice with 100 sides.")
    await ctx.reply(embed=embed, mention_author=False)
    return
   inf = re.search(r'^\d+', info)
   inf2 = re.search(r'\d+$', info)
   if not inf2:
    embed = discord.Embed(title="Invalid Choice ❎", color=0x2f3136, description="Correct usage example: **`p!roll 2d100`** to roll 2 dice with 100 sides.")
    await ctx.reply(embed=embed, mention_author=False)
   if not inf:
    for x in range(int(1)):
      lol = random.randint(0, int(inf2.group()))
      xd = "".join(str(lol))
      total = lol
    embed = discord.Embed(title="Dice roll", color=0x2f3136, description=f"**{info}**: [ {xd}]\nTotal: **`{total}`**")
    await ctx.reply(embed=embed, mention_author=False)

   if inf:
    xd = ""
    total = 0
    for x in range(int(inf.group())):
      lol = random.randint(0, int(inf2.group()))
      xd += str(lol) + " "
      total = total + lol
    embed = discord.Embed(title="Dice roll", color=0x2f3136, description=f"**{info}**: [ {xd}]\nTotal: **`{total}`**")
    await ctx.reply(embed=embed, mention_author=False)






@bot.command(aliases=["member_count", "count"])
async def membercount(ctx):
        embed = discord.Embed()

        embed.set_author(name="Member Count", icon_url=bot.user.avatar_url)
        embed.add_field(name="Current Member Count:", value=ctx.guild.member_count)
        embed.set_footer(text=ctx.guild, icon_url=ctx.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.reply(embed=embed, mention_author=False)
    

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply('Channel locked.', mention_author=False)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply('Channel unlocked.', mention_author=False)


@bot.command(aliases=["av", "pfp"])
async def avatar(ctx, *, member: discord.Member = None):
        if not member:member=ctx.message.author

        message = discord.Embed(title=str(member), color=discord.Colour.orange())
        message.set_image(url=member.avatar_url)

        await ctx.reply(embed=message, mention_author=False)

  
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000, 1)
    await ctx.reply(f"**Pong!** `{latency}ms`", mention_author=False)


@bot.command()
async def invite(ctx):
 embed=discord.Embed(title="Thanks for using GreeD!!!") 
 embed.add_field(name="Bot invite", value="[Click here](https://discord.com/api/oauth2/authorize?client_id=804663463842283562&permissions=8&scope=bot%20applications.commands)")
 await ctx.reply(embed=embed, mention_author=False)

@bot.command(aliases=["calculate","calc","maths"])
async def math(ctx, *, expression:str):
 async with ctx.typing():
    await asyncio.sleep(1)
    calculation = eval(expression)
    await ctx.reply('{}\n**Your answer is** {}'.format(expression, calculation), mention_author=False)

@bot.command(aliases=["toss","coin","flip"])
async def coinflip(ctx):
    if random.choice(determine_flip) == 1:
        embed = discord.Embed(title="Coinflip", description=f"{ctx.author.mention} Flipped coin, we got **Heads**!")
        await ctx.reply(embed=embed, mention_author=False)

    else:
        embed = discord.Embed(title="Coinflip", description=f"{ctx.author.mention} Flipped coin, we got **Tails**!")
        await ctx.reply(embed=embed, mention_author=False)




@bot.command()
@has_permissions(manage_messages = True)
@commands.cooldown(1,30,commands.BucketType.user)
async def dm(ctx, user: discord.User, *, message=None):
        message = message or "DM message to be sent"
        try:
            await user.send(message)
            await ctx.reply("Message sent successfully.", mention_author=False)
        except: 
            await ctx.reply("Dms off or the user is bot.", mention_author=False)
 
@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("A required agument is missing.", mention_author=False) 

    
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): 
        msg = '**Still on cooldown**, please try again in {:.2f}s.'.format(error.retry_after)
        await ctx.reply(msg, mention_author=False) 
       


    
@bot.command(aliases=["yt"])
@commands.cooldown(1,10,commands.BucketType.user)
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_content= html_content.read().decode()
    search_results = re.findall(r'\/watch\?v=\w+', search_content)
    await ctx.reply('https://www.youtube.com' + search_results[0], mention_author=False)

    
@youtube.error
async def youtube_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("A required agument is missing.", mention_author=False) 
        
        
@bot.command(description="Set the guild icon")
@commands.cooldown(1,30,commands.BucketType.user)
async def seticon(ctx, url: str):
    """Set the guild icon."""
    if ctx.message.guild is None:
        return

    permissions = ctx.message.author.permissions_in(ctx.channel)
    if not permissions.manage_guild:
        await ctx.reply("You don't have the required permissions to do this.", mention_author=False)
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.reply('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.message.guild.edit(icon=data.read())
            await ctx.reply("Icon set successfully!", mention_author=False)   
  
@bot.command(description="Set the guild banner image")
async def setbanner(ctx, url: str):
    """Set the guild banner image."""
    if ctx.message.guild is None:
        return

    permissions = ctx.message.author.permissions_in(ctx.channel)
    if not permissions.manage_guild:
        print("You don't have the required permissions to do this.")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.reply('Could not download file...', mention_author=False)
            data = io.BytesIO(await resp.read())
            await ctx.message.guild.edit(banner=data.read())
            await ctx.reply("Banner set successfully!", mention_author=False)

@setbanner.error
async def setbanner_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("A required agument is missing.", mention_author=False) 
      
@seticon.error
async def seticon_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("A required agument is missing.", mention_author=False) 

        
@bot.command(aliases=["serverlogo", "serverav", "serveravatar"])
async def geticon(ctx):
    if ctx.message.guild is None:
        return
    await ctx.reply(ctx.message.guild.icon_url, mention_author=False)        

@bot.command(aliases=["serverbanner"])
async def getbanner(ctx):
    """Get the guild banner image."""
    if ctx.message.guild is None:
        return
    await ctx.reply(ctx.message.guild.banner_url, mention_author=False)   
        
@math.error
async def math_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("A required agument is missing.", mention_author=False) 
  


@bot.command(aliases=["addemoji","stealemoji"])
@commands.has_permissions(manage_emojis = True)
async def steal(ctx, emotes: Greedy[Union[discord.Emoji, discord.PartialEmoji]]):
    if not emotes:
        return await ctx.reply('You didn\'t specify any emotes.', mention_author=False)
    in_server, added = [], []
    for emote in emotes:
        if isinstance(emote, discord.Emoji) and emote.guild == ctx.guild:
            in_server.append(emote)
        else:
            added.append(await ctx.guild.create_custom_emoji(
                name=emote.name,
                image=await emote.url.read(),
                reason=f'Added by {ctx.author} ({ctx.author.id})'))

    if not added:
        return await ctx.reply(f'Specified emote{"s" if len(emotes) != 1 else ""} are already in this server >:(')
    if in_server:
        return await ctx.reply(f'{" ".join(map(str, added))} have been added to this server, while '
                              f'{" ".join(map(str, in_server))} wasn\'t because they are already added!', mention_author=False)
    await ctx.reply(f'{" ".join(map(str, added))} has been added to this server!', mention_author=False)



    
    

bot.run("ODA0NjYzNDYzODQyMjgzNTYy.YBPnPw.RwS-sDSy8clfbs4g7-fF-aHGP8Y")
