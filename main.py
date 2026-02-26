import os
import uuid
import random
import httpx
from fastapi import FastAPI, BackgroundTasks

app = FastAPI(title="King Dev Academy - Like Generator")

# Configurações extraídas via Sniffer (Exemplo)
GARENA_API = "https://freefire.api.garena.com" 
GAME_VERSION = "1.103.1" # Mantenha sempre atualizado

def generate_device_id():
    """Gera um ID de dispositivo aleatório para cada like"""
    return str(uuid.uuid4()).replace("-", "")[:16]

async def process_like(target_uid: str, region: str):
    """Lógica principal do Bot"""
    device_id = generate_device_id()
    
    async with httpx.AsyncClient() as client:
        # 1. PASSO: Autenticação Guest
        # Nota: O endpoint real deve ser capturado no login do jogo
        auth_url = f"{GARENA_API}/network/v1/login"
        auth_payload = {
            "device_id": device_id,
            "region": region,
            "version": GAME_VERSION
        }
        
        auth_res = await client.post(auth_url, json=auth_payload)
        
        if auth_res.status_code == 200:
            token = auth_res.json().get("access_token")
            
            # 2. PASSO: Enviar o Like
            like_url = f"{GARENA_API}/social/v1/like"
            headers = {
                "Authorization": f"Bearer {token}",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-G998B)",
                "Content-Type": "application/json"
            }
            like_payload = {"target_uid": target_uid}
            
            response = await client.post(like_url, json=like_payload, headers=headers)
            print(f"Like enviado para {target_uid} | Status: {response.status_code}")

@app.get("/")
def home():
    return {"message": "King Dev Academy - Gerador Ativo"}

@app.post("/add-like/{uid}")
async def add_like(uid: str, background_tasks: BackgroundTasks, region: str = "BR"):
    # Rodar em background para não travar a resposta da API
    background_tasks.add_task(process_like, uid, region)
    return {"status": "Processando", "target": uid, "info": "Likes sendo enviados em fila"}
