from asyncio.tasks import wait
import discord
from discord.ext import commands
import src.utils
import youtube_dl
import os
from youtubesearchpython import VideosSearch
import src.config as c




bot = commands.Bot(command_prefix = c.config['prefix'])

@bot.event
async def on_connect():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{bot.command_prefix}help"))

@bot.command()
async def r_animal(ctx, text):
    response = src.features.random_animal(animal=text)
    if response == 'host not responding or invalid animal':
        await ctx.send(response)
    else:
        embed = discord.Embed(color = 0xff9900, title = ' ') 
        embed.set_image(url = response) 
        await ctx.send(embed = embed)

@bot.command()
async def r_anime(ctx, text):
    if text == 'quoute':
        response = src.features.random_anime_quote()
        if response == 'error while getting the quoute':
            await ctx.send(response)
        else:
            embed = discord.Embed(color = 0xff9900, title = response['sentence'])
            embed.set_footer(text = 'characther: ' + response['characther'] + ',\nanime: ' + response['anime']) 
            await ctx.send(embed = embed)
    else:
        response = src.features.r_anime(category=text)
        if response == 'host not responding or invalid category':
            await ctx.send(response)
        else:
            embed = discord.Embed(color = 0xff9900, title = ' ') 
            embed.set_image(url = response) 
            await ctx.send(embed = embed)

@bot.command()
async def repeat(ctx, text):
    await ctx.send(text)

@bot.command()
async def short_url(ctx, text):
    response = src.features.shorten_url(text)
    if response == 'invalid url format':
        await ctx.send(response)
    else:
        embed = discord.Embed(color = 0xff9900, title = response)
        await ctx.send(embed = embed)


@bot.command()
async def insult(ctx, text):
    Response = src.features.get_insult(text)
    if Response == 'host not responding or invalid lang':
        await ctx.send(Response)
    else:
        embed = discord.Embed(color = 0xff9900, title = Response)
        await ctx.send(embed = embed)






@bot.command()
async def play(ctx, mode : str, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return
    if mode == '-l':
        url = url
    elif mode == '-s':
        videosSearch = VideosSearch(url, limit = 1).result()
        for item in videosSearch['result']:
            eurl = item['link']
        url = eurl
        print(url)

    voiceChannel = discord.utils.get(ctx.guild.voice_channels)
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()






def run():
    try:
        print('- the bot is runing')
        bot.run(c.config['token'])
    except Exception as error:
        print('failed to run bot due to \n', error)
