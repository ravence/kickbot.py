import discord
import asyncio
from discord.ext import commands
import random



bot = commands.Bot(command_prefix=";;k ")    # bot prefix
user_to_roles = {}     # dictionary that maps kicked user IDs to a list of roles
ROULETTE_ROLE = 00000000000000000      # roulette role id
ROULETTE_ON = False


async def send_invite(member, channel):
    """creates invite and sends it to member.
       returns True if successful and False if an error occurs"""

    invite = await channel.create_invite(max_age=86400, max_uses=1,
                                         temporary=True)

    try:
        await member.send(invite.url)
        return True
    except discord.Forbidden:

        return False

async def do_kick(member, channel):
    """does the kick and returns true+sends msg if the user was kicked"""
    try:
        await member.kick()
        await channel.send(member.mention + " was kicked")
        return True
    except discord.Forbidden:
        await channel.send("i don't have the permissions to kick this user!")
        return False


@bot.event
async def on_ready():
    """jst outputs to console when logged in, you can ignore this"""

    print("Logged in as", bot.user.name)
    print("-----")

@bot.event
async def on_member_join(member):
    """reassigns roles if someone was kicked by the bot"""

    if member.id in user_to_roles:
        await member.edit(roles=user_to_roles[member.id])
        del user_to_roles[member.id]


@bot.command()
async def self(ctx):
    """kicks sender of the message while making note of their roles"""

    sent_invite = await send_invite(ctx.author, ctx.message.channel)
    if sent_invite == False:
        await ctx.send(ctx.author.mention + " you don't have DMs on! \ni won't kick you w/ this command while ur DMs are off ;;")
        return
    user_to_roles[ctx.author.id] = ctx.author.roles
    await do_kick(ctx.author, ctx.channel)

@bot.command()
async def roulette(ctx):
    """actual roulette thing"""

    global ROULETTE_ON

    if ROULETTE_ON:
        await ctx.send("game is in progress!")
    else:
        ROULETTE_ON = True
        # just pretends 2 type for like 5-10 seconds
        async with ctx.typing():
            await asyncio.sleep(random.randint(5,10))

        # gets members with ROULETTE_ROLE and chooses a random one,
        # assuming it's possible. if it's not possible it quits the game.
        members = ctx.guild.get_role(ROULETTE_ROLE).members
        if members == None or len(members) == 0:
            await ctx.send("nobody has the roulette role or role DNE, game cancelled!")
            ROULETTE_ON = False
            return
        kicked = random.choice(members)

        # tells them they will be kicked
        await ctx.send("we have selecetd. " + kicked.mention + " will be kicked in 30 seconds. \nplease keep in mind that **your DMs should be ON** or else i won't be able 2 invite u back!")

        async with ctx.typing():
            await asyncio.sleep(15)
            await ctx.send(kicked.mention + " will be kicked in 15 seconds,,,")
            await asyncio.sleep(5)
            await ctx.send(kicked.mention + " will be kicked in 10 seconds,,,")
            await asyncio.sleep(5)
            await ctx.send(kicked.mention + " will be kicked in 5 seconds,,,")
            await asyncio.sleep(2)
            await ctx.send(kicked.mention + " will be kicked in 3 seconds,,,")
            await asyncio.sleep(2)
            await ctx.send(kicked.mention + " will be kicked in 1 second,,,")
            await asyncio.sleep(1)

        # sends invites and gets roles before kicking
        sent_invite = await send_invite(kicked, ctx.message.channel)
        user_to_roles[kicked.id] = kicked.roles


        # makes sure ppl know if sending the invite failed
        if await do_kick(kicked, ctx.channel) == True and sent_invite == False:
            await ctx.send("i couldn't DM the user the invite so someone. might want to check that out?")
        ROULETTE_ON = False


@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

bot.run("[SECRET TOKEN]")
