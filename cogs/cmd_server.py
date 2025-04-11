import disnake as discord
import time

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_server(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Информация о сервере
    @commands.slash_command(
        name="serverinfo", description="Server information | Информация о сервере"
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def server(self, ctx):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            embed = discord.Embed(
                description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется обработка данных...')}",
                color=0xF4900C,
            )
            await ctx.send(embed=embed)


            count = 0  # всего онлайн
            online = 0  # в сети
            idle = 0  # не активен
            dnd = 0  # не беспокоить
            offline = 0  # не в сети
            for user in ctx.guild.members:
                if user.status != discord.Status.offline:
                    count += 1
                if user.status == discord.Status.online:
                    online += 1
                elif user.status == discord.Status.idle:
                    idle += 1
                elif user.status == discord.Status.dnd:
                    dnd += 1
                else:
                    offline += 1

            latency = round(self.client.latency * 1000, 1)
            # <:channel:842446310946766848> Всего: {len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)}
            embed = discord.Embed(
                title=f"{get_language(ctx.guild.id,'Информация о сервере')} **{ctx.guild.name}**",
                color=0x2F3136,
            )

            categories1 = len(ctx.guild.categories)
            categories0 = f"<:category:842445848549916762> {categories1}\n"
            if categories1 == 0:
                categories0 = ""
            text_channels1 = len(ctx.guild.text_channels)
            text_channels0 = f"<:chat:842446578521341993> {text_channels1}\n"
            if text_channels1 == 0:
                text_channels0 = ""
            voice_channels1 = len(ctx.guild.voice_channels)
            voice_channels0 = f"<:voice:842447248264134756> {voice_channels1}\n"
            if voice_channels1 == 0:
                voice_channels0 = ""
            stage_channels1 = len(ctx.guild.stage_channels)
            stage_channels0 = f"<:stage:875028214186143806> {stage_channels1}\n"
            if stage_channels1 == 0:
                stage_channels0 = ""
            roles1 = len(ctx.guild.roles)
            roles0 = f"<:role:842446865320378388> {roles1}"
            if roles1 == 0:
                roles0 = ""
            bot1 = len([m for m in ctx.guild.members if m.bot])
            bot0 = f"{get_language(ctx.guild.id,'<:BOT:842444823604363324>')} {get_language(ctx.guild.id,'Ботов:')} {bot1}"
            if bot1 == 0:
                bot0 = ""
                members0 = ""
            online1 = online
            online0 = f"<:online:841950162904678401> {online}\n"
            if online1 == 0:
                online0 = ""
            idle1 = idle
            idle0 = f"<:idle:841950163080970260> {idle}\n"
            if idle1 == 0:
                idle0 = ""
            dnd1 = dnd
            dnd0 = f"<:dnd:841950162862735401> {dnd}\n"
            if dnd1 == 0:
                dnd0 = ""
            offline1 = offline
            offline0 = f"<:offline:841950163147685898> {offline}"
            if offline1 == 0:
                offline0 = ""
            members1 = len(ctx.guild.members)
            members0 = f"<:users:842445268489994270> {get_language(ctx.guild.id,'Всего:')} {members1}\n"
            if bot1 == 1:
                members0 = ""

            if ctx.guild.banner != None:
                ename = f"{get_language(ctx.guild.id,'Другое:')}"
            else:
                ename = f"{get_language(ctx.guild.id,'Каналы & Роли:')}"
            embed.add_field(
                name=ename,
                value=f"{categories0}{text_channels0}{voice_channels0}{stage_channels0}{roles0}",
                inline=True,
            )

            new_member = []
            for member in [m for m in ctx.guild.members if not m.bot]:
                if (int(time.time()) - member.joined_at.timestamp()) // 86400 // 7 < 1:
                    new_member.append(member.mention)
            if len(new_member) == 0:
                new_members = ""
            else:
                new_members = f"\n<:new_user:970231707364130896> {get_language(ctx.guild.id,'Новичков:')} {len(new_member)}"

            embed.add_field(
                name=f"{get_language(ctx.guild.id,'Участники:')}",
                value=f"{members0}<:user:842445581426753606> {get_language(ctx.guild.id,'Людей:')} {len([m for m in ctx.guild.members if not m.bot])}\n{bot0}{new_members}",
                inline=True,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'По статусам:')}",
                value=f"{online0}{idle0}{dnd0}{offline0}",
                inline=True,
            )
            """rgs = {
            'brazil': f"{get_language(ctx.guild.id,'🇧🇷 Бразилия')}",
            'europe': f"{get_language(ctx.guild.id,'🇪🇺 Европа')}",
            'hongkong': f"{get_language(ctx.guild.id,'🇭🇰 Гонконг')}",
            'india': f"{get_language(ctx.guild.id,'🇮🇳 Индия')}",
            'japan': f"{get_language(ctx.guild.id,'🇯🇵 Япония')}",
            'russia': f"{get_language(ctx.guild.id,'🇷🇺 Россия')}",
            'singapore': f"{get_language(ctx.guild.id,'🇸🇬 Сингапур')}",
            'southafrica': f"{get_language(ctx.guild.id,'🇿🇦 ЮАР')}",
            'sydney': f"{get_language(ctx.guild.id,'🇦🇺 Сидней')}",
            'us-central': f"{get_language(ctx.guild.id,'🇺🇸 Центральная Америка')}",
            'us-east': f"{get_language(ctx.guild.id,'🇺🇸 Америка (Восток)')}",
            'us-south': f"{get_language(ctx.guild.id,'🇺🇸 Америка (Юг)')}",
            'us-west': f"{get_language(ctx.guild.id,'🇺🇸 Америка (Запад)')}",
            'stockholm': f"{get_language(ctx.guild.id,'🇸🇪 Стокгольм')}"
            }"""
            vlevels = {
                "none": f"{get_language(ctx.guild.id,'Отсутствует')}",
                "low": f"{get_language(ctx.guild.id,'Низкая')}",
                "medium": f"{get_language(ctx.guild.id,'Средняя')}",
                "high": f"{get_language(ctx.guild.id,'Высокая')}",
                "highest": f"{get_language(ctx.guild.id,'Самая высокая')}",
            }
            vlevels0 = {
                "none": f"<:v_not:810860032190316555>",
                "low": f"<:v_low:810860032576192522>",
                "medium": f"<:v_medium:810860032454426635>",
                "high": f"<:v_high:810860032392560641>",
                "highest": f"<:v_highest:810860032425721886>",
            }
            vlevelsg = vlevels0[str(ctx.guild.verification_level)]
            vlevelsg1 = vlevels[str(ctx.guild.verification_level)]
            embed.add_field(
                name=f"{vlevelsg} {get_language(ctx.guild.id,'Проверка:')}",
                value=vlevelsg1,
                inline=True,
            )
            d = f"<t:{int(ctx.guild.created_at.timestamp())}:d>"
            embed.add_field(
                name=f"{get_language(ctx.guild.id,':calendar_spiral: Создан:')}",
                value=f"{d}",
                inline=True,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'<:s_owner:841953225682714624> Владелец:')}",
                value=f"{ctx.guild.owner}",
                inline=True,
            )
            """try:
                embed.add_field(name=f"{get_language(ctx.guild.id,'Регион:')}", value=rgs[str(ctx.guild.region)], inline=True)
            except:
                embed.add_field(name=f"{get_language(ctx.guild.id,'Регион:')}", value=ctx.guild.region, inline=True)"""
            # embed.add_field(name='Дата создания:', value=f'{d}', inline=True)#({(datetime.datetime.now() - ctx.guild.created_at).days} дней назад)
            # embed.add_field(name='\📡Сеть:', value=f'Шард **{ctx.guild.shard_id}**: `{round(self.client.get_shard(ctx.guild.shard_id).latency * 1000, 1)} мс`', inline=True)
            embed.set_footer(
                text=f"ID: {ctx.guild.id} ㅤ|ㅤ {get_language(ctx.guild.id,'Шард')} {ctx.guild.shard_id}"
            )
            if ctx.guild.icon != None:
                embed.set_thumbnail(url=ctx.guild.icon)
            if ctx.guild.banner != None:
                embed.set_image(url=ctx.guild.banner)
            await ctx.edit_original_message(embed=embed)


def setup(client):
    client.add_cog(class_server(client))
