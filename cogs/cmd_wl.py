import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum


class option(int, Enum):
    add = 1
    remove = 2


class class_wl(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Занести или удалить бота из белого списка
    @commands.slash_command(
        name="wl",
        description="Whitelist management | Управление белым списком",
        guild_ids=[826022179568615445],
    )
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    #@commands.guild_permissions(826022179568615445, users={351020816466575372: True})
    async def wl(
        self,
        ctx,
        option: option = commands.Param(description="Select an option | Укажите опцию"),
        user: discord.User = commands.Param(
            description="Specify the user or his ID | Укажите пользователя или его ID"
        ),
        link = None,
        reason_bot = None,
    ):
        if ctx.author.id == 351020816466575372:
            if user.bot:
                if option == 1:
                    if user.public_flags.verified_bot:
                        if user.id in wlbotsdata[0]["Bots"]:
                            embed = discord.Embed(
                                description=f"<a:vega_x:810843492266803230> Бот **{user}** уже есть в списке!",
                                color=0xCC1A1D,
                            )
                            await ctx.send(embed=embed, delete_after=10.0)
                        else:
                            try:
                                w = wlbotsdata[0]["Bots"]
                            except KeyError:
                                w = []
                            w.append(user.id)
                            embed = discord.Embed(
                                description=f"<a:vega_check_mark:821700784927801394> Бот **{user}** занесен в белый список!",
                                color=0x43B581,
                            )

                            # Сохранение и редактирование кол-ва ботов в белом списке
                            with open('json/count_wlbots.json', 'r') as f:
                                ct = json.load(f)
                            count = ct["count_wlbots"]["count"]
                            counti = int(count) + 1
                            ct["count_wlbots"] = ({
                                "count": counti
                            })
                            with open('json/count_wlbots.json', 'w') as f:
                                json.dump(ct, f, indent=4)


                            wlbots.add(0, {"Bots": w})
                            await ctx.send(embed=embed)

                            if user.public_flags.verified_bot:
                                verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                            else:
                                verification_bot = f"{get_language(ctx.guild.id,'<:BOT:842444823604363324>')}"

                            embed = discord.Embed(
                                title="<a:vega_check_mark:821700784927801394> Whitelisted:",
                                description=f"[{user}]({link}) {verification_bot}\n\n`ID: {user.id}`",
                                color=0x43B581,
                            )
                            try:
                                embed.set_thumbnail(url=user.avatar.replace(size=1024))
                            except:
                                pass
                            await self.client.get_channel(837623697888116767).send(
                                embed=embed
                            )

                            if link:
                                reason = f"\n {link}"
                            else:
                                reason = ""

                            server = self.client.get_guild(909463311937056788)
                            await server.ban(user, reason=f"В белом списке!{reason}")

                            emb = discord.Embed(
                                title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Бан')}",
                                color=0xFF2B2B,
                            )
                            emb.add_field(
                                name=f"{get_language(ctx.guild.id,'Модератор:')}",
                                value=f"{ctx.author.mention}\n{ctx.author}",
                                inline=True,
                            )
                            emb.add_field(
                                name=f"{get_language(ctx.guild.id,'Нарушитель:')}",
                                value=f"{user.mention}\n{user}",
                                inline=True,
                            )
                            if reason != None:
                                emb.add_field(
                                    name=f"{get_language(ctx.guild.id,'Причина:')}",
                                    value=f"В белом списке!{reason}",
                                    inline=False,
                                )
                            emb.set_thumbnail(
                                url="https://cdn.discordapp.com/attachments/713751423128698950/810933957197037588/ban.png"
                            )
                            await self.client.get_channel(911205950176772137).send(
                                embed=emb
                            )
                    else:
                        embed = discord.Embed(
                            title=f":warning: Это неверифицированный бот!\n\n**ЗАПРЕЩЕНО:**\n— Добавлять данных ботов в белый список.", color=0xFCC21B
                        )
                        await ctx.send(embed=embed, ephemeral=True)

                elif option == 2:
                    if user.id in wlbotsdata[0]["Bots"]:
                        # Нужно исправить, он почему то удаляет все ид ботов, удаляет Bots
                        wlbots.delete(0, {"Bots": user.id})
                        newwl = wlbotsdata[0]["Bots"]
                        del newwl[user.id]
                        wlbots.add(0, {"Bots": newwl})

                        # Сохранение и редактирование кол-ва ботов в белом списке
                        with open('json/count_wlbots.json', 'r') as f:
                            ct = json.load(f)
                        count = ct["count_wlbots"]["count"]
                        counti = int(count) - 1
                        ct["count_wlbots"] = ({
                            "count": counti
                        })
                        with open('json/count_wlbots.json', 'w') as f:
                            json.dump(ct, f, indent=4)

                        embed = discord.Embed(
                            description=f":warning: Бот **{user}** удален из белого списка!",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed)

                        if user.public_flags.verified_bot:
                            verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                        else:
                            verification_bot = f"{get_language(ctx.guild.id,'<:BOT:842444823604363324>')}"

                        embed = discord.Embed(
                            title="<a:vega_x:810843492266803230> Removed from the white list:",
                            description=f"{user} {verification_bot}\n\n`ID: {user.id}`\n\n**Reason:**\n{reason_bot}",
                            color=0xCC1A1D,
                        )
                        try:
                            embed.set_thumbnail(url=user.avatar.replace(size=1024))
                        except:
                            pass
                        await self.client.get_channel(837623697888116767).send(
                            embed=embed
                        )

                        server = self.client.get_guild(909463311937056788)
                        await server.unban(user)
                        emb = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Разбан')}",
                            color=0x43B581,
                        )
                        emb.add_field(
                            name=f"{get_language(ctx.guild.id,'Модератор:')}",
                            value=f"{ctx.author.mention}\n{ctx.author}",
                            inline=True,
                        )
                        emb.add_field(
                            name=f"{get_language(ctx.guild.id,'Пользователь:')}",
                            value=f"{user.mention}\n{user}",
                            inline=True,
                        )
                        await self.client.get_channel(911205950176772137).send(
                            embed=emb
                        )
                    else:
                        embed = discord.Embed(
                            description=f"<a:vega_x:810843492266803230> Бот **{user}** не найден!",
                            color=0xCC1A1D,
                        )
                        await ctx.send(embed=embed, delete_after=10.0)
                else:
                    embed = discord.Embed(
                        title=f":warning: Неизвестная опция!", color=0xFCC21B
                    )
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                pass
        else:
            embed = discord.Embed(
                description=f"**{get_language(ctx.guild.id,'Команда только для РАЗРАБОТЧИКОВ!')}**",
                color=0xCC1A1D,
            )
            await ctx.send(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(class_wl(client))
