import disnake as discord
import disnake

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class links(disnake.ui.View):
    def __init__(self, ctx):
        super().__init__()

        url = f"{get_language(ctx.guild.id,'https://discord.com/invite/8YhmtsYvpK')}"
        self.add_item(
            disnake.ui.Button(
                label=f"{get_language(ctx.guild.id,'🔗 Сервер поддержки')}", url=url
            )
        )

        url1 = f"{get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian-language/')}"
        self.add_item(
            disnake.ui.Button(
                label=f"{get_language(ctx.guild.id,'📚 Документация')}", url=url1
            )
        )

        url2 = "https://vega-bot.ru/"
        self.add_item(
            disnake.ui.Button(label=f"{get_language(ctx.guild.id,'🌐 Сайт')}", url=url2)
        )


class class_links(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Ссылки
    @commands.slash_command(name="links", description="Useful links | Полезные ссылки")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def links(self, ctx):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            try:
                await ctx.author.send(
                    f"{get_language(ctx.guild.id,'Полезные ссылки:')}",
                    view=links(ctx),
                )
                await ctx.send(
                    f"🎫  {ctx.author.mention}, {get_language(ctx.guild.id,'я отправил информацию тебе в личку.')}",
                    ephemeral=True,
                )

            except:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: **Cообщение небыло доставлено!**')}\n{get_language(ctx.guild.id,'Пожалуйста, включите доступ на отправку личных сообщений.')}\n— {get_language(ctx.guild.id,'Проверьте, не заблокирован ли у вас бот?')}\n\n[support.discord.com]({get_language(ctx.guild.id,'https://support.discord.com/hc/ru/articles/217916488-Блокировка-Настройки-Конфиденциальности')})",
                    color=0xFCC21B,
                )
                embed.set_image(
                    url=f"{get_language(ctx.guild.id,'https://media.discordapp.net/attachments/713751423128698950/859751617942519878/unknown.png')}"
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_links(client))
