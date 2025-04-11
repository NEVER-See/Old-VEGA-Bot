import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_emb(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Наисать от лица бота эмбенд
    """@commands.slash_command(
        name="emb",
        description="A message from the bot's face in the panel | Сообщение от лица бота в панели",
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(administrator=True)
    async def emb(
        self,
        ctx,
        *,
        description: str = commands.Param(
            name="description", description="Enter the text | Введите текст"
        ),
        title=None,
        thumbnail_url=None,
        image_url=None,
        icon_author_url=None,
        name_author=None,
        author_url=None,
        icon_footer_url=None,
        text_footer=None,
        channel: discord.TextChannel = None,
    ):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            try:
                embed = discord.Embed(color=0x2F3136)

                if title != None:
                    embed.title = f"{title}"
                else:
                    pass

                embed.description = f"{description}"

                if icon_author_url and name_author and author_url != None:
                    embed.set_author(
                        name=f"{name_author}", url=author_url, icon_url=icon_author_url
                    )
                elif name_author and author_url != None:
                    embed.set_author(name=f"{name_author}", url=author_url)
                elif name_author != None:
                    embed.set_author(name=f"{name_author}")
                else:
                    pass

                if thumbnail_url != None:
                    embed.set_thumbnail(url=thumbnail_url)
                else:
                    pass

                if image_url != None:
                    embed.set_image(url=image_url)
                else:
                    pass

                if icon_footer_url and text_footer != None:
                    embed.set_footer(text=f"{text_footer}", icon_url=icon_footer_url)
                elif text_footer != None:
                    embed.set_footer(text=f"{text_footer}")
                else:
                    pass
                await ctx.send(f"<a:vega_check_mark:821700784927801394> {get_language(ctx.guild.id,'Действие успешно выполнено!')}", ephemeral=True)
                if channel:
                    await self.client.get_channel(channel.id).send(embed=embed)
                else:
                    await ctx.channel.send(embed=embed)
            except:
                embed = discord.Embed(
                    description=f"**{get_language(ctx.guild.id,'Что-то пошло не так! Проверьте последовательность аргументов или ошибки в написании.')}**",
                    color=0xCC1A1D,
                )
                await ctx.send(embed=embed, ephemeral=True)"""


def setup(client):
    client.add_cog(class_emb(client))
