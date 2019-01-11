import discord
import asyncio
import re
import base64
import sys
import json
from binascii import Error, Incomplete


dbg = False

if len(sys.argv) == 2:
    if sys.argv[1] == "debug":
        print("Debug messages active.")
        print("")
        dbg = True

client = discord.Client()
with open('commands.json', 'r') as data_commands:
    commands = json.load(data_commands)


prefixesf = open('token/guilds', 'r')
prefixes = prefixesf.read().strip()
prefixes = re.findall(r"([\d]{18})(.)*", prefixes)
if dbg:
    for gset in prefixes:
        print("Guild {}: {}".format(gset[0], gset[1]))
prefixesf.close()
prefixes = dict(prefixes)


bandf = open('token/banned', 'r')
band = bandf.read().strip().split('\n')
if dbg:
    for person in band:
        print('UID {} is banned from using the report command.'.format(person))
cocmds = commands['Core']
cicmds = commands['Ciphers']
bdcmds = commands['Bot Admin']


@client.event
async def on_ready():
    if client.user.name == "ARGDog":
        print('Logged in as ARGDog. Bark bark.')
    else:
        print('Logged in as {}.'.format(client.user.name))
    print('-'*20)


@client.event
async def on_message(message):
    prf = None
    if not message.author.bot:
        prf = message.content[0]

    if message.server == None or message.author.bot:
        return

    prfg = prefixes[message.server.id]
    if prefixes.get(message.server.id) == None:
        prefixes[message.server.id] = "!"

    if prf != prfg:
        return

    msgc = message.content[1:].split()
    cmd = msgc[0].lower()
    if dbg:
        print("Dispatching {} to {}.".format(cmd, message.server.id))

    guy = message.author.nick
    if guy == None:
        guy = message.author.name

    if cmd in cocmds[0]['aliases']:
        if len(msgc) == 1:
            string = ""
            string += "```md\n#List of Commands```"
            string += "\nUse {0}help <command> if you need help about how to use a specific command.\n".format(prfg)
            i = 1
            for category in commands:
                string += "**{}. {} - **".format(i, category)
                i += 1
                for command in commands[category]:
                    string += "`{}` ".format(command['command'])
                string +="\n"
            await client.send_message(message.channel, string)
        else:
            # Specifically asked for help for a command. Now... here we go:
            string = None
            for category in commands:
                for command in commands[category]:
                    if msgc[1] in command['aliases']:
                        string = ""
                        string += "**`{}{}`** __`{}`__\n".format(prfg, command['command'], command['description'])
                        string += "**Aliases:** "
                        for alias in command['aliases']:
                            string += "`{}`, ".format(alias)
                        string = string[:-2]  # Remove last ", ".
                        string += "\n\n"
                        string += "**Usage:** {}{}".format(prfg, command['usage'])
                        break
            if string == None:
                string = "Sorry, couldn't find that command!"
            await client.send_message(message.channel, string)
    elif cmd in cocmds[1]['aliases']:
        if len(msgc) != 2:
            await client.send_message(message.channel, 'Please call this command with a one-character argument to set your prefix to.')
            await client.send_message(message.channel, 'Guild\'s current prefix is: {}'.format(prfg))
        else:
            prefixes[message.server.id] = msgc[1][0]
            if dbg:
                print("Prefix for {} has been set to \"{}\".".format(message.server.id, msgc[1][0]))
            await client.send_message(message.channel, 'Guild prefix set to `{}`.'.format(msgc[1][0]))
    elif cmd in cocmds[2]['aliases']:
        if message.author.id in band:
            await client.send_message(message.channel, 'Afraid not. From my point of view, looks like you\'re banned from using this command.')
        elif len(msgc) == 1:
            await client.send_message(message.channel, 'Please give me something to relay to my owner. Bark. I\'m still a dog, you know.')
        else:
            del msgc[0]
            args = ' '.join(msgc)
            author = await client.get_user_info(109122112643440640)
            await client.send_message(author, 'Userid {} ({}#{}) has this to say to you.'.format(message.author.id, message.author.name, message.author.discriminator))
            await client.send_message(author, '```\n{}\n```'.format(args))
            await client.send_message(message.channel, 'Your message has been relayed to my owner, alongside your UID, in case he needs to get back in touch with you.')
    elif cmd in cicmds[0]['aliases']:
        if len(msgc) == 1:
            usage = "{}{}".format(prfg, cicmds[0]['usage'])
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
    elif cmd in cicmds[1]['aliases']:
        if len(msgc) == 1:
            usage = "{}{}".format(prfg, cicmds[1]['usage'])
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
    elif cmd in cicmds[2]['aliases']:
        if len(msgc) == 1:
            usage = "{}{}".format(prfg, cicmds[1]['usage'])
            await client.send_message(message.channel, 'Usage: `{}`'.format(usage))
        else:
            del msgc[0]
            args = ' '.join(msgc)
            string = ""
            for character in args:
                string += bin(ord(character))[2:].zfill(8) + " "
            string = string[:-1] # Remove last space. Might be unnecessary..
            messager = '**Input** ```fix\n{}\n```\n**Output**\n```\n{}\n```'.format(args, string)
            title = "**Binary encoding for {} ".format(guy)
            title += "-" * (80 - len(title))
            title += "**"
            messager = discord.Embed(title=title, type="rich", description="{}".format(messager), color=0xff8000)
            await client.send_message(message.channel, embed=messager)
    elif cmd in cicmds[3]['aliases']:
        if len(msgc) == 1:
            usage = "{}{}".format(prfg, cicmds[3]['usage'])
            await client.send_message(message.channel, 'Usage: `{}`'.format(usage))
        else:
            args = False
            try:
                del msgc[0]
                string = ""
                if len(msgc) == 1:
                    binary = re.findall('.{8}', msgc[0])
                    if binary == []:
                        raise ValueError('string not 8 characters or longer')
                    for encodedbinary in binary:
                        string += chr(int(encodedbinary, 2))
                    messager = '**Input** ```fix\n{}\n```\n**Output**\n```\n{}\n```'.format(msgc[0], string)
                    title = "**Binary decoding for {} ".format(guy)
                    title += "-" * (80 - len(title))
                    title += "**"
                    messager = discord.Embed(title=title, type="rich", description="{}".format(messager), color=0xff8000)
                else:
                    for binary in msgc:
                        string += chr(int(binary, 2))
                    args = ' '.join(msgc)
                    messager = '**Input** ```fix\n{}\n```\n**Output**\n```\n{}\n```'.format(args, string)
                    title = "**Binary decoding for {} ".format(guy)
                    title += "-" * (80 - len(title))
                    title += "**"
                    messager = discord.Embed(title=title, type="rich", description="{}".format(messager), color=0xff8000)
                await client.send_message(message.channel, embed=messager)
            except ValueError:
                e = sys.exc_info()[1]
                if args:
                    messager = '**Input** ```fix\n{}\n```\nError: `{}`'.format(args, e)
                else:
                    messager = '**Input** ```fix\n{}\n```\nError: `{}`'.format(msgc[0], e)
                title = "**Error in binary encoding for {} ".format(guy)
                title += "-" * (80 - len(title))
                title += "**"
                messager = discord.Embed(title=title, type="rich", description="{}".format(messager), color=0xff0000)
                await client.send_message(message.channel, embed=messager)
                ex = ' '.join(str(e).split()[0:4])
                if ex == 'invalid literal for int()':
                    await client.send_message(message.channel, "You probably didn't use a string of zeroes and ones. Are you sure this is binary?")
            except:
                e = sys.exc_info()[0]
                if args:
                    messager = '**Input** ```fix\n{}\n```\nError: `{}`'.format(args, e)
                else:
                    messager = '**Input** ```fix\n{}\n```\nError: `{}`'.format(msgc[0], e)
                title = "**Error in binary encoding for {} ".format(guy)
                title += "-" * (80 - len(title))
                title += "**"
                messager = discord.Embed(title=title, type="rich", description="{}".format(messager), color=0xff0000)
    elif cmd in bdcmds[0]['aliases']:
        if message.author.id not in (109122112643440640, 337295484559425537):
            await client.send_message(message.channel, "No.")
        elif len(msgc) != 2:
            await client.send_message(message.channel, "Try again mate.")
        else:
            band.append(msgc[1])
            await client.send_message(message.channel, "UID {} banned.".format(msgc[1]))
    elif cmd in bdcmds[1]['aliases']:
        if message.author.id not in (109122112643440640, 337295484559425537):
            await client.send_message(message.channel, "No.")
        elif len(msgc) != 2:
            await client.send_message(message.channel, "Try again mate.")
        else:
            if msgc[1] in band:
                while msgc[1] in band:
                    band.remove(msgc[1])
                await client.send_message(message.channel, "UID {} unbanned.".format(msgc[1]))
            else:
                await client.send_message(message.channel, "UID {} isn't banned.")
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
