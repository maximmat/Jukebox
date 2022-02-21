import discord
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch
import asyncio
from time import sleep

client = commands.Bot(command_prefix='.')

queue = []

client.remove_command('help')

@client.event  
async def on_ready():
	print('Bot online')

@client.command()
async def join(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()

@client.command()
async def leave(ctx):
	await ctx.voice_client.disconnect()

@client.command()
async def lg(ctx):
	url = "https://www.youtube.com/watch?v=iuJDhFRDx9M"
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		
	YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', "cachedir": "False"}
	FFMPEG_OPTIONS = {
		'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
	voice = get(client.voice_clients, guild=ctx.guild)

	if not voice.is_playing():
		with YoutubeDL(YDL_OPTIONS) as ydl:
			info = ydl.extract_info(url, download=False)
		URL = info['url']
		voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
		voice.is_playing()
		await ctx.send('Song for LG')

	while voice.is_playing(): 
		await asyncio.sleep(1) 
	else:
		 
		while voice.is_playing(): 
			break 
		else:
			await asyncio.sleep(900)
			await voice.disconnect() 

@client.command()
async def play(ctx, *, search):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		
	YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', "cachedir": "False", 'cookiefile': '/home/pi/dc_bots/jukebox#0466/YT-cookies.txt'}
	FFMPEG_OPTIONS = {
		'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

	voice = get(client.voice_clients, guild=ctx.guild)

	videoSearch = VideosSearch(search, limit = 1)

	for i in range(1):
		url = videoSearch.result()["result"][i]["link"]
		name = videoSearch.result()["result"][i]["title"]
		await ctx.send(name)
		await ctx.send(url)

	if not voice.is_playing():
		await ctx.send('Are you ready?')    
		with YoutubeDL(YDL_OPTIONS) as ydl:
			info = ydl.extract_info(url, download=False)
		URL = info['url']
		voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
		voice.is_playing()
		await ctx.send("Let's go!!!")
	else:
		queue.append(url)
		await ctx.send(name + " added to queue.")

	while voice.is_playing(): 
		await asyncio.sleep(1)
			
	if queue:
		url = queue[0]

		with YoutubeDL(YDL_OPTIONS) as ydl:
			info = ydl.extract_info(url, download=False)

		URL = info['url']
		voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
		voice.is_playing()
		queue.pop(0)
	else:  
		await asyncio.sleep(500) 
		while voice.is_playing(): 
			  break 
		else:
			await voice.disconnect()
		 
@client.command()
async def stop(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice.is_playing():
		voice.stop()
		await ctx.send("Is this end?")
		await voice.disconnect()

@client.command(name="next", aliases=["skip"])
async def next(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)

	if queue:
		voice.stop()
		await ctx.send("Playing next song.")

	else:
		await ctx.send("queue is empty.")

@client.command()
async def help(ctx):
	await ctx.send("play 'song name' - Play song\njoin - Join VC\nleave - Leave VC\nstop - Stop song\nskip/next - Skip song")

client.run(TOKEN)