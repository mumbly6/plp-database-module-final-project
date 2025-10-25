# FastAPI Orders CRUD

## Requirements
Python 3.10+

## Install
py -m venv .venv
.venv\Scripts\activate   # Windows
# or `source .venv/bin/activate` on mac/linux
py -m pip install -r requirements.txt

## Run
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

## Database
SQLite file `orders.db` created automatically.

## Endpoints
POST /orders/           -> create order (body: customer_name, optional products list)
GET  /orders/           -> list orders
GET  /orders/{order_id} -> read order with products
PUT  /orders/{order_id} -> update customer name (body: customer_name)
DELETE /orders/{order_id} -> delete order

POST /orders/{order_id}/products -> add or update product (body: product, quantity)
DELETE /orders/{order_id}/products/{product} -> delete product

## Example curl
Create order:
curl -s -X POST "http://127.0.0.1:8000/orders/" -H "Content-Type: application/json" -d "{\"customer_name\":\"John Doe\",\"products\":[{\"product\":\"Laptop\",\"quantity\":2},{\"product\":\"Mouse\",\"quantity\":1}]}"

Get order:
curl "http://127.0.0.1:8000/orders/1"

Add product:
curl -X POST "http://127.0.0.1:8000/orders/1/products" -H "Content-Type: application/json" -d "{\"product\":\"Keyboard\",\"quantity\":1}"

Delete product:
curl -X DELETE "http://127.0.0.1:8000/orders/1/products/Mouse"

## GitHub
git init
git add .
git commit -m "Initial FastAPI Orders CRUD"
# create repo on GitHub then:
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
