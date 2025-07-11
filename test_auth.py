#!/usr/bin/env python3
"""
Script de teste para verificar a autenticação Bearer do Instagram MCP Server
"""
import httpx
import asyncio
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
SERVER_URL = "http://localhost:8080"

async def test_authentication():
    """Testa a autenticação Bearer do servidor."""
    print("🧪 Testando Autenticação Bearer")
    print("=" * 40)
    
    async with httpx.AsyncClient() as client:
        # Teste 1: Requisição sem token (deve falhar)
        print("\n1. Teste sem Authorization header:")
        try:
            response = await client.get(f"{SERVER_URL}/sse")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   Erro: {e}")
        
        # Teste 2: Requisição com token inválido (deve falhar)
        print("\n2. Teste com token inválido:")
        headers = {"Authorization": "Bearer invalid_token"}
        try:
            response = await client.get(f"{SERVER_URL}/sse", headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   Erro: {e}")
        
        # Teste 3: Requisição com token válido (deve funcionar)
        if BEARER_TOKEN:
            print("\n3. Teste com token válido:")
            headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
            try:
                response = await client.get(f"{SERVER_URL}/sse", headers=headers)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    print("   ✅ Autenticação bem-sucedida!")
                else:
                    print(f"   Response: {response.text}")
            except Exception as e:
                print(f"   Erro: {e}")
        else:
            print("\n3. Token não encontrado no arquivo .env")
            print("   Configure BEARER_TOKEN no arquivo .env")

if __name__ == "__main__":
    print("⚠️  Certifique-se de que o servidor está rodando antes de executar este teste")
    print("   Execute: python instagram-mcp.py")
    print("\n" + "=" * 60)
    
    asyncio.run(test_authentication())
