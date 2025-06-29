import discord
from discord.ext import commands, tasks
import requests
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

LINK_DOSYA = "linkler.txt"  ##Linkler Buraya Kaydedilicek Eğer Yoksa Otomatik Oluşturur!
BOT_SAHIBI_ID = 123456789012345678  # Kendi kullanıcı ID'ni buraya yaz!

if not os.path.exists(LINK_DOSYA):
    with open(LINK_DOSYA, "w") as f:
        pass

def linkleri_yukle():
    linkler = []
    with open(LINK_DOSYA, "r") as f:
        for satir in f:
            parcalar = satir.strip().split("||")
            if len(parcalar) == 2:
                linkler.append({"sahip": parcalar[0], "url": parcalar[1]})
    return linkler

def link_ekle(user_id, url):
    with open(LINK_DOSYA, "a") as f:
        f.write(f"{user_id}||{url}\n")

def link_sil(user_id, url):
    linkler = linkleri_yukle()
    with open(LINK_DOSYA, "w") as f:
        for link in linkler:
            if not (link["sahip"] == str(user_id) and link["url"] == url):
                f.write(f'{link["sahip"]}||{link["url"]}\n')

@tasks.loop(minutes=5)
async def uptime():
    linkler = linkleri_yukle()
    print(f"[UPTIME] {len(linkler)} link kontrol ediliyor...")
    for link in linkler:
        try:
            requests.get(link["url"])
            print(f"[✔] {link['url']} aktif.")
        except:
            print(f"[✖] {link['url']} ulaşılamıyor.")

@bot.event
async def on_ready():
    print(f"{bot.user} aktif oldu!")
    uptime.start()

@bot.command()
async def link_ekle(ctx, url):
    if not url.startswith("http"):
        return await ctx.send("🚫 Link düzgün değil knk, http veya https ile başlamalı.")

    linkler = linkleri_yukle()
    for link in linkler:
        if link["sahip"] == str(ctx.author.id) and link["url"] == url:
            return await ctx.send("⚠️ Bu link zaten sende kayıtlı.")

    link_ekle(ctx.author.id, url)
    await ctx.send(f"✅ Link eklendi: {url}")

@bot.command()
async def linklerim(ctx):
    linkler = linkleri_yukle()
    kendi_linkler = [l["url"] for l in linkler if l["sahip"] == str(ctx.author.id)]

    if not kendi_linkler:
        return await ctx.send("📝 Hiç link eklememişsin knk.")

    mesaj = "**Senin Linklerin:**\n"
    for i, url in enumerate(kendi_linkler, 1):
        mesaj += f"{i}. {url}\n"

    await ctx.send(mesaj)

@bot.command()
async def link_sil(ctx, url):
    linkler = linkleri_yukle()
    if not any(l["sahip"] == str(ctx.author.id) and l["url"] == url for l in linkler):
        return await ctx.send("❗ Bu link sende kayıtlı değil.")

    link_sil(ctx.author.id, url)
    await ctx.send(f"🗑️ Link silindi: {url}")

@bot.command()
async def tum_linkler(ctx):
    if ctx.author.id != BOT_SAHIBI_ID:
        return await ctx.send("🚫 Bu komut sadece bot sahibine açık knk.")

    linkler = linkleri_yukle()
    if not linkler:
        return await ctx.send("📂 Hiç link yok.")

    mesaj = "**Tüm Linkler:**\n"
    for i, link in enumerate(linkler, 1):
        mesaj += f"{i}. {link['url']} | Sahip: <@{link['sahip']}>\n"

    await ctx.send(mesaj[:2000])  # 2000 karakter sınırı için dikkat!

with open("token.token", "r") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)
