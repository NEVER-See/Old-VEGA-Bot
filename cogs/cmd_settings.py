import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *

prefix = "/"


class class_settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Посмотреть настройки бота
    @commands.slash_command(
        name="settings",
        description="Bot settings | Настройки бота",
        case_insensitive=True,
    )
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def settings(self, ctx):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            try:
                enabled = languagedata[ctx.guild.id]["language"]
            except KeyError:
                enabled = False
            if enabled:
                slang = "Русский"
            else:
                slang = "English"

            try:
                enabled = antibotdata[ctx.guild.id]["enabled"]
            except KeyError:
                enabled = False
            if enabled:
                abon = "<a:on:863478700891963402>"
            else:
                abon = "<a:off:863478700845694987>"

            try:
                enabled = hard_antibotdata[ctx.guild.id]["enabled"]
            except KeyError:
                enabled = False
            if enabled:
                habon = "<a:on:863478700891963402>"
            else:
                habon = "<a:off:863478700845694987>"

            try:
                enabled = user_anticrashdata[ctx.guild.id]["enabled"]
            except KeyError:
                enabled = False
            if enabled:
                uaon = "<a:on:863478700891963402>"
            else:
                uaon = "<a:off:863478700845694987>"

            try:
                enabled = editserverdata[ctx.guild.id]["enabled"]
            except KeyError:
                enabled = False
            if enabled:
                eson = "<a:on:863478700891963402>"
                eson2 = "<a:vega_x:826158328610291802>"
            else:
                eson = "<a:off:863478700845694987>"
                eson2 = "<a:vega_check_mark:826158327968694333>"

            # amsg = gdata("vega", "antimsg")
            # try:
            #     enabled = amsg[str(ctx.guild.id)]
            # except KeyError:
            #     enabled = False
            # if enabled:
            #     amsg0 = "<a:on:863478700891963402>"
            # else:
            amsg0 = "<a:off:863478700845694987>"

            # ai = gdata("vega", "antiinvite")
            # try:
            #     enabled = ai[str(ctx.guild.id)]
            # except KeyError:
            #     enabled = False
            # if enabled:
            #     aion = "<a:on:863478700891963402>"
            # else:
            aion = "<a:off:863478700845694987>"

            w = logchanneldata
            try:
                l = self.client.get_channel(int(w[ctx.guild.id]["logchannel"]))
                if ctx.guild.id in w:
                    logch = f"{l.mention}"
                else:
                    logch = "`None`"
            except:
                logch = "`None`"

            """mr = gdata("vega", "muterole")
            try:
                c = ctx.guild.get_role(int(mr[str(ctx.guild.id)]))
                if str(ctx.guild.id) in mr and c:
                    muter = f"{c.mention}"
                else:
                    muter = "`None`"
            except:
                muter = "`None`"
            """
            embed = discord.Embed(
                title=f"{get_language(ctx.guild.id,'🔧 Настройки бота')}",
                description=f"{get_language(ctx.guild.id,'**🔎 Префикс:**')}  `{prefix}`    <:language:863473448771387402> {get_language(ctx.guild.id,'**Язык:**')} `{slang}`\n\n{get_language(ctx.guild.id,'**📃 Логи:**')} {logch}\nㅤ",
                color=0x202225,
            )
            """embed.add_field(
                name=f"{get_language(ctx.guild.id,'Каналы & Роли:')}",
                value=f"{get_language(ctx.guild.id,'**📃 Логи:**')} {logch}",
                inline=True,
            )"""
            """\n\n<:muted:842447248277241867> {get_language(ctx.guild.id,'**Роль мьюта:**')} {muter}ㅤ"""
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'Выключатели:')}",
                value=f"{abon} **AntiBot**\n\n{habon} **HARD-AntiBot**\n\n{uaon} **AntiCrash**",
                inline=True,
            )
            embed.add_field(
                name=f"ㅤ",
                value=f"{eson} {get_language(ctx.guild.id,'**Редактирование сервера**')} {eson2}\n\n{amsg0} **AntiMSGBot**\n\n{aion} {get_language(ctx.guild.id,'**Анти приглашение**')}",
                inline=True,
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(class_settings(client))
