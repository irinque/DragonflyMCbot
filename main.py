import discord
from discord.ext import commands
from discord.ui import View
from discord.utils import get
from config import *
from protected_data import TOKEN, prefix

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=discord.Intents().all())
client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()


@bot.tree.command(name="send_embed", description="Отправляет Embed-Сообщение в Канал.")
async def send_embed(interaction: discord.Interaction):
    async def select_callback(interaction: discord.Interaction):
        channel = discord.utils.get(interaction.guild.channels, name=str(dropdown.values[0]))
        class SendApplication(discord.ui.Modal, title="📝 СОЗДАНИЕ EMBED"):
            message_title = discord.ui.TextInput(label="🎴 ЗАГОЛОВОК", style=discord.TextStyle.short)
            description = discord.ui.TextInput(label="🀄 ОПИСАНИЕ", style=discord.TextStyle.long, required=True)
            image = discord.ui.TextInput(label="🌄 КАРТИНКА", style=discord.TextStyle.short, required=False)
            async def on_submit(self, interaction: discord.Interaction):
                embed = discord.Embed(title=self.message_title, description=self.description, colour=discord.Colour.from_str(color_main))
                if self.image:
                    embed.set_image(url=self.image)
                embed.set_footer(text=prefix)
                await channel.send(embed=embed)
                embed = discord.Embed(title="✅ СООБЩЕНИЕ ОТПРАВЛЕНО В КАНАЛ!")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                await interaction.delete_original_response()
        await interaction.response.send_modal(SendApplication())
    view = View()
    embed = discord.Embed(title="🛠️ ВЫБЕРИТЕ КАНАЛ ДЛЯ ОТПРАВКИ:")
    dropdown = discord.ui.ChannelSelect(channel_types=[discord.ChannelType.text, discord.ChannelType.news], min_values=1, max_values=1)
    dropdown.callback = select_callback
    view.add_item(dropdown)
    embed.set_footer(text=prefix)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True,delete_after=60)


if __name__ == "__main__":
    bot.run(TOKEN)