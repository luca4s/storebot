import discord, os, re
from discord import ui, app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

def LojaAberta():
    ticket = 1067933165605372036
    guild = bot.get_guild(1067626063410253874)
    return bot.get_channel(ticket).permissions_for(guild.default_role).view_channel

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
    elif not message.guild and message.author.id == 1052328074399719585 and not message.content == None:
        await bot.get_channel(1067642931185463467).send(message.content)
    
    msg = message.content.lower()
    if re.findall(".*loja.*aberta|fechada.*", msg) and msg.endswith("?"):
        ticket = 1067933165605372036
        lojaaberta = LojaAberta()
        response = ""
        if lojaaberta != False:
            response = f"A loja está aberta! Vá em <#{ticket}> para fazer um pedido!"
        else:
            response = f"A loja infelizmente está fechada."
        await message.reply(response)
    elif re.findall(".*como.*compra.*", msg) or re.findall(".*como.*abre.*ticket.*", msg):
        comocomprar = 1067904352292970606
        await message.reply(f"Verifique o <#{comocomprar}>.")
    elif re.findall(".*que.*hora.*abre.*", msg):
        ticket = 1067933165605372036
        await message.reply(f"Nós normalmente abrimos o <#{ticket}> das 17:00 as 22:30.")
    elif (re.findall("vendo|vendendo", msg) or (re.findall("troco|lf|procuro|procurando", msg) and re.findall(" pix | p1x | robux ", msg))) and message.channel.id == 1068366008517140500:
        roles = [1069360991055388683, 1079960179774341170, 1067999699367374878, 1069163179638259733]
        if roles.count(message.author.top_role.id):
            embed = discord.Embed(title="Possível venda detectada.", description=f"{message.content} ([Vá para a mensagem]({message.jump_url}))", color=0x990000)
            embed.set_author(name=message.author, icon_url=message.author.avatar.url)
            embed.set_footer(text=f"ID Mensagem: {message.id}\nID Remetente: {message.author.id}")
            await bot.get_channel(1071578248930131998).send("<@&1071267815316803694> <@&1068396717705273384>", embed=embed)
    elif msg == "<@843250104437571614> x <@1052328074399719585>" or msg == "<@1052328074399719585> x <@843250104437571614>":
        await message.reply("dois gay q eu amo mt :heart_eyes:")
        # https://docs.google.com/document/d/1qy_wclat0mKZen2NuGWqw6EIMgOJkmsWJrHtbDMxv5k/edit?usp=sharing

@bot.tree.command(name="server", description="Mostra o link do servidor privado.")
async def server(interaction: discord.Interaction):
    await interaction.response.send_message("https://www.roblox.com/games/142823291?privateServerLinkCode=71053601020321642732428738897954")

@bot.tree.command(name="pix", description="Mostra o QR code do PIX para pagamento.")
async def pix(interaction: discord.Interaction):
    embed = discord.Embed(title="QR Code - PIX", description="Ou use a chave aleatória inserida no conteúdo da mensagem.", color=0xE52D2D)
    embed.set_image(url="https://fsmm2.github.io/images/QR.png")
    await interaction.response.send_message("841a1001-12ec-46ae-8358-327595617102", embed=embed)

@bot.tree.command(name="cliente", description="Dá o cargo de cliente para alguém.")
@app_commands.describe(user = "Usuário")
async def pix(interaction: discord.Interaction, user: str):
    roles = [1071267815316803694]
    if roles.count(interaction.user.top_role.id):
        user_id = user[2:len(user)-1]
        guild = bot.get_guild(1067626063410253874)
        cliente = guild.get_role(1067999699367374878)
        guild.get_member(user_id).add_roles(cliente)
        await interaction.response.send_message("Pronto!", ephemeral=True)
    else:
        await interaction.response.send_message(":x: | Você não tem permissão de fazer isso!", ephemeral=True)

bot.run(os.getenv("TOKEN"))