#!/usr/bin/env python3
"""
Script para gerar tokens Bearer seguros
"""
import secrets
import string

def generate_bearer_token(length: int = 64) -> str:
    """Gera um token Bearer seguro usando caracteres alfanuméricos."""
    alphabet = string.ascii_letters + string.digits + "-_"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hex_token(length: int = 32) -> str:
    """Gera um token Bearer seguro usando hexadecimal."""
    return secrets.token_hex(length)

def generate_url_safe_token(length: int = 32) -> str:
    """Gera um token Bearer seguro usando base64 URL-safe."""
    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    print("🔐 Gerador de Tokens Bearer Seguros")
    print("=" * 40)
    
    print("\n1. Token Alfanumérico (64 caracteres):")
    print(f"BEARER_TOKEN={generate_bearer_token()}")
    
    print("\n2. Token Hexadecimal (64 caracteres):")
    print(f"BEARER_TOKEN={generate_hex_token()}")
    
    print("\n3. Token URL-Safe Base64 (43 caracteres):")
    print(f"BEARER_TOKEN={generate_url_safe_token()}")
    
    print("\n⚠️  Importante:")
    print("- Copie um dos tokens acima e adicione ao seu arquivo .env")
    print("- Mantenha o token seguro e não compartilhe")
    print("- Use este token no header: Authorization: Bearer <seu_token>")
