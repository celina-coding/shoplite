import sqlite3
from domain.order import Order
from application.place_order import OrderRepository

class SqliteOrderRepository(OrderRepository):
    def __init__(self, db_name="shop.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute('''CREATE TABLE IF NOT EXISTS orders
                        (order_id TEXT, customer TEXT, total REAL)''')
        conn.commit()
        conn.close()

    def save(self, order: Order) -> None:
        conn = sqlite3.connect(self.db_name)
        conn.execute('INSERT INTO orders (order_id, customer, total) VALUES (?, ?, ?)',
                     (order.order_id, order.customer_id, float(order.total())))
        conn.commit()
        conn.close()
        