import disnake
import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum

prefix = "/"


class option(int, Enum):
    channels = 1
    ignores = 2
    passings = 4
    wlusers = 5
    all = 6


class yes_or_no_channels(disnake.ui.View):
    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="✔️", custom_id="YES")
    async def yes(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы подтвердили действие!')}\n", ephemeral=True)
        try:
            ch = gdata("vega", "channel_rights")
            del ch[str(interaction.guild.id)]
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс ограниченных каналов')}",
                description=f"{get_language(interaction.guild.id,'<a:vega_check_mark:821700784927801394> Сброс ограниченных каналов прошел успешно!')}",
                color=0x43B581,
            )
            await interaction.response.edit_message(embed=embed, view=None)
            wdata("vega", "channel_rights", ch)
        except:
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс ограниченных каналов')}",
                description=f":warning: {get_language(interaction.guild.id,'Каналы отсутствуют')}",
                color=0xFCC21B,
            )
            await interaction.response.edit_message(embed=embed, view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.grey, emoji="❌", custom_id="NO")
    async def no(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы отменили действие!')}\n", ephemeral=True)
        embed = discord.Embed(
            title=f"{get_language(interaction.guild.id,'Сброс ограниченных каналов')}",
            description=f"❌ {get_language(interaction.guild.id,'Действие отменено!')}",
            color=0xCC1A1D,
        )
        await interaction.response.edit_message(embed=embed, view=None)


class yes_or_no_ignores(disnake.ui.View):
    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="✔️", custom_id="YES")
    async def yes(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы подтвердили действие!')}\n", ephemeral=True)
        try:
            ig = gdata("vega", "ignorebots")
            del ig[str(interaction.guild.id)]
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс игнорируемых ботов')}",
                description=f"{get_language(interaction.guild.id,'<a:vega_check_mark:821700784927801394> Сброс игнорируемых ботов прошел успешно!')}",
                color=0x43B581,
            )
            await interaction.response.edit_message(embed=embed, view=None)
            wdata("vega", "ignorebots", ig)
        except:
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс игнорируемых ботов')}",
                description=f":warning: {get_language(interaction.guild.id,'Боты отсутствуют')}",
                color=0xFCC21B,
            )
            await interaction.response.edit_message(embed=embed, view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.grey, emoji="❌", custom_id="NO")
    async def no(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы отменили действие!')}\n", ephemeral=True)
        embed = discord.Embed(
            title=f"{get_language(interaction.guild.id,'Сброс игнорируемых ботов')}",
            description=f"❌ {get_language(interaction.guild.id,'Действие отменено!')}",
            color=0xCC1A1D,
        )
        await interaction.response.edit_message(embed=embed, view=None)


"""class yes_or_no_muteusers(disnake.ui.View):
    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="✔️", custom_id="YES")
    async def yes(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы подтвердили действие!')}\n", ephemeral=True)
        try:
            m = gdata("vega", "mute_users")
            mr = gdata("vega", "muterole")
            muterole = interaction.guild.get_role(int(mr[str(interaction.guild.id)]))
            for member in interaction.guild.members:
                if str(member.id) in m[str(interaction.guild.id)]:
                    m.update(
                        {
                            str(interaction.guild.id): m[
                                str(interaction.guild.id)
                            ].replace(str(f"{member.id} "), "")
                        }
                    )
                    await member.remove_roles(muterole)
            del m[str(interaction.guild.id)]

            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс замьюченных пользователей')}",
                description=f"{get_language(interaction.guild.id,'<a:vega_check_mark:821700784927801394> Сброс замьюченных пользователей прошел успешно!')}",
                color=0x43B581,
            )
            await interaction.response.edit_message(embed=embed, view=None)
            wdata("vega", "mute_users", m)
        except:
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс замьюченных пользователей')}",
                description=f":warning: {get_language(interaction.guild.id,'Пользователи отсутствуют')}",
                color=0xFCC21B,
            )
            await interaction.response.edit_message(embed=embed, view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.grey, emoji="❌", custom_id="NO")
    async def no(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы отменили действие!')}\n", ephemeral=True)
        embed = discord.Embed(
            title=f"{get_language(interaction.guild.id,'Сброс замьюченных пользователей')}",
            description=f"❌ {get_language(interaction.guild.id,'Действие отменено!')}",
            color=0xCC1A1D,
        )
        await interaction.response.edit_message(embed=embed, view=None)
"""

class yes_or_no_passings(disnake.ui.View):
    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="✔️", custom_id="YES")
    async def yes(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы подтвердили действие!')}\n", ephemeral=True)
        try:
            p = gdata("vega", "passbots")
            del p[str(interaction.guild.id)]
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс пропусков')}",
                description=f"{get_language(interaction.guild.id,'<a:vega_check_mark:821700784927801394> Сброс пропусков прошел успешно!')}",
                color=0x43B581,
            )
            await interaction.response.edit_message(embed=embed, view=None)
            wdata("vega", "passbots", p)
        except:
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс пропусков')}",
                description=f":warning: {get_language(interaction.guild.id,'Боты отсутствуют')}",
                color=0xFCC21B,
            )
            await interaction.response.edit_message(embed=embed, view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.grey, emoji="❌", custom_id="NO")
    async def no(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы отменили действие!')}\n", ephemeral=True)
        embed = discord.Embed(
            title=f"{get_language(interaction.guild.id,'Сброс пропусков')}",
            description=f"❌ {get_language(interaction.guild.id,'Действие отменено!')}",
            color=0xCC1A1D,
        )
        await interaction.response.edit_message(embed=embed, view=None)


class yes_or_no_wlusers(disnake.ui.View):
    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="✔️", custom_id="YES")
    async def yes(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы подтвердили действие!')}\n", ephemeral=True)
        try:
            wu = gdata("vega", "wluser")
            del wu[str(interaction.guild.id)]
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс белого списка участников')}",
                description=f"{get_language(interaction.guild.id,'<a:vega_check_mark:821700784927801394> Сброс белого списка участников прошел успешно!')}",
                color=0x43B581,
            )
            await interaction.response.edit_message(embed=embed, view=None)
            wdata("vega", "wluser", wu)
        except:
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс белого списка участников')}",
                description=f":warning: {get_language(interaction.guild.id,'Участники отсутствуют')}",
                color=0xFCC21B,
            )
            await interaction.response.edit_message(embed=embed, view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.grey, emoji="❌", custom_id="NO")
    async def no(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы отменили действие!')}\n", ephemeral=True)
        embed = discord.Embed(
            title=f"{get_language(interaction.guild.id,'Сброс белого списка участников')}",
            description=f"❌ {get_language(interaction.guild.id,'Действие отменено!')}",
            color=0xCC1A1D,
        )
        await interaction.response.edit_message(embed=embed, view=None)


class yes_or_no_all(disnake.ui.View):
    @disnake.ui.button(style=disnake.ButtonStyle.green, emoji="✔️", custom_id="YES")
    async def yes(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы подтвердили действие!')}\n", ephemeral=True)
        try:
            ch = gdata("vega", "channel_rights")
            ig = gdata("vega", "ignorebots")
            #m = gdata("vega", "mute_users")
            #mr = gdata("vega", "muterole")
            p = gdata("vega", "passbots")
            lang = gdata("vega", "language")
            log = gdata("vega", "logchannel")
            a = gdata("vega", "antibot")
            ha = gdata("vega", "hard_antibot")
            ua = gdata("vega", "user_anticrash")
            es = gdata("vega", "editserver")
            wu = gdata("vega", "wluser")

            with open('json/msg_appeal.json', 'r') as f:
                ma = json.load(f)
            del ma[str(interaction.guild.id)]
            with open('json/msg_appeal.json', 'w') as f:
                json.dump(ma, f, indent=4)
            try:
                del ch[str(interaction.guild.id)]
            except:
                pass
            try:
                del ig[str(interaction.guild.id)]
            except:
                pass
            """try:
                muterole = interaction.guild.get_role(
                    int(mr[str(interaction.guild.id)])
                )
                for member in interaction.guild.members:
                    if str(member.id) in m[str(interaction.guild.id)]:
                        m.update(
                            {
                                str(interaction.guild.id): m[
                                    str(interaction.guild.id)
                                ].replace(str(f"{member.id} "), "")
                            }
                        )
                        await member.remove_roles(muterole)
            except:
                pass"""
            try:
                del p[str(interaction.guild.id)]
            except:
                pass
            try:
                del wu[str(interaction.guild.id)]
            except:
                pass
            try:
                if str(interaction.guild.id) in lang:
                    if str(interaction.guild.region) == "russia":
                        lang[str(interaction.guild.id)] = True
                    else:
                        lang[str(interaction.guild.id)] = False
            except:
                pass
            try:
                del log[str(interaction.guild.id)]
            except:
                pass
            try:
                del a[str(interaction.guild.id)]
            except:
                pass
            try:
                del ha[str(interaction.guild.id)]
            except:
                pass
            try:
                del ua[str(interaction.guild.id)]
            except:
                pass
            try:
                del es[str(interaction.guild.id)]
            except:
                pass
            try:
                antimsg.remove(interaction.guild.id)
            except:
                pass
            try:
                antiinvite.remove(interaction.guild.id)
            except:
                pass
            """try:
                del mr[str(interaction.guild.id)]
            except:
                pass"""

            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс всех настроек')}",
                description=f"{get_language(interaction.guild.id,'<a:vega_check_mark:821700784927801394> Сброс всех настроек прошел успешно!')}",
                color=0x43B581,
            )
            await interaction.response.edit_message(embed=embed, view=None)
            wdata("vega", "channel_rights", ch)
            wdata("vega", "ignorebots", ig)
            #wdata("vega", "mute_users", m)
            wdata("vega", "passbots", p)
            wdata("vega", "wluser", wu)
            wdata("vega", "language", lang)
            wdata("vega", "logchannel", log)
            wdata("vega", "antibot", a)
            wdata("vega", "hard_antibot", ha)
            #wdata("vega", "muterole", mr)
            wdata("vega", "editserver", es)
            wdata("vega", "user_anticrash", ua)
        except:
            embed = discord.Embed(
                title=f"{get_language(interaction.guild.id,'Сброс всех настроек')}",
                description=f":warning: {get_language(interaction.guild.id,'Все настройки отсутствуют')}",
                color=0xFCC21B,
            )
            await interaction.response.edit_message(embed=embed, view=None)

    @disnake.ui.button(style=disnake.ButtonStyle.grey, emoji="❌", custom_id="NO")
    async def no(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # await interaction.response.send_message(f"{get_language(interaction.guild.id,'Вы отменили действие!')}\n", ephemeral=True)
        embed = discord.Embed(
            title=f"{get_language(interaction.guild.id,'Сброс всех настроек')}",
            description=f"❌ {get_language(interaction.guild.id,'Действие отменено!')}",
            color=0xCC1A1D,
        )
        await interaction.response.edit_message(embed=embed, view=None)


class class_reset(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Сбросить все или определенную настройку бота
    @commands.slash_command(
        name="reset", description="Resetting the bot settings | Сброс натсроек бота"
    )
    @commands.cooldown(1, 30, commands.BucketType.member)
    @commands.guild_only()
    async def reset(
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
            if ctx.author == ctx.guild.owner:
                if option is not None:
                    if option == 1:
                        # Временно!
                        embed = discord.Embed(
                            description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.slash_command.reset_cooldown(ctx)
                        """embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'Сброс ограниченных каналов')}",
                            description=f"{get_language(ctx.guild.id,'Вы точно хотите сбросить все каналы?')}\n{get_language(ctx.guild.id,'Бот станет отвечать на все команды во всех каналах!')}",
                            color=0x2F3136,
                        )
                        embed.set_footer(
                            text=f"{get_language(ctx.guild.id,'Кнопки будут недоступны через 30 сек!')}"
                        )
                        yes_or_no_view = yes_or_no_channels(timeout=30)
                        await ctx.send(embed=embed, view=yes_or_no_view, ephemeral=True)
                        await yes_or_no_view.wait()
                        # embed = discord.Embed(title=f"{get_language(ctx.guild.id,'Сброс ограниченных каналов')}", description=f":warning: {get_language(ctx.guild.id,'Действие отменено!')}", color=0xfcc21b)
                        try:
                            await ctx.edit_original_message(view=None)
                        except:
                            pass"""
                    elif option == 2:
                        # Временно!
                        embed = discord.Embed(
                            description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.slash_command.reset_cooldown(ctx)
                        """embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'Сброс игнорируемых ботов')}",
                            description=f"{get_language(ctx.guild.id,'Вы точно хотите сбросить всех игнорируемых ботов?')}\n{get_language(ctx.guild.id,'Бот станет реагировать на действия не игнорируемых ботов!')}",
                            color=0x2F3136,
                        )
                        embed.set_footer(
                            text=f"{get_language(ctx.guild.id,'Кнопки будут недоступны через 30 сек!')}"
                        )
                        yes_or_no_view = yes_or_no_ignores(timeout=30)
                        await ctx.send(embed=embed, view=yes_or_no_view, ephemeral=True)
                        await yes_or_no_view.wait()
                        # embed = discord.Embed(title=f"{get_language(ctx.guild.id,'Сброс игнорируемых ботов')}", description=f":warning: {get_language(ctx.guild.id,'Действие отменено!')}", color=0xfcc21b)
                        try:
                            await ctx.edit_original_message(view=None)
                        except:
                            pass"""
                    elif option == 4:
                        # Временно!
                        embed = discord.Embed(
                            description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.slash_command.reset_cooldown(ctx)
                        """embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'Сброс пропусков')}",
                            description=f"{get_language(ctx.guild.id,'Вы точно хотите сбросить все пропуски?')}",
                            color=0x2F3136,
                        )
                        embed.set_footer(
                            text=f"{get_language(ctx.guild.id,'Кнопки будут недоступны через 30 сек!')}"
                        )
                        yes_or_no_view = yes_or_no_passings(timeout=30)
                        await ctx.send(embed=embed, view=yes_or_no_view, ephemeral=True)
                        await yes_or_no_view.wait()
                        try:
                            await ctx.edit_original_message(view=None)
                        except:
                            pass"""
                    elif option == 5:
                        # Временно!
                        embed = discord.Embed(
                            description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.slash_command.reset_cooldown(ctx)
                        """embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'Сброс белого списка участников')}",
                            description=f"{get_language(ctx.guild.id,'Вы точно хотите сбросить белый список участников?')}",
                            color=0x2F3136,
                        )
                        embed.set_footer(
                            text=f"{get_language(ctx.guild.id,'Кнопки будут недоступны через 30 сек!')}"
                        )
                        yes_or_no_view = yes_or_no_wlusers(timeout=30)
                        await ctx.send(embed=embed, view=yes_or_no_view, ephemeral=True)
                        await yes_or_no_view.wait()
                        try:
                            await ctx.edit_original_message(view=None)
                        except:
                            pass"""
                    elif option == 6:
                        # Временно!
                        embed = discord.Embed(
                            description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.slash_command.reset_cooldown(ctx)
                        """embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'Сброс всех настроек')}",
                            description=f"{get_language(ctx.guild.id,'Вы точно хотите сбросить все настройки бота?')}\n\n{get_language(ctx.guild.id,'**Будут сброшены:**')}\n{get_language(ctx.guild.id,'Язык, ограниченные каналы, логи, редактирование сервера, AntiBot, HARD-AntiBot, AntiCrash, AntiMSGBot, игнорируемые боты, пропуски, белый список участников, анти приглашение, сообщение апелляции.')}",
                            color=0x2F3136,
                        )
                        embed.set_footer(
                            text=f"{get_language(ctx.guild.id,'Кнопки будут недоступны через 30 сек!')}"
                        )
                        yes_or_no_view = yes_or_no_all(timeout=30)
                        await ctx.send(embed=embed, view=yes_or_no_view, ephemeral=True)
                        await yes_or_no_view.wait()
                        try:
                            await ctx.edit_original_message(view=None)
                        except:
                            pass"""
                    
                    
                    
                    """elif option == 3:
                        embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'Сброс замьюченных пользователей')}",
                            description=f"{get_language(ctx.guild.id,'Вы точно хотите сбросить всех замьюченных пользователей?')}",
                            color=0x2F3136,
                        )
                        embed.set_footer(
                            text=f"{get_language(ctx.guild.id,'Кнопки будут недоступны через 30 сек!')}"
                        )
                        yes_or_no_view = yes_or_no_muteusers(timeout=30)
                        await ctx.send(embed=embed, view=yes_or_no_view, ephemeral=True)
                        await yes_or_no_view.wait()
                        try:
                            await ctx.edit_original_message(view=None)
                        except:
                            pass"""
                else:
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию!')}",
                        color=0x8899A6,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Команда предназначена для сброса настроек бота.')}\n{get_language(ctx.guild.id,'`channels` — сброс игнорируемых каналов')}\n{get_language(ctx.guild.id,'`ignores` — сброс игнорируемых ботов')}\n{get_language(ctx.guild.id,'`muteusers` — сброс замьюченных пользователей')}\n{get_language(ctx.guild.id,'`pass` — сброс пропусков')}\n{get_language(ctx.guild.id,'`all` — сброс всех настроек бота')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`channels`; `ignores`; `muteusers`; `pass`; `all`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Пример:')}",
                        value=f"{prefix}reset all",
                        inline=False,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.slash_command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: **Вы не являетесь Владельцем данного сервера!**')}",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.slash_command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_reset(client))
