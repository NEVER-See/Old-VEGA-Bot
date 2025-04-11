import disnake as discord
import random

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_8ball(commands.Cog):
    def __init__(self, client):
        self.client = client

    # шар
    @commands.slash_command(
        name="8ball", description="Ask the balloon a question | Задайте вопрос шару"
    )
    async def _8ball(
        self,
        inter,
        *,
        question: str = commands.Param(
            name="question",
            description="Ask the balloon a question | Задайте вопрос шару",
        ),
    ):
        ctx = inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if question is not None:
                if question:
                    user = ctx.author
                    responses = [
                        f"{get_language(ctx.guild.id,'это несомненно 👌')}",
                        f"{get_language(ctx.guild.id,'это определенно так.')}",
                        f"{get_language(ctx.guild.id,'без сомнения 👌')}",
                        f"{get_language(ctx.guild.id,'определенно - да!')}",
                        f"{get_language(ctx.guild.id,'вероятнее всего.')}",
                        f"{get_language(ctx.guild.id,'хорошие перспективы 👌')}",
                        f"{get_language(ctx.guild.id,'да 👍')}",
                        f"{get_language(ctx.guild.id,'признаки указывают на Да.')}",
                        f"{get_language(ctx.guild.id,'ответ туманный, попробуйте задать другой вопрос.')}",
                        f"{get_language(ctx.guild.id,'спроси позже.')}",
                        f"{get_language(ctx.guild.id,'не буду говорить об этом.')}",
                        f"{get_language(ctx.guild.id,'сейчас не могу подсказать.')}",
                        f"{get_language(ctx.guild.id,'сосредоточься и спроси еще раз.')}",
                        f"{get_language(ctx.guild.id,'не рассчитывай на это 👎')}",
                        f"{get_language(ctx.guild.id,'мои источники говорят, что Нет.')}",
                        f"{get_language(ctx.guild.id,'перспективы не очень хорошие 👎')}",
                        f"{get_language(ctx.guild.id,'очень сомнительно.')}",
                        f"{get_language(ctx.guild.id,'нет <a:vega_x:810843492266803230>')}",
                    ]
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'Вопрос:')}",
                        description=f"{question}\n\n**{get_language(ctx.guild.id,'Ответ:')}**\n\🎱 {user.mention}, {random.choice(responses)}",
                        color=0x2F3136,
                    )
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Задайте вопрос!')}",
                    color=0x8899A6,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Описание:')}",
                    value=f"{get_language(ctx.guild.id,'Задайте вопрос шару и узнайте правду.')}",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                    value=f"`{get_language(ctx.guild.id,'{текст}')}`",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Пример:')}",
                    value=f"{ctx.prefix}8ball {get_language(ctx.guild.id,'Завтра будет ясная погода?')}",
                    inline=False,
                )
                await ctx.send(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(class_8ball(client))
