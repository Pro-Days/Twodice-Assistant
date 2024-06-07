import discord

discord_client = discord.Client(intents=discord.Intents.all())


@discord_client.event
async def on_ready():
    print(f"'{discord_client.user.name}' 로그인 성공 (ID: {discord_client.user.id})")


@discord_client.event
async def on_message(message):
    if not (message.content.startswith("!")):
        return
    await test_send(message.channel)


async def test_send(channel):
    embed = discord.Embed()
    embed.title = "한월 title"
    embed.type = "link"
    embed.description = "한월 description"
    embed.url = "https://hanwol.skhidc.kr/index.php"
    embed.set_footer(
        text="한월 footer",
        icon_url="https://www.google.co.kr/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
    )
    embed.set_image(
        url="https://www.google.co.kr/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    )
    embed.set_thumbnail(
        url="https://www.google.co.kr/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    )
    embed.set_author(
        name="한월 author",
        url="https://github.com/Pro-Days",
        icon_url="https://www.google.co.kr/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
    )
    embed.add_field(
        name="한월 field1",
        value="한월 value1",
        inline=False,
    )
    embed.add_field(
        name="한월 field2",
        value="한월 value2",
        inline=False,
    )
    await channel.send(embed=embed)


discord_client.run(os.getenv("DISCORD_TOKEN"))
