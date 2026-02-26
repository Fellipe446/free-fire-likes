import os
import asyncio
import discord
from discord.ext import commands
from fastapi import FastAPI
import uvicorn
import threading
import uuid
import httpx
import random

# --- CONFIGURAÇÃO WEB (FASTAPI) ---
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "King Dev Academy - Online", "bot": "Active"}

# --- CONFIGURAÇÃO DISCORD BOT ---
TOKEN = os.getenv("DISCORD_TOKEN") # Pega o token das variáveis do Render
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def send_likes_logic(ctx, uid: str, amount: int):
    async with httpx.AsyncClient() as client:
        for i in range(amount):
            # Simulação do processo Garena
            # Aqui você insere a lógica de Login Guest + POST Like que discutimos
            await asyncio.sleep(random.randint(140, 150)) # Delay para 25/hora
            
            if (i + 1) % 5 == 0:
                await ctx.send(f"✅ **[{i+1}/{amount}]** Likes processados para o UID: `{uid}`")

@bot.command()
async def like(ctx, uid: str):
    # Definimos 25 como padrão para King Dev Academy
    quantidade = 25
    await ctx.send(f"⚡ **King Dev Academy**\nIniciando ciclo de **{quantidade} likes** para o UID: `{uid}`\nPrevisão: 60 minutos.")
    bot.loop.create_task(send_likes_logic(ctx, uid, quantidade))

@bot.event
async def on_ready():
    print(f"Bot logado como {bot.user.name} - King Dev Academy")

# --- EXECUÇÃO EM PARALELO ---
def run_api():
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Inicia o servidor Web em uma thread separada
    t = threading.Thread(target=run_api)
    t.start()
    
    # Roda o bot do Discord na thread principal
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERRO: Variável DISCORD_TOKEN não encontrada!")
