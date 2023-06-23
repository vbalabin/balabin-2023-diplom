from dataclasses import dataclass
from decimal import Decimal
from helpers.wrappers import WrappedLocator
from typing import Optional


@dataclass
class InventoryItem:
    title: WrappedLocator
    description: str
    price: Decimal
    add_to_cart: Optional[WrappedLocator] = None
    remove: Optional[WrappedLocator] = None
