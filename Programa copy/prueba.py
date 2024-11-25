import requests

url = "http://127.0.0.1:8000/invoice"
data = {
    "name": "John Doe",
    "address": "123 Main St",
    "city": "Metropolis",
    "postal_code": "12345",
    "total": 2599.97,
    "carrito": [
        {"id": 3, "nombre": "iPhone 14 Pro", "precio": 1099.99, "cantidad": 1},
        {"id": 2, "nombre": "Dell XPS 13", "precio": 999.99, "cantidad": 1},
        {"id": 9, "nombre": "Monitor LG UltraGear 27\"", "precio": 499.99, "cantidad": 1}
    ]
}

response = requests.post(url, json=data)
print(response.text)