from abc import ABC, abstractmethod
from decimal import Decimal
import uuid
from domain.order import Order, OrderLine

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass

class Notifier(ABC):
    @abstractmethod
    def notify(self, to: str, msg: str) -> None:
        pass

class PlaceOrder:
    def __init__(self, repo: OrderRepository, notifier: Notifier):
        self.repo = repo
        self.notifier = notifier

    def execute(self, customer_id: str, email: str, items: list[dict]) -> Order:
        order = Order(order_id=str(uuid.uuid4()), customer_id=customer_id)
        for it in items:
            order.add_line(OrderLine(it["product_id"], it["qty"], Decimal(str(it["price"]))))
        order.confirm()
        self.repo.save(order)
        self.notifier.notify(email, "Merci pour votre commande !")
        return order
        