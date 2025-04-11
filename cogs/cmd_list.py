import disnake as discord
import json

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum


class option(int, Enum):
    ignores = 1
    passings = 2
    wl = 3
    wluser = 4


class class_list(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Посмотреть лист
    @commands.slash_command(
        name="list", description="Lists of channels and bots | Списки каналов и ботов"
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def list(
        self,
        ctx,
        option: option = commands.Param(description="Select an option | Укажите опцию"),
    ):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if option is not None:
                if option:

                    # Считает кол-во ботов в белом списке в файле
                    with open('json/count_wlbots.json', 'r') as f:
                        ct = json.load(f)
                    count = ct["count_wlbots"]["count"]

                    # if count:
                    #     print(f"[ Проверка ]  Ботов в белом списке: {count}")
                    # else:
                    #     print("[ ОШИБКА ]  Ботов в белом списке не обнаружено!")

                    i = ignorebotsdata
                    wu = wluserdata
                    #                l = gdata('vega', 'logchannel')
                    ig = []
                    gwu = []
                    #                log = []
                    if ctx.guild.id in i:
                        if "rights" in i[ctx.guild.id]:
                            for bot in i[ctx.guild.id]['rights']:
                                try:
                                    b = self.client.get_user(int(bot))
                                    ig.append(b.mention)
                                except:
                                    pass
                    if ctx.guild.id in wu:
                        if "members" in wu[ctx.guild.id]:
                            for user in wu[ctx.guild.id]['members']:
                                try:
                                    d = self.client.get_user(int(user))
                                    gwu.append(d.mention)
                                except:
                                    pass
                    if option == 1:
                        try:
                            embed = discord.Embed(
                                title=f"{get_language(ctx.guild.id,'Игнорируемые боты:')}",
                                color=0x2F3136,
                            )
                            if len(ig) == 0:
                                embed.description = (
                                    f"{get_language(ctx.guild.id,'Боты отсутствуют')}"
                                )
                            else:
                                embed.description = ", ".join(
                                    ig
                                )  # если надо в столбик, то '\n'.join(ig)
                            await ctx.send(embed=embed)
                        except:
                            with open("ignored-bots.log", "w") as file:
                                file.write(", ".join(ig))
                            with open("ignored-bots.log", "rb") as file:
                                await ctx.send(
                                    f"{get_language(ctx.guild.id,'Игнорируемые боты:')}",
                                    file=discord.File(file, "ignored-bots.log"),
                                )
                    elif option == 2:
                        p = gdata("vega", "passbots")
                        try:
                            pass0 = p[str(ctx.guild.id)]
                            pass0 = pass0[0:-2]
                            try:
                                if len(pass0) == 0:
                                    embed = discord.Embed(
                                        title=f"{get_language(ctx.guild.id,'Пропуск есть у:')}",
                                        description=f"{get_language(ctx.guild.id,'Боты отсутствуют')}",
                                        color=0x2F3136,
                                    )
                                    await ctx.send(embed=embed)
                                else:
                                    embed = discord.Embed(
                                        title=f"{get_language(ctx.guild.id,'Пропуск есть у:')}",
                                        description=f"{pass0}.",
                                        color=0x2F3136,
                                    )
                                    await ctx.send(embed=embed)
                            except:
                                with open("pass-bots.log", "w") as file:
                                    file.write(f"{pass0}")
                                with open("pass-bots.log", "rb") as file:
                                    await ctx.send(
                                        f"{get_language(ctx.guild.id,'Пропуск есть у:')}",
                                        file=discord.File(file, "pass-bots.log"),
                                    )
                        except:
                            embed = discord.Embed(
                                title=f"{get_language(ctx.guild.id,'Пропуск есть у:')}",
                                description=f"{get_language(ctx.guild.id,'Боты отсутствуют')}",
                                color=0x2F3136,
                            )
                            await ctx.send(embed=embed)
                    elif option == 3:
                        embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'🤖 Ботов в белом списке:')} `{count}`",
                            description=f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915> Все боты из списка были проверены!')}\n\n\
                        [{get_language(ctx.guild.id,'🔗 Белый список ботов')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots')})",
                            color=0x2F3136,
                        )
                        await ctx.send(embed=embed)
                    elif option == 4:
                        try:
                            embed = discord.Embed(
                                title=f"{get_language(ctx.guild.id,'Участников в белом списке:')}",
                                color=0x2F3136,
                            )
                            if len(gwu) == 0:
                                if str(ctx.guild.id) in wu:
                                    embed.description = (
                                        f"{get_language(ctx.guild.id,'Участники отсутствуют')}\n{get_language(ctx.guild.id,'Идентификатор сервера есть в базе данных без пользователей! Просим вас написать команду `/reset wlusers`, для очистки данных.')}"
                                    )
                                else:
                                    embed.description = (
                                        f"{get_language(ctx.guild.id,'Участники отсутствуют')}\n{get_language(ctx.guild.id,'Идентификатора сервера нет в базе данных.')}"
                                    )
                            else:
                                embed.description = ", ".join(
                                    gwu
                                )  # если надо в столбик, то '\n'.join(gwu)
                            await ctx.send(embed=embed)
                        except:
                            with open("wlusers.log", "w") as file:
                                file.write(", ".join(gwu))
                            with open("wlusers.log", "rb") as file:
                                await ctx.send(
                                    f"{get_language(ctx.guild.id,'Участников в белом списке:')}",
                                    file=discord.File(file, "wlusers.log"),
                                )
            #            elif option.lower() == 'logchannel':
            #                embed = discord.Embed(title='Канал с логами:', color=0x2f3136)
            #                if len(log) == 0:
            #                    embed.description = 'Канал отсутствует'
            #                else:
            #                    embed.description = ', '.join(log) # если надо в столбик, то '\n'.join(log)
            #                    await ctx.send(embed=embed)
            #            elif option.lower() in ["members", "участников"]:
            #                for guild in bot.guilds:
            #                    for member in guild.members:
            #                        await ctx.send(member)
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию!')}",
                    color=0x8899A6,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Описание:')}",
                    value=f"{get_language(ctx.guild.id,'Данной командой можно посмотреть список ограниченных каналов, игнорируемых ботов, пропусков и количество ботов в белом списке.')}",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                    value=f"`channels`; `ignores`; `pass`; `wl`",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Пример:')}",
                    value=f"{ctx.prefix}list channels",
                    inline=False,
                )
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author}")
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_list(client))
