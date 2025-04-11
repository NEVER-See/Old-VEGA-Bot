import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_wlbots(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Скачать или посмотреть белый список ботов
    @commands.slash_command(
        name="wlbots", description="White list of bots | Белый список ботов"
    )
    @commands.cooldown(1, 20, commands.BucketType.member)
    @commands.guild_only()
    async def wlbots(self, ctx):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            # try:
            wl = wlbotsdata
            s_wlbots = []
            if "Bots" in wl[0]:
                for a_wlbots in wl[0]["Bots"]:
                    try:
                        wlb = self.client.get_user(a_wlbots)
                        s_wlbots.append(wlb.id)
                    except:
                        pass

            # wlbots0 = wl[0, {'Bots'}]
            # wlbots0 = wlbots0[0:-2] — удаляет последние 2 символа
            embed = discord.Embed(
                description=f"🔗 [{get_language(ctx.guild.id,'Окрыть белый список ботов')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots')})",
                color=0x2F3136,
            )

            def TripleID(l):
                a = ''.join(l)
                b = ''
                cnt = 0
                for i in a:
                    if i == ',':
                        cnt += 1
                    if cnt == 5 and i == ' ':
                        i = '*'
                        cnt = 0
                    b += i
                    d = b.split('*')
                return '\n'.join(d)
                
            with open("wlbots.txt", "w") as file:
                file.write(TripleID(str(s_wlbots)[1: -1]))
                # file.write(f"{wlbots0}")
            with open("wlbots.txt", "rb") as file:
                await ctx.author.send(
                    f"**{get_language(ctx.guild.id,'📔 Белый список ботов:')}**",
                    embed=embed,
                    file=discord.File(file, "wlbots.txt"),
                )
            await ctx.send(
                f"🎫  {(ctx.author.mention)}, {get_language(ctx.guild.id,'я отправил информацию тебе в личку.')}",
                ephemeral=True,
            )
            # except:
            #    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: **Cообщение небыло доставлено!**')}\n{get_language(ctx.guild.id,'Пожалуйста, включите доступ на отправку личных сообщений.')}\n— {get_language(ctx.guild.id,'Проверьте, не заблокирован ли у вас бот?')}\n\n[<:discord:848272401913217075> support.discord.com]({get_language(ctx.guild.id,'https://support.discord.com/hc/ru/articles/217916488-Блокировка-Настройки-Конфиденциальности')})", color=0xfcc21b)
            #    embed.set_image(url=f"{get_language(ctx.guild.id,'https://media.discordapp.net/attachments/713751423128698950/859751617942519878/unknown.png')}")
            #    await ctx.message.reply(embed=embed, delete_after=25.0)
            #    ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_wlbots(client))
