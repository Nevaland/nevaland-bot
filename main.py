import discord
from discord.http import Route

client = discord.Client()
http = client.http
emoji_res_msg = None


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('?'):
        cmds = ['?', 'hello', 'embed', 'join', 'leave', 'me', 'img', 'emoji', 'direct', 'btn']
        embed = discord.Embed(title="명령어 모음", color=0x000000)
        # for cmd in cmds:
        #     embed.add_field(name=cmd, value=cmd, inline=False)
        embed.description = '\n'.join(cmds)
        await msg.channel.send(embed=embed)

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

    if msg.content.startswith('emoji'):
        global emoji_res_msg
        emoji_res_msg = await msg.channel.send("👍")
        await emoji_res_msg.add_reaction("👍")

    if msg.content.startswith('direct'):
        r = Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id)
        payload = {
            "content": "Direct Message"
        }
        await http.request(r, json=payload)

    if msg.content.startswith('btn'):
        r = Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id)
        payload = {
            "content": "This is a message with components",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "버튼",
                            "style": 1,
                            "custom_id": "test_btn"
                        }
                    ]

                }
            ]
        }
        await http.request(r, json=payload)


@client.event
async def on_raw_reaction_add(payload):
    global emoji_res_msg
    if emoji_res_msg and payload.message_id == emoji_res_msg.id and payload.user_id != client.user.id:
        await emoji_res_msg.edit(content=emoji_res_msg.content + str(payload.emoji))


@client.event
async def on_raw_reaction_remove(payload):
    global emoji_res_msg
    if emoji_res_msg and payload.message_id == emoji_res_msg.id and payload.user_id != client.user.id:
        await emoji_res_msg.edit(content=emoji_res_msg.content + str(payload.emoji))


@client.event
async def on_socket_response(payload):
    d = payload.get("d", {})
    t = payload.get("t")
    if t == "INTERACTION_CREATE" and d.get("type") == 3:
        message = d.get("message")

        await http.request(
            Route('PATCH', '/channels/{channel_id}/messages/{message_id}',
                  channel_id=message.get("channel_id"), message_id=message.get('id')), json={"content": "Pressed"}
        )
        interaction_id = d.get("id")
        interaction_token = d.get("token")
        await client.http.request(
            Route("POST", f"/interactions/{interaction_id}/{interaction_token}/callback"),
            json={"type": 4, "data": {
                "content": "Button Pressed!",
                "flags": 64
            }},
        )

with open('./token.txt', 'r') as f:
    token = f.read()

client.run(token)
