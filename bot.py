import discord
from discord.ext import commands
import asyncio
import uuid
import httpx
import random

# Configurações King Dev Academy
TOKEN = "SEU_TOKEN_AQUI"  # Lembre-se: Se deixar no código, o Discord reseta!
GARENA_AUTH = "https://auth.garena.com/network/v1/login"
GARENA_LIKE = "https://freefire.api.garena.com/social/v1/like"

intents = discord.Intents.default()
bot = commands.Bot(command_command_prefix="!", intents=intents)

async def send_likes_task(ctx, uid: str, quantity: int):
    async with httpx.AsyncClient() as client:
        for i in range(quantity):
            device = str(uuid.uuid4()).replace("-", "")[:16]
            
            # Simulação de Login e Like (Lógica já discutida)
            # 1. Login... 2. Like...
            
            # Feedback no Discord a cada 5 likes para não floodar
            if (i + 1) % 5 == 0:
                await ctx.send(f"✅ {i + 1} likes enviados para o UID: {uid}")
            
            # Delay de segurança (25 likes/hora = ~144 segundos entre cada um)
            # Para 25 likes em 1 hora, usamos um delay maior:
            await asyncio.sleep(144) 

@bot.command()
async def like(ctx, uid: str, quantidade: int = 25):
    if quantidade > 30:
        await ctx.send("⚠️ Por segurança, o limite máximo é de 30 likes por comando.")
        return

    await ctx.send(f"🚀 **King Dev Academy** iniciando envio de {quantidade} likes para `{uid}`.\nTempo estimado: 1 hora.")
    
    # Inicia a tarefa em segundo plano para não travar o bot
    bot.loop.create_task(send_likes_task(ctx, uid, quantidade))

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} online - King Dev Academy")

bot.run(TOKEN)
