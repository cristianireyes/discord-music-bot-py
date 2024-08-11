import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import os
import functools  # Importa functools para ejecutar funciones bloqueantes en un ejecutor

intents = discord.Intents.default()
intents.message_content = True
token = os.environ['BOT_TOKEN']

bot = commands.Bot(command_prefix='-', intents=intents) 

ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'auto',
    'quiet': True,
    'extract_flat': 'in_playlist',
    'no_warnings': True,
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        to_run = functools.partial(ytdl.extract_info, url, download=False)
        data = await loop.run_in_executor(None, to_run)
        
        if 'entries' in data:
            print(data)
            data = data['entries'][0]
        print(data['id'])
        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.command(name='play', help='Reproduce una canción de YouTube')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send("¡Debes estar en un canal de voz para usar este comando!")
        return

    channel = ctx.message.author.voice.channel

    try:
        
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            await channel.connect()
            voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
        async with ctx.typing():
            player = await YTDLSource.from_url(url)
            voice_client.play(player, after=lambda e: print(f'Error: {e}') if e else None)
            await ctx.send(f'Ahora reproduciendo: {player.title}')
    except discord.errors.Forbidden:
      await ctx.send("No tengo permiso para conectarme o hablar en este canal de voz.")
    except discord.errors.ClientException as e:
        await ctx.send(f"Error de cliente: {str(e)}")

@bot.command(name='stop', help='Detiene la reproducción y desconecta el bot')
async def stop(ctx):
    try:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_client:
            await voice_client.disconnect()
            await ctx.send("¡Detenido y desconectado del canal de voz!")
    except discord.errors.Forbidden:
        await ctx.send("No tengo permiso para desconectarme de este canal de voz.")


bot.run(token)
