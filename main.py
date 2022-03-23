from disnake.ext import commands
from disnake.ext import tasks
from pytube import Channel
import json


bot = commands.Bot(
    command_prefix="="
)


@bot.event
async def on_ready():
    print("Ich bin an lol!")


@tasks.loop(minutes=15)
async def reminder():
    print("Starte Loop")
    with open(
        "youtubedata.json", 
        "r", 
        encoding="UTF-8"
    ) as f:
        data = json.load(f)

    check = data["video_check"]
    name = "".join(data["url"])

    for channel in data["url"]:
        youtube_channel = Channel(
            "".join(channel)
        )
        print(f"Joined {channel}")

    for url in youtube_channel.video_urls[:1]:
        if check.count(url) > 0:
            print("Url doppelt!")
        else:
            print("Nachricht geschickt!")

            data["video_check"].append(url)
            with open(
                "youtubedata.json", 
                "w", 
                encoding='UTF-8'
            ) as data_file:
                json.dump(
                    data, 
                    data_file, 
                    indent=4
                )

            discord_channel = bot.get_channel(
                data["channel"]
            )
            await discord_channel.send(
                f"Jo, **{name[22:]}** hat ein neues Video hochgeladen\n{url}"
            )


@reminder.before_loop
async def before_maxreminder():
    await bot.wait_until_ready()


if __name__ == "__main__":
    reminder.start()
    bot.run("token")
