import discord

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('hello'):
        await msg.channel.send('Hello!')

    if msg.content.startswith('embed'):
        embed = discord.Embed(title="제목", description="설명", color=0xFF0000)
        embed.add_field(name=":game_die: 필드이름", value=":game_die: 필드설명", inline=True)
        embed.add_field(name=":game_die: 필드이름", value=":game_die: 필드설명", inline=True)
        embed.set_footer(text="footer")
        await msg.channel.send(embed=embed)

    if msg.content.startswith('join'):
        channel = msg.author.voice.channel
        await channel.connect()

    if msg.content.startswith('leave'):
        await client.voice_clients[0].disconnect()

    if msg.content.startswith('me'):
        await msg.channel.send(msg.author.name + ": " + str(msg.author.id))

    if msg.content.startswith('img'):
        await msg.channel.send(file=discord.File('image.jpg'))

with open('./token.txt', 'r') as f:
    token = f.read()

client.run(token)
