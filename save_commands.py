#    role = get(guild.roles, name='Muted')
#    if role == None:
#        role = await guild.create_role(name='Muted', permissions=discord.Permissions.none(), colour=discord.Colour(0x808080))

#    role = get(guild.roles, name='Muted')
#    for i in guild.text_channels:
#        await i.set_permissions(role, send_messages=False, read_messages=False, read_message_history=None, add_reactions=False)
    
#    for i in guild.voice_channels:
#        await i.set_permissions(role, speak=False, read_messages=False)

#    else:
#        embed = discord.Embed(description='<a:vega_check_mark:821700784927801394> Бот ограничил роль `Muted` по каналам!', color=0x43b581)
#        await entry.user.send(embed=embed)
    
#    text_channel = get(guild.text_channels, name='логи-vegabot')
#    if text_channel == None:
#        text_channel = await guild.create_text_channel(name='логи-vegabot')
#        await text_channel.send(f'{guild.owner.mention}, {entry.user.mention}, канал с логами для бота **{client.user.mention}** готов!')
#        await text_channel.set_permissions(guild.default_role, send_messages=False, read_messages=False, add_reactions=False)
#        embed = discord.Embed(description=f'📔 **Информация:**\n\
#            • Вы можете переименовывать канал, изменять его права, но не удаляйте его!\n\n\
#            <a:attention:810912730588512306> **Внимание!**\n\
#            Настоятельно не рекомендуем удалять канал {text_channel.mention}, так как бот перестанет давать информацию о приглашенных ботах и наказаниях!\n\
#            Вам придется заново пригласить бота для создания каналов с логами. В будущем мы сделаем команду пересоздания|перенаправления канала для логов.', color=0xfcc21b)
#        await text_channel.send(embed=embed)
    #with open('json/logchannel.json', 'r') as f:
        #data = json.load(f)
#    data = gdata('vega', 'logchannel')
#    data[str(guild.id)] = text_channel.id
    #with open('json/logchannel.json', 'w') as f:
        #json.dump(data, f)
#    wdata('vega', 'logchannel', data)





#Активные и неактивные настройки
#@client.command(name="stg", aliases=["settings", "настройки"])
#@commands.guild_only()
#@commands.cooldown(1, 20, commands.BucketType.member)
#async def stg(ctx, help=None):
#    if await checkchannel(ctx):
#        lc = gdata('vega', 'logchannel')
#        ch = gdata('vega', 'channel_rights')
#        mr = gdata('vega', 'muterole')
#
#        channel1 = []
#        channel2 = []
#        imr = []
#        if str(ctx.guild.id) in lc:
#            for channel in lc[str(ctx.guild.id)].split(' '):
#                try:
#                    c = client.get_channel(int(channel))
#                    channel1.append(c.mention)
#                except:
#                    pass

#        if str(ctx.guild.id) in ch:
#            for channel in ch[str(ctx.guild.id)].split(' '):
#                try:
#                    c = client.get_channel(int(channel))
#                    channel2.append(c.mention)
#                except:
#                    pass

#        if str(ctx.guild.id) in mr:
#            for bot in mr[str(ctx.guild.id)].split(' '):
#                try:
#                    b = client.get_user(int(bot))
#                    imr.append(b.mention)
#                except:
#                    pass
        
#        embed = discord.Embed(title='Настройки бота:', color=0x2f3136)
#        if len(channel1) == 0:
#            embed.description = 'Канал не указан!'
#        else:
#            embed.description = ', '.join(channel1) # если надо в столбик, то '\n'.join(channels)
#        if len(channel2) == 0:
#            embed.description = 'Канал не указан!'
#        else:
#            embed.description = ', '.join(channel2)
#        if len(imr) == 0:
#            embed.description = 'Канал не указан!'
#        else:
#            embed.description = ', '.join(imr)
#        await ctx.send(embed=embed)
#    else:
#        embed = discord.Embed(description=f'<a:attention:810912730588512306> Эта команда доступна только в определенных каналах!', color=0xfcc21b)
#        await ctx.send(embed=embed, delete_after=5.0)



