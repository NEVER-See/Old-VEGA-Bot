import datetime
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as font_manager
import random
import discord
from cache import *

async def send_graph(
    ctx, x, y, title="Простой график, ничего необычного", label_color="white", background_color="#202225", line_color="#e21e1e", xlabel="Время", ylabel="Величина", xfields=None, yfields=None
):
    fe = font_manager.FontEntry(
        fname='fonts\\Rubik-Light.ttf',
        name='Rubik')
    font_manager.fontManager.ttflist.insert(0, fe)
    plt.rcParams['text.color'] = label_color
    plt.rcParams['axes.labelcolor'] = label_color
    plt.rcParams['xtick.color'] = label_color
    plt.rcParams['ytick.color'] = label_color
    plt.rcParams['font.family'] = fe.name
    plt.rcParams['font.size'] = 16
    fig, ax1 = plt.subplots(1, 1)
    ax1.set_facecolor(background_color)
    fig.patch.set_facecolor(background_color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax1.plot(x, y, color=line_color)
    fig.canvas.draw()
    labels = [item.get_text() for item in ax1.get_xticklabels()]
    ax1.set_title(title)
    if xfields:
        labels = xfields
        ax1.set_xticklabels(labels)
    labels = [item.get_text() for item in ax1.get_yticklabels()]
    if yfields:
        labels = yfields
        ax1.set_yticklabels(labels)
    code = ''.join(random.choices("abcdef0123456789", k = 6))
    plt.savefig(os.path.dirname(os.path.realpath(__file__)) + f"\\{code}.png")
    await ctx.send(file=discord.File(os.path.dirname(os.path.realpath(__file__)) + f"\\{code}.png"))
    os.remove(os.path.dirname(os.path.realpath(__file__)) + f"\\{code}.png")