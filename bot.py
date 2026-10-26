# ==============================================
# ✅ SEMUA IMPORT DI ATAS
# ==============================================
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from logic import proses_pesan

# ==============================================
# KONEKSI BOT
# ==============================================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==============================================
# BOT SIAP
# ==============================================
@bot.event
async def on_ready():
    print(f"✅ Bot sudah masuk sebagai: {bot.user}")
    print("📖 Siap! Contoh: !bola")
    print("📖 Atau ketik banyak kata: !bola tas lampu")

# ==============================================
# TERIMA PESAN
# ==============================================
@bot.event
async def on_message(pesan):
    if pesan.author == bot.user:
        return
    
    jawab = proses_pesan(pesan.content)
    if jawab:
        await pesan.channel.send(jawab)

# ==============================================
# JALANKAN
# ==============================================
if __name__ == "__main__":
    bot.run("fill your own token")
