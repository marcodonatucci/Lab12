from dataclasses import dataclass
from model.retailer import Retailer


@dataclass
class edges:
    retailer1: Retailer
    retailer2: Retailer
    weight: int
