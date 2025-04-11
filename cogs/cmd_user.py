import disnake
import disnake as discord
import time

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_user(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Информация о пользователе
    @commands.slash_command(
        name="userinfo", description="User information | Информация о пользователе"
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.bot_has_permissions(send_messages=True)
    async def user(self, ctx, *,
        user: disnake.Member = None,
    ):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            w = gdata("vega", "mute_users")
            if user == None:
                user = ctx.author

            embed = discord.Embed(
                description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется обработка данных...')}",
                color=0xF4900C,
            )
            await ctx.send(embed=embed)

            # Статусы
            statuses = {
                disnake.Status.online: f"{get_language(ctx.guild.id,'<:online:841950162904678401>В сети')}",
                disnake.Status.idle: f"{get_language(ctx.guild.id,'<:idle:841950163080970260>Не активен')}",
                disnake.Status.dnd: f"{get_language(ctx.guild.id,'<:dnd:841950162862735401>Не беспокоить')}",
                disnake.Status.offline: f"{get_language(ctx.guild.id,'<:offline:841950163147685898>Не в сети')}",
            }
            status = statuses[user.status]
            roles = [role for role in user.roles]
            req = await self.client.http.request(
                discord.http.Route("GET", "/users/{uid}", uid=user.id)
            )
            if user.bot:
                banner_color = 0x2F3136
            else:
                banner_color = req["accent_color"]

            """denied = '`*~_<>|'
            denied.split()
            declined = False
            for s in user.name:
                if s in denied:
                    declined = True
            if not declined:
                declined=user
            else:
                for si in denied.split():
                    declined=f"\{si}"""

            if (int(time.time()) - user.joined_at.timestamp()) // 86400 // 7 < 1:
                newuser = f"\n{get_language(ctx.guild.id,'Новый участник сервера')}: **{user.name}** <:new_user:970231707364130896>"
            else:
                newuser = ""
            try:
                embed = discord.Embed(
                    title=f"{get_language(ctx.guild.id,'Информация о пользователе')}",
                    description=f"<:redline:838450844571271189><:redline:838450844571271189><:redline:838450844571271189><:redline:838450844571271189>ㅤ{newuser}",
                    color=banner_color,
                )
            except:
                embed = discord.Embed(
                    title=f"{get_language(ctx.guild.id,'Информация о пользователе')}",
                    description=f"<:redline:838450844571271189><:redline:838450844571271189><:redline:838450844571271189><:redline:838450844571271189>ㅤ{newuser}",
                    color=0x2F3136,
                )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'Ник:')}",
                value=f"<@!{user.id}>\n {user}",
                inline=True,
            )
            if len(roles) > 1:
                if user.mobile_status == disnake.Status.online:
                    statusmobile = "<:online_mobile:1047136984549818388> "
                elif user.mobile_status == disnake.Status.idle:
                    statusmobile = "<:idle_mobile:1047137001054425128> "
                elif user.mobile_status == disnake.Status.dnd:
                    statusmobile = "<:dnd_mobile:1047137021967216660> "
                else:
                    statusmobile = ""
                if user.desktop_status == disnake.Status.online:
                    statusdesctop = "<:online_desktop:1047137058776436838> "
                elif user.desktop_status == disnake.Status.idle:
                    statusdesctop = "<:idle_desktop:1047137084097429544> "
                elif user.desktop_status == disnake.Status.dnd:
                    statusdesctop = "<:dnd_desktop:1047137103865196655> "
                else:
                    statusdesctop = ""
                if user.web_status == disnake.Status.online:
                    statusweb = "<:online_web:1047145028562198568> "
                elif user.web_status == disnake.Status.idle:
                    statusweb = "<:idle_web:1047145048250261554> "
                elif user.web_status == disnake.Status.dnd:
                    statusweb = "<:dnd_web:1047145067296587786> "
                else:
                    statusweb = ""
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Профиль:')}",
                    value=f"{status}\n{statusmobile}{statusdesctop}{statusweb}",
                    inline=True,
                )
                if user.public_flags.staff:
                    bd_staff_user = "<:dd_staff:810846754962145330> "
                else:
                    bd_staff_user = ""
                if user.public_flags.partner:
                    bd_partner_user = "<a:dd_partner:810846755054288926> "
                else:
                    bd_partner_user = ""
                if user.public_flags.hypesquad:
                    bd_hypesquad_user = "<:hypesquad_events:902644621664985088> "
                else:
                    bd_hypesquad_user = ""
                if user.public_flags.bug_hunter:
                    bd_bug_hunter_user = "<:bughunter_1:902644621669195837> "
                else:
                    bd_bug_hunter_user = ""
                if user.public_flags.hypesquad_bravery:
                    bd_hypesquad_bravery_user = "<:bravery:902644621564338216> "
                else:
                    bd_hypesquad_bravery_user = ""
                if user.public_flags.hypesquad_brilliance:
                    bd_hypesquad_brilliance_user = "<:brilliance:902644621690159114> "
                else:
                    bd_hypesquad_brilliance_user = ""
                if user.public_flags.hypesquad_balance:
                    bd_hypesquad_balance_user = "<:balance:902644621455286292> "
                else:
                    bd_hypesquad_balance_user = ""
                if user.public_flags.early_supporter:
                    bd_early_supporter_user = "<:early_supporter:902644621857927188> "
                else:
                    bd_early_supporter_user = ""
                if user.public_flags.bug_hunter_level_2:
                    bd_bug_hunter_level_2_user = "<:bughunter_2:902644621631430697> "
                else:
                    bd_bug_hunter_level_2_user = ""
                if user.public_flags.verified_bot_developer:
                    bd_verified_bot_developer_user = "<:vb_developer:931450178488107060> "
                else:
                    bd_verified_bot_developer_user = ""
                try:
                    if user.public_flags.active_developer:
                        bd_active_developer_user = "<:Active_Developer_Badge:1047120466273374230> "
                    else:
                        bd_active_developer_user = ""
                except:
                    bd_active_developer_user = ""
                if user.public_flags.discord_certified_moderator:
                    bd_discord_certified_moderator_user = "<:Discord_Certified_Moderator:943816629379297352> "
                else:
                    bd_discord_certified_moderator_user = ""
                if bd_staff_user or bd_partner_user or bd_hypesquad_user or bd_bug_hunter_user or bd_hypesquad_bravery_user or bd_hypesquad_brilliance_user or bd_hypesquad_balance_user or bd_early_supporter_user or bd_bug_hunter_level_2_user or bd_verified_bot_developer_user or bd_active_developer_user or bd_discord_certified_moderator_user:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Значки:')}",
                        value=f"{bd_staff_user}{bd_partner_user}{bd_hypesquad_user}{bd_bug_hunter_user}{bd_hypesquad_bravery_user}{bd_hypesquad_brilliance_user}{bd_hypesquad_balance_user}{bd_early_supporter_user}{bd_bug_hunter_level_2_user}{bd_verified_bot_developer_user}{bd_active_developer_user}{bd_discord_certified_moderator_user}",
                        inline=True,
                    )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'<:roles:842446865320378388>Ролей:')} ` {len(roles)} `",
                    value=f"**{get_language(ctx.guild.id,'Наивысшая роль:')}**\n{user.top_role.mention}",
                    inline=False,
                )
            else:
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Профиль:')}",
                    value=f"{status}\n{get_language(ctx.guild.id,'<:roles:842446865320378388>Ролей:')} {len(roles)}",
                    inline=True,
                )
                if user.public_flags.staff:
                    bd_staff_user = "<:dd_staff:810846754962145330> "
                else:
                    bd_staff_user = ""
                if user.public_flags.partner:
                    bd_partner_user = "<a:dd_partner:810846755054288926> "
                else:
                    bd_partner_user = ""
                if user.public_flags.hypesquad:
                    bd_hypesquad_user = "<:hypesquad_events:902644621664985088> "
                else:
                    bd_hypesquad_user = ""
                if user.public_flags.bug_hunter:
                    bd_bug_hunter_user = "<:bughunter_1:902644621669195837> "
                else:
                    bd_bug_hunter_user = ""
                if user.public_flags.hypesquad_bravery:
                    bd_hypesquad_bravery_user = "<:bravery:902644621564338216> "
                else:
                    bd_hypesquad_bravery_user = ""
                if user.public_flags.hypesquad_brilliance:
                    bd_hypesquad_brilliance_user = "<:brilliance:902644621690159114> "
                else:
                    bd_hypesquad_brilliance_user = ""
                if user.public_flags.hypesquad_balance:
                    bd_hypesquad_balance_user = "<:balance:902644621455286292> "
                else:
                    bd_hypesquad_balance_user = ""
                if user.public_flags.early_supporter:
                    bd_early_supporter_user = "<:early_supporter:902644621857927188> "
                else:
                    bd_early_supporter_user = ""
                if user.public_flags.bug_hunter_level_2:
                    bd_bug_hunter_level_2_user = "<:bughunter_2:902644621631430697> "
                else:
                    bd_bug_hunter_level_2_user = ""
                if user.public_flags.verified_bot_developer:
                    bd_verified_bot_developer_user = "<:vb_developer:931450178488107060> "
                else:
                    bd_verified_bot_developer_user = ""
                if user.public_flags.discord_certified_moderator:
                    bd_discord_certified_moderator_user = "<:Discord_Certified_Moderator:943816629379297352> "
                else:
                    bd_discord_certified_moderator_user = ""
                if bd_staff_user or bd_partner_user or bd_hypesquad_user or bd_bug_hunter_user or bd_hypesquad_bravery_user or bd_hypesquad_brilliance_user or bd_hypesquad_balance_user or bd_early_supporter_user or bd_bug_hunter_level_2_user or bd_verified_bot_developer_user or bd_discord_certified_moderator_user:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Значки:')}",
                        value=f"{bd_staff_user}{bd_partner_user}{bd_hypesquad_user}{bd_bug_hunter_user}{bd_hypesquad_bravery_user}{bd_hypesquad_brilliance_user}{bd_hypesquad_balance_user}{bd_early_supporter_user}{bd_bug_hunter_level_2_user}{bd_verified_bot_developer_user}{bd_discord_certified_moderator_user}",
                        inline=True,
                    )

            # Профиль
            try:
                artists_string = ""
                # activities = 'Отсутствует'
                if len(user.activities) != 0:
                    activities = ""
                for activity in user.activities:
                    if isinstance(activity, disnake.Spotify):
                        if activity != None:
                            for artist in activity.artists:
                                if activity.artists.index(
                                    artist
                                ) != activity.artists.index(activity.artists[-1]):
                                    artists_string += f'[{artist}]({urlspotify(f"https://open.spotify.com/search/{artist}")}), '
                                else:
                                    artists_string += f'[{artist}]({urlspotify(f"https://open.spotify.com/search/{artist}")})'
                            activities += f"{get_language(ctx.guild.id,'**Слушает:**')} <:spotify:811191409184473138> [{activity.title}]({urlspotify(f'https://open.spotify.com/search/{activity.title}')}) — ({artists_string}) [🖼️]({activity.album_cover_url})\n"
                    elif activity.type == disnake.ActivityType.competing:
                        if activity != None:
                            activities += f"{get_language(ctx.guild.id,'**Соревнуется в:**')} [{activity.name}]({url_game_search(f'https://www.google.com/search?q={activity.name}')})\n"
                    elif activity.type == disnake.ActivityType.playing:
                        if activity != None:
                            activities += f"{get_language(ctx.guild.id,'**Играет в:**')} [{activity.name}]({url_game_search(f'https://www.google.com/search?q={activity.name}')})\n"
                    elif activity.type == disnake.ActivityType.streaming:
                        if activity != None:
                            activities += f"{get_language(ctx.guild.id,'**Стримит:**')} <:streaming:842043258879737898>[{activity.name}]({activity.url})\n"
                    elif activity.type == disnake.ActivityType.watching:
                        if activity != None:
                            activities += f"{get_language(ctx.guild.id,'**Смотрит:**')} {activity.name}\n"
                    elif activity.type == disnake.ActivityType.custom:
                        if activity != None:
                            # an = activity.name.replace("https://" or "http://", " ")
                            try:
                                if (
                                    activity.emoji in self.client.emojis
                                    or not activity.emoji.id
                                ):
                                    if activity.name == None:
                                        activities += f"{get_language(ctx.guild.id,'**Пользовательский статус:**')} {activity.emoji}\n"
                                    else:
                                        activities += f"{get_language(ctx.guild.id,'**Пользовательский статус:**')} {activity.emoji} {activity.name}\n"
                                else:
                                    if activity.name == None:
                                        pass
                                    else:
                                        activities += f"{get_language(ctx.guild.id,'**Пользовательский статус:**')} {activity.name}\n"
                            except:
                                if activity.name == None:
                                    pass
                                else:
                                    activities += f"{get_language(ctx.guild.id,'**Пользовательский статус:**')} {activity.name}\n"
                if len(activities) > 0:
                    try:
                        if user.voice.channel:
                            embed.add_field(
                                name=f"{get_language(ctx.guild.id,'Активность:')}",
                                value=f"{activities}{get_language(ctx.guild.id,'**Находится в канале:**')}\n{user.voice.channel.mention}",
                                inline=False,
                            )
                    except:
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Активность:')}",
                            value=activities,
                            inline=False,
                        )
            except:
                try:
                    if user.voice.channel:
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Активность:')}",
                            value=f"{get_language(ctx.guild.id,'**Находится в канале:**')}\n{user.voice.channel.mention}",
                            inline=False,
                        )
                except:
                    pass
            """except:
                try:
                    if user.voice.channel:
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Активность:')}", value=f"{activities}{get_language(ctx.guild.id,'**Находится в канале:**')} {user.voice.channel.mention}", inline=False)
                except:
                    pass"""

            try:
                if str(user.id) in w[str(ctx.guild.id)]:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,':warning: Пользователь')} {get_language(ctx.guild.id,'уже замьючен!')}",
                        value=f"ㅤ",
                        inline=False,
                    )
                else:
                    pass
            except:
                pass

            """try:
                oldestMessage = None
                for channel in ctx.guild.text_channels:
                    fetchMessage = await channel.history().find(lambda m: m.author.id == user.id)
                    if fetchMessage is None:
                        continue
                    if oldestMessage is None:
                        oldestMessage = fetchMessage
                    else:
                        if fetchMessage.created_at > oldestMessage.created_at:
                            oldestMessage = fetchMessage

                if (oldestMessage is not None) and user.voice.channel:
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Активность:')}", value=f"{get_language(ctx.guild.id,'**Находится в канале:**')} {user.voice.channel.mention}\n{get_language(ctx.guild.id,'**Последнее сообщение:**')} [{get_language(ctx.guild.id,'📥 перейти к сообщению')}]({oldestMessage.jump_url})", inline=False)
            except:
                try:
                    if user.voice.channel:
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Активность:')}", value=f"{get_language(ctx.guild.id,'**Находится в канале:**')} {user.voice.channel.mention}", inline=False)
                except:
                    oldestMessage = None
                    for channel in ctx.guild.text_channels:
                        fetchMessage = await channel.history().find(lambda m: m.author.id == user.id)
                        if fetchMessage is None:
                            continue
                        if oldestMessage is None:
                            oldestMessage = fetchMessage
                        else:
                            if fetchMessage.created_at > oldestMessage.created_at:
                                oldestMessage = fetchMessage
                    if (oldestMessage is not None):
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Активность:')}", value=f"{get_language(ctx.guild.id,'**Последнее сообщение:**')} [{get_language(ctx.guild.id,'📥 перейти к сообщению')}]({oldestMessage.jump_url})", inline=False)"""

            # embed.add_field(name='Наивысшая роль:', value=user.top_role.mention, inline=True)
            # embed.add_field(name=f"{get_language(ctx.guild.id,'Присоединился к серверу:')}", value=f"{str(user.joined_at.strftime('%d.%m.%Y, %H:%M:%S GMT'))} ({(datetime.datetime.now() - user.joined_at).days} {get_language(ctx.guild.id,'дней назад')})", inline=False)
            # embed.add_field(name=f"{get_language(ctx.guild.id,'Аккаунт создан:')}", value=f"{str(user.created_at.strftime('%d.%m.%Y, %H:%M:%S GMT'))} ({(datetime.datetime.now() - user.created_at).days} {get_language(ctx.guild.id,'дней назад')})", inline=False)
            if user.public_flags.spammer:
                spamm_user = f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
            else:
                spamm_user = f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}"
            if user.public_flags.system:
                system_user = f"{get_language(ctx.guild.id,'Официально представляет Discord')}\n"
            else:
                system_user = ""
            if user.bot:
                if user.public_flags.http_interactions_bot:
                    http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Использует только HTTP взаимодействия')}\n"
                else:
                    http_interactions_bot_bot = f"{get_language(ctx.guild.id,'Не использует HTTP взаимодействия')}\n"
                if user.public_flags.verified_bot:
                    verification_bot = f"**{get_language(ctx.guild.id,'Верификация:')}** {get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}\n"
                else:
                    verification_bot = f"**{get_language(ctx.guild.id,'Верификация:')}** {get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}\n"
            else:
                http_interactions_bot_bot = ""
                verification_bot = ""
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'Аккаунт:')}",
                value=f"{system_user}{http_interactions_bot_bot}{verification_bot}**{get_language(ctx.guild.id,'Спамер?:')}** {spamm_user}\n**{get_language(ctx.guild.id,'Присоединился:')}** <t:{int(user.joined_at.timestamp())}:D> *(<t:{int(user.joined_at.timestamp())}:R>)*\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(user.created_at.timestamp())}:D> *(<t:{int(user.created_at.timestamp())}:R>)*",
                inline=False,
            )
            if user.bot:
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470> Бот?')}",
                    value=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}",
                    inline=True,
                )

                wl = gdata("vega", "wlbots")
                ig = gdata("vega", "ignorebots")
                if str(ctx.guild.id) in ig:
                    dop = ig[str(ctx.guild.id)]
                else:
                    dop = ""
                if str(user.id) in wl[str("Bots")]:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915> В белом списке?')}",
                        value=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}",
                        inline=True,
                    )
                elif str(user.id) in dop:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470> Игнорируется?')}",
                        value=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}",
                        inline=True,
                    )
                else:
                    pass
            else:
                # embed.add_field(name='<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470> Бот?', value='<a:vega_x:810843492266803230> Нет', inline=True)
                if user == ctx.guild.owner:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'<:owner:860380081594564688> Владелец?')}",
                        value=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}",
                        inline=True,
                    )
                else:
                    ua = gdata("vega", "user_anticrash")
                    try:
                        enabled = ua[str(ctx.guild.id)]
                    except KeyError:
                        enabled = False
                    if enabled:
                        if ctx.guild.id in wluserdata:
                            if "members" in wluserdata[ctx.guild.id]:
                                if user.id in wluserdata[ctx.guild.id]["members"]:
                                    embed.add_field(
                                        name=f"{get_language(ctx.guild.id,'<:user:842445581426753606> В белом списке?')}",
                                        value=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}",
                                        inline=True,
                                    )
                                else:
                                    embed.add_field(
                                        name=f"{get_language(ctx.guild.id,'<:user:842445581426753606> В белом списке?')}",
                                        value=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}",
                                        inline=True,
                                    )
                            else:
                                embed.add_field(
                                    name=f"{get_language(ctx.guild.id,'<:user:842445581426753606> В белом списке?')}",
                                    value=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}",
                                    inline=True,
                                )
                        else:
                            embed.add_field(
                                name=f"{get_language(ctx.guild.id,'<:user:842445581426753606> В белом списке?')}",
                                value=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}",
                                inline=True,
                            )
                    else:
                        pass
                    # embed.add_field(name=f"{get_language(ctx.guild.id,'<:owner:860380081594564688> Владелец?')}", value=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}", inline=True)
            if user.guild_permissions.administrator:
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'<:admin:860380081536761886> Администратор?')}",
                    value=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}",
                    inline=True,
                )
            else:
                pass
                # embed.add_field(name=f"{get_language(ctx.guild.id,'<:admin:860380081536761886> Администратор?')}", value=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}", inline=True)

            badge = {
                351020816466575372: f"{get_language(ctx.guild.id,'<:vb_developer:931450178488107060> — Разработчик бота.')}",
                750245767142441000: f"{get_language(ctx.guild.id,'<:vb_developer:931450178488107060> — Разработчик бота.')}",
                313972726681567242: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                426663999136858113: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                301295716066787332: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                722288513206321263: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                596201949708156958: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                838037604955193354: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                729639044757192786: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
            }

            if user.id in badge:
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Дополнительная информация:')}",
                    value=badge[user.id],
                    inline=False,
                )


            embed.set_footer(text=f"ID: {user.id}")
            if user.avatar != None:
                embed.set_thumbnail(
                    url=user.avatar.replace(size=1024)
                )

            """req = await self.client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
            banner_id = req["banner"]
            if banner_id:
                try:
                    embed.set_image(url=f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}.gif?size=1024")
                except:
                    embed.set_image(url=f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}.png?size=1024")"""
            try:
                user = await self.client.fetch_user(user.id)
                if not user.bot:
                    if user.banner:
                        embed.set_image(url=user.banner)
                    else:
                        pass
                else:
                    pass
            except:
                pass

            # await ctx.send('🎫  {}, информация о пользователе отправлена тебе в личку.'.format(ctx.message.author.mention), delete_after=15.0)
            await ctx.edit_original_message(embed=embed)
            # await ctx.author.send(embed=embed)


def setup(client):
    client.add_cog(class_user(client))