#Сброс прав бота по каналам
#@client.command(name="reset", aliases=["сброс"])
#@commands.guild_only()
#@commands.cooldown(1, 300, commands.BucketType.member)
#async def reset(ctx, guild=None):
#    if await checkchannel(ctx):
#        if ctx.author == ctx.guild.owner:
#            guild = ctx.guild
#            if guild is not None:
#                if not ctx.guild.get_member(client.user.id).guild_permissions.administrator:
#                    msg = ctx.message
#                    await msg.add_reaction('<a:attention:810912730588512306>')
#                    embed = discord.Embed(description='<a:attention:810912730588512306> **У бота отсутствует право Администратора!**', color=0xfcc21b)
#                    await ctx.send(embed=embed, delete_after=8.0)

#                else:
#                    msg = ctx.message
#                    await msg.add_reaction('♨️')
#
#                    embed = discord.Embed(description='Пожалуйста подождите, выполняется настройка прав...', color=0xf4900c)
#                    msg = await ctx.send(embed=embed)
#                    new = await ctx.channel.fetch_message(msg.id)

            
#                    role = get(ctx.guild.roles, name='Muted')
#                    if role == None:
#                        role = await ctx.guild.create_role(name='Muted', permissions=discord.Permissions.none(), colour=discord.Colour(0x808080))

#                    role = get(guild.roles, name='Muted')
#                    for i in guild.text_channels:
#                        await i.set_permissions(role, send_messages=False, read_messages=False, read_message_history=None, add_reactions=False)

#                    for i in guild.voice_channels:
#                        await i.set_permissions(role, speak=False)
            
#                    else:
#                        user = ctx.guild.get_member(client.user.id)
#                        msg = ctx.message
#                        await msg.remove_reaction(member=user, emoji='♨️')
#                        await msg.add_reaction('<a:vega_check_mark:821700784927801394>')
#                        await asyncio.sleep(5)

        #                await new.delete() #удаляет сообщение бота


#                        embed = discord.Embed(description='\
#                            Выполняется проверка:\n\
#                            <:l_vega_s:810834352865935370><:e_vega_s:810834352694362113>                       `[20%]`\nПожалуйста подождите...', color=0xf4900c)
#                        await new.edit(embed=embed)

#                        await asyncio.sleep(3)

#                        embed = discord.Embed(description='\
#                            Выполняется проверка:\n\
#                            <:l_vega_s:810834352865935370><:c_vega_s:810834352820715550><:e_vega_s:810834352694362113>                      `[30%]`\nПожалуйста подождите...', color=0xf4900c)
#                        await new.edit(embed=embed)

#                        await asyncio.sleep(3)

#                        embed = discord.Embed(description='\
#                            Выполняется проверка:\n\
#                            <:l_vega_s:810834352865935370><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:e_vega_s:810834352694362113>            `[60%]`\nПожалуйста подождите...', color=0xf4900c)
#                        await new.edit(embed=embed)

#                        await asyncio.sleep(2)

#                        embed = discord.Embed(description='\
#                            Выполняется проверка:\n\
#                            <:l_vega_s:810834352865935370><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:e_vega_s:810834352694362113>     `[90%]`\nПожалуйста подождите...', color=0xf4900c)
#                        await new.edit(embed=embed)

#                        await asyncio.sleep(2)

#                        embed = discord.Embed(description='\
#                            Выполняется проверка:\n\
#                            <:l_vega_s:810834352865935370><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:c_vega_s:810834352820715550><:e_vega_s:810834352694362113> `[100%]`\nПожалуйста подождите...', color=0xf4900c)
#                        await new.edit(embed=embed)

#                        await asyncio.sleep(3)

#                        embed = discord.Embed(description='<a:vega_check_mark:821700784927801394> **Проверка завершена!**', color=0x43b581)
#                        await new.edit(embed=embed, delete_after=5.0)
                


#                        embed = discord.Embed(description='<a:vega_check_mark:821700784927801394> **Роль `Muted` восстановлена по умолчанию!**', color=0x43b581)
#                        await ctx.author.send(embed=embed)
#        else:
#            embed = discord.Embed(description='<a:attention:810912730588512306> **Вы не являетесь Владельцем данного сервера!**', color=0xfcc21b)
#            await ctx.send(embed=embed, delete_after=10.0)
#    else:
#        embed = discord.Embed(description=f'<a:attention:810912730588512306> Эта команда доступна только в определенных каналах!', color=0xfcc21b)
#        await ctx.send(embed=embed, delete_after=5.0)






#Кнопки для теста
#@client.command()
#async def thelp(ctx):
#    embed = discord.Embed(title='🔧 Список доступных команд:', description=f'Префикс на сервере: `{ctx.prefix}`\nУзнать информацию о группе: `{ctx.prefix}help [*группа]`\nУзнать информацию о команде: `{ctx.prefix}help [команда]`', color=0xe21e1e)
#    embed.add_field(name='❓ *Информация (`v!help *info`):', value=f'`ping` `info` `stats` `server` `links` `invite` `wlbots` `list` `say`', inline=False)
#    embed.add_field(name='*Для Владельца (`v!help *owner`):', value=f'`rgive` `rselect` `antibot` `antiinvite` `ignore` `delchannels` `delroles`', inline=False)
#    embed.add_field(name='*Для Администратора (`v!help *admin`):', value=f'`prefix` `log` `channel` `rmute` `clear` `uclear` `echo` `emb` `slowmode`', inline=False)
#    embed.add_field(name='*Для Модератора (`v!help *moder`):', value=f'`checkwl` `ban` `unban` `kick` `rolen` `user` `mute` `unmute`', inline=False)
#    embed.add_field(name='*Веселье (`v!help *fun`):', value=f'`8ball` `avatar` `emoji` `rand` `calc`', inline=False)
#    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
#    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar_url,\
#        text='NEVER See#9278 © 2021 Все права защищены!')
#    msg = await ctx.send(embed=embed, buttons=[
#        Button(style=ButtonStyle.emoji, label="❓"),
#        Button(style=ButtonStyle.URL, label="📚 Документация", url="https://never-see.gitbook.io/vega-bot/v/russian/"),
#        Button(style=ButtonStyle.URL, label="🌐 Сайт", url="https://vegabot.xyz/vegabot")
#    ])
#    res = await ddb.wait_for_button_click(msg)
#    await res.respond(type = InteractionType.IgnoredChannelMessageWithSource, content="Что за хуйня блять, пошли в пизду!")
#    if res.button.label == "❓":
#        обязательный_параметр = '{**_обязательный параметр_**}'
#        embed = discord.Embed(title='❓ Группа: Информация', description=f'> **{обязательный_параметр}**ㅤ**[**_необязательный параметр_**]**\n\n• Узнать информацию о команде: `{ctx.prefix}help [команда]`', color=0xd81911)
#        embed.add_field(name='Команды:', value=f'`{ctx.prefix}ping` — пинг бота и состояние шардов.\n`{ctx.prefix}info` — информация о боте.\n`{ctx.prefix}stats` — статистика бота.\n`{ctx.prefix}server` — информация о сервере.\n`{ctx.prefix}links` — полезные ссылки.\n\
#        `{ctx.prefix}invite` — пригласить бота.\n`{ctx.prefix}wlbots` — проверить бота в белом списке.\n`{ctx.prefix}list` — посмотреть ограниченные каналы и игнорируемых ботов.\n`{ctx.prefix}say` — отправить сообщение разработчику.', inline=False)
#        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
#        embed.set_footer(icon_url=client.get_user(351020816466575372).avatar_url,\
#            text='NEVER See#9278 © 2021 Все права защищены!')
#        await ctx.send(embed=embed, buttons=[
#            Button(style=ButtonStyle.URL, label="📚 Документация", url="https://never-see.gitbook.io/vega-bot/v/russian/"),
#            Button(style=ButtonStyle.URL, label="🌐 Сайт", url="https://vegabot.xyz/vegabot")
#        ])
#    else:
#        await ctx.send('Ладно, забей)')




