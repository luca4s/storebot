import discord, os, re, requests, emoji
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

def LojaAberta():
    ticket = 0
    guild = bot.get_guild(0)
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
    
    logchannels = [0]
    if logchannels.count(message.channel.id):
        provas = bot.get_channel(0)
        avaliacoes = bot.get_channel(0)
        data = {'provas':[],'avaliacoes':[]}
        async for prova in provas.history(limit=10):
            if prova.attachments[0]:
                data['provas'].append(prova.attachments[0].url)
        async for avaliacao in avaliacoes.history(limit=10):
            if avaliacao.author.avatar:
                data['avaliacoes'].append({'content':emoji.emojize(avaliacao.content),'avatar':avaliacao.author.avatar.url,'name':avaliacao.author.display_name})
            else:
                data['avaliacoes'].append({'content':emoji.emojize(avaliacao.content),'avatar':None,'name':avaliacao.author.display_name})
        requests.post("insira sua api", json=data)
    else:
        msg = message.content.lower()
        if (re.findall(".*loja.*aberta.*", msg) or re.findall(".*loja.*fechada.*", msg)) and msg.endswith("?"):
            ticket = 0
            lojaaberta = LojaAberta()
            response = ""
            if lojaaberta != False:
                response = f"A loja está aberta! Vá em <#{ticket}> para fazer um pedido!"
            else:
                response = f"A loja infelizmente está fechada."
            await message.reply(response)
        elif (re.findall(".*como.*compra.*", msg) or re.findall(".*como.*abre.*ticket.*", msg)) and not re.findall(".*robux.*", msg):
            comocomprar = 0
            await message.reply(f"Verifique o <#{comocomprar}>.")
        elif re.findall(".*q.*hora.*abr.*", msg) or re.findall(".*quando.*abr.*", msg) or re.findall(".*loja.*abr.*quando.*", msg):
            ticket = 0
            await message.reply(f"Não temos horário fixo.")
        elif (re.findall("vendo|vendendo", msg) or (re.findall("troco|lf|procuro|procurando", msg) and re.findall(" pix| p1x | robux ", msg))) and message.channel.id == 1068366008517140500:
            roles = [0]
            if roles.count(message.author.top_role.id):
                embed = discord.Embed(title="Possível venda detectada.", description=f"{message.content} ([Vá para a mensagem]({message.jump_url}))", color=0x990000)
                embed.set_author(name=message.author, icon_url=message.author.avatar.url)
                embed.set_footer(text=f"ID Mensagem: {message.id}\nID Remetente: {message.author.id}")
                await bot.get_channel(1071578248930131998).send("<@&0>", embed=embed)

@bot.tree.command(name="server", description="Mostra o link do servidor privado.")
async def server(interaction: discord.Interaction):
    await interaction.response.send_message("0")

@bot.tree.command(name="pix", description="Mostra o QR code do PIX para pagamento.")
async def pix(interaction: discord.Interaction):
    embed = discord.Embed(title="QR Code - PIX", description="Ou use a chave aleatória inserida no conteúdo da mensagem.", color=0xE52D2D)
    embed.set_image(url="insira imagem")
    await interaction.response.send_message("insira chave pix", embed=embed)

@bot.tree.command(name="cliente", description="Dá o cargo de cliente para alguém.")
@app_commands.describe(user = "Usuário")
async def cliente(interaction: discord.Interaction, user: discord.Member):
    roles = [0]
    if roles.count(interaction.user.top_role.id):
        if user:
            guild = bot.get_guild(1067626063410253874)
            cliente = guild.get_role(1067999699367374878)
            if guild.get_member(bot.user.id).top_role.position > cliente.position:
                await user.add_roles(cliente)
                await interaction.response.send_message(":white_check_mark: | Pronto!", ephemeral=True)
            else:
                await interaction.response.send_message(":warning: | O bot não tem a permissão de dar este cargo!", ephemeral=True)
        else:
            await interaction.response.send_message(":warning: | Este usuário não existe! Use apenas menções, tags e IDs.", ephemeral=True)
    else:
        await interaction.response.send_message(":x: | Você não tem permissão de fazer isso!", ephemeral=True)

bot.run(os.getenv("TOKEN"))
