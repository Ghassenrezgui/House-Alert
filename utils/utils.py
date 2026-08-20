"""
utils.py

Shared utilities: logging helper, price/size filter criteria, and validation logic.
"""

from __future__ import annotations

import re
from datetime import datetime

# Critère principal de recherche
TARGET_HOUSES = [
    {"price": 1650.0, "sizeMin": 35.0},
]

def log(message: str = "Log", domain: str = "app") -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\033[90m{timestamp}\033[0m｜[House-Alert] [{domain}] {message}")

def check_price_in_range(price: float | str, size: float | str, title: str = "") -> bool:
    """
    Retourne True si le bien respecte le prix, la taille minimale ET est un 3 pièces / T3.
    """
    price = float(re.sub(r'[^\d.]', '', price.replace(" ", "").replace(",", "."))) if isinstance(price, str) else price
    size  = float(re.sub(r'm.*$',   '', size ).replace(" ", "").replace(",", ".")) if isinstance(size,  str) else size

    # Sécurité T3 : Si un titre ou descriptif est fourni, on vérifie la présence de "3 pièces", "t3", "f3" ou "2 chambres"
    if title:
        title_clean = title.lower()
        has_3_rooms = any(x in title_clean for x in ["3 pièces", "3 pieces", "t3", "f3", "3 p.", "2 chambres", "2 ch"])
        # Si l'annonce mentionne explicitement un studio ou un 2 pièces (T2/F2), on l'exclut d'office
        is_smaller = any(x in title_clean for x in ["studio", "1 pièce", "1 piece", "2 pièces", "2 pieces", "t2", "f2", "1 chambre", "1 ch"])
        
        if is_smaller and not has_3_rooms:
            return False

    for house in TARGET_HOUSES:
        if size >= house["sizeMin"] and price <= house["price"]:
            return True

    return False
