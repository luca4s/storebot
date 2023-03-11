import discord, os, re
from discord import ui, app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

def LojaAberta():
    tickets = 1067933165605372036
    guild = bot.get_guild(1067626063410253874)
    return bot.get_channel(tickets).permissions_for(guild.default_role).view_channel

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
    except Exception as e:
        print(f"Error syncing command(s): {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    msg = message.content.lower()
    if len(re.findall("loja|aberta|fechada", msg)) >= 2 and msg.endswith("?"):
        tickets = 1067933165605372036
        horarios = 1070775740653654027
        lojaaberta = LojaAberta()
        response = ""
        if lojaaberta != False:
            response = f"A loja está aberta! Vá em <#{tickets}> para fazer um pedido!"
        else:
            response = f"A loja infelizmente está fechada. Verifique os <#{horarios}> caso queira abrir um mais tarde!"
        await message.reply(response)
    elif re.findall(".*como.*compra", msg) or re.findall(".*como.*abre.*ticket.*", msg):
        comocomprar = 1067904352292970606
        lojaaberta = LojaAberta()
        response = ""
        if lojaaberta != False:
            response = f"Verifique o <#{comocomprar}>."
        else:
            response = f"Atualmente a loja está fechada, mas verifique o <#{comocomprar}>."
        await message.reply(response)
    elif (re.findall("vendo|vendendo", msg) or (re.findall("troco|lf|procuro|procurando", msg) and re.findall("pix|p1x|robux", msg))) and message.channel.id == 1068366008517140500:
        roles = [1069360991055388683, 1079960179774341170, 1067999699367374878, 1069163179638259733]
        if roles.count(message.author.top_role.id):
            embed = discord.Embed(title="Possível venda detectada.", description=f"{message.content} ([Vá para a mensagem]({message.jump_url}))", color=0x990000)
            embed.set_author(name=message.author, icon_url=message.author.avatar.url)
            embed.set_footer(text=f"ID Mensagem: {message.id}\nID Remetente: {message.author.id}")
            await bot.get_channel(1071578248930131998).send("<@&1071267815316803694> <@&1068396717705273384>", embed=embed)
    elif len(re.findall("<@843250104437571614>|x|<@1052328074399719585>", msg)) == 3:
        await message.reply("dois gay q eu amo mt :heart_eyes:")

@bot.tree.command(name="server", description="Mostra o link do servidor privado.")
async def server(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.roblox.com/games/142823291?privateServerLinkCode=71053601020321642732428738897954")

@bot.tree.command(name="pix", description="Mostra o QR code do PIX para pagamento.")
async def pix(interaction: discord.Interaction):
    embed = discord.Embed(title="QR Code - PIX", description="Ou use a chave aleatória inserida no conteúdo da mensagem.", color=0xE52D2D)
    embed.set_image(url="https://fsmm2.github.io/images/QR.png")
    await interaction.response.send_message("841a1001-12ec-46ae-8358-327595617102", embed=embed)

bot.run(os.getenv("TOKEN"))