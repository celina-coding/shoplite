from dataclasses import dataclass, field
from decimal import Decimal

MAX_ITEMS = 10

@dataclass
class OrderLine:
    product_id: str
    quantity: int
    unit_price: Decimal

@dataclass
class Order:
    order_id: str
    customer_id: str
    lines: list[OrderLine] = field(default_factory=list)
    status: str = "DRAFT"

    def add_line(self, line: OrderLine) -> None:
        if self.status != "DRAFT":
            raise ValueError("Commande déjà confirmée")
        if line.quantity <= 0:
            raise ValueError("Quantité invalide")
        if self.item_count() + line.quantity > MAX_ITEMS:
            raise ValueError("Maximum 10 articles")
        self.lines.append(line)

    def item_count(self) -> int:
        return sum(l.quantity for l in self.lines)

    def total(self) -> Decimal:
        return sum((l.quantity * l.unit_price for l in self.lines), Decimal("0"))

    def confirm(self) -> None:
        if not self.lines:
            raise ValueError("Commande vide")
        self.status = "CONFIRMED"
        