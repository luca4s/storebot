import discord, os, re, requests, emoji
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

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
    
    logchannels = [1067938728292651098, 1067905559203958835]
    if logchannels.count(message.channel.id):
        provas = bot.get_channel(1067938728292651098)
        avaliacoes = bot.get_channel(1067905559203958835)
        data = {'provas':[],'avaliacoes':[]}
        async for prova in provas.history(limit=10):
            if prova.attachments[0]:
                data['provas'].append(prova.attachments[0].url)
        async for avaliacao in avaliacoes.history(limit=10):
            if avaliacao.author.avatar:
                data['avaliacoes'].append({'content':emoji.emojize(avaliacao.content),'avatar':avaliacao.author.avatar.url,'name':avaliacao.author.display_name})
            else:
                data['avaliacoes'].append({'content':emoji.emojize(avaliacao.content),'avatar':None,'name':avaliacao.author.display_name})
        requests.post("https://fsmm2.herokuapp.com/post", json=data)
    else:
        msg = message.content.lower()
        if (re.findall(".*loja.*aberta.*", msg) or re.findall(".*loja.*fechada.*", msg)) and msg.endswith("?"):
            ticket = 1067933165605372036
            lojaaberta = LojaAberta()
            response = ""
            if lojaaberta != False:
                response = f"A loja está aberta! Vá em <#{ticket}> para fazer um pedido!"
            else:
                response = f"A loja infelizmente está fechada."
            await message.reply(response)
        elif (re.findall(".*como.*compra.*", msg) or re.findall(".*como.*abre.*ticket.*", msg)) and not re.findall(".*robux.*", msg):
            comocomprar = 1067904352292970606
            await message.reply(f"Verifique o <#{comocomprar}>.")
        elif re.findall(".*q.*hora.*abr.*", msg) or re.findall(".*quando.*abr.*", msg) or re.findall(".*loja.*abr.*quando.*", msg):
            ticket = 1067933165605372036
            await message.reply(f"Nos dias que iremos abrir, nós **__normalmente__** abrimos o <#{ticket}> das 19:00 as 22:00. ")
        elif (re.findall("vendo|vendendo", msg) or (re.findall("troco|lf|procuro|procurando", msg) and re.findall(" pix| p1x | robux ", msg))) and message.channel.id == 1068366008517140500:
            roles = [1069360991055388683, 1079960179774341170, 1067999699367374878, 1069163179638259733]
            if roles.count(message.author.top_role.id):
                embed = discord.Embed(title="Possível venda detectada.", description=f"{message.content} ([Vá para a mensagem]({message.jump_url}))", color=0x990000)
                embed.set_author(name=message.author, icon_url=message.author.avatar.url)
                embed.set_footer(text=f"ID Mensagem: {message.id}\nID Remetente: {message.author.id}")
                await bot.get_channel(1071578248930131998).send("<@&1071267815316803694> <@&1068396717705273384>", embed=embed)

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
async def cliente(interaction: discord.Interaction, user: discord.Member):
    roles = [1082368752512933978, 1071267815316803694, 1068721364892139541, 1068396717705273384, 1075148178543890582, 1067999262266376272, 1069723376756719697]
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