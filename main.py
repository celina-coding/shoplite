from fastapi import FastAPI
from application.place_order import PlaceOrder
from infrastructure.sqlite_repo import SqliteOrderRepository
from infrastructure.smtp_notifier import SmtpNotifier

app = FastAPI()

repo = SqliteOrderRepository()
notifier = SmtpNotifier()
place_order_uc = PlaceOrder(repo, notifier)

@app.post('/orders')
def create_order(data: dict):
    try:
        order = place_order_uc.execute(
            customer_id=data['customer'],
            email=data['email'],
            items=data['items']
        )
        return {'order_id': order.order_id, 'total': str(order.total())}
    except ValueError as e:
        return {'error': str(e)}
    