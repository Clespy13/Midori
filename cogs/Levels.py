import discord
import json

from discord.ext import commands

with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\Rank Levels.json", encoding='utf-8') as f:
  try:
    xp = json.load(f)
    xp = {}
    xp['Ranks'] = []
  except ValueError:
    xp = {}
    xp['Ranks'] = []

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open(r'C:\Users\fclem\Desktop\On The Code Again\cogs\users.json', "r") as f:
            self.users = json.load(f)

    def lvl_up(self, author_id):
        cur_xp = self.users[author_id]["xp"]
        cur_lvl = self.users[author_id]["level"]

        if cur_xp >= round((4 * (cur_lvl ** 3)) / 5):
            self.users[author_id]["level"] += 1
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        global author_id
        author_id = str(message.author.id)

        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]["level"] = 1
            self.users[author_id]["xp"] = 0

        self.users[author_id]["xp"] += 1

        if self.lvl_up(author_id):
            await message.channel.send(f"{message.author.mention} is now level {self.users[author_id]['level']}!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\users.json", "w") as f:
            json.dump(self.users, f, indent=4)

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\Rank Levels.json", "r") as f:
            xp = json.load(f)

        cur_xp = self.users[author_id]["xp"]
        for exp in xp["Ranks"]:
            if str(cur_xp) >= exp["req_xp"]:
                role = discord.utils.get(message.guild.roles, name=exp["role"])
                if role in message.author.roles:
                    pass
                else:
                    await message.author.add_roles(role)
                    await message.channel.send(f"{message.author.mention} is now an {exp['role']} member!")
                break
        else:
            return

    # @commands.command()
    # async def addranklevel(self, ctx, role: str=None, *, req_xp: int=0):
    #     with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\Rank Levels.json", "r") as f:
    #         xp = json.load(f)
    #
    #     if not role:
    #         await ctx.send("Please specify a role to attribute when someone will reach this level!")
    #         return
    #     if not req_xp:
    #         await ctx.send("Please specify the required experience to obtain this role!")
    #         return
    #
    #     for exp in xp["Ranks"]:
    #         if exp["role"] == role:
    #             print("already in")
    #             break
    #     else:
    #         xp["Ranks"].append({
    #             "role": role,
    #             "req_xp": str(req_xp)
    #         })
    #         await ctx.send(f"Successfully added {role} level rank!")
    #
    #     with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\Rank Levels.json", "w") as f:
    #         json.dump(xp, f, indent=4)
    #
    # @commands.command()
    # async def delranklevel(self, ctx, *, role: str=None):
    #     with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\Rank Levels.json", "r") as f:
    #         xp = json.load(f)
    #
    #     if not role:
    #         await ctx.send("Please specify a role to delete from the Rank Levels")
    #         return
    #
    #     for exp in xp["Ranks"]:
    #         if role == exp["role"]:
    #             exp.pop("role")
    #             exp.pop("req_xp")
    #             # exp.pop("{}")
    #             await ctx.send(f"Successfully removed {role} level rank!")
    #             break
    #     else:
    #         await ctx.send("Role doesn't exist in level ranks! (To see the level ranks, use !lvlranks)")
    #
    #     with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\Rank Levels.json", "w") as f:
    #         json.dump(xp, f, indent=4)

    @commands.command()
    async def lvlranks(self, ctx):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\Rank Levels.json", "r") as f:
            xp = json.load(f)

        for exp in xp["Ranks"]:
                leaderboard = sorted(exp, key=lambda x : exp[x].get('role', 0), reverse=True)
                msg = ''
                for number, user in enumerate(leaderboard):
                    msg += '{0}. {1} with {2} xp\n'.format(number +1, user, exp[user].get('role', 0))
                    if number == 10:
                        break
                    else:
                        number += 1
        await ctx.send(f"Here are the level ranks existing: " + msg)

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        else:
            member = member

        member_id = str(member.id)

        if not member_id in self.users:
            await ctx.send("Member doesn't have a level!")
        else:
            level = discord.Embed(
                color = 0xff0000,
                timestamp = ctx.message.created_at
            )

            level.set_author(name=f"Level - {member}", icon_url=self.bot.user.avatar_url)
            level.set_footer(text="By Nashie and Clespy")

            level.add_field(name="Level", value=self.users[member_id]["level"])
            level.add_field(name="XP", value=self.users[member_id]["xp"])

            await ctx.send(embed=level)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlevel(self, ctx, member: discord.Member = None, *, a: int):
        if not member:
            await ctx.send("Please specify a member!")
            return

        member_id = str(member.id)

        self.users[member_id]["level"] = a
        await ctx.send(f"{member.name} has successfully a level of {a}!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\users.json", "w") as f:
            json.dump(self.users, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setxp(self, ctx, member: discord.Member = None, *, a: int):
        if not member:
            await ctx.send("Please specify a member!")
            return

        member_id = str(member.id)

        self.users[member_id]["xp"] = a
        await ctx.send(f"{member.name} has successfully an xp of {a}!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\users.json", "w") as f:
            json.dump(self.users, f, indent=4)

    @commands.command()
    async def lvltop(self, ctx):
        global author_id
        author_id = ctx.message.author.id

        leaderboard = sorted(self.users, key=lambda x : self.users[x].get('xp', 0), reverse=True)
        msg = ''
        for number, user in enumerate(leaderboard):
            msg += '{0}. <@!{1}> with {2} xp\n'.format(number +1, user, self.users[user].get('xp', 0))
            if number == 10:
                break
            else:
                number += 1

        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Levels(bot))
