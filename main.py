import discord
from discord.ext import commands

TOKEN_DOSYA = "token.token"

def token_oku():
    try:
        with open(TOKEN_DOSYA, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

TOKEN = token_oku()
if TOKEN is None or TOKEN == "":
    print("token.token dosyasında geçerli token yok!")
    exit()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="u!", intents=intents)

BOT_SAHIBI_ID = 123456789012345678  # Buraya kendi Discord ID'ni yaz

@bot.event
async def on_ready():
    print(f"{bot.user} aktif oldu!")

@bot.command(name="link-ekle")
async def link_ekle(ctx, url=None):
    if url is None:
        await ctx.send("❌ URL girmen gerekiyor! Örnek: `u!link-ekle https://site.com`")
        return
    with open("linkler.txt", "a", encoding="utf-8") as f:
        f.write(f"{ctx.author.id} {url}\n")
    await ctx.send(f"✅ Link eklendi: {url}")

@bot.command(name="linklerim")
async def linklerim(ctx):
    try:
        with open("linkler.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        await ctx.send("Henüz hiç link eklenmemiş.")
        return

    user_links = [line.split(' ', 1)[1].strip() for line in lines if line.startswith(str(ctx.author.id))]
    if not user_links:
        await ctx.send("Senin kayıtlı linkin yok.")
        return

    mesaj = "**Senin linklerin:**\n" + "\n".join(user_links)
    await ctx.send(mesaj)

@bot.command(name="link-sil")
async def link_sil(ctx, url=None):
    if url is None:
        await ctx.send("❌ Silmek istediğin linki yazmalısın! Örnek: `u!link-sil https://site.com`")
        return
    try:
        with open("linkler.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        await ctx.send("Henüz hiç link eklenmemiş.")
        return

    yeni_lines = []
    silindi = False
    for line in lines:
        if line.startswith(str(ctx.author.id)) and url in line:
            silindi = True
            continue
        yeni_lines.append(line)

    if silindi:
        with open("linkler.txt", "w", encoding="utf-8") as f:
            f.writelines(yeni_lines)
        await ctx.send(f"✅ Link silindi: {url}")
    else:
        await ctx.send("❌ O linki sen eklememişsin veya böyle bir link yok.")

@bot.command(name="tum_linkler")
async def tum_linkler(ctx):
    if ctx.author.id != BOT_SAHIBI_ID:
        await ctx.send("❌ Bu komutu sadece bot sahibi kullanabilir.")
        return
    try:
        with open("linkler.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        await ctx.send("Henüz hiç link eklenmemiş.")
        return
    if not lines:
        await ctx.send("Link listesi boş.")
        return

    mesaj = "**Tüm linkler:**\n" + "".join(lines)
    if len(mesaj) > 2000:
        await ctx.send("Linkler çok uzun, dosya olarak gönderiyorum...")
        with open("tum_linkler.txt", "w", encoding="utf-8") as f:
            f.writelines(lines)
        await ctx.send(file=discord.File("tum_linkler.txt"))
    else:
        await ctx.send(mesaj)

@bot.command(name="yardım")
async def yardim(ctx):
    mesaj = (
        "**Uptime Bot Komutları:**\n"
        "`u!link-ekle <url>` : Link ekle\n"
        "`u!linklerim` : Kendi linklerini göster\n"
        "`u!link-sil <url>` : Link sil\n"
        "`u!tum_linkler` : (Sadece bot sahibi) Tüm linkler\n"
        "`u!yardım` : Bu mesajı gösterir"
    )
    await ctx.send(mesaj)

bot.run(TOKEN)
