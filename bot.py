import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from modules.messages import build_announcement_embed, ConfirmView
from modules.actas import ActaModal
from aiohttp import web
import asyncio

INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.message_content = False  # no necesario para slash commands
bot = commands.Bot(command_prefix="!", intents=INTENTS)
cfg = json.loads(open("config.json").read())

async def handle(request):
    return web.Response(text="FS Bot alive")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()

@bot.event
async def on_ready():
    print(f"Bot iniciado como {bot.user} (ID: {bot.user.id})")
    try:
        await bot.tree.sync()
        print("Comandos slash sincronizados.")
    except Exception as e:
        print("Error sincronizando:", e)
    bot.loop.create_task(start_webserver())

@bot.tree.command(name="anuncio", description="Publica un anuncio bonito (embed) en este canal.")
@app_commands.describe(titulo="Título del anuncio", contenido="Contenido del anuncio", color="Color del embed (opcional)")
async def anuncio(interaction: discord.Interaction, titulo: str, contenido: str, color: str = None):
    embed = build_announcement_embed(titulo, contenido, color, author=interaction.user)
    view = ConfirmView()
    await interaction.response.send_message(content="Publicando anuncio...", ephemeral=True)
    sent = await interaction.channel.send(embed=embed, view=view)
    try:
        original = await interaction.original_response()
        await original.delete()
    except:
        pass

@bot.tree.command(name="mensaje", description="Crea un embed con color, título y contenido.")
@app_commands.describe(color="color (rojo, verde, azul...)", titulo="Título", contenido="Contenido del mensaje")
async def mensaje(interaction: discord.Interaction, color: str, titulo: str, contenido: str):
    embed = build_announcement_embed(titulo, contenido, color, author=interaction.user)
    view = ConfirmView()
    await interaction.response.send_message(content="Publicando mensaje...", ephemeral=True)
    await interaction.channel.send(embed=embed, view=view)
    try:
        original = await interaction.original_response()
        await original.delete()
    except:
        pass

@bot.tree.command(name="acta", description="Abre un formulario para crear un acta de reunión (modal).")
@app_commands.describe(target_channel="Canal donde publicar el acta (opcional)")
async def acta(interaction: discord.Interaction, target_channel: discord.TextChannel = None):
    modal = ActaModal(target_channel=target_channel)
    await interaction.response.send_modal(modal)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("ERROR: define la variable de entorno DISCORD_TOKEN")
        exit(1)
    bot.run(TOKEN)
