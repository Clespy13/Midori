import discord
import random
import json
import os
import asyncio

from discord.ext import commands, tasks
from discord.utils import get
from random import randint, choice

async def get_pre(bot, message):
    with open(r'C:\Users\fclem\Desktop\On The Code Again\Prefixes.json', "r") as f:
        data = json.load(f)
    try:
        prefix = data[str(message.guild.id)]['prefix']
        return prefix
    except Exception as e:
        return '!'

TOKEN = open(r"C:\Users\fclem\Desktop\On The Code Again\Token.txt", "r").read()
bot = commands.Bot(command_prefix = get_pre)

@bot.event
async def on_ready():
    #afk_check().start()
    await bot.change_presence(activity=discord.Game(name=f"On {len(bot.guilds)} Servers"))
    print("-----------------------------")
    print("Bot Name: " + bot.user.name)
    print("Bot ID: " + str(bot.user.id))
    print("Discord Version: " + discord.__version__ + "\n")
    print(f"On {len(bot.guilds)} Servers")
    print("Servers Connected To: ")

    for server in bot.guilds:
        name = str(server.name)
        id = str(server.id)
        members = str(server.member_count)
        owner = str(server.owner)
        print(f"-{name} {id} {members} members | Owner: {owner}".encode("utf-8"))
    print("-----------------------------")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command does not exist!")
    elif isinstance(error, commands.CommandOnCooldown):
        hour = 0
        if error.retry_after >= 3600:
            hour += 1
            rest = error.retry_after - 3600
            minute = 0
            while rest >= 60:
                minute += 1
                rest -= 60
                while minute >= 60:
                    hour += 1
                    minute -= 60
            if minute == 0:
                await ctx.send(f"You will be able to use that command again in {hour} hour!")
            else:
                await ctx.send(f"You will be able to use that command again in {hour} hour and {minute} minutes!")
    else:
        raise error

@bot.event
async def on_guild_join(guild):
    await bot.change_presence(activity=discord.Game(name=f"On {len(bot.guilds)} Servers"))
    with open(r"C:\Users\fclem\Desktop\On The Code Again\server_join.txt", "a", encoding="utf-8") as f:
        f.write(f"Joined Server: {guild.name}\nID: {guild.id}\nOwner: {guild.owner}\nNumber Of Members: {guild.member_count}\n\n")
        f.close()
    print("Joined New Server")

@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(activity=discord.Game(name=f"On {len(bot.guilds)} Servers"))
    with open(r"C:\Users\fclem\Desktop\On The Code Again\server_leave.txt", "a", encoding="utf-8") as f:
        f.write(f"Removed from: {guild.name}\nID: {guild.id}\nOwner: {guild.owner}\nNumber Of Members: {guild.member_count}\n\n")
        f.close()
    print("Removed From a Server")

@bot.command()
async def ping(ctx):
    await ctx.send(f":ping_pong: Pong!\n {round(bot.latency * 1000)}ms")

@bot.command()
async def roll(ctx):
    num = randint(1, 6)
    await ctx.send(f"You rolled a {num}!")

@bot.command()
async def coin(ctx):
    possibility = ["heads", "tales"]
    await ctx.send(f"The coin landed on {choice(possibility)}!")

@bot.command()
async def avatar(ctx, member: discord.User=None):
    if not member:
        member = ctx.message.author
    await ctx.send(f"Avatar of {member}: \n" + str(member.avatar_url))

@bot.command()
async def rps(ctx, choice: str=None):
    if not choice:
        await ctx.send("Please give a choice! (Rock, Paper or Scissors)")
        return

    choice.lower()
    choices = ["rock", "paper", "scissors"]
    computer = choices[randint(0, 2)]

    if choice == "rock":
        if computer == "paper":
            await ctx.send(f"You lost! (Your choice: {choice}, My choice: {computer})")
        elif computer == "rock":
            await ctx.send(f"It's a tie! (Your choice: {choice}, My choice: {computer})")
        else:
            await ctx.send(f"You won! (Your choice: {choice}, My choice: {computer})")
    elif choice == "paper":
        if computer == "scissors":
            await ctx.send(f"You lost! (Your choice: {choice}, My choice: {computer})")
        elif computer == "paper":
            await ctx.send(f"It's a tie! (Your choice: {choice}, My choice: {computer})")
        else:
            await ctx.send(f"You won! (Your choice: {choice}, My choice: {computer})")
    elif choice == "scissors":
        if computer == "rock":
            await ctx.send(f"You lost! (Your choice: {choice}, My choice: {computer})")
        elif computer == "scissors":
            await ctx.send(f"It's a tie! (Your choice: {choice}, My choice: {computer})")
        else:
            await ctx.send(f"You won! (Your choice: {choice}, My choice: {computer})")
    else:
        await ctx.send("Please give a valid choice! (Rock, Paper or Scissors)")

