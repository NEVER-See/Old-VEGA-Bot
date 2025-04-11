import disnake as discord
import typing

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum

prefix = "/"


class option(int, Enum):
    all = 1
    delbots = 2


class class_checkwl(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Проверить бота в белом списке
    @commands.slash_command(
        name="checkwl",
        description="Checking bots in the ignored and whitelisted list | Проверка ботов в игнорируемом и белом списке",
    )
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def checkwl(
        self,
        inter,
        bot: typing.Optional[discord.User] = None,
        option: option = commands.Param(description="Select an option | Укажите опцию")
        == None,
    ):
        ctx = inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if bot or option:
                try:
                    if ctx.channel.id == 826326189324763166:
                        if ctx.author.id in config["owner_ids"]:
                            if bot:
                                if bot.bot:
                                    w = gdata("vega", "wlbots")
                                    if str(bot.id) in w[str("Bots")]:
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{bot}** {get_language(ctx.guild.id,'есть в белом списке!')}\n\n{get_language(ctx.guild.id,':warning: **Внимание!**')}\n{get_language(ctx.guild.id,'Данного бота невозможно занести в игнорируемый список!')}\n\n**[{get_language(ctx.guild.id,'Проверить бота')}](https://discord.com/api/oauth2/authorize?client_id={bot.id}&permissions=8&scope=&scope=bot%20applications.commands)**",
                                            color=0x43B581,
                                        )
                                        if bot.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                        if bot.public_flags.verified_bot:
                                            verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if bot.public_flags.spammer:
                                            spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        if bot.avatar != None:
                                            embed.set_thumbnail(
                                                url=bot.avatar.replace(
                                                    size=1024, format="png"
                                                )
                                            )
                                        embed.set_footer(text=f"ID: {bot.id}")
                                        await ctx.send(embed=embed)
                                    else:
                                        data = gdata("vega", "antibot")
                                        try:
                                            enabled = data[str(ctx.guild.id)]
                                        except KeyError:
                                            enabled = False
                                        if bot:
                                            if enabled:
                                                wl = gdata("vega", "ignorebots")
                                                try:
                                                    enabled = False
                                                    if str(ctx.guild.id) in wl:
                                                        dop = wl[str(ctx.guild.id)]
                                                    else:
                                                        dop = ""
                                                except KeyError:
                                                    print(
                                                        "[ ОШИБКА ] Произошла неизвестная ошибка!"
                                                    )
                                                    pass
                                                if str(bot.id) in dop:
                                                    embed = discord.Embed(
                                                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бота')} **{bot}** {get_language(ctx.guild.id,'нет в белом списке!')}\n\n**[{get_language(ctx.guild.id,'Проверить бота')}](https://discord.com/api/oauth2/authorize?client_id={bot.id}&permissions=8&scope=&scope=bot%20applications.commands)**",
                                                        color=0xCC1A1D,
                                                    )
                                                    embed.add_field(
                                                        name=f"{get_language(ctx.guild.id,':warning: Внимание!')}",
                                                        value=f"**{bot}** {get_language(ctx.guild.id,'игнорируется на данном сервере!')}",
                                                        inline=False,
                                                    )
                                                    if bot.public_flags.http_interactions_bot:
                                                        http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                                    else:
                                                        http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                                    if bot.public_flags.verified_bot:
                                                        verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                    else:
                                                        verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                    if bot.public_flags.spammer:
                                                        spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                    else:
                                                        spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                    embed.add_field(
                                                        name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                                        value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                                        inline=False,
                                                    )
                                                    if bot.avatar != None:
                                                        embed.set_thumbnail(
                                                            url=bot.avatar.replace(
                                                                size=1024, format="png"
                                                            )
                                                        )
                                                    embed.set_footer(text=f"ID: {bot.id}")
                                                    await ctx.send(embed=embed)
                                                else:
                                                    embed = discord.Embed(
                                                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бота')} **{bot}** {get_language(ctx.guild.id,'нет в белом списке!')}\n\n**[{get_language(ctx.guild.id,'Проверить бота')}](https://discord.com/api/oauth2/authorize?client_id={bot.id}&permissions=8&scope=&scope=bot%20applications.commands)**",
                                                        color=0xCC1A1D,
                                                    )
                                                    embed.add_field(
                                                        name=f"{get_language(ctx.guild.id,':warning: Внимание!')}",
                                                        value=f"**{bot}** {get_language(ctx.guild.id,'может быть забанен функцией **AntiBot**!')}\n{get_language(ctx.guild.id,'Воспользуйтесь командой')} `{prefix}ignore add {bot.id}`, {get_language(ctx.guild.id,'чтобы занести бота в игнорируемый список.')}\n\n{get_language(ctx.guild.id,'Если хотите пропустить бота на сервер, не добавляя его в игнорируемый список, то выдайте ему пропуск командой:')} `{prefix}pass add {bot.id}`",
                                                        inline=False,
                                                    )
                                                    if bot.public_flags.http_interactions_bot:
                                                        http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                                    else:
                                                        http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                                    if bot.public_flags.verified_bot:
                                                        verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                    else:
                                                        verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                    if bot.public_flags.spammer:
                                                        spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                    else:
                                                        spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                    embed.add_field(
                                                        name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                                        value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                                        inline=False,
                                                    )
                                                    if bot.avatar != None:
                                                        embed.set_thumbnail(
                                                            url=bot.avatar.replace(
                                                                size=1024, format="png"
                                                            )
                                                        )
                                                    embed.set_footer(text=f"ID: {bot.id}")
                                                    await ctx.send(embed=embed)
                                            else:
                                                wl = gdata("vega", "ignorebots")
                                                try:
                                                    enabled = False
                                                    if str(ctx.guild.id) in wl:
                                                        dop = wl[str(ctx.guild.id)]
                                                    else:
                                                        dop = ""
                                                except KeyError:
                                                    print(
                                                        "[ ОШИБКА ] Произошла неизвестная ошибка!"
                                                    )
                                                    pass
                                                if str(bot.id) in dop:
                                                    embed = discord.Embed(
                                                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бота')} **{bot}** {get_language(ctx.guild.id,'нет в белом списке!')}\n\n**[{get_language(ctx.guild.id,'Проверить бота')}](https://discord.com/api/oauth2/authorize?client_id={bot.id}&permissions=8&scope=&scope=bot%20applications.commands)**",
                                                        color=0xCC1A1D,
                                                    )
                                                    embed.add_field(
                                                        name=f"{get_language(ctx.guild.id,':warning: Внимание!')}",
                                                        value=f"**{bot}** {get_language(ctx.guild.id,'игнорируется на данном сервере!')}",
                                                        inline=False,
                                                    )
                                                    if bot.public_flags.http_interactions_bot:
                                                        http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                                    else:
                                                        http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                                    if bot.public_flags.verified_bot:
                                                        verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                    else:
                                                        verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                    if bot.public_flags.spammer:
                                                        spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                    else:
                                                        spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                    embed.add_field(
                                                        name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                                        value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                                        inline=False,
                                                    )
                                                    if bot.avatar != None:
                                                        embed.set_thumbnail(
                                                            url=bot.avatar.replace(
                                                                size=1024, format="png"
                                                            )
                                                        )
                                                    embed.set_footer(text=f"ID: {bot.id}")
                                                    await ctx.send(embed=embed)
                                                else:
                                                    embed = discord.Embed(
                                                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бота')} **{bot}** {get_language(ctx.guild.id,'нет в белом списке!')}\n\n**[{get_language(ctx.guild.id,'Проверить бота')}](https://discord.com/api/oauth2/authorize?client_id={bot.id}&permissions=8&scope=&scope=bot%20applications.commands)**",
                                                        color=0xCC1A1D,
                                                    )
                                                    embed.add_field(
                                                        name=f"{get_language(ctx.guild.id,':warning: Внимание!')}",
                                                        value=f"**{bot}** {get_language(ctx.guild.id,'не игнорируется на данном сервере!')}\n{get_language(ctx.guild.id,'Воспользуйтесь командой')} `{prefix}ignore add {bot.id}`, {get_language(ctx.guild.id,'чтобы занести бота в игнорируемый список.')}",
                                                        inline=False,
                                                    )
                                                    if bot.public_flags.http_interactions_bot:
                                                        http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                                    else:
                                                        http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                                    if bot.public_flags.verified_bot:
                                                        verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                    else:
                                                        verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                    if bot.public_flags.spammer:
                                                        spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                    else:
                                                        spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                    embed.add_field(
                                                        name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                                        value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                                        inline=False,
                                                    )
                                                    if bot.avatar != None:
                                                        embed.set_thumbnail(
                                                            url=bot.avatar.replace(
                                                                size=1024, format="png"
                                                            )
                                                        )
                                                    embed.set_footer(text=f"ID: {bot.id}")
                                                    await ctx.send(embed=embed)
                                else:
                                    embed = discord.Embed(
                                        description=f"<a:vega_x:810843492266803230> **{bot.id}** {get_language(ctx.guild.id,'не является ботом!')}",
                                        color=0xCC1A1D,
                                    )
                                    await ctx.send(embed=embed, delete_after=12.0)

                            elif option:
                                if option == 2:
                                    w = gdata("vega", "wlbots")
                                    ig = []
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется проверка ботов...')}",
                                        color=0xF4900C,
                                    )
                                    await ctx.send(embed=embed)
                                    for ban_entry in [m async for m in self.client.get_guild(909463311937056788).bans()]:
                                        user = ban_entry.user
                                        if (
                                            user.bot
                                            and user.name.startswith("Deleted User")
                                            and str(user.id) in w[str("Bots")]
                                            or not user.public_flags.verified_bot
                                        ):
                                            ig.append(user.id)

                                    embed = discord.Embed(
                                        title=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Проверка завершена!')}",
                                        color=0x43B581,
                                    )
                                    if len(ig) == 0:
                                        embed.description = f"{get_language(ctx.guild.id,'Все боты были проверены.')}"
                                    else:
                                        embed.description = f"{get_language(ctx.guild.id,'Аппликации данных ботов возможно удалены!')}\n{get_language(ctx.guild.id,'Воспользуйтесь командой')} `{prefix}wl remove {get_language(ctx.guild.id,'@пользователь')}`, {get_language(ctx.guild.id,'чтобы удалить бота из белого списка.')}"
                                        embed.add_field(
                                            name="Боты:",
                                            value=", ".join(map(str, ig)),
                                            inline=False,
                                        )
                                    await ctx.edit_original_message(embed=embed)

                                elif option == 1:
                                    w = gdata("vega", "wlbots")
                                    wl = gdata("vega", "ignorebots")
                                    ig = []
                                    try:
                                        enabled = False
                                        if str(ctx.guild.id) in wl:
                                            dop = wl[str(ctx.guild.id)]
                                        else:
                                            dop = ""
                                    except KeyError:
                                        print(
                                            "[ ОШИБКА ] Произошла неизвестная ошибка!"
                                        )
                                        pass
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется проверка ботов...')}",
                                        color=0xF4900C,
                                    )
                                    await ctx.send(embed=embed)
                                    for member in [
                                        m for m in ctx.guild.members if m.bot
                                    ]:
                                        if (
                                            not str(member.id) in w[str("Bots")]
                                            and not str(member.id) in dop
                                        ):
                                            ig.append(member.mention)
                                    bot1 = len(
                                        [m for m in ctx.guild.members if m.bot]
                                    )
                                    if bot1 > 1:
                                        # if member in [m for m in ctx.guild.members if m.bot and m != ctx.guild.me]:
                                        embed = discord.Embed(
                                            title=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Проверка завершена!')}",
                                            color=0x43B581,
                                        )
                                        if len(ig) == 0:
                                            embed.description = f"{get_language(ctx.guild.id,'Все боты были проверены.')}"
                                        else:
                                            data = gdata("vega", "antibot")
                                            try:
                                                enabled = data[str(member.guild.id)]
                                            except KeyError:
                                                enabled = False
                                            if member.bot:
                                                if enabled:
                                                    embed.description = f"{get_language(ctx.guild.id,'Данные боты могут быть забанены функцией **AntiBot**!')}\n{get_language(ctx.guild.id,'Воспользуйтесь командой')} `{prefix}ignore add {get_language(ctx.guild.id,'@пользователь')}`, {get_language(ctx.guild.id,'чтобы занести ботов в игнорируемый список.')}"
                                                    embed.add_field(
                                                        name="Боты:",
                                                        value=", ".join(ig),
                                                        inline=False,
                                                    )
                                                else:
                                                    embed.description = f"{get_language(ctx.guild.id,'Данные боты не занесены в игнорируемый список!')}\n{get_language(ctx.guild.id,'Воспользуйтесь командой')} `{prefix}ignore add {get_language(ctx.guild.id,'@пользователь')}`, {get_language(ctx.guild.id,'чтобы занести ботов в список.')}"
                                                    embed.add_field(
                                                        name=f"{get_language(ctx.guild.id,'Боты:')}",
                                                        value=", ".join(ig),
                                                        inline=False,
                                                    )
                                        await ctx.edit_original_message(embed=embed)
                                    else:
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Боты не обнаружены!')}",
                                            color=0xCC1A1D,
                                        )
                                        await ctx.edit_original_message(embed=embed)
                                else:
                                    try:
                                        option = int(option)
                                        if 1e17 < option < 1e18:
                                            embed = discord.Embed(
                                                description=f"<a:vega_x:810843492266803230> **{option}** {get_language(ctx.guild.id,'не является пользователем!')}",
                                                color=0xCC1A1D,
                                            )
                                            await ctx.send(
                                                embed=embed, delete_after=12.0
                                            )
                                        else:
                                            pass
                                    except:
                                        ctx.command.reset_cooldown(ctx)
                except:
                    pass

                if ctx.channel.id != 826326189324763166:
                    if bot:
                        if bot.bot:
                            w = gdata("vega", "wlbots")
                            if str(bot.id) in w[str("Bots")]:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{bot}** {get_language(ctx.guild.id,'есть в белом списке!')}\n\n{get_language(ctx.guild.id,':warning: **Внимание!**')}\n{get_language(ctx.guild.id,'Данного бота невозможно занести в игнорируемый список!')}",
                                    color=0x43B581,
                                )
                                if bot.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                if bot.public_flags.verified_bot:
                                    verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if bot.public_flags.spammer:
                                    spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                if bot.avatar != None:
                                    embed.set_thumbnail(
                                        url=bot.avatar.replace(size=1024, format="png")
                                    )
                                embed.set_footer(text=f"ID: {bot.id}")
                                await ctx.send(embed=embed)
                            else:
                                data = gdata("vega", "antibot")
                                try:
                                    enabled = data[str(ctx.guild.id)]
                                except KeyError:
                                    enabled = False
                                if bot:
                                    if enabled:
                                        wl = gdata("vega", "ignorebots")
                                        try:
                                            enabled = False
                                            if str(ctx.guild.id) in wl:
                                                dop = wl[str(ctx.guild.id)]
                                            else:
                                                dop = ""
                                        except KeyError:
                                            print(
                                                "[ ОШИБКА ] Произошла неизвестная ошибка!"
                                            )
                                            pass
                                        if str(bot.id) in dop:
                                            embed = discord.Embed(
                                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бота')} **{bot}** {get_language(ctx.guild.id,'нет в белом списке!')}",
                                                color=0xCC1A1D,
                                            )
                                            embed.add_field(
                                                name=f"{get_language(ctx.guild.id,':warning: Внимание!')}",
                                                value=f"**{bot}** {get_language(ctx.guild.id,'игнорируется на данном сервере!')}",
                                                inline=False,
                                            )
                                            if bot.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                            if bot.public_flags.verified_bot:
                                                verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if bot.public_flags.spammer:
                                                spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                                inline=False,
                                            )
                                            if bot.avatar != None:
                                                embed.set_thumbnail(
                                                    url=bot.avatar.replace(
                                                        size=1024, format="png"
                                                    )
                                                )
                                            embed.set_footer(text=f"ID: {bot.id}")
                                            await ctx.send(embed=embed)
                                        else:
                                            embed = discord.Embed(
                                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бота')} **{bot}** {get_language(ctx.guild.id,'нет в белом списке!')}",
                                                color=0xCC1A1D,
                                            )
                                            embed.add_field(
                                                name=f"{get_language(ctx.guild.id,':warning: Внимание!')}",
                                                value=f"**{bot}** {get_language(ctx.guild.id,'может быть забанен функцией **AntiBot**!')}\n{get_language(ctx.guild.id,'Воспользуйтесь командой')} `{prefix}ignore add {bot.id}`, {get_language(ctx.guild.id,'чтобы занести бота в игнорируемый список.')}\n\n{get_language(ctx.guild.id,'Если хотите пропустить бота на сервер, не добавляя его в игнорируемый список, то выдайте ему пропуск командой:')} `{prefix}pass add {bot.id}`",
                                                inline=False,
                                            )
                                            if bot.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                            if bot.public_flags.verified_bot:
                                                verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if bot.public_flags.spammer:
                                                spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                                inline=False,
                                            )
                                            if bot.avatar != None:
                                                embed.set_thumbnail(
                                                    url=bot.avatar.replace(
                                                        size=1024, format="png"
                                                    )
                                                )
                                            embed.set_footer(text=f"ID: {bot.id}")
                                            await ctx.send(embed=embed)
                                    else:
                                        wl = gdata("vega", "ignorebots")
                                        try:
                                            enabled = False
                                            if str(ctx.guild.id) in wl:
                                                dop = wl[str(ctx.guild.id)]
                                            else:
                                                dop = ""
                                        except KeyError:
                                            print(
                                                "[ ОШИБКА ] Произошла неизвестная ошибка!"
                                            )
                                            pass
                                        if str(bot.id) in dop:
                                            embed = discord.Embed(
                                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бота')} **{bot}** {get_language(ctx.guild.id,'нет в белом списке!')}",
                                                color=0xCC1A1D,
                                            )
                                            embed.add_field(
                                                name=f"{get_language(ctx.guild.id,':warning: Внимание!')}",
                                                value=f"**{bot}** {get_language(ctx.guild.id,'игнорируется на данном сервере!')}",
                                                inline=False,
                                            )
                                            if bot.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                            if bot.public_flags.verified_bot:
                                                verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if bot.public_flags.spammer:
                                                spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                                inline=False,
                                            )
                                            if bot.avatar != None:
                                                embed.set_thumbnail(
                                                    url=bot.avatar.replace(
                                                        size=1024, format="png"
                                                    )
                                                )
                                            embed.set_footer(text=f"ID: {bot.id}")
                                            await ctx.send(embed=embed)
                                        else:
                                            embed = discord.Embed(
                                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бота')} **{bot}** {get_language(ctx.guild.id,'нет в белом списке!')}",
                                                color=0xCC1A1D,
                                            )
                                            embed.add_field(
                                                name=f"{get_language(ctx.guild.id,':warning: Внимание!')}",
                                                value=f"**{bot}** {get_language(ctx.guild.id,'не игнорируется на данном сервере!')}\n{get_language(ctx.guild.id,'Воспользуйтесь командой')} `{prefix}ignore add {bot.id}`, {get_language(ctx.guild.id,'чтобы занести бота в игнорируемый список.')}",
                                                inline=False,
                                            )
                                            if bot.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}"
                                            if bot.public_flags.verified_bot:
                                                verification_bot = f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if bot.public_flags.spammer:
                                                spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(ctx.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(ctx.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(bot.created_at.timestamp())}:D> *(<t:{int(bot.created_at.timestamp())}:R>)*",
                                                inline=False,
                                            )
                                            if bot.avatar != None:
                                                embed.set_thumbnail(
                                                    url=bot.avatar.replace(
                                                        size=1024, format="png"
                                                    )
                                                )
                                            embed.set_footer(text=f"ID: {bot.id}")
                                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(
                                description=f"<a:vega_x:810843492266803230> **{bot.id}** {get_language(ctx.guild.id,'не является ботом!')}",
                                color=0xCC1A1D,
                            )
                            await ctx.send(embed=embed, ephemeral=True)

                    elif option:
                        if option == 2:
                            embed = discord.Embed(
                                description=f"**{get_language(ctx.guild.id,'Команда только для РАЗРАБОТЧИКОВ!')}**",
                                color=0xCC1A1D,
                            )
                            await ctx.send(embed=embed, ephemeral=True)

                        elif option == 1:
                            w = gdata("vega", "wlbots")
                            wl = gdata("vega", "ignorebots")
                            ig = []
                            try:
                                enabled = False
                                if str(ctx.guild.id) in wl:
                                    dop = wl[str(ctx.guild.id)]
                                else:
                                    dop = ""
                            except KeyError:
                                print("[ ОШИБКА ] Произошла неизвестная ошибка!")
                                pass
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется проверка ботов...')}",
                                color=0xF4900C,
                            )
                            await ctx.send(embed=embed)
                            for member in [m for m in ctx.guild.members if m.bot]:
                                if (
                                    not str(member.id) in w[str("Bots")]
                                    and not str(member.id) in dop
                                ):
                                    ig.append(member.mention)
                            bot1 = len([m for m in ctx.guild.members if m.bot])
                            if bot1 > 1:
                                # if member in [m for m in ctx.guild.members if m.bot and m != ctx.guild.me]:
                                embed = discord.Embed(
                                    title=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Проверка завершена!')}",
                                    color=0x43B581,
                                )
                                if len(ig) == 0:
                                    embed.description = f"{get_language(ctx.guild.id,'Все боты были проверены.')}"
                                else:
                                    data = gdata("vega", "antibot")
                                    try:
                                        enabled = data[str(member.guild.id)]
                                    except KeyError:
                                        enabled = False
                                    if member.bot:
                                        if enabled:
                                            embed.description = f"{get_language(ctx.guild.id,'Данные боты могут быть забанены функцией **AntiBot**!')}\n{get_language(ctx.guild.id,'Воспользуйтесь командой')} `{prefix}ignore add {get_language(ctx.guild.id,'@пользователь')}`, {get_language(ctx.guild.id,'чтобы занести ботов в игнорируемый список.')}"
                                            embed.add_field(
                                                name="Боты:",
                                                value=", ".join(ig),
                                                inline=False,
                                            )
                                        else:
                                            embed.description = f"{get_language(ctx.guild.id,'Данные боты не занесены в игнорируемый список!')}\n{get_language(ctx.guild.id,'Воспользуйтесь командой')} `{prefix}ignore add {get_language(ctx.guild.id,'@пользователь')}`, {get_language(ctx.guild.id,'чтобы занести ботов в список.')}"
                                            embed.add_field(
                                                name=f"{get_language(ctx.guild.id,'Боты:')}",
                                                value=", ".join(ig),
                                                inline=False,
                                            )
                                await ctx.edit_original_message(embed=embed)
                            else:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Боты не обнаружены!')}",
                                    color=0xCC1A1D,
                                )
                                await ctx.edit_original_message(embed=embed)
                        else:
                            try:
                                option = int(option)
                                if 1e17 < option < 1e18:
                                    embed = discord.Embed(
                                        description=f"<a:vega_x:810843492266803230> **{option}** {get_language(ctx.guild.id,'не является пользователем!')}",
                                        color=0xCC1A1D,
                                    )
                                    await ctx.send(embed=embed, ephemeral=True)
                                else:
                                    pass
                            except:
                                ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите одного или всех ботов!')}",
                    color=0x8899A6,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Описание:')}",
                    value=f"{get_language(ctx.guild.id,'Только пользователи с правом Администратора или Управлениея сервером, могут проверить наличие одного или всех ботов из сервера в белом списке!')}",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                    value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID бота}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{all}')}`",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Пример:')}",
                    value=f"`{prefix}checkwl {get_language(ctx.guild.id,'ID бота')}` {get_language(ctx.guild.id,'или')} `{prefix}checkwl all`",
                    inline=False,
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar.replace(), text=f"{ctx.author}"
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_checkwl(client))
