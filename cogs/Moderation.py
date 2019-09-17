import discord
import json

from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["clear", "nuke"])
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount=5):
        msgs = await ctx.channel.purge(limit=amount + 1)
        message = await ctx.send(f"Cleaned {len(msgs) - 1} messages!", delete_after=4)

    @clean.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```You don't have the correct permissions! \nRequired Permissions: Manage Messages```")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            await ctx.send("Please specify a member to kick!")
        else:
            await member.kick(reason=reason)
            await ctx.send(f"{member} successfully kicked!")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```You don't have the correct permissions! \nRequired Permissions: Kick Members```")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, *, reason=None):
        if not member:
            await ctx.send("Please specify a member to ban!")
            return
        elif not reason:
            await ctx.send("Please specify a reason to ban this member!")
            return
        else:
            await member.ban(reason=reason)
            await ctx.send(f"{member} successfully banned!")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```You don't have the correct permissions! \nRequired Permissions: Ban Members```")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.name}#{user.discriminator} successfully!")
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```You don't have the correct permissions! \nRequired Permissions: Ban Members```")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member=None):
        if not member:
            await ctx.send("Please specify a member to mute!")
            return
        else:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.add_roles(role)
            await ctx.send(f"{member.mention} has been muted successfully!")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```You don't have the correct permissions! \nRequired Permissions: Manage Roles```")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member=None):
        if not member:
            await ctx.send("Please specify a member to unmute!")
            return
        else:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(role)
            await ctx.send(f"{member.mention} has been unmuted successfully!")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```You don't have the correct permissions! \nRequired Permissions: Manage Roles```")

    @commands.command()
    @commands.has_permissions(manage_server=True)
    async def warn(self, ctx, member: discord.Member=None, *, reason: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\warns.json", "r") as f:
            warns = json.load(f)

        if not member:
            await ctx.send("Please specify a member to warn!")
            return
        if not reason:
            await ctx.send("Please specify a reason to warn this member!")
            return

        member_id = str(member.id)

        if not member_id in warns:
            warns[member_id] = {}
            warns[member_id]["Reasons"] = []

        warns[member_id]["Reasons"].append(reason)
        await ctx.send(f"Successfully warned {member.name}!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\warns.json",'w+') as f:
            json.dump(warns, f, indent=4)

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```You don't have the correct permissions! \nRequired Permissions: Manage Server```")

    @commands.command(aliases=["warns"])
    async def warnings(self, ctx, member: discord.Member=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\warns.json", "r") as f:
            warns = json.load(f)

        member_id = str(member.id)

        if member_id in warns:
            await ctx.send(f"{member.name} has been warned {len(warns[member_id]['Reasons'])} times : {', '.join(warns[member_id]['Reasons'])}")
        else:
            await ctx.send(f"{member.name} has never been warned")

    @commands.command()
    @commands.has_permissions(manage_server=True)
    async def clearwarn(self, ctx, member: discord.Member=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\warns.json", "r") as f:
            warns = json.load(f)

        if not member:
            await ctx.send("Please specify a user!")
            return

        member_id = str(member.id)

        if member_id in warns:
            warns.pop(member_id)
            await ctx.send(f"Cleared {member.name}'s warnings successfully!")

        else:
            await ctx.send(f"{member.name} has never been warned!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\warns.json",'w+') as f:
            json.dump(warns, f, indent=4)


    @clearwarn.error
    async def clearwarn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```You don't have the correct permissions! \nRequired Permissions: Manage Server```")

def setup(bot):
    bot.add_cog(Moderation(bot))
