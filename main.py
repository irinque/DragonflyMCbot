import discord
from discord.ext import commands
from discord.ui import View, Button
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
                embed = discord.Embed(title="✅ СООБЩЕНИЕ ОТПРАВЛЕНО В КАНАЛ!", colour=discord.Colour.from_str(color_main))
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)
        await interaction.response.send_modal(SendApplication())
    view = View()
    embed = discord.Embed(title="🛠️ ВЫБЕРИТЕ КАНАЛ ДЛЯ ОТПРАВКИ:", colour=discord.Colour.from_str(color_main))
    dropdown = discord.ui.ChannelSelect(channel_types=[discord.ChannelType.text, discord.ChannelType.news], min_values=1, max_values=1)
    dropdown.callback = select_callback
    view.add_item(dropdown)
    embed.set_footer(text=prefix)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True,delete_after=60)

@bot.tree.command(name="send_form", description="Отправляет форму в канал.")
async def send_form(interaction: discord.Interaction):
    embed = discord.Embed(title="📝 АНКЕТА ДЛЯ ИГРЫ НА СЕРВЕРЕ", description="📑 Заполните короткую форму, после чего вы сможете зайти на сервер!\n", colour=discord.Colour.from_str(color_main))
    embed.set_footer(text=prefix)
    view = View()
    view_button = Button(label="📨 Анкета", style=discord.ButtonStyle.green, custom_id="button_anketa_open")
    view.add_item(view_button)
    channel = discord.utils.get(interaction.guild.channels, id=channel_createform_data)
    await channel.send(embed=embed, view=view)
    embed = discord.Embed(title="✅ СООБЩЕНИЕ ОТПРАВЛЕНО В КАНАЛ!", colour=discord.Colour.from_str(color_main))
    await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)
    

if __name__ == "__main__":
    bot.run(TOKEN)