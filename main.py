import discord
from discord.ext import commands
import json  
import asyncio
import ffmpeg
from discord import FFmpegPCMAudio
#import wget
import requests


file = open('config.json' , 'r')
config = json.load(file)

intents = discord.Intents.all()

bot = commands.Bot(config["prefix"], intents=intents)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f'{ctx.author.mention}нет')

@bot.command(name="play")
async def play(ctx, *args):
    # Проверяем, что пользователь находится в голосовом канале
    if ctx.author.voice is None:
        await ctx.send("Вы не находитесь в голосовом канале.")
        return
    try:
        await ctx.voice_client.disconnect()
    except:
        pass
    

    link = None
    for arg in args:
        if arg.startswith('-l='):
            link = arg[3:]
    
    if link is None:
        await ctx.send("Вы не указали ссылку на аудиофайл.")
        return

    print(link)
    filename = link.split("/")[-1]
    #print(filename)
    r = requests.get(link, allow_redirects = True)
    open(filename, "wb").write(r.content)
 

    # Подключаемся к голосовому каналу пользователя
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()



    # Создаем плеер и запускаем проигрывание аудио
    abssa =  FFmpegPCMAudio(filename, executable='/ffmpeg')
    vc.play(abssa)

    # Ждем, пока аудио не закончится
    while vc.is_playing():
        await asyncio.sleep(1)

    # Отключаемся от голосового канала
    await vc.disconnect()




@bot.command(name="play_radio")
async def play_radio(ctx, r_name):
    # Проверяем, что пользователь находится в голосовом канале
    if ctx.author.voice is None:
        await ctx.send("Вы не находитесь в голосовом канале.")
        return

    try:
        await ctx.voice_client.disconnect()
    except:
        pass

    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()

    with open('r-list.json' ,encoding="utf-8") as f:
        data = json.load(f)

    if r_name in data:
        abssa = FFmpegPCMAudio(data[r_name], executable='/ffmpeg')
        vc.play(abssa)

        while vc.is_playing():
            await asyncio.sleep(1)

        # Отключаемся от голосового канала
        await vc.disconnect()
    else:
        await ctx.send(f"Радиостанция {r_name} не найдена в списке.")
        stations = "\n".join(data.keys())
        await ctx.send(f"Список всех радиостанций:\n{stations}")
        await vc.disconnect()


@bot.command(name="stop")
async def stop(ctx):

    if ctx.voice_client is None:
        await ctx.send("Бот не находится в голосовом канале.")
        return
    await ctx.voice_client.disconnect()














bot.run(config['token'])
