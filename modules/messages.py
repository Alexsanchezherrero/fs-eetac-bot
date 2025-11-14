import discord
import json
from pathlib import Path

cfg = json.loads(Path("config.json").read_text())

def color_from_name(name: str) -> discord.Color:
    name = (name or cfg.get("DEFAULT_COLOR", "azul")).lower()
    colors = cfg.get("VALID_COLORS", {})
    val = colors.get(name, colors.get(cfg.get("DEFAULT_COLOR", "azul"), 3447003))
    return discord.Color(int(val))

def build_announcement_embed(titulo: str, contenido: str, color_name: str=None, author: discord.Member=None):
    color = color_from_name(color_name)
    embed = discord.Embed(title=f"📢 {titulo}", description=contenido, color=color)
    banner = cfg.get("BANNER_URL")
    if banner:
        embed.set_image(url=banner)
    embed.set_footer(text=cfg.get("FOOTER", "Equipo"))
    if author:
        embed.set_author(name=author.display_name, icon_url=getattr(author.avatar, "url", None) or author.display_avatar.url)
    return embed

class ConfirmView(discord.ui.View):
    def __init__(self, timeout: int = 300):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="👍 He leído", style=discord.ButtonStyle.secondary, custom_id="fs_he_leido")
    async def leido(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content=f"{interaction.user.mention} ha confirmado que ha leído este mensaje.", ephemeral=True)

    @discord.ui.button(label="📝 Marcar reunión", style=discord.ButtonStyle.primary, custom_id="fs_marca_reunion")
    async def marca(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="✅ Has marcado asistencia tentativamente. (Funcionalidad ampliable)", ephemeral=True)
