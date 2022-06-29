import discord
from discord.colour import Color
from discord.ext import commands, tasks
from responseseball import response
from itertools import cycle
import random


client = commands.Bot(command_prefix=';')
status = cycle(['helping your you know what it is! XD', 'IDK what this is?'])



# this will be printed on the console when the bot is ready to be used
@client.event
async def on_ready():
    changing_status.start()
    await client.change_presence(status=discord.Status.online)
    return f"Logged in as {client.user} and ready to go!"


# changing status
@tasks.loop(seconds=20)
async def changing_status():
    await client.change_presence(activity=discord.Game(next(status)))


# this command/function will print a message when someone joins the server
@client.event
async def on_member_join(ctx, member):
    print(f"Welcome to the server {member}!")
    ctx.send(f"Welcome to the server! {member.mention}")


# this command/function will print a message when a member leaves the server
@client.event
async def on_member_remove(ctx, member):
    print(f"We are sad, that {member} has left the guild...")
    ctx.send(f"We are sad that {member.mention}, has left the server... :(")


# this command/function will return the latency of the bot
@client.command()
async def ping(ctx):
    await ctx.send(f'ping = {round(client.latency * 1000)}ms')


# this command/function is 8ball and if you don't know what 8ball is then fuck off
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(response)}")


# for error handling when someone doesn't pass in a question in the 8ball function
@_8ball.error
async def eball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Please Enter a question for me to answer! ')


# for error handling (if a user enters a command which doesn't not exist
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Command doesn't exist/Invalid command used")
        print("Someone used an invalid command")


# this command/function will delete the amount of messages entered by the user
@client.command(aliases=['cls', 'purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


# this command/function will kick the member from the server
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked...")


# when a user doesn't have the permission to kick members then this message will be displayed
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"you don't have the permission to kick members")
        print("a user who doesn't have the permission to kick members tried it and didn't work")


# this command/function will ban the person from the guild
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.')


# this command/function will unban a person from the server
@client.command(aliases=['ub'])
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = ctx.guild.bans()
    member_name, member_disc = member.split('#')
    for banned_entry in banned_users:
        user = banned_entry.user
        if(user.name, user.disc) == (member_name, member_disc):
            await ctx.guild.unban()
            await ctx.send(f'{user.name} {user.disc} has been unbanned')
            return


client.run("<<scrubbed>>")
