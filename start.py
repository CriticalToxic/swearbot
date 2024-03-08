from discord.ext import commands
from bot_db import Db
from typing import Optional
import discord
import config


jsonfile = "swearcount.json"

swearwords = ["fuck","shit","cunt","bitch","peenus","asshole","dick","peen","wanker","dickhead"]

intents=discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="$")

database = Db()



@bot.event
async def on_ready():
    for i in bot.guilds:
        print(f"Connected to {i.name}")


@bot.slash_command(
        name="ping",
        description="Pings the bot to test for latency"
)
async def ping(ctx):
    await ctx.respond(f"PONG! ({round(bot.latency*1000)}ms)")


@bot.event
async def on_message(message):
    try:
        database.add_user(message.author.id)
    except Exception as error:
        pass

    if len(message.content) > 0:
        if message.author.id != 1126881419566796882:
            database.increase_messages(message.author.id)

    for swear in swearwords:
        msg = message.content.lower()
        occurances = msg.count(swear)

        database.add_swear(message.author.id, swear, occurances)


@bot.slash_command(
        name="botinfo",
        description="Information for the bot."
)
async def botinfo(ctx):

    dev = await bot.fetch_user(206542052996022272)
    embed=discord.Embed()
    embed.add_field(name="ID", value=bot.user.id, inline=False)
    embed.add_field(name="Developer", value=dev.mention)
    await ctx.respond(embed=embed)




@bot.slash_command(
    name="swears",
    description="Gets a list of all swear words the bot currently tracks."
)
async def swears(ctx):
    stringswears = ""
    for word in swearwords:
        print(word)
        stringswears += f"\n{word}"

    await ctx.respond(f"Here is all the swears I currently track:```{stringswears}```")


@bot.slash_command(
    name="addswear",
    description="Add's a swear word to a users record."
)
async def addswear(ctx, user:discord.Member, swear:str, amount=1):
    userroles = [str(role.id) for role in ctx.author.roles]

    if user == None:
        user = ctx.author

    if str(config.memberroleid) in userroles or ctx.author.id == 206542052996022272:
        if swear.lower() in swearwords:
            database.add_swear(user.id, swear, amount)
            await ctx.respond(f"Made a record of {user.mention}'s foul mouth and using the word {swear}.")
        else:
            await ctx.respond(f"{swear} is not a word that I track.")
    else:
        await ctx.respond("Only TM Members can add a swear.")

@bot.slash_command(
    name="swearingprofile",
    description="Views a person stats"
)
async def swearingprofile(ctx, user:discord.Member):
    try:
        data = list(database.get_profile(user.id))
        data.pop(0)

        embed=discord.Embed(title=f"{user.display_name}'s profile", description=f"All information tracked about user {user.name}")
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="Messages Sent", value=data[0], inline=False)
        embed.set_footer(text=f"User ID: {user.id}")

        data.pop(0)

        for ind, word in enumerate(swearwords):
            embed.add_field(name=f"Swore ({word})", value=f"{data[ind]} time/s.", inline=True)

        await ctx.respond(embed=embed)
    except TypeError:
        await ctx.respond("This user does not have a profile since they have not spoke since the bot has been active.", ephemeral=True)

    

    

bot.run(config.token)     