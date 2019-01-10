import discord
import asyncio
import re

client = discord.Client()

prefixesf = open('token/guilds', 'r')
prefixes = prefixesf.read().strip()
prefixes = re.findall(r"([\d]{18})(.)*", prefixes)
for gset in prefixes:
    print("Guild {}: {}".format(gset[0], gset[1]))
prefixesf.close()
print(prefixes)
prefixes = dict(prefixes)
print(prefixes)

@client.event
async def on_ready():
    if client.user.name == "ARGDog":
        print('Logged in as ARGDog. Bark bark.')
    else:
        print('Logged in as {}.'.format(client.user.name))
    print('------')

@client.event
async def on_message(message):
    prf = message.content[0]
    msgc = message.content[1::].split()
    if prefixes.get(message.server.id) == None:
        prefixes[message.server.id] = "!"
    prfg = prefixes[message.server.id]
    if prf == prfg:
        if msgc[0] == 'test':
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1

            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        elif msgc[0] == 'sleep':
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')
        elif msgc[0] == 'prefix':
            if len(msgc) != 2:
                await client.send_message(message.channel, 'Please call this command with a one-character argument to set your prefix to.')
                await client.send_message(message.channel, 'Guild\'s current prefix is: {}'.format(prfg))
            else:
                prefixes[message.server.id] = msgc[1][0]
                print("Prefix for {} has been set to \"{}\".".format(message.server.id, msgc[1][0]))
                await client.send_message(message.channel, 'Guild prefix set to `{}`.'.format(msgc[1][0]))

tokenf = open('token/token', 'r')
token = tokenf.read().strip()
tokenf.close()
client.run(token)

prefixesf = open('token/guilds', 'w')
saveStr = ""
for k,v in prefixes.items():
    saveStr += "{}: {}\n".format(k, v)
prefixesf.write(saveStr)
prefixesf.close()