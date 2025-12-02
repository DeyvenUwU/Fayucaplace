#!/usr/bin/env python
"""
Script para generar una SECRET_KEY segura para Django.
Uso: python generate_secret_key.py
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("\nGenerated SECRET_KEY:")
    print(f"export DJANGO_SECRET_KEY='{secret_key}'")
    print(f"\nO en PowerShell:")
    print(f"$env:DJANGO_SECRET_KEY = '{secret_key}'")
    print(f"\nO en .env:")
    print(f"DJANGO_SECRET_KEY={secret_key}")