#Тестовая команда
#@client.command(name='test', aliases=["тест"], pass_context=True)
#@commands.guild_only()
#@commands.bot_has_permissions(send_messages=True)
#async def test(ctx):
#    img = Image.open('images/raw.png') #фон
#    draw = ImageDraw.Draw(img)
#    font = ImageFont.truetype('arial.ttf', size=25)
#    color = 'rgb(255, 255, 255)'
#    draw.text((150, 200), 'Тестовая команда!', fill=color, font=font)
#    img.save('images/image.png')
#    file = discord.File("images/image.png", filename="images/image.png")
#
#    await ctx.send(file=file)





#@client.command(aliases=['mb', 'mass-ban'])
#@commands.cooldown(1, 150, commands.BucketType.member)
#@commands.has_permissions(administrator=True)
#async def massban(ctx, users: commands.Greedy[discord.User], time1: typing.Optional[str] = '0s', *, reason = None):
#    def check(ctx, member):
#        if ctx.guild.get_member(member.id):
#            m = ctx.guild.get_member(member.id)
#            return member.top_role >= ctx.author.top_role
#        return member != ctx.author and member.id != client.user.id
#    if len(users) > 50:
#        await messages.err(ctx, "Вы можете забанить за раз не более 50 пользователей.", True)
#    else:
#        if word.ishs(time1):
#            tc = word.string_to_seconds(time1)
#        else:
#            tc = 0
#            if reason is not None:
#                reason = time1 + ' ' + reason

#        if reason is None:
#            reason1 = 'Не указана'
#            reason2 = 'Причина не указана'
#        else:
#            reason1, reason2 = reason, reason

#        embed = discord.Embed()
#        embed.color = Color.danger
#        banned = 0
#        await ctx.send(':hourglass_flowing_sand:')
#        if tc == 0:
#            embed.title = f"<:ban:810927364707713025> | "
#            tc = 228133722
#        for user in users:
#            if check(ctx, user):
#                try:
#                    if tc != 228133722:
#                        await user.ban(reason=f'Массовый бан от {ctx.author}: {reason2} | {word.hms(tc)}')
#                        #await punishments.tempban(ctx, user, tc)
#                    else:
#                        await user.ban(reason=f'Массовый бан от {ctx.author}: {reason2}')
#                    banned += 1
#                    await asyncio.sleep(2)
#                except:
#                    pass
        
#        if banned > 0:
#            if tc == 228133722:
#                embed.title = f"<:ban:810927364707713025> | {banned} {word.word_correct(banned, 'пользователь был забанен', 'пользователя были забанены', 'пользователей были забанены')}"
#                embed.description = f'''
#**Модератор:** {ctx.author} ({ctx.author.mention})
#**Причина:** {reason1}
#                '''
#            else:
#                embed.title = f"<:ban:810927364707713025> | {banned} {word.word_correct(banned, 'пользователь был временно забанен', 'пользователя были временно забанены', 'пользователей были временно забанены')}"
#                embed.description = f'''
#**Модератор:** {ctx.author} ({ctx.author.mention})
#**Время:** {word.hms(float(tc))}
#**Причина:** {reason1}
#                '''
#        else:
#            embed.title = ":x: | Никто не был забанен"
#            embed.description = f'**Модератор:** {ctx.author} ({ctx.author.mention})'
        
#        await ctx.send(embed=embed)





