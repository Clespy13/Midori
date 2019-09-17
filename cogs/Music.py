import discord
import asyncio
import youtube_dl
import os
import random
import threading

from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from PyLyrics import *

songs = asyncio.Queue()
play_next_song = asyncio.Event()
current = None
volume = 0.7
vid = []
task = None
loop_bool = False
queueloop = False
i = 1

ytdl_opts = {
'format': 'bestaudio/best',
'extractaudio': True,
'audioformat': 'mp3',
'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
'restrictfilenames': True,
'noplaylist': True,
'nocheckcertificate': True,
'ignoreerrors': False,
'logtostderr': False,
'quiet': True,
'no_warnings': True,
'default_search': 'auto',
'source_address': '0.0.0.0',
}

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -loglevel quiet',
}

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players = {}
        self.voters = []
        vc = None

    async def audio_player_task():
        while True:
            play_next_song.clear()
            current = await songs.get()

            try:
                vc.play(discord.FFmpegPCMAudio(current[0]["url"], **ffmpeg_opts), after=lambda e: Music.toggle_next())
            except IndexError:
                return

            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = volume

            await play_next_song.wait()


    def toggle_next():
        global loop_bool
        global queueloop
        global i

        paused = True

        if loop_bool:
            vc.play(discord.FFmpegPCMAudio(vid[0]["url"], **ffmpeg_opts), after=lambda e: Music.toggle_next())
        elif queueloop:
            number_of_tarcks = len(vid)
            m = list(range(0, int(number_of_tarcks)))

            try:
                song = m[i]
            except IndexError:
                i = 0
                song = m[i]

            vc.play(discord.FFmpegPCMAudio(vid[song]["url"], **ffmpeg_opts), after=lambda e: Music.toggle_next())
            i += 1

        else:
            vid.remove(vid[0])
            play_next_song.set()


    @commands.command(aliases=["join", "summon"])
    async def connect(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send("No channel to join. Please specify a channel or join one.")
                return

        vc = ctx.voice_client

        if vc:
            if vc.id == channel.id:
                return
            else:
                await vc.move_to(channel)
        else:
            await channel.connect()

        await ctx.send(f"Successfully connected to: **{channel}**", delete_after=5)

    @commands.command(aliases=["leave", "dc"])
    async def disconnect(self, ctx):
        guild = ctx.guild
        vc = ctx.voice_client
        channel = vc.channel

        await guild.voice_client.disconnect()
        await ctx.send(f"Successfully disconnected from **{channel}**", delete_after=5)

    @commands.command()
    async def play(self, ctx, *, search: str= None):

        global vc
        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect)
            vc = ctx.voice_client

        await ctx.send("Getting everything ready...", delete_after=5)
        ytdl = YoutubeDL(ytdl_opts)

        player = ytdl.extract_info(search, download=False)
        global video
        if 'entries' in player:
            video = player['entries'][0]
        else:
            video = player
        vid.append(video)
        await songs.put(vid)

        title = video["alt_title"]
        author = video["uploader"]

        await ctx.send(f"Enqueued {title} from {author} successfully.")

    @commands.command()
    async def pause(self, ctx):
        vc = ctx.voice_client

        if not vc:
            await ctx.send("I am not connected to any voice channel!", delete_after=5)
            return
        elif vc.is_paused():
            await ctx.send("Music already paused!")
            return

        vc.pause()
        await ctx.send(f"**{ctx.author}** paused the song!")

    @commands.command()
    async def resume(self, ctx):
        vc = ctx.voice_client

        if not vc:
            await ctx.send("I am not connected to any voice channel!", delete_after=5)
            return
        elif not vc.is_paused():
            await ctx.send("Music not paused!")
            return

        vc.resume()
        await ctx.send(f"**{ctx.author}** resumed the song!")

    @commands.command()
    async def stop(self, ctx):
        vc = ctx.voice_client

        if not vc:
            await ctx.send("I am not connected to any voice channel!", delete_after=5)
            return
        elif not vc.is_playing():
            await ctx.send("I am not playing anything currently!", delete_after=5)

        vc.stop()
        await ctx.send(f"**{ctx.author}** stopped the song!")

    @commands.command(aliases=["next"])
    async def skip(self, ctx):
        vc = ctx.voice_client
        channel = ctx.author.voice.channel
        voice_channel = get(ctx.guild.voice_channels, id = channel.id)
        members = voice_channel.members

        if not vc:
            await ctx.send("I am not connected to any voice channel!", delete_after=5)
            return
        elif not vc.is_playing():
            await ctx.send("I am not playing anything currently!", delete_after=5)
            return

        u = [x.name for x in members]
        if "Midori" in u:
            u.remove("Midori")

        if len(u) >=3:
            author = ctx.author.name
            if author not in self.voters:
                self.voters.append(author)

                if len(self.voters) >= 3:
                    vc.stop()
                    await ctx.send(f"Successfully skipped the song!")
                    self.voters.clear()
                    print(self.voters)
                else:
                    await ctx.send(f"Skip vote added, currently at **{len(self.voters)}/3**")
            else:
                await ctx.send("You already voted to skip this song.")
        else:
            vc.stop()
            await ctx.send(f"**{ctx.author}** skipped the song!")

    @commands.command()
    async def volume(self, ctx, vol: float):
        vc = ctx.voice_client

        if not vc:
            await ctx.send("I am not playing anything currently!", delete_after=5)
            return

        if 0 < vol < 101:
            volume = vol / 100
            vc.source.volume = volume
            await ctx.send(f'**`{ctx.author}`**: Set the volume to **{vol}%**')
        else:
            await ctx.send('Please enter a value between 1 and 100.', delete_after=5)
            return

    @commands.command()
    async def now(self, ctx):
        title = vid[0]["alt_title"]
        author = vid[0]["uploader"]
        url = vid[0]["webpage_url"]
        thumbnail = vid[0]["thumbnail"]
        duration = vid[0]["duration"]
        uploader_url = vid[0]['uploader_url']

        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append(f'{days} days')
        if hours > 0:
            duration.append(f'{hours} hours')
        if minutes > 0:
            duration.append(f'{minutes} minutes')
        if seconds > 0:
            duration.append(f'{seconds} seconds')

        dur = ', '.join(duration)

        music = discord.Embed(
            title = "Now Playing",
            description = f"```css\n{title}\n```",
            color = 0xff0000
        )
        music.add_field(name="Duration", value=dur)
        music.add_field(name="Uploader", value=f"[{author}]({uploader_url})")
        music.add_field(name="URL", value=f"[Click]({url})")
        music.set_thumbnail(url=thumbnail)
        await ctx.send(embed=music)

    @commands.command(aliases=["queueinfo"])
    async def queue(self, ctx):
        if len(vid) == 0:
            await ctx.send("Empty Queue.")
            return
        elif len(vid) == 1:
            await ctx.send("Empty Queue.")
            return

        u = 1

        queue = ''
        for i, music in enumerate(vid[u]):
            try:
                title = vid[u]["alt_title"]
                url = vid[u]["webpage_url"]
                author = vid[u]["uploader"]
                queue += f'`{i + 1}.` [{title}]({url}) from {author}\n'
                u += 1
            except IndexError:
                break

        t = "track"
        if len(vid) - 1 == 1:
            t = "track"
        else:
            t = "tracks"

        embed = discord.Embed(
            title = f"{len(vid) - 1} {t}:",
            description = f"{queue}",
            color = 0x0000FF
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx, index: int):
        if len(vid) == 0:
            await ctx.send("Empty Queue.")
            return
        elif len(vid) == 1:
            await ctx.send("Empty Queue.")
            return

        title = vid[index]["alt_title"]
        vid.remove(vid[index])
        await ctx.send(f"Successfully removed {title} from the queue")

    @commands.command()
    async def loop(self, ctx):
        global loop_bool
        if loop_bool:
            loop_bool = False
            await ctx.send("Successfully stopped looping the music.")
        else:
            loop_bool = True
            await ctx.send("Successfully looping the music.")

    @commands.command()
    async def queueloop(self, ctx):
        global queueloop
        if queueloop:
            queueloop = False
            await ctx.send("Successfully stopped looping the queue.")
        else:
            queueloop = True
            await ctx.send("Successfully looping the queue.")

    @commands.command()
    async def lyrics(self, ctx, music: str=None, *, author: str=None):
        try:
            title = music.title()
            author = author.title()
        except AttributeError:
            title = vid[0]["alt_title"]
            author = vid[0]["uploader"]

        try:
            lyrics = PyLyrics.getLyrics(f"{author}", f"{title}")
        except ValueError:
            await ctx.send("Lyrics not found. (They propably aren't available yet in the API)")
            return

        lyrics = discord.Embed(
            title = f"{author} - {title} | Lyrics",
            description = f"{lyrics}",
            color = 0x0339FC
        )

        await ctx.send(embed = lyrics)

def setup(bot):
    bot.add_cog(Music(bot))
    bot.loop.create_task(Music.audio_player_task())
    # bot.loop.create_task(Music.timer())
