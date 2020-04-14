import discord, asyncio, requests, sqlite3,\
        os, sys
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.utils import get
from lib import Discord_Player

bot = commands.Bot(command_prefix=">")

class Client(discord.Client):

    @bot.event
    async def on_ready():
        print("Logged in\n\nLogs: ")
        await bot.change_presence(activity=discord.Streaming(name=default_stream, url=f"https://twitch.tv/{default_stream}"))

    @bot.command()
    async def play(self, *args):
        await Player.retrieve_data(self.message, " ".join(arg for arg in args))
    
    @bot.command()
    async def search(self, *args):
        await Player.retrieve_data(self.message, " ".join(arg for arg in args), direct=0)

    @bot.command()
    async def remove(self, content):
        await Player.remove_music(self.message, int(content))

    @bot.command()
    async def pause(self):
        await Player.pause_music(self.message)

    @bot.command()
    async def resume(self):
        await Player.resume_music(self.message)

    @bot.command()
    async def stop(self):
        Player.leave = True
        await Player.stop_music(self.message, False)

    @bot.command()
    async def skip(self):
        await Player.skip_music(self.message)

    @bot.command()
    async def loop(self):
        await Player.start_loop(self.message)

    @bot.command()
    async def stoploop(self):
        await Player.stop_loop(self.message)

    @bot.command()
    async def queue(self):
        await Player.show_queue(self.message)

    @bot.command()
    async def display(self, content):
        await Player.set_displayed_songs(self.message, content)

    @bot.command()
    async def volume(self, volume):
        await Player.set_volume(self.message, volume)

    @bot.command()
    async def currentvolume(self):
        await Player.current_volume(self.message)

    @bot.command()
    async def autoplay(self):
        await Player.start_autoplay(self.message)

    @bot.command()
    async def stopautoplay(self):
        await Player.stop_autoplay(self.message)

    @bot.command()
    async def q(self):
        if self.message.author.id == owner_id:
            await Player.stop_music(self.message, True)
            connection.close()
            await bot.logout()

    @bot.command()
    async def r(self):
        if self.message.author.id == owner_id:
            await Player.stop_music(self.message, True)
            connection.close()
            os.startfile(__file__)
            await bot.logout()
            
    @bot.command()
    # table cant start with a number
    async def playlist(self, *args):
        try:
            cursor.execute(
                f"CREATE TABLE a{self.message.author.id} (id INTEGER PRIMARY KEY, title TEXT, link TEXT)")
        except:
            pass

    @bot.command()
    async def playlistplay(self):
        await Player.playlist_play(self.message)

    @bot.command()
    async def playlistadd(self, *args):
        await Player.playlist_add(self.message, " ".join(args))
    
    @bot.command()
    async def playlistshow(self):
        await Player.playlist_show(self.message)

    @bot.command()
    async def playlistdelete(self, arg):
        await Player.playlist_delete(self.message, arg)

    @bot.command()
    async def playlistmove(self, *args):
        await Player.playlist_move(self.message, args)

    @bot.command()
    async def playlistclear(self):
        await Player.playlist_clear(self.message)

    @bot.command() 
    async def lyrics(self, *args):
        await Player.get_lyrics(self.message.channel, " ".join(args))

    @bot.command()
    async def direct(self, arg):
        await Player.set_direct(self.message.channel, int(arg))
    
    @bot.command()
    async def history(self):
        await Player.get_history(self.message.channel)
    
    @bot.command()
    async def clearhistory(self):
        await Player.clear_history(self.message.channel)

if __name__ == "__main__":

    print("Loading...")

    try:
        f = open("TOKEN.txt", "r")
    except IOError:
        with open("TOKEN.txt", "w+", encoding="utf-8") as f:
            f.write(input("Looks like you are running this for the first time.\nEnter your discord token: ") + "\n" +
                    input("\nEnter a genius token to access song lyrics (you can leave this blank): "))
        os.startfile(__file__)
        sys.exit()
    else:
        discord_token = f.readline().strip()
        genius_token = f.readline().strip()
        f.close()

    connection = sqlite3.connect("playlists.db")
    cursor = connection.cursor()

    default_stream = "( ͡° ͜ʖ ͡°)"

    owner_id = 609337374480269352

    Player = Discord_Player("playlists.db", bot, genius_token)

    print("Logging in...")
    bot.run(discord_token)