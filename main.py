from fastapi import FastAPI
from uvicorn import run as uvicorn_run

app = FastAPI(title="Multitasker")

fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
]


@app.get('/users/{user_id}')
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC",
        "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC",
        "side": "sell", "price": 125, "amount": 2.12},
    {"id": 3, "user_id": 1, "currency": "BTC",
        "side": "sell", "price": 125, "amount": 2.12},
    {"id": 4, "user_id": 1, "currency": "BTC",
        "side": "sell", "price": 125, "amount": 2.12},
    {"id": 5, "user_id": 1, "currency": "BTC",
        "side": "sell", "price": 125, "amount": 2.12},
]


@app.get('/trades')
def get_trades(limit: int = 2, offset: int = 0):
    return fake_trades[offset:][:limit]


fake_users2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
]


def get_user_by_id(user_id: int, user_list: list):
    return list(filter(lambda user: user.get('id') == user_id, user_list))[0]


@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = get_user_by_id(user_id, fake_users2)
    print(current_user)
    current_user['name'] = new_name
    return {'status': 200, 'data': current_user}


if __name__ == '__main__':
    uvicorn_run('main:app', reload=True)