@bot.command()
async def info(ctx, member: discord.User=None):
    if not member:
        member = ctx.message.author

    roles = [role for role in member.roles]

    info = discord.Embed(
        color = 0x0339FC
    )
    info.set_author(name=f"Info Card - {member}")
    info.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
    info.set_thumbnail(url=member.avatar_url)

    info.add_field(name="Name:", value=member.name)
    info.add_field(name="Nickname:", value=member.nick, inline=True)
    info.add_field(name="ID:", value=member.id, inline=False)
    info.add_field(name="Status", value=member.status, inline=True)
    info.add_field(name="Created on:", value=member.created_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"), inline=True)
    info.add_field(name="Joined on:", value=member.joined_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"), inline=False)
    info.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=True)
    info.add_field(name="Top role:", value=member.top_role.mention, inline=True)
    info.add_field(name="Bot ?", value=member.bot)

    await ctx.send(embed=info)

@bot.command(aliases=["p"])
async def prefix(ctx):
    await ctx.send(f"Current prefix: {bot.command_prefix}")

@bot.command(aliases=["sp", "prefixset"])
@commands.has_permissions(manage_server=True)
async def setprefix(ctx, prefix: str=None):
    guild_id = str(ctx.guild.id)
    if not prefix:
        await ctx.send("Please select a new prefix to set!")
    if len(prefix) > 4:
        await ctx.channel.send(f'Prefix {prefix} is too long. Please choose a shorter one.')
        return

    with open(r'C:\Users\fclem\Desktop\On The Code Again\Prefixes.json', "r") as f:
        data = json.load(f)
        data[guild_id] = {}
        data[guild_id]["prefix"] = prefix
    with open(r"C:\Users\fclem\Desktop\On The Code Again\Prefixes.json", "w") as f:
        json.dump(data, f, indent=4)
    await ctx.send(f"Prefix set to {prefix}")

@setprefix.error
async def setprefix_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("```You don't have the correct permissions! \nRequired Permissions: Manage Server```")

@bot.command()
async def serverinfo(ctx):
    server = ctx.message.guild

    online = 0
    for i in server.members:
        if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
            online += 1
    all_users = []
    for user in server.members:
        all_users.append('{}#{}'.format(user.name, user.discriminator))
    all_users.sort()
    all = '\n'.join(all_users)

    tchannel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])
    vchannel_count = len([x for x in server.channels if type(x) == discord.channel.VoiceChannel])

    role_count = len(server.roles)
    emoji_count = len(server.emojis)

    em = discord.Embed(color=0xea7938)
    em.add_field(name='Name', value=server.name)
    em.add_field(name='Owner', value=server.owner, inline=False)
    em.add_field(name='Members', value=server.member_count)
    em.add_field(name='Currently Online', value=online)
    em.add_field(name='Text Channels', value=str(tchannel_count))
    em.add_field(name="Voice Channels", value=str(vchannel_count))
    em.add_field(name='Region', value=server.region)
    em.add_field(name='Verification Level', value=str(server.verification_level))
    em.add_field(name='Number of roles', value=str(role_count))
    em.add_field(name='Number of emotes', value=str(emoji_count))
    em.add_field(name='Created On', value=server.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
    em.set_thumbnail(url=server.icon_url)
    em.set_author(name='Server Info', icon_url=server.icon_url)
    em.set_footer(text='Server ID: %s' % server.id)
    await ctx.send(embed=em)

@bot.command()
async def suggest(ctx, *, suggestion: str=None):
    if not suggestion:
        await ctx.send("Great.. empty.. suggestion..")
        return

    author = ctx.message.author

    sug = discord.Embed(
        color = 0xfcf803
    )
    sug.set_author(name="|| Suggestion ||")
    sug.set_thumbnail(url="https://images-ext-1.discordapp.net/external/51D8UCM-w6zPu5i8knC-IG76A6SPkeroemt3_4tbeak/%3Fv%3D1/https/cdn.discordapp.com/emojis/442387680962019349.png")
    sug.set_footer(text=f"Suggested by {author}", icon_url=author.avatar_url)

    sug.add_field(name="Suggester", value=author.mention)
    sug.add_field(name="Suggestion", value=suggestion)

    channel = bot.get_channel(605721654752051200)
    msg = await channel.send(embed=sug)

    check = "✅"
    cross = "❌"

    await msg.add_reaction(check)
    await msg.add_reaction(cross)


#######GIVEAWAY##########
with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\giveaway.json", "r") as f:
    users = json.load(f)

@bot.command()
async def giveaway(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Giveaway")
    if role in ctx.author.roles:
        guild_id = str(ctx.guild.id)

        channel = ctx.message.channel
        author = ctx.message.author
        await channel.send("Ready for a new giveaway ? :tada:")

        content = "yes"
        msg = await bot.wait_for('message', check = lambda message: message.author == ctx.author)
        if msg.content == "yes":
            await channel.send('Great! What will be the gift for this giveaway ?')
            msg = await bot.wait_for("message", check = lambda message: message.author == ctx.author)
            gift = msg.content
            await channel.send(f"Are you sure about this gift ? Current gift: {gift}")
            content = "yes" or "no"
            comfirm = await bot.wait_for('message', check = lambda message: message.author == ctx.author)
            if comfirm.content == "yes":
                await ctx.send("Perfect! How long will the duration of the giveaway be ?\n(To specify seconds, minutes or hours use s, m or h)")
                time = await bot.wait_for("message", check = lambda message: message.author == ctx.author)
                timee = time.content
                if timee.endswith("s"):
                    time_value = "seconds"
                    time = timee[:-1]
                elif timee.endswith("m"):
                    time_value = "minutes"
                    time = timee[:-1]
                elif timee.endswith("h"):
                    time_value = "hours"
                    time = timee[:-1]
                await ctx.send(f"Are you sure for this duration time ? Current time set: {timee}")
                comfirm = await bot.wait_for('message', check = lambda message: message.author == ctx.author)
                content = "yes" or "no"
                if comfirm.content == "yes":
                    channel = discord.utils.get(bot.get_all_channels(), guild__name=f'{ctx.guild}', name='giveaways')
                    if channel:
                        channel_id = channel.id
                        await ctx.send(f"Perfect! The giveaway has started in <#{channel_id}>!")

                        tada = "🎉"

                        giveaway = discord.Embed(
                            title = f"{tada} Giveaway | " + gift + f" {tada}",
                            description = "React with :tada: to enter!",
                            color = 0xff0000,
                        )
                        giveaway.set_footer(text="Ends in " + timee + " " + time_value)
                        guild = ctx.guild


                        msg = await channel.send(embed=giveaway)

                        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\giveaway_id.txt", "w") as f:
                            f.write(str(msg.id))

                        guild_id = str(ctx.guild.id)

                        tada = "🎉"
                        await msg.add_reaction(tada)

                        time = int(time)
                        if time_value == "minutes":
                            time *= 60
                        elif time_value == "hours":
                            time *= 60*60
                        await asyncio.sleep(time)
                        await channel.send("Giveaway ended!")

                        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\giveaway.json", "w") as f:
                            if "591440336472244235" in users[guild_id]["Users"]:
                                users[guild_id]["Users"].remove("591440336472244235")
                                json.dump(users, f, indent=4)

                        if not users[guild_id]["Users"]:
                            await channel.send("No human user joined this giveaway!")
                            return
                        else:
                            winner = choice(users[guild_id]["Users"])

                        winner = bot.get_user(int(winner))
                        await channel.send(f"Congratulations {winner.mention}! You have won {gift}")

                        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\giveaway.json", "w") as f:
                            list = users[guild_id]["Users"]
                            list.clear()
                            del list[:]
                            json.dump(users, f, indent=4)
                    else:
                        await ctx.send("The giveaway couldn't be created! `giveaways` channel does not exist!")
                        return

                elif comfirm.content == "no":
                    await ctx.send("Canceling giveaway... :disappointed_relieved:")

            elif comfirm.content == "no":
                await ctx.send("Canceling giveaway... :disappointed_relieved:")
        else:
            await ctx.send("Canceling giveaway... :disappointed_relieved:")
    else:
        await ctx.send("```You don't have the correct role! \nRequired Role: Giveaway```")

@bot.event
async def on_raw_reaction_add(payload):
    guild_id = str(payload.guild_id)
    with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\giveaway_id.txt", "r") as f:
        giveaway_id = f.read()
    if int(giveaway_id) == payload.message_id:

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\giveaway.json", "w") as f:
            if guild_id not in users:
                users[guild_id] = {}
                users[guild_id]["Users"] = []
            else:
                users[guild_id]["Users"].append(str(payload.user_id))

                json.dump(users, f, indent=4)

@bot.command()
async def invitelink(ctx):
    await ctx.send("https://discordapp.com/api/oauth2/authorize?client_id=591440336472244235&permissions=8&scope=bot")

for filename in os.listdir(r"C:\Users\fclem\Desktop\On The Code Again\cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)
