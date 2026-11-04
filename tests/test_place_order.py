from decimal import Decimal
from domain.order import Order
from application.place_order import PlaceOrder, OrderRepository, Notifier
import pytest

class FakeRepo(OrderRepository):
    def __init__(self):
        self.saved_orders = []

    def save(self, order: Order) -> None:
        self.saved_orders.append(order)

class FakeNotifier(Notifier):
    def __init__(self):
        self.messages = []

    def notify(self, to: str, msg: str) -> None:
        self.messages.append((to, msg))

def test_place_order_success():
    repo = FakeRepo()
    notifier = FakeNotifier()
    use_case = PlaceOrder(repo, notifier)
    
    items = [{"product_id": "p1", "qty": 2, "price": 50}]
    order = use_case.execute(customer_id="Alice", email="alice@x.fr", items=items)

    assert order.status == "CONFIRMED"
    assert order.total() == Decimal("100")
    assert len(repo.saved_orders) == 1
    assert len(notifier.messages) == 1

def test_place_order_too_many_items():
    repo = FakeRepo()
    notifier = FakeNotifier()
    use_case = PlaceOrder(repo, notifier)
    
    items = [{"product_id": "p1", "qty": 11, "price": 10}]

    with pytest.raises(ValueError, match="Maximum 10 articles"):
        use_case.execute(customer_id="Bob", email="bob@x.fr", items=items)

def test_place_order_empty_cart():
    repo = FakeRepo()
    notifier = FakeNotifier()
    use_case = PlaceOrder(repo, notifier)
    
    # Panier vide (0 article)
    items = []

    with pytest.raises(ValueError, match="Commande vide"):
        use_case.execute(customer_id="Charlie", email="charlie@x.fr", items=items)
        