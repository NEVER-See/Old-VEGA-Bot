import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Аватар пользователя
    @commands.slash_command(
        name="avatar",
        description="View the avatar (of the user) | Посмотреть аватар (пользователя)",
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    async def avatar(self, inter, *,
        user: discord.Member = None,
    ):
        ctx = inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if user == None:
                user = ctx.author
            try:
                try:
                    description0 = f'<:user:842445581426753606>ㅤ[png]({user.avatar.replace(size=1024, format="png")}) | [jpg]({user.avatar.replace(size=1024, format="jpg")}) | [webp]({user.avatar.replace(size=1024, format="webp")}) | [gif]({user.avatar.replace(size=1024, format="gif")})'
                except:
                    description0 = f'<:user:842445581426753606>ㅤ[png]({user.avatar.replace(size=1024, format="png")}) | [jpg]({user.avatar.replace(size=1024, format="jpg")}) | [webp]({user.avatar.replace(size=1024, format="webp")})'
                if user.avatar != user.display_avatar:
                    try:
                        description1 = f'\n\n<:servers:842447666625773568>ㅤ[png]({user.display_avatar.replace(size=1024, format="png")}) | [jpg]({user.display_avatar.replace(size=1024, format="jpg")}) | [webp]({user.display_avatar.replace(size=1024, format="webp")}) | [gif]({user.display_avatar.replace(size=1024, format="gif")})'
                    except:
                        description1 = f'\n\n<:servers:842447666625773568>ㅤ[png]({user.display_avatar.replace(size=1024, format="png")}) | [jpg]({user.display_avatar.replace(size=1024, format="jpg")}) | [webp]({user.display_avatar.replace(size=1024, format="webp")})'
                else:
                    description1 = ""
                embed = discord.Embed(
                    description=f"{description0}{description1}", color=0x2F3136
                )
                if user.avatar == user.display_avatar:
                    embed.set_author(
                        name=f"{get_language(ctx.guild.id,'Аватар:')} {user}",
                        icon_url=user.avatar.replace(size=1024, format="gif"),
                    )
                    embed.set_image(
                        url=user.avatar.replace(size=1024, format="gif")
                    )
                else:
                    embed.set_author(
                        name=f"{get_language(ctx.guild.id,'Аватар:')} {user}",
                        icon_url=user.display_avatar.replace(
                            size=1024, format="gif"
                        ),
                    )
                    embed.set_thumbnail(url=user.avatar.replace(size=1024))
                    embed.set_image(
                        url=user.display_avatar.replace(size=1024, format="gif")
                    )
            except:
                try:
                    description0 = f'<:user:842445581426753606>ㅤ[png]({user.avatar.replace(size=1024, format="png")}) | [jpg]({user.avatar.replace(size=1024, format="jpg")}) | [webp]({user.avatar.replace(size=1024, format="webp")}) | [gif]({user.avatar.replace(size=1024, format="gif")})'
                except:
                    description0 = f'<:user:842445581426753606>ㅤ[png]({user.avatar.replace(size=1024, format="png")}) | [jpg]({user.avatar.replace(size=1024, format="jpg")}) | [webp]({user.avatar.replace(size=1024, format="webp")})'
                if user.avatar != user.display_avatar:
                    try:
                        description1 = f'\n\n<:servers:842447666625773568>ㅤ[png]({user.display_avatar.replace(size=1024, format="png")}) | [jpg]({user.display_avatar.replace(size=1024, format="jpg")}) | [webp]({user.display_avatar.replace(size=1024, format="webp")}) | [gif]({user.display_avatar.replace(size=1024, format="gif")})'
                    except:
                        description1 = f'\n\n<:servers:842447666625773568>ㅤ[png]({user.display_avatar.replace(size=1024, format="png")}) | [jpg]({user.display_avatar.replace(size=1024, format="jpg")}) | [webp]({user.display_avatar.replace(size=1024, format="webp")})'
                else:
                    description1 = ""
                embed = discord.Embed(
                    description=f"{description0}{description1}", color=0x2F3136
                )
                embed.set_author(
                    name=f"{get_language(ctx.guild.id,'Аватар:')} {user}",
                    icon_url=user.avatar.replace(size=1024, format="png"),
                )
                if user.avatar == user.display_avatar:
                    embed.set_author(
                        name=f"{get_language(ctx.guild.id,'Аватар:')} {user}",
                        icon_url=user.avatar.replace(size=1024, format="png"),
                    )
                    embed.set_image(
                        url=user.avatar.replace(size=1024, format="png")
                    )
                else:
                    embed.set_author(
                        name=f"{get_language(ctx.guild.id,'Аватар:')} {user}",
                        icon_url=user.display_avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_thumbnail(url=user.avatar.replace(size=1024))
                    embed.set_image(
                        url=user.display_avatar.replace(size=1024, format="png")
                    )
            # embed.set_image(url=user.avatar.replace(format=None, size=1024))
            # embed.set_footer(icon_url=ctx.author.avatar(format="png", size=1024), text=f'{ctx.author}')
            await ctx.send(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(class_avatar(client))
