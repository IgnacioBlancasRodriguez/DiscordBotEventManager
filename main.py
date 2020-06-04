import discord
import json
import time
import random
import calendar as cl
import os

with open("token.json") as token_list:
    tokens = json.load(token_list)
    token = tokens.get("token")
    server_id = int(tokens.get("server_id"))
    swear_words = tokens.get("bad_words")

client = discord.Client()
event_requested = False
event_state = 0
data = {}

@client.event
async def on_ready():
    print("bot is ready")
@client.event
async def on_member_join(member):
    print(f"""{member} has joined""")
    for channel in member.guild.channels:
        if str(channel) == "greetings":
            embed = discord.Embed(title="Greetings",colour=discord.Colour.gold())
            embed.add_field(name="Welcome", value=f"""Welcome to the server {member.mention}""")
            await channel.send(f"""Welcome to the server {member.mention}""")

@client.event
async def on_message(message):
    global event_state
    global data
    global event_requested
    id_name = client.get_guild(server_id)
    if message.author != client.user:
        for word in swear_words:
            if message.content.find(word) != -1:
                print("bad word alert!")
                await message.channel.purge(limit=1)
    if message.author != client.user and str(message.channel) == "events":
        if message.content.find("enseñame eventos cercanos") != -1:
            print("requested to show near events")
            events_near = cl.show_events_near()
            if events_near == False:
                embed = discord.Embed(title="Eventos cercanos")
                embed.add_field(name="Eventos para mañana", value="No hay eventos para mañana")
                await message.channel.send(content=None, embed=embed)
            else:
                print("near")
                embed = discord.Embed(title="Eventos cercanos")
                for events in events_near:
                    for event in events:
                        for i in event:
                            embed.add_field(name="Eventos para mañana", value=f"-{i}")
                await message.channel.send(content=None, embed=embed)

        if message.content.find("crear evento") != -1:
            print("Event creation requested")
            global event_requested
            event_requested = True
            event_state = 1
            embed = discord.Embed(title="Creación de evento", description="Parte 1:", colour=discord.Colour.dark_gold())
            embed.add_field(name="-1ª pregunta:", value="-¿Cuál es el título del evento?-   Responde diciendo !nombre:")
            data["event"] = {
                "name": None,
                "date": {
                    "day": None,
                    "hour_strats": None,
                    "hour_finish": None
                }

            }
            await message.channel.send(content=None, embed=embed)
        if message.content.find("!nombre:") != -1 and event_requested and event_state == 1:
            name = message.content
            name = name.replace("!nombre:", "")
            data["event"]["name"] = name
            print(data)
            event_requested = True
            event_state += 1
            embed = discord.Embed(title="Creación de evento", description="Parte 2:", colour=discord.Colour.dark_magenta())
            embed.add_field(name="-1ª pregunta:", value="-¿Cuando se realizará el evento?-   Responde diciendo !día: y la fecha(año-mes-día)")
            embed.add_field(name="-2ª pregunta:", value="-¿A qué hora empezará el evento?-   Responde diciendo !hora_inicio:")
            embed.add_field(name="-3ª pregunta:", value="-¿A qué hora terminará el evento?-   Responde diciendo !hora_finalizar:")
            await message.channel.send(content=None, embed=embed)
        if message.content.find("!día:") != -1 and event_requested and event_state > 1 and event_state < 5:
            day = message.content
            day = day.replace("!día:","")
            data["event"]["date"]["day"] = day
            event_requested = True
            event_state += 1
            if event_state == 3:
                embed = discord.Embed(title="Creación de evento", description="Parte 2:", colour=discord.Colour.dark_magenta())
                embed.add_field(name="-2ª pregunta:", value="-¿A qué hora empezará el evento?-   Responde diciendo !hora_inicio:")
                embed.add_field(name="-3ª pregunta:", value="-¿A qué hora terminará el evento?-   Responde diciendo !hora_finalizar:")
            if event_state == 4 and data["event"]["date"]["hour_finish"] == None:
                embed = discord.Embed(title="Creación de evento", description="Parte 2:", colour=discord.Colour.dark_magenta())
                embed.add_field(name="-3ª pregunta:", value="-¿A qué hora terminará el evento?-   Responde diciendo !hora_finalizar:")
            if event_state == 4 and data["event"]["date"]["hour_starts"] == None:
                embed = discord.Embed(title="Creación de evento", description="Parte 2:", colour=discord.Colour.dark_magenta())
                embed.add_field(name="-2ª pregunta:", value="-¿A qué hora empezará el evento?-   Responde diciendo !hora_inicio:")
            elif event_state == 5:
                embed = discord.Embed(title="Creación de evento", description="Parte 3:", colour=discord.Colour.dark_teal())
                embed.add_field(name="-1ª pregunta:", value="-¿Quieres confirmar la creación de este evento?-   Responde diciendo !SI o !NO:")
            await message.channel.send(content=None, embed=embed)
        if message.content.find("!hora_inicio:") != -1 and event_requested and event_state > 1 and event_state < 5:
            hour_strats = message.content
            hour_strats = hour_strats.replace("!hora_inicio:","")
            data["event"]["date"]["hour_starts"] = hour_strats
            event_requested = True
            event_state += 1
            if event_state == 3:
                embed = discord.Embed(title="Creación de evento", description="Parte 2:", colour=discord.Colour.dark_magenta())
                embed.add_field(name="-1ª pregunta:", value="-¿Cuando se realizará el evento?-   Responde diciendo !día: y la fecha(año-mes-día)")
                embed.add_field(name="-3ª pregunta:", value="-¿A qué hora terminará el evento?-   Responde diciendo !hora_finalizar:")
            if event_state == 4 and data["event"]["date"]["hour_finish"] == None:
                embed = discord.Embed(title="Creación de evento", description="Parte 2:", colour=discord.Colour.dark_magenta())
                embed.add_field(name="-3ª pregunta:", value="-¿A qué hora terminará el evento?-   Responde diciendo !hora_finalizar:")
            if event_state == 4 and data["event"]["date"]["day"] == None:
                embed = discord.Embed(title="Creación de evento", description="Parte 2:", colour=discord.Colour.dark_magenta())
                embed.add_field(name="-1ª pregunta:", value="-¿Cuando se realizará el evento?-   Responde diciendo !día: y la fecha(año-mes-día)")
            elif event_state == 5:
                embed = discord.Embed(title="Creación de evento", description="Parte 3:", colour=discord.Colour.dark_teal())
                embed.add_field(name="-1ª pregunta:", value="-¿Quieres confirmar la creación de este evento?-   Responde diciendo !SI o !NO:")
            await message.channel.send(content=None, embed=embed)
        if message.content.find("!hora_finalizar:") != -1 and event_requested and event_state > 1 and event_state < 5:
            hour_finish = message.content
            hour_finish = hour_finish.replace("!hora_finalizar:","")
            data["event"]["date"]["hour_finish"] = hour_finish
            event_requested = True
            event_state += 1
            if event_state == 3:
                embed = discord.Embed(title="Event creation", description="Parte 2:", colour=discord.Colour.dark_magenta())
                embed.add_field(name="-1ª pregunta:", value="-¿Cuando se realizará el evento?-   Responde diciendo !día: y la fecha(año-mes-día)")
                embed.add_field(name="-3ª pregunta:", value="-¿A qué hora terminará el evento?-   Responde diciendo !hora_finalizar:")
            if event_state == 4 and data["event"]["date"]["hour_starts"] == None:
                embed = discord.Embed(title="Creación de evento", description="Parte 2:", colour=discord.Colour.dark_magenta())
                embed.add_field(name="-2ª pregunta:", value="-¿A qué hora empezará el evento?-   Responde diciendo !hora_inicio:")
            if event_state == 4 and data["event"]["date"]["day"] == None:
                embed = discord.Embed(title="Creación de evento", description="Parte 2:", colour=discord.Colour.dark_magenta())
                embed.add_field(name="-1ª pregunta:", value="-¿Cuando se realizará el evento?-   Responde diciendo !día: y la fecha(año-mes-día)")
            elif event_state == 5:
                embed = discord.Embed(title="Creación de evento", description="Parte 3:", colour=discord.Colour.dark_teal())
                embed.add_field(name="-1ª pregunta:", value="-¿Quieres confirmar la creación de este evento?-   Responde diciendo !SI o !NO:")
            await message.channel.send(content=None, embed=embed)
        if message.content.find("!SI") != -1 and event_requested and event_state == 5:
            event_requested = False
            converted_data = json.dumps(data, indent=4)
            with open("events.json","w") as f:
                f.write(converted_data)
            with open("events.json") as values_container:
                values = json.load(values_container)
                name = values["event"].get("name")
                day = values["event"]["date"].get("day")
                hour_strats = values["event"]["date"].get("hour_starts")
                hour_finish = values["event"]["date"].get("hour_finish")
                cl.save_event(name, day, hour_strats, hour_finish)
            await message.channel.send("Evento creado de manera satisfactoria.")
            os.remove("events.json")

client.run(token)
