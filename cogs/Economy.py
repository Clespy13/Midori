import discord
import json
import random

from discord.ext import commands
from random import randint, choice

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trade_id = 0
        self.msg_member = None
        self.author = None
        self.offer_item = None
        self.against_item = None
        self.channel = None

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\balances.json", "r") as f:
            self.money = json.load(f)

    @commands.command()
    @cooldown(1, per_min=30, per_hour=1, type=commands.BucketType.user)
    async def work(self, ctx):
        author_id = str(ctx.message.author.id)
        amount = randint(23, 150)

        if not author_id in self.money:
            self.money[author_id] = {}
            self.money[author_id]["Kryska"] = 0

        self.money[author_id]["Kryska"] += amount

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\balances.json", "w") as f:
            json.dump(self.money, f, indent=4)

        await ctx.send(f"You have worked and gained {amount} Kryska!")

    @commands.command()
    @cooldown(1, per_hour=1, type=commands.BucketType.user)
    async def slut(self, ctx):
        author_id = str(ctx.message.author.id)
        amount = randint(50, 250)

        if not author_id in self.money:
            self.money[author_id] = {}
            self.money[author_id]["Kryska"] = 0

        self.money[author_id]["Kryska"] += amount

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\balances.json", "w") as f:
            json.dump(self.money, f, indent=4)

        await ctx.send(f"You have worked and gained {amount} Kryska!")

    @commands.command()
    @cooldown(1, per_hour=3, type=commands.BucketType.user)
    async def crime(self, ctx):
        author_id = str(ctx.message.author.id)
        amount = randint(100, 2000)
        win = randint(1, 2)

        if not author_id in self.money:
            self.money[author_id] = {}
            self.money[author_id]["Kryska"] = 0

        if win == 1:
            self.money[author_id]["Kryska"] += amount
            await ctx.send(f"You stole and gained {amount} Kryska!")
        else:
            self.money[author_id]["Kryska"] -= amount
            await ctx.send(f"You stole but got caught and had to pay {amount} Kryska!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\balances.json", "w") as f:
            json.dump(self.money, f, indent=4)

    @commands.command()
    @cooldown(1, per_hour=1, type=commands.BucketType.user)
    async def hourly(self, ctx):
        author_id = str(ctx.message.author.id)
        amount = randint(23, 250)

        if not author_id in self.money:
            self.money[author_id] = {}
            self.money[author_id]["Kryska"] = 0

        self.money[author_id]["Kryska"] += amount

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\balances.json", "w") as f:
            json.dump(self.money, f, indent=4)

        await ctx.send(f"Here is your hourly reward! {amount} Kryska!")

    @commands.command()
    @cooldown(1, per_hour=24, type=commands.BucketType.user)
    async def daily(self, ctx):
        author_id = str(ctx.message.author.id)
        amount = randint(85, 493)

        if not author_id in self.money:
            self.money[author_id] = {}
            self.money[author_id]["Kryska"] = 0

        self.money[author_id]["Kryska"] += amount

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\balances.json", "w") as f:
            json.dump(self.money, f, indent=4)

        await ctx.send(f"Here is your daily reward! {amount} Kryska!")

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        else:
            member = member

        member_id = str(member.id)

        if not member_id in self.money:
            await ctx.send("Member doesn't have an account!")
        else:
            bal = discord.Embed(
                color = 0xff0000,
                timestamp = ctx.message.created_at
            )

            bal.set_author(name=f"Balance - {member}", icon_url=self.bot.user.avatar_url)

            bal.add_field(name="Money", value=self.money[member_id]["Kryska"])

            await ctx.send(embed=bal)

    @commands.command()
    async def baltop(self, ctx):
        global author_id
        author_id = ctx.author.id

        leaderboard = sorted(self.money, key=lambda x : self.money[x].get('Kryska', 0), reverse=True)
        msg = ''
        for number, user in enumerate(leaderboard):
            msg += '{0}. <@!{1}> with {2} Kryska\n'.format(number +1, user, self.money[user].get('Kryska', 0))
            if number == 10:
                break
            else:
                number += 1

        await ctx.send(msg)

    @commands.command()
    async def shop(self, ctx):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\shop.json", "r") as f:
            shop = json.load(f)

        s = ""
        for i, item in enumerate(shop["Shop"]):
            name = item["name"]
            price = item["price"]
            desc = item["desc"]
            s += f"`{i + 1}` **{price} - {name}**\n{desc}\n\n"

        embed = discord.Embed(
            title = str(ctx.guild),
            description = f"{s}",
            color = 0x0000FF
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, *, item: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\shop.json", "r") as f:
            shop = json.load(f)
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "r") as f:
            inv = json.load(f)

        if not item:
            await ctx.send("Use the command as: `buy <name>`")
            return

        author_id = str(ctx.author.id)
        item = item.title()

        items = []
        for it in shop["Shop"]:
            name = it["name"]
            price = it["price"]
            type = it["type"]
            items += name, price, type

        if item in items:
            item_index = items.index(item)
            price_index = item_index + 1
            type_index = price_index + 1

            final_price = items[price_index]
            type = items[type_index]

            if int(final_price) < self.money[author_id]["Kryska"]:
                await ctx.send(f"You bought {item} for {final_price}!")
                self.money[author_id]["Kryska"] -= int(final_price)

                if not author_id in inv:
                    inv[author_id] = {}
                    inv[author_id]["Inventory"] = []

                inv[author_id]["Inventory"].append({
                    "name": item,
                    "type": type
                })

                with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\balances.json", "w") as f:
                    json.dump(self.money, f, indent=4)
                with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "w") as f:
                    json.dump(inv, f, indent=4)
                return
            else:
                await ctx.send("You do not have enough money to buy this item!")
                return
        else:
            await ctx.send("Item does not exist in the shop! To check the shop use the command `shop`")
            return

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "r") as f:
            inv = json.load(f)

        author_id = str(ctx.message.author.id)
        i = inv[author_id]["Inventory"]

        if not i:
            no_inv = discord.Embed(
                color = 0x87f542,
                description = "Nothing here"
            )
            no_inv.set_author(name="Inventory", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=no_inv)
            return

        inventorie = inv[author_id]["Inventory"]
        names = []
        for i in inventorie:
            name = i["name"]
            names.append(name)
        i = "\n - ".join(names)

        inventory = discord.Embed(
            color = 0x87f542
        )
        inventory.set_author(name="Inventory", icon_url=ctx.message.author.avatar_url)
        inventory.add_field(name="Your inventory:", value="- " + i)

        await ctx.send(embed=inventory)

    @commands.command()
    async def use(self, ctx, *, item: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "r") as f:
            inv = json.load(f)
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\shop.json", "r") as f:
            shop = json.load(f)

        if not item:
            await ctx.send("Specify an item to use!")
            return

        author_id = str(ctx.message.author.id)
        author = ctx.message.author
        item = item.title()

        inventory = inv[author_id]["Inventory"]

        names = []
        for i in inventory:
            name = i["name"]
            names.append(name)

        if item in names:

            items = []
            for it in inventory:
                name = it["name"]
                type = it["type"]
                items += name, type

            item_index = items.index(item)
            final_name = items[item_index]
            type_index = item_index + 1
            type = items[type_index]

            names = []
            for shop_items in shop["Shop"]:
                shop_name = shop_items["name"]
                shop_type = shop_items["type"]
                names += shop_name, shop_type

            if type == "Color":
                role = discord.utils.get(ctx.guild.roles, name=final_name)
                await author.add_roles(role)
            elif type == "Common Crate":
                item_choice = random.choice(names)
                if item_choice == "Color":
                    item_choice = random.choice(names)
                else:
                    print(item_choice)
                item_type_index = names.index(item_choice) + 1
                item_type = names[item_type_index]
                await ctx.send(f"You opened this common crate and got {item_choice}!")
                inventory.append({
                    "name": item_choice,
                    "type": item_type
                })
            elif type == "Epic Crate":
                item_choice = random.choice(names)
                if item_choice == "Color":
                    item_choice = random.choice(names)

                item_type_index = names.index(item_choice) + 1
                item_type = names[item_type_index]
                await ctx.send(f"You opened this epic crate and got {item_choice}!")
                inventory.append({
                    "name": item_choice,
                    "type": item_type
                })

            inventory.remove({
                "name": item,
                "type": type
            })

        else:
            await ctx.send("You don't have this item in your inventory")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "w") as f:
            json.dump(inv, f, indent=4)

    @commands.command()
    async def give(self, ctx, member: discord.Member=None, *, item: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "r") as f:
            inv = json.load(f)

        if not member:
            await ctx.send("Please Specify a user to give an item!")
            return
        if not item:
            await ctx.send("Please specify an item to give to that user!")
            return

        member_id = str(member.id)
        author_id = str(ctx.message.author.id)
        item = item.title()

        if not member_id in inv:
            inv[member_id] = {}
            inv[member_id]["Inventory"] = []
        if not author_id in inv:
            await ctx.send("You do not have items in your inventory to give to someone!")
            return

        items = []
        for it in inventory:
            name = it["name"]
            type = it["type"]
            items += name, type

        item_index = items.index(item)
        final_name = items[item_index]
        type_index = item_index + 1
        type = items[type_index]

        aut_inventory = inv[author_id]["Inventory"]
        mem_inventory = inv[member_id]["Inventory"]

        aut_inventory.remove({
            "name": final_name,
            "type": type
        })
        mem_inventory.append({
            "name": final_name,
            "type": type
        })

        await ctx.send(f"{ctx.message.author.mention} gave {member.mention} the {final_name} item!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "w") as f:
            json.dump(inv, f, indent=4)

    @commands.command()
    async def sell(self, ctx, *, item: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "r") as f:
            inv = json.load(f)
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\shop.json", "r") as f:
            shop = json.load(f)

        if not item:
            await ctx.send("Specify an item to sell!")
            return

        author_id = str(ctx.message.author.id)
        author = ctx.message.author
        item = item.title()

        inventory = inv[author_id]["Inventory"]

        item_names = []
        for it in shop["Shop"]:
            name = it["name"]
            price = it["price"]
            type = it["type"]
            item_names.append(name)
            item_names.append(price)
            item_names.append(type)

        if item not in item_names:
            await ctx.send("This item doesn't exist in the shop!")
            return
        item_index = item_names.index(item)
        final_name = item_names[item_index]
        item_price = item_names[item_index + 1]
        type = item_names[item_price + 1]
        final_price = int(item_price) - 100
        if final_name in inventory:
            inventory.remove({
                "name": final_name,
                "type": type
            })
            self.money[author_id]["Kryska"] += final_price
            await ctx.send(f"You sold {final_name} for {final_price}")
        else:
            await ctx.send("The item you chose to sell isn't in your inventory!")
            return

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "w") as f:
            json.dump(inv, f, indent=4)

    @commands.command()
    async def createguild(self, ctx, *, name: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
            guild = json.load(f)

        if not name:
            await ctx.send("Please specify a name for your guild!")
            return

        await ctx.send("Do you want to require an invite to join this guild ? (y/n)")
        content = "y" or "n"
        req_invite = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author)
        if req_invite.content == "y":
            invite_req = "yes"
        elif req_invite.content == "n":
            invite_req = "no"
        else:
            await ctx.send("Your answer doesn't match the required field!")
            return

        await ctx.send("Enter the guilds description")
        msg = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author)
        desc = msg.content

        author = str(ctx.message.author)
        guild_id = str(ctx.guild.id)

        if name in guild:
            await ctx.send("The Guild Name you asked for is already token, please choose another one!")
            return
        else:

            with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "w") as f:
                if guild_id not in guild:
                    guild[guild_id] = {}
                    guild[guild_id][name] = {}
                    guild[guild_id][name]["Invite required"] = invite_req
                    guild[guild_id][name]["Owner"] = author
                    guild[guild_id][name]["Description"] = desc
                    guild[guild_id][name]["Members"] = []
                    await ctx.send(f"Successfully created the guild {name}!")
                else:
                    guild[guild_id][name] = {}
                    guild[guild_id][name]["Invite required"] = invite_req
                    guild[guild_id][name]["Owner"] = author
                    guild[guild_id][name]["Description"] = desc
                    guild[guild_id][name]["Members"] = []
                    await ctx.send(f"Successfully created the guild {name}!")

                json.dump(guild, f, indent=4)

    @commands.command()
    async def deleteguild(self, ctx, *, name: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
            guild = json.load(f)

        guild_id = str(ctx.guild.id)

        if not name:
            await ctx.send("Please specify the name of the Guild to delete!")
            return
        if not name in guild[guild_id]:
            await ctx.send("This Guild does not exist!")
            return


        guild_owner = guild[guild_id][name]["Owner"]
        author = str(ctx.message.author)
        if guild_owner == author:
            guild[guild_id].pop(name)
            await ctx.send(f"Successfully deleted the guild {name}")
        else:
            await ctx.send("You are not the owner of this guild! Only the owner can delete this guild!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "w") as f:
            json.dump(guild, f, indent=4)

    @commands.command()
    async def leaveguild(self, ctx, *, name: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
            guild = json.load(f)

        if not name:
            await ctx.send("Please specify a guild to leave!")
            return

        guild_id = str(ctx.guild.id)

        guild_owner = guild[guild_id][name]["Owner"]
        author = str(ctx.message.author)
        if guild_owner == author:
            await ctx.send("You cannot leave this guild whilst you are the owner!")
            return
        else:
            guild[guild_id][name]["Members"].remove(author)
            await ctx.send(f"You left successfully the guild {name}!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "w") as f:
            json.dump(guild, f, indent=4)

    @commands.command()
    async def joinguild(self, ctx, *, name: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
            guild = json.load(f)
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\invites.json", "r") as f:
            invite = json.load(f)

        author = ctx.message.author
        author_id = str(author.id)

        if not name:
            await ctx.send("Please specify a guild to join!")
            return
        if author_id not in invite:
            invite[author_id] = {}
            invite[author_id]["Guilds"] = []

        guild_id = str(ctx.guild.id)

        if str(author) in guild[guild_id][name]["Members"]:
            await ctx.send("You are already in this guild!")
            return


        if guild[guild_id][name]["Invite required"] == "yes":
            if name in invite[author_id]["Guilds"]:
                guild[guild_id][name]["Members"].append(str(author))
                invite[author_id]["Guilds"].remove(name)
                await ctx.send(f"You successfully joined the guild {name}")
            else:
                await ctx.send("To join this guild, the owner of it needs to invite you!")
                return

        else:
            guild[guild_id][name]["Members"].append(str(author))
            await ctx.send(f"You successfully joined the guild {name}")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "w") as f:
            json.dump(guild, f, indent=4)
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\invites.json", "w") as f:
            json.dump(invite, f, indent=4)

    @commands.command()
    async def inviteguild(self, ctx, member: discord.Member=None, *, name: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
            guild = json.load(f)
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\invites.json", "r") as f:
            invite = json.load(f)

        guild_id = str(ctx.guild.id)

        if not member:
            await ctx.send("Please specify a member to invite to the guild!")
            return
        if not guild:
            await ctx.send("Please specify a guild to invite this member!")
            return
        if member in guild[guild_id][name]["Members"]:
            await ctx.send("This member is already in this guild!")
            return
        if guild[guild_id][name]["Invite required"] == "no":
            await ctx.send("You don't need to invite members for them to join this guild!")
            return

        member_id = str(member.id)
        guild_owner = guild[guild_id][name]["Owner"]
        author = str(ctx.message.author)

        if author == guild_owner:
            invite[member_id] = {}
            invite[member_id]["Guilds"] = []
            invite[member_id]["Guilds"].append(name)
            await ctx.send(f"Successfully invited {member.name} to the guild {name}!")
        else:
            await ctx.send("Only the guild owner can invite members!")

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\invites.json", "w") as f:
            json.dump(invite, f, indent=4)

    @commands.command()
    async def setguild(self, ctx, *, name: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
            guild = json.load(f)

        guild_id = str(ctx.guild.id)

        if not name:
            await ctx.send("Please specify the name of the guild to change the setting of!")
            return
        if name not in guild[guild_id][name]:
            await ctx.send("This guild does not exist!")
            return

        guild_owner = guild[guild_id][name]["Owner"]
        author = str(ctx.message.author)
        if author == guild_owner:
            await ctx.send(f"What do you want to change in your guild ? (description or invite requirement)")
            message = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author)
            option = message.content

            if option == "description":
                await ctx.send("What description do you wanna set for the guild ?\nCurrent description: " + guild[guild_id][name]["Description"])
                msg = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author)
                guild[guild_id][name]["Description"] = msg.content

                with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "w") as f:
                    json.dump(guild, f, indent=4)

                await ctx.send(f"Successfully set the guild {name}'s description to {msg.content}")

            elif option == "invite requirement":
                await ctx.send(f"Do you want an invite required to join the guild ? (y/n)\nCurrent status: " + guild[guild_id][name]["Invite required"])
                msg = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author)
                val = ""
                if msg.content == "y":
                    val = "yes"
                elif msg.content == "n":
                    val = "no"
                guild[guild_id][name]["Invite required"] = val

                with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "w") as f:
                    json.dump(guild, f, indent=4)

                await ctx.send(f"Successfully set the guild {name} invite requirement to {val}")

            else:
                await ctx.send("Option unknown")
                return
        else:
            await ctx.send("You are not the owner of this guild!")

    @commands.command()
    async def guildinfo(self, ctx, *, name: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
            guild = json.load(f)
        if not name:
            await ctx.send("Please specify the name of the guild you want to see info of!")
            return
        guild_id = str(ctx.guild.id)
        if name not in guild[guild_id]:
            await ctx.send("This guild does not exist!")
            return


        g = discord.Embed(
            color = 0xff0000
        )
        g.set_author(name="Guild Info")
        g.add_field(name="Name:", value=name)
        g.add_field(name="Invite requirement:", value=guild[guild_id][name]["Invite required"])
        g.add_field(name="Owner:", value=guild[guild_id][name]["Owner"])
        g.add_field(name="Description:", value=guild[guild_id][name]["Description"])
        g.add_field(name="Members:", value=len(guild[guild_id][name]["Members"]))

        await ctx.send(embed=g)

    @commands.command()
    async def guilds(self, ctx):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
            guild = json.load(f)

        guild_id = str(ctx.guild.id)
        name = []
        for g in guild[guild_id]:
            name.append(g)

        await ctx.send("Guilds: " + "\n".join(name))

    @commands.command()
    async def guildserver(self, ctx):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
            guild = json.load(f)

        guild_id = str(ctx.guild.id)

        await ctx.send(f'This server has {len(guild[guild_id])} guilds!\n')

    # @commands.command()
    # async def guildtop(self, ctx):
    #     with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\guilds.json", "r") as f:
    #         guild = json.load(f)
    #
    #     guild_id = str(ctx.guild.id)
    #     u = []
    #     for i in guild[guild_id]:
    #         g = guild[guild_id][i]["Members"]
    #         u.append(len(g))
    #
    #         index = u.index(len(g))
    #
    #         leaderboard = sorted(guild[guild_id], key=lambda x : u[index], reverse=True)
    #         msg = ''
    #         for number, user in enumerate(leaderboard):
    #             msg += '{0}. {1} with {2} members!\n'.format(number +1, user, u[index])
    #             if number == 10:
    #                 break
    #             else:
    #                 number += 1
    # EMBED
    #         await ctx.send(msg)


    @commands.command()
    async def createshop(self, ctx):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\usershops.json", "r") as f:
            s = json.load(f)

        author = str(ctx.author)
        guild_id = str(ctx.guild.id)

        if s:
            if author in s[guild_id]:
                await ctx.send("You already have a shop at your name. If you want to add an item to your shop use `!setshop <name> <price>`")
                return
        else:

            s[guild_id] = {}
            s[guild_id][author] = []

            await ctx.send("Successfully created your shop.")

            with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\usershops.json", "w") as f:
                json.dump(s, f, indent=4)

    @commands.command()
    async def setshop(self, ctx, item: str=None, *, price: int=0):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\usershops.json", "r") as f:
            s = json.load(f)
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "r") as f:
            inv = json.load(f)

        if not item:
            await ctx.send("Please specify an item to put on sell.")
            return
        if price == 0:
            await ctx.send("Please specify a price for your item on sell.")
            return

        author = str(ctx.author)
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)

        if not author_id in inv:
            await ctx.send("You do not have items in your inventory to put on sell!")
            return

        if s:
            if author not in s[guild_id]:
                await ctx.send("You don't have a shop at your name. If you want to create your shop use `!createshop`")
                return


        inventory = inv[author_id]["Inventory"]

        items = []
        for it in inventory:
            name = it["name"]
            type = it["type"]
            items += name, type

        if item not in items:
            await ctx.send("You do not have that item in your inventory to put on sell!")
            return

        item_index = items.index(item)
        final_name = items[item_index]
        type_index = item_index + 1
        type = items[type_index]

        inventory.remove({
            "name": final_name,
            "type": type
        })

        s[guild_id][author].append({
            "name": item,
            "price": str(price),
            "type": type
        })

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\usershops.json", "w") as f:
            json.dump(s, f, indent=4)
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "w") as f:
            json.dump(inv, f, indent=4)

        await ctx.send(f"Successfully added {item} for {price} to your shop")

    @commands.command()
    async def shopuser(self, ctx, member: discord.Member=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\usershops.json", "r") as f:
            s = json.load(f)

        if not member:
            await ctx.send("Please specify a member.")
            return

        member = str(member)
        guild_id = str(ctx.guild.id)

        if s:
            if member not in s[guild_id]:
                await ctx.send("This user doesn't have a shop.")
                return

        shopuser = ""
        for i, item in enumerate(s[guild_id][member]):
            name = item["name"]
            price = item["price"]
            shopuser += f"`{i + 1}` {name} for {price}\n\n"

        embed = discord.Embed(
            title = f"Shop of - {member} || {len(s[guild_id][member])} item for sale",
            description = f"{shopuser}",
            color = 0xffa826
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def buyuser(self, ctx, member: discord.Member=None, *, item: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\usershops.json", "r") as f:
            s = json.load(f)
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "r") as f:
            inv = json.load(f)

        if not member:
            await ctx.send("Please specify a member to buy that item from.")
            return
        if not item:
            await ctx.send("Please specify an item to buy from that user.")
            return

        m = member
        author = str(ctx.author)
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        member_id = str(member.id)
        member = str(member)

        items = []
        if s:
            if member not in s[guild_id]:
                await ctx.send("This user doesn't have a shop.")
                return

        for it in s[guild_id][member]:
            name = it["name"]
            price = it["price"]
            type = it["type"]
            items += name, price, type

        if item in items:
            item_index = items.index(item)
            price_index = item_index + 1
            type_index = price_index + 1

            final_price = items[price_index]
            type = items[type_index]

            if int(final_price) < self.money[author_id]["Kryska"]:
                await ctx.send(f"You bought {item} for {final_price}!")
                self.money[author_id]["Kryska"] -= int(final_price)
                self.money[member_id]["Kryska"] += int(final_price)

                if not author_id in inv:
                    inv[author_id] = {}
                    inv[author_id]["Inventory"] = []

                inv[author_id]["Inventory"].append({
                    "name": item,
                    "type": type
                })

                s[guild_id][member].remove({
                    "name": item,
                    "price": final_price,
                    "type": type
                })

                with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\balances.json", "w") as f:
                    json.dump(self.money, f, indent=4)
                with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "w") as f:
                    json.dump(inv, f, indent=4)
                with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\usershops.json", "w") as f:
                    json.dump(s, f, indent=4)
            else:
                await ctx.send("You do not have enough money to buy this item!")
        else:
            await ctx.send(f"Item does not exist in {m.name}'s shop! To check the users shop use the command `!shopuser <member>`")

    @commands.command()
    async def trade(self, ctx, member: discord.Member=None, *, item: str=None):
        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "r") as f:
            inv = json.load(f)

        if not member:
            await ctx.send("Please specify a member to trade that item from.")
            return
        if not item:
            await ctx.send("Please specify an item to trade with that user.")
            return


        m = member
        author = str(ctx.author)
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        member_id = str(member.id)
        member = str(member)

        if not member_id in inv:
            inv[member_id] = {}
            inv[member_id]["Inventory"] = []

        with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "w") as f:
            json.dump(inv, f, indent=4)

        mem_items = []
        aut_inventory = inv[author_id]["Inventory"]
        mem_inventory = inv[member_id]["Inventory"]
        aut_items = []

        for it in mem_inventory:
            name = it["name"]
            type = it["type"]
            mem_items += name, type

        for it in aut_inventory:
            name = it["name"]
            type = it["type"]
            aut_items += name, type

        if item in mem_items:
            await ctx.send(f"What item do you want to trade with {m.mention} for his {item}")
            msg = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author)
            trade = msg.content
            t = trade
            if trade in aut_items:
                await ctx.send("Waiting for member's response to the trade...")
                trade = discord.Embed(
                    color = 0x0d22df
                )
                trade.set_author(name=f"Trade | {author} - {member}")
                trade.add_field(name=f"{ctx.author.name}'s offer:", value=t, inline=True)
                trade.add_field(name=f"Against:", value=item + f" from {m.name}", inline=True)
                msg = await ctx.send(embed=trade, delete_after=60*60*24)
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")

                self.trade_id = msg.id
                self.msg_member = m
                self.author = ctx.author
                self.offer_item = t
                self.against_item = item
                self.channel = ctx.message.channel

                await m.send(f"{author} wants to trade with you in {ctx.guild}, you have 24 hours to accept it or reject it!")

            else:
                await ctx.send("You do not have this item in you're inventory.")
        else:
            await ctx.send(f"{m.mention} doesn't have this item in his inventory!")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.trade_id == reaction.message.id:
            if user == self.msg_member:
                if reaction.emoji == "✅":
                    with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "r") as f:
                        inv = json.load(f)

                    member_id = str(user.id)
                    author_id = str(self.author.id)
                    item = self.against_item
                    trade = self.offer_item

                    aut_inventory = inv[author_id]["Inventory"]
                    mem_inventory = inv[member_id]["Inventory"]
                    mem_items = []
                    aut_items = []

                    for it in mem_inventory:
                        name = it["name"]
                        type = it["type"]
                        mem_items += name, type

                    for it in aut_inventory:
                        name = it["name"]
                        type = it["type"]
                        aut_items += name, type

                    item_index = mem_items.index(item)
                    type_index = item_index + 1
                    mem_type = mem_items[type_index]

                    item_index = aut_items.index(trade)
                    type_index = item_index + 1
                    aut_type = aut_items[type_index]

                    mem_inventory.append({
                        "name": trade,
                        "type": aut_type
                    })

                    mem_inventory.remove({
                        "name": item,
                        "type": str(aut_type)
                    })

                    aut_inventory.append({
                        "name": item,
                        "type": mem_type
                    })

                    aut_inventory.remove({
                        "name": trade,
                        "type": mem_type
                    })

                    with open(r"C:\Users\fclem\Desktop\On The Code Again\cogs\inventories.json", "w") as f:
                        json.dump(inv, f, indent=4)

                    await self.channel.send("Successfully traded!")

                elif reaction.emoji == "❌":
                    await self.channel.send(f"{user} didn't accept the trade.")
        else:
            pass

def setup(bot):
    bot.add_cog(Economy(bot))
