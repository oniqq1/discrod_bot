import discord
from discord.ext import commands
from settings import TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="basic_user")

    if role:
        await member.add_roles(role, reason='Automatic role assignment on join')
    else:
        print(f'Role "{"basic_user"}" didnt found  "{member.guild.name}"')

    channel = discord.utils.get(member.guild.system_channel)

    if channel:
        await channel.send(f'Welcome to the server, {member.mention}!')




@bot.command()
async def users(ctx):
    member_count = ctx.guild.member_count
    online_count = 0

    for member in ctx.guild.members:
        if member.status != discord.Status.offline:
            online_count += 1



    await ctx.send(f'This server has **{member_count}** members. \n **{online_count}** members online.')


@bot.command()
async def ticket(ctx):
    basic_role = discord.utils.get(ctx.guild.roles, name="basic_user")
    admin_role = discord.utils.get(ctx.guild.roles, name="admin")


    overwrites = {
        basic_role: discord.PermissionOverwrite(view_channel=False, send_messages=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        admin_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    channel = await ctx.guild.create_text_channel(
        name=f"ticket-{ctx.author.name}",
        overwrites=overwrites,
        topic=f"Ticket channel for {ctx.author.name}"
    )

    await channel.send(f"{ctx.author.name}, your ticket channel was created.")


@bot.command()
async def close_ticket(ctx):
    if ctx.channel.name.startswith('ticket-'):
        await ctx.channel.delete()
    else:
        await ctx.send('This command can only be used in ticket channels.')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(TOKEN)