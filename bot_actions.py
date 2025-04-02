import asyncio
import discord
from discord import FFmpegPCMAudio


async def join_and_play(client, voice_channel, sound_file):
    if not voice_channel:
        return

    voice_client = discord.utils.get(
        client.voice_clients, guild=voice_channel.guild)

    if voice_client:
        if voice_client.is_playing():  # type: ignore
            voice_client.stop()  # type: ignore
        await voice_client.disconnect(force=True)

    voice_client = await voice_channel.connect()

    try:
        source = FFmpegPCMAudio(sound_file)
        voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
            _cleanup_voice(voice_client),
            client.loop
        ))
    except Exception as e:
        print(f"Error playing sound: {e}")
        await _cleanup_voice(voice_client)


async def _cleanup_voice(voice_client):
    try:
        if voice_client.is_connected():
            await voice_client.disconnect()
    except:
        pass
