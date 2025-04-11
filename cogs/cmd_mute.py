from async_timeout import timeout
import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *

prefix = "/"
Animal = commands.option_enum(["60 SECS", "5 MINS", "10 MINS", "1 HOUR", "1 DAY", "1 WEEK"])

class class_mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Мьют пользователя
    @commands.slash_command(
        name="mute",
        description="Mute the user | Замьютить пользователя",
        pass_context=True,
    )
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True, send_messages=True)
    @commands.has_permissions(moderate_members=True)
    async def mute(
        self,
        ctx,
        member: discord.Member = commands.Param(
            name="member",
            description="Specify the user or his ID | Укажите пользователя или его ID",
        ),
        time: Animal = commands.Param(description="Set an existing time | Установить существующее время") == None,
        its_time: int = commands.Param(description="Set your time in sec | Установить свое время в сек") == None,
        *,
        reason=None,
    ):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if member:
                #try:
                #mr = gdata("vega", "muterole")
                """w = gdata("vega", "mute_users")
                if str(ctx.guild.id) not in w:
                    w.update({str(ctx.guild.id): ""})"""

                user = ctx.author
                if (
                    member in ctx.guild.members
                    and member != user
                    and member != self.client.user
                    and user.top_role <= member.top_role
                ):
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,':warning: Невозможно замьютить пользователя, роль которого выше или равна вашей!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif member == user:
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,':warning: Невозможно замьютить себя!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif member == self.client.user:
                    embed = discord.Embed(
                        description=f":warning: {self.client.user.mention} {get_language(ctx.guild.id,'не может себя замьютить!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)

                else:
                    if time and its_time:
                        emb = discord.Embed(
                            description=f":warning: {get_language(ctx.guild.id,'Выберите только один вариант времени!')} (`time` {get_language(ctx.guild.id,'или')} `its_time`)",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=emb, ephemeral=True)
                    else:
                        if time or its_time:
                            #if str(ctx.guild.id) in mr:
                            """muterole = ctx.guild.get_role(
                                int(mr[str(ctx.guild.id)])
                            )
                            if muterole not in member.roles:
                                w.update(
                                    {
                                        str(ctx.guild.id): w[str(ctx.guild.id)]
                                        .replace(str(member.id), "")
                                        .strip()
                                    }
                                )"""
                            """if member.current_timeout:
                                try:
                                    w.update(
                                        {
                                            str(ctx.guild.id): w[str(ctx.guild.id)].replace(
                                                str(f"{member.id} "), ""
                                            )
                                        }
                                    )
                                    #await member.remove_roles(muterole)
                                except:
                                    pass"""
                            if member.current_timeout == None:
                                """if str(member.id) not in w[str(ctx.guild.id)]:
                                    w.update(
                                        {
                                            str(ctx.guild.id): w[
                                                str(ctx.guild.id)
                                            ].strip()
                                            + str(member.id)
                                            + " "
                                        }
                                    )"""
                                emb = discord.Embed(
                                    title=f"{get_language(ctx.guild.id,'<:muted:842447248277241867> Мьют')}",
                                    color=0xFDE910,
                                )
                                emb.add_field(
                                    name=f"{get_language(ctx.guild.id,'Модератор:')}",
                                    value=ctx.author.mention,
                                    inline=True,
                                )
                                emb.add_field(
                                    name=f"{get_language(ctx.guild.id,'Нарушитель:')}",
                                    value=member.mention,
                                    inline=True,
                                )
                                emb.set_thumbnail(
                                    url=member.avatar.replace(size=1024)
                                )
                                if time != None:
                                    try:
                                        if time == "60 SECS":
                                            dtimeout = f"60 {get_language(ctx.guild.id,'сек')}"
                                        elif time == "5 MINS":
                                            dtimeout = f"5 {get_language(ctx.guild.id,'мин')}"
                                        elif time == "10 MINS":
                                            dtimeout = f"10 {get_language(ctx.guild.id,'мин')}"
                                        elif time == "1 HOUR":
                                            dtimeout = f"1 {get_language(ctx.guild.id,'час')}"
                                        elif time == "1 DAY":
                                            dtimeout = f"1 {get_language(ctx.guild.id,'день')}"
                                        elif time == "1 WEEK":
                                            dtimeout = f"1 {get_language(ctx.guild.id,'неделя')}"
                                        emb.add_field(
                                            name=f"{get_language(ctx.guild.id,'Время тайм-аута:')}",
                                            value=dtimeout,
                                            inline=False,
                                        )
                                    except:
                                        pass
                                if its_time != None:
                                    try:
                                        if its_time:
                                            cdtimeout = f"{its_time} {get_language(ctx.guild.id,'сек')}"
                                        emb.add_field(
                                            name=f"{get_language(ctx.guild.id,'Время тайм-аута:')}",
                                            value=cdtimeout,
                                            inline=False,
                                        )
                                    except:
                                        pass
                                if reason != None:
                                    emb.add_field(
                                        name=f"{get_language(ctx.guild.id,'Причина:')}",
                                        value=reason,
                                        inline=False,
                                    )
                                if reason != None:
                                    dreason = reason
                                else:
                                    dreason = f"{ctx.author}"

                                if time == "60 SECS" and dreason:
                                    await member.timeout(duration=60, reason=dreason)
                                elif time == "5 MINS" and dreason:
                                    await member.timeout(duration=60*5, reason=dreason)
                                elif time == "10 MINS" and dreason:
                                    await member.timeout(duration=60*10, reason=dreason)
                                elif time == "1 HOUR" and dreason:
                                    await member.timeout(duration=60*60, reason=dreason)
                                elif time == "1 DAY" and dreason:
                                    await member.timeout(duration=60*1440, reason=dreason)
                                elif time == "1 WEEK" and dreason:
                                    await member.timeout(duration=60*60*168, reason=dreason)
                                elif its_time and dreason and not time:
                                    if its_time <= 60*60*168+60*60*168+60*60*168+60*60*168:
                                        await member.timeout(duration=its_time, reason=dreason)
                                    else:
                                        emb = discord.Embed(
                                            description=f":warning: {get_language(ctx.guild.id,'Максимальное время 2419200 сек (28 дней)!')}",
                                            color=0xFCC21B,
                                        )
                                        await ctx.send(embed=emb, ephemeral=True)
                                #await member.add_roles(muterole)
                                if time or its_time <= 60*60*168+60*60*168+60*60*168+60*60*168:
                                    await ctx.send(embed=emb)
                                else:
                                    pass
                                #wdata("vega", "mute_users", w)
                            else:
                                emb = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,':warning: Пользователь')} {member.mention} {get_language(ctx.guild.id,'уже замьючен!')}",
                                    color=0xFCC21B,
                                )
                                await ctx.send(embed=emb, ephemeral=True)
                            """else:
                                emb = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,':warning: Укажите роль мьюта!')}",
                                    color=0xFCC21B,
                                )
                                emb.add_field(
                                    name=f"{get_language(ctx.guild.id,'Команда:')}",
                                    value=f"`{prefix}rmute add {get_language(ctx.guild.id,'@роль')}`",
                                    inline=True,
                                )
                                await ctx.send(embed=emb, ephemeral=True)"""
                        else:
                            emb = discord.Embed(
                                description=f":warning: {get_language(ctx.guild.id,'Укажите время тайм-аута!')}",
                                color=0xFCC21B,
                            )
                            await ctx.send(embed=emb, ephemeral=True)
                """except:
                    embed = discord.Embed(
                        description=f":warning: **ERROR**\n{get_language(ctx.guild.id,'Проверьте права у бота, а так же расположение ролей!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)"""
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите пользователя!')}",
                    color=0x8899A6,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Описание:')}",
                    value=f"{get_language(ctx.guild.id,'Замьютьте пользователя. Причину можно не указывать.')}\n{get_language(ctx.guild.id,'Вы сами должны настроить роль мьюта!')}",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                    value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Пример:')}",
                    value=f"{prefix}mute {get_language(ctx.guild.id,'@пользователь')} {get_language(ctx.guild.id,'Спам!')}",
                    inline=False,
                )
                embed.set_footer(icon_url=ctx.author.avatar, text=f"{ctx.author}")
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_mute(client))
