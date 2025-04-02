import os
from dotenv import load_dotenv
import discord
from bot_actions import join_and_play
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

with open('members_sounds.json', 'r') as f:
    test = json.load(f)

members_dict = {}

for value in test.items():
    members_dict[value[1]['id']] = value[1]['soundFile']

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_voice_state_update(member, before, after):
    if member.id in members_dict and before.channel != after.channel:
        if after.channel and not before.channel:
            print(f"Joined {after.channel}")
            await join_and_play(client, after.channel, members_dict[member.id])
        elif before.channel and not after.channel:
            print(f"Left {before.channel}")
        else:
            print(f"moved from {before.channel} to {after.channel}")
            await join_and_play(client, after.channel, members_dict[member.id])


async def disconnect_from_voice_channels(voice_clients):
    for vc in voice_clients:
        vc.stop()
        await vc.disconnect()


def main():
    client.run(token=TOKEN)  # type: ignore


if __name__ == '__main__':
    main()
