import discord
import json
import asyncio

from discord.ext import commands

afk_list = []

async def afk_check(bot):
    await bot.wait_until_ready()
    with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\afk.json", "r") as f:
        afk = json.load(f)
    # print(bot.guilds)
    # print(afk[guild_id])
        # while not bot.is_closed():
        #     if afk["afk"] in afk_list:
        #         afk_list.append(afk["afk"])
        #         print(afk_list)
        #         await asyncio.sleep(1)
        #         print("aa")
        #     else:
        #         print(afk_list)
        #         print("uu")
        #         pass

class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def afk(self, ctx, msg=None):
        author = str(ctx.message.author)
        author_id = str(ctx.message.author.id)
        guild_id = str(ctx.guild.id)

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\afk.json", "r") as f:
            afk = json.load(f)

        message = str(msg)

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\afk.json", "w") as f:
            if guild_id not in afk:
                afk[guild_id] = {}
                afk[guild_id][author] = {}
                afk[guild_id][author]["Reason"] = message
            else:
                afk[guild_id][author] = {}
                afk[guild_id][author]["Reason"] = message
            json.dump(afk, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        mentioned = message.mentions
        author = str(message.author)
        aut = message.author

        # print(afk_list)

        af = []
        for a in afk_list:
            print(a)
            for i in a:
                print(i)
                af.append(i)
        # print(af)
        if author in af:
            print("aa")
            afk_user = af.index(author)
            af.pop(afk_user)

            with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\afk.json", "r") as f:
                afk = json.load(f)

                u = aut.name + "#" + aut.discriminator

                afk["afk"].pop(str(u))

                with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\afk.json", "w") as f:
                    json.dump(afk, f, indent=4)

                channel = message.channel
                await channel.send(f"You are no longer AFK.")

        for user in mentioned:
            afk = []
            for a in afk_list:
                for i in a:
                    afk.append(i)

            if str(user) in afk:
                channel = message.channel
                await channel.send(f"User is currently AFK.")

def setup(bot):
    bot.loop.create_task(afk_check(bot))
    bot.add_cog(Afk(bot))
