import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Статистика бота
    @commands.slash_command(
        name="stats", description="Bot statistics | Статистика бота"
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def stats(self, ctx):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            import time

            embed = discord.Embed(
                title=f"{get_language(ctx.guild.id,'📊 Статистика бота:')}",
                color=0x5865F2,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'<:servers:842447666625773568> Всего серверов:')}",
                value=f"```{len(self.client.guilds)}```",
                inline=False,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'<:users:842445268489994270> Всего пользователей:')}",
                value=f"```{len([m for m in self.client.users if not m.bot])}```",
                inline=False,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'📡 Аптайм хоста')}",
                value=f"```{hmsd1(ctx, time.perf_counter())}```",
                inline=False,
            )
            try:
                ub = f"<t:{int(self.client.start_time.timestamp())}:R>"
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'📡 Аптайм бота')}",
                    value=ub,
                    inline=False,
                )
            except:
                pass
            embed.set_thumbnail(
                url=self.client.get_user(795551166393876481).avatar.replace(
                    size=1024
                )
            )
            embed.set_footer(
                icon_url=ctx.author.avatar.replace(size=1024), text=f"{ctx.author}"
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(class_stats(client))