#Временный бан пользователя
#@client.command(name='tban', aliases=["тбан"], pass_context = True)
#@commands.guild_only()
#@commands.bot_has_permissions(kick_members=True, send_messages=True)
#@commands.has_permissions(ban_members=True)
#async def tban(ctx, member:discord.Member, time:int, *, reason):
#    user = ctx.author
#    if member == user:
#        await ctx.send('\⚠️ Невозможно забанить себя!', delete_after=7.0)
#    elif user.top_role <= member.top_role:
#        await ctx.send('\⚠️ Невозможно забанить пользователя, роль которого выше или равна вашей!', delete_after=15.0)
#    else:
#        emb = discord.Embed(title="\🚫 Временный Бан", color=0xf04747)
#        emb.add_field(name='Модератор:', value=f'{ctx.message.author.mention}\n{user}', inline=True)
#        emb.add_field(name='Нарушитель:', value=f'{member.mention}\n{member}', inline=True)
#        emb.add_field(name='Причина:', value=reason, inline=False)
#        emb.add_field(name='Время:', value=f"`{time} мин`", inline=False)
#        await member.send(f'\🚫 **{user}** забанил(а) вас на сервере **{ctx.guild.name}**.\nДо разбана осталось:` {time} мин `\n**Причина:** {reason}')
#        await ctx.guild.ban(member, reason=reason)
#        await member.ban()
#        await ctx.send(embed=emb)
#        await asyncio.sleep(time * 60)
#        await member.unban()





#Занести или удалить бота из белого списка ид канала: 806889107594674236
#@client.command()
#@commands.cooldown(1, 10, commands.BucketType.member)
#@commands.guild_only()
#async def wl(ctx, option, user:int):
#    if ctx.author.id == 351020816466575372:
#        w = gdata('vega', 'wlbots')
#        if option.lower() == 'add':
#            if not str(user) in w:
#                w.update({str(user) + ' '})
#                embed = discord.Embed(description=f'<a:vega_check_mark:821700784927801394> Бот **{user}** занесен в белый список!', color=0x43b581)
#                await ctx.send(embed=embed, delete_after=12.0)
#                await client.get_channel(806889107594674236).send(embed=embed)
#            else:
#                embed = discord.Embed(description=f'<a:vega_x:810843492266803230> Бот **{user}** уже есть в списке!', color=0xcc1a1d)
#                await ctx.send(embed=embed, delete_after=10.0)
#        elif option.lower() == 'remove':
#            if str(user) in w:
#                requests.get({str(user), ''})
#                embed = discord.Embed(description=f'<a:attention:810912730588512306> Бот **{user}** удален из белого списка!', color=0xfcc21b)
#                await ctx.send(embed=embed, delete_after=12.0)
#                await client.get_channel(806889107594674236).send(embed=embed)
#            else:
#                embed = discord.Embed(description=f'<a:vega_x:810843492266803230> Бот **{user}** не найден!', color=0xcc1a1d)
#                await ctx.send(embed=embed, delete_after=10.0)
#        else:
#            embed = discord.Embed(title=f'<a:attention:810912730588512306> Неизвестная опция!', color=0xfcc21b)
#            await ctx.send(embed=embed, delete_after=8.0)
#        wdata('vega', 'wlbots', w)
#    else:
#        pass





#для белого списка ботов
#async def refreshwl():
#    global whitelistedbot
#    while True:
#        try:
#            whitelistedbot = requests.get('https://vegabot.xyz/vegabot/data/whitelist.data').text.split('\n')
#        except:
#            pass
#        await asyncio.sleep(40)

#client.loop.create_task(refreshwl())





#Команда для кика бота с сервера
#@client.command()
#async def leave(ctx, VEGA, guild=None):
#    if ctx.author.id == 351020816466575372:
#        if guild == None:
#
#            user = ctx.author
#            msg = ctx.message
#            await msg.add_reaction('<a:vega_check_mark:821700784927801394>')
#
#            await ctx.guild.leave()
#        else:
#            guild = client.get_guild(int(guild))
#            await guild.leave()
#
#            user = ctx.author
#            msg = ctx.message
#            await msg.add_reaction('<a:vega_check_mark:821700784927801394>')