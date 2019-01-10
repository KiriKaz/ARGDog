import discord
import asyncio
import re
import base64
import sys
from binascii import Error, Incomplete

client = discord.Client()

prefixesf = open('token/guilds', 'r')
prefixes = prefixesf.read().strip()
prefixes = re.findall(r"([\d]{18})(.)*", prefixes)
for gset in prefixes:
    print("Guild {}: {}".format(gset[0], gset[1]))
prefixesf.close()
prefixes = dict(prefixes)
print(prefixes)

@client.event
async def on_ready():
    if client.user.name == "ARGDog":
        print('Logged in as ARGDog. Bark bark.')
    else:
        print('Logged in as {}.'.format(client.user.name))
    print('-'*20)

@client.event
async def on_message(message):
    if prefixes.get(message.server.id) == None:
        prefixes[message.server.id] = "!"
    ignoremsg = False
    if not message.author.bot:
        prf = message.content[0]
    else:
        prf = None
    prfg = prefixes[message.server.id]
    if prf != prfg or message.author.bot:
        ignoremsg = True
    if ignoremsg:
        pass
    else:
        msgc = message.content[1:].split()
        cmd = msgc[0].lower()
        print("Dispatching {} to {}.".format(cmd, message.server.id))

        guy = message.author.nick
        if guy == None:
            guy = message.author.name

        if cmd in ('help', 'commands'):
            title = "**List of Commands**"
            helpembed = discord.Embed(title=title, type="rich", color=0xffffff)
            cprefixt = "{0}prefix, {0}pref".format(prfg)
            cprefixv = "```{0}prefix $```\nChange the prefix used for commands for this server.".format(prfg)
            helpembed.add_field(name=cprefixt, value=cprefixv, inline=False)
            cb64et = "{0}b64e, {0}base64e, {0}b64encode, {0}base64encode".format(prfg)
            cb64ev = "```{0}b64e Super secret message...!```\nEncode a message in base64.".format(prfg)
            helpembed.add_field(name=cb64et, value=cb64ev, inline=False)
            cb64dt = "{0}b64d, {0}base64d, {0}b64decode, {0}base64decode".format(prfg)
            cb64dv = "```{0}b64d aHVudGVyMg==```\nDecode a base64 message.".format(prfg)
            helpembed.add_field(name=cb64dt, value=cb64dv, inline=False)
            await client.send_message(message.channel, embed=helpembed)
        elif cmd in ('prefix', 'pref'):
            if len(msgc) != 2:
                await client.send_message(message.channel, 'Please call this command with a one-character argument to set your prefix to.')
                await client.send_message(message.channel, 'Guild\'s current prefix is: {}'.format(prfg))
            else:
                prefixes[message.server.id] = msgc[1][0]
                print("Prefix for {} has been set to \"{}\".".format(message.server.id, msgc[1][0]))
                await client.send_message(message.channel, 'Guild prefix set to `{}`.'.format(msgc[1][0]))
        elif cmd in ('b64e', 'base64e', 'b64encode', 'base64encode'):
            if len(msgc) == 1:
                usage = "{}{} Message to encode here".format(prfg, cmd)
                await client.send_message(message.channel, 'Usage: `{}`'.format(usage))
            else:
                del msgc[0]
                args = ' '.join(msgc)
                try:
                    b64r = base64.b64encode(bytes(args, 'utf-8'))
                    b64r = str(b64r)[2:-1]
                    messager = '**Input** ```fix\n{}\n```\n**Output**\n```\n{}\n```'.format(args, b64r)
                    title = "**Base64 encoding for {} ".format(guy)
                    title += "-" * (80 - len(title))
                    title += "**"
                    messager = discord.Embed(title=title, type="rich", description="{}".format(messager), color=0xff8000)
                    await client.send_message(message.channel, embed=messager)
                except Error:
                    e = sys.exc_info()[1]
                    messager = '**Input** ```fix\n{}\n```\nError: `{}`'.format(args, e)
                    title = "**Error in base64 encoding for {} ".format(guy)
                    title += "-" * (80 - len(title))
                    title += "**"
                    messager = discord.Embed(title=title, type="rich", description="{}".format(messager), color=0xff0000)
                    await client.send_message(message.channel, embed=messager)
                except:
                    e = sys.exc_info()[0]
                    messager = '**Input** ```fix\n{}\n```\nError: `{}`'.format(args, e)
                    title = "**Error in base64 encoding for {} ".format(guy)
                    title += "-" * (80 - len(title))
                    title += "**"
                    messager = discord.Embed(title=title, type="rich", description="{}".format(messager), color=0xff0000)
                    await client.send_message(message.channel, embed=messager)
        elif cmd in ('b64d', 'base64d', 'b64decode', 'base64decode'):
            if len(msgc) == 1:
                usage = "{}{} base64msg [otherb64msg] [anotherb64msg]".format(prfg, cmd)
                await client.send_message(message.channel, 'Usage: `{}`'.format(usage))
            else:
                del msgc[0]
                bufer = []
                errored = False
                for b64msgs in msgc:
                    try:
                        b64r = base64.b64decode(b64msgs)
                        b64r = str(b64r)[2:-1]
                        bufers = '**Input** ```fix\n{}\n```\n**Output**\n```\n{}\n```'.format(b64msgs, b64r)
                        if "\\" in b64r:
                            bufers += '\nLooks like the result is a bit garbled. Is your b64 correct?'
                        bufer.append(bufers)
                    except Error:
                        errored = True
                        e = sys.exc_info()[1]
                        bufers = '**Input** ```fix\n{}\n```\nError: `{}`'.format(b64msgs, e)
                        if str(e) == "Incorrect padding":
                            bufers += '\nAll base64 strings have a multiple of four as the amount of characters. Are you sure your string is base64?'
                        bufer.append(bufers)
                    except:
                        e = sys.exc_info()[0]
                        bufers = '**Input** ```fix\n{}\n```\nError: `{}`'.format(b64msgs, e)
                        bufer.append(bufers)
                if errored:
                    title = "**Error in base64 decoding for {} ".format(guy)
                    title += "-" * (80 - len(title))
                    title += "**"
                    messager = discord.Embed(title=title, type="rich", color=0xff0000)
                else:
                    title = "**Base64 decoding for {} ".format(guy)
                    title += "-" * (80 - len(title))
                    title += "**"
                    messager = discord.Embed(title=title, type="rich", color=0x0080ff)
                i = 1
                for calc in bufer:
                    messager.add_field(name="Message {}".format(i), value="{}".format(calc), inline=False)
                    i += 1
                await client.send_message(message.channel, embed=messager)
        else:
            await client.send_message(message.channel, "Command not recognized.")




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