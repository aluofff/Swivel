import discord
from discord.ext import commands
import json
from discord import app_commands
import keep_alive
import discord as d
from discord.ext import commands as c
from discord import app_commands as a
from datetime import datetime
from discord import Interaction
from typing import Optional
import random
from datetime import timedelta
import os
from discord.ext import commands
import datetime
from discord.ext import tasks

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.event
async def on_ready():
    switch_presence.start()

@tasks.loop(minutes=1)
async def switch_presence():
    if switch_presence.current_loop % 2 == 0:
        # Even loop number, show number of servers
        servers = len(bot.guilds)
        await bot.change_presence(activity=discord.Game(f"in {servers} servers!"))
    else:
        # Odd loop number, show number of users
        total_users = 0
        for guild in bot.guilds:
            total_users += guild.member_count
        await bot.change_presence(activity=discord.Game(f"with {total_users} users!"))
    print("Bot is online")
    print("ck#0004")
    print("discord.gg/riv")
    print("Aluof#7221")
    print(f"Servers: {len(bot.guilds)}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.command()
async def scheck(ctx):
    guilds = bot.guilds
    response = "**Here are the servers I am currently in:\n\n**"
    for guild in guilds:
        response += f" - {guild.name}\n"
    await ctx.send(response)

@bot.tree.command()
async def rps(ctx, choice: str):
    """Play a game of rock-paper-scissors with the bot"""
    choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(choices)

    if choice not in choices:
        await ctx.response.send_message("Invalid choice. Choose either 'rock', 'paper', or 'scissors'.")
    elif choice == bot_choice:
        await ctx.response.send_message(f"We both chose {choice}. It's a tie!")
    elif choice == 'rock' and bot_choice == 'scissors' or \
         choice == 'paper' and bot_choice == 'rock' or \
         choice == 'scissors' and bot_choice == 'paper':
        await ctx.response.send_message(f"You chose {choice} and I chose {bot_choice}. You win!")
    else:
        await ctx.response.send_message(f"You chose {choice} and I chose {bot_choice}. I win!")

## commands
@bot.tree.command(name="afk",description="I set afk")
@a.describe(afk_message = "The afk message that will be displayed in the chat")
async def afk(ctx: d.Interaction,afk_message: str):
    await ctx.response.send_message(f'**{ctx.user.display_name} 🟢 I set you afk to   "{afk_message}"🟢**')

@bot.tree.command(name="dick",description="see how big is your dick")
async def dick(ctx: d.Interaction):
  await ctx.response.send_message(f"**{ctx.user.mention} your dick size is {random.randint(a=0,b=100)}**")

@bot.tree.command()
@commands.has_permissions(kick_members=True)
async def clear(interaction, number: int):
    """Clears the specified number of messages from the channel."""
    if number <= 0:
        await interaction.response.send_message("The number of messages to clear must be greater than 0.")
        return
    elif number > 100:
        await interaction.response.send_message("You cannot clear more than 100 messages at once.")
        return
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message(embed=discord.Embed(description="You don't have required permissions.", color=0xff5050))
        return
    await interaction.channel.purge(limit=number)
    await interaction.response.send_message(f"{number} messages have been cleared.", delete_after=5)


@bot.tree.command(name="mute", description="Mutes a user for a specified time.")
@commands.has_permissions(ban_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, timelimit: str):
    if not interaction.user.guild_permissions.kick_members:
        embed = discord.Embed(description="You don't have the required permissions.", color=0xff5050)
        await interaction.response.send_message(embed=embed)
        return
    if "m" in timelimit:
        gettime = timelimit.strip("m")
        newtime = datetime.timedelta(minutes=int(gettime))
        await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
        embed = discord.Embed(description=f"{member.mention} has been timed out for {timelimit}", color=0x00ff00)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(description="Please include the 'm' character in your timelimit value.", color=0xff5050)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="unmute", description="unmutes a user")
@commands.has_permissions(kick_members=True)
async def unmute(ctx: commands.Context, member: discord.Member):
    await member.edit(timed_out_until=None)
    await ctx.response.send_message(embed=discord.Embed(description=f"**{member.mention} has been unmuted.**", color=0x00ff00))

@bot.tree.command(name="unban",description="unbans a user")
async def unban(ctx, user: discord.User):
    """Unbans a user from the server"""
    try:
        await ctx.guild.unban(user)
        embed = discord.Embed(title="User unbanned", description=f"{user.name}#{user.discriminator} has been unbanned. :white_check_mark: ", color=discord.Color.green())
        await ctx.response.send_message(embed=embed)
    except discord.NotFound:
        embed = discord.Embed(title="User not found", description="The specified user was not found.", color=discord.Color.red())
        await ctx.response.send_message(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="Permission error", description="I don't have permission to unban that user.", color=discord.Color.red())
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="warn",description="warns a user")
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason: str = "Not Specified"):
    if member == ctx.user:
        await ctx.response.send_message("**You can't warn yourself, smart ass**")
    else:
        em = discord.Embed(title="**Warned**", description=f"{member}, {member.mention}, was warned because of {reason}", color=discord.Color.red())
        em2 = discord.Embed(title="**Warning nofitication**", description=f"You have been warned because of {reason}", color=discord.Color.red())
        await member.send(embed=em2)
        await ctx.response.send_message(embed=em)

@bot.tree.command(name='ban', description='bans a user')
async def ban(interaction : discord.Interaction, user : discord.Member, delete_message_days : int = None, reason : str = None):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(embed=discord.Embed(description="You don't have required permissions.", color=0xff5050))
    if delete_message_days == None:
        delete_message_days = 0
    if delete_message_days > 7 or delete_message_days < 0:
        await interaction.response.send_message(embed=discord.Embed(description='Invalid amount of days.', color=0xff5050))

    await user.ban(reason=reason, delete_message_seconds=delete_message_days * 86400)
    await interaction.response.send_message(embed=discord.Embed(description=f"Banned {user} for {reason}", color=0x50ff50))

@bot.tree.command(name='kick', description='kicks a user')
async def kick(interaction : discord.Interaction, user : discord.Member, reason : str = None):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message(embed=discord.Embed(description="You don't have required permissions.", color=0xff5050))
        return

    await user.kick(reason=reason)
    await interaction.response.send_message(embed=discord.Embed(description=f"Kicked {user} for {reason}", color=0x50ff50))

@bot.tree.command(name='membercount', description='Shows the servers membercount')
async def membercount(interaction):
    await interaction.response.defer()
    embed = discord.Embed(title='Member Count', description=f'**The server has {interaction.guild.member_count} members!**', color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@bot.tree.command(name='cole', description='Cole is better')
async def cole(ctx):
  await ctx.response.send_message("Cole is better")

@bot.command()
async def bu(ctx, *, message = None):
  if message == None:
    return
  else:
    embed = discord.Embed(title = 'Information', description = message, color=discord.Color.green())
    embed.set_footer(text = f'Announced by {ctx.author}')
    await ctx.send(embed = embed)

@bot.tree.command(name='say', description='Says somthing with the bot (anything)')
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
  await interaction.response.send_message(f"**{thing_to_say}**")

@bot.tree.command(name='whois', description='Get a users info')
async def whois(ctx, member: discord.Member):
    embed = discord.Embed(title=member.name, description=member.mention, color=discord.Color.orange())
    embed.add_field(name='ID', value=member.id, inline=False)
    embed.add_field(name='Status', value=member.status, inline=False)
    embed.add_field(name='Joined', value=member.joined_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)
    embed.add_field(name="Bot", value=member.bot, inline=True)
    embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
    embed.add_field(name="Created At", value=member.created_at.strftime("%a, %d %B %Y %I:%M %p UTC"), inline=True)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.response.send_message(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} ({guild.id})", color=0x00ff00)
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Region", value=guild.region, inline=False)
    embed.add_field(name="Members", value=guild.member_count, inline=False)
    embed.set_thumbnail(url=guild.icon_url)
    await ctx.send(embed=embed)

@bot.tree.command(name='ping', description='Shows the ping of the bot')
async def ping(ctx):
    embed = discord.Embed(title="Pong! :ping_pong:", description=f"Latency: {round(bot.latency * 1000)}ms", color=0x00FF00)
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name='help', description='Lists all the commands of the bot' )
async def help(ctx):
    em = discord.Embed(title='HELP', description='*This is a list of all the commands of the bot !!* **( more coming soon !)**', color=discord.Color.red())
    em.add_field(name='Commands', value='`ban` use this to ban a user for ex (/ban user reason)\n`kick` Use this command to kick other users for ex (/kick user reason)\n`ping` to get the bots ping\n`help` This command will list every command in the bot\n`Membercount`This will show you the membercount of the server\n`unban` Use this to unban someone from the server\n`whois` to get a users info\n`say` to say a message as the bot\n`afk` sets you afk.\n`dick` to see your dick size (fun command)\n`mute` to mute a user\n`unmute` to unmute a user.', inline=False)
    await ctx.response.send_message(embed=em)

token = os.getenv('token')

keep_alive.keep_alive()
token = os.environ['token']
bot.run(token)
