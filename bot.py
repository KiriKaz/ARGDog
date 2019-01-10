import discord
import asyncio


def main(token):
    client = discord.Client()

    @client.event
    async def on_ready():
        if client.user.name == "ARGDog":
            print('Logged in as {}. Bark bark.'.format(client.user.name))
        else:
            print('Logged in as {}.'.format(client.user.name))
        print('------')

    @client.event
    async def on_message(message):
        if message.content.startswith('!test'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1

            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        elif message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')

    tokenf = open('token/token', 'r')
    token = tokenf.read().strip()

    client.run(token)
    tokenf.close()
