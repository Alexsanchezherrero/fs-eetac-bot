import discord
from discord import ui
import json
from pathlib import Path
cfg = json.loads(Path("config.json").read_text())

class ActaModal(ui.Modal, title="Crear acta de reunión"):
    titulo = ui.TextInput(label="Título de la reunión", style=discord.TextStyle.short, max_length=100, placeholder="Revisión semanal")
    resumen = ui.TextInput(label="Resumen/decisiones", style=discord.TextStyle.paragraph, max_length=2000, placeholder="Puntos tratados y decisiones")
    asistentes = ui.TextInput(label="Asistentes (separados por comas)", style=discord.TextStyle.short, required=False, max_length=250)
    tareas = ui.TextInput(label="Tareas asignadas (formato: tarea - responsable)", style=discord.TextStyle.paragraph, required=False, max_length=1200)

    def __init__(self, target_channel: discord.TextChannel=None):
        super().__init__()
        self.target_channel = target_channel

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"🗒️ Acta: {self.titulo.value}", description=self.resumen.value, color=discord.Color.dark_gold())
        footer = cfg.get("FOOTER", "Equipo")
        embed.set_footer(text=footer)
        if self.attendees == (self.asistentes.value or "").strip():
            embed.add_field(name="Asistentes", value=self.attendees, inline=False)
        if self.tareas == (self.tareas.value or "").strip():
            embed.add_field(name="Tareas asignadas", value=self.tareas, inline=False)
        chan = self.target_channel or interaction.channel
        await chan.send(embed=embed)
        await interaction.response.send_message(content="✅ Acta publicada correctamente.", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message("❌ Error al crear el acta.", ephemeral=True)
