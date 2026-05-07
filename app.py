from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

productos = [
    {"id": 1, "nombre": "Muzzarella", "precio": 8000.0, "descripcion": "Clasica con salsa de tomate y muzzarella"},
    {"id": 2, "nombre": "Napolitana", "precio": 9500.0, "descripcion": "Muzzarella, rodajas de tomate y ajo"},
    {"id": 3, "nombre": "Fugazzetta", "precio": 9000.0, "descripcion": "Muzzarella y abundante cebolla"},
    {"id": 4, "nombre": "Calabresa", "precio": 10500.0, "descripcion": "Muzzarella y longaniza"}
]

carrito = {}

@app.get('/productos')
def get_productos():
    """
    Productos disponibles
    ---
    responses:
      200:
        description: Una lista de productos
    """
    return jsonify(productos), 200

@app.post('/carrito')
def agregar_al_carrito():
    """
    Agregar un producto al carrito
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            cantidad:
              type: integer
              example: 1
    responses:
      200:
        description: Producto agregado exitosamente
      400:
        description: Faltan datos o error de validación
      404:
        description: Esta pizza no existe
    """
    datos = request.get_json()
    if not datos or 'id' not in datos:
        return jsonify({"error": "Se requiere el 'id' del producto"}), 400

    prod_id = datos['id']
    cantidad = datos['cantidad']

    if not any(p['id'] == prod_id for p in productos):
        return jsonify({"error": "Producto no encontrado"}), 404

    if prod_id in carrito:
        carrito[prod_id] += cantidad
    else:
        carrito[prod_id] = cantidad

    return jsonify({"mensaje": "Producto agregado al carrito exitosamente"}), 200

@app.get('/carrito')
def get_carrito():
    """
    Obtener el estado actual del carrito
    ---
    responses:
      200:
        description: Detalles del carrito de compras y total
    """
    items_detalle = []
    total = 0.0

    for prod_id, cantidad in carrito.items():
        producto = next((p for p in productos if p["id"] == prod_id), None)
        if producto:
            subtotal = producto["precio"] * cantidad
            total += subtotal
            items_detalle.append({
                "producto": producto,
                "cantidad": cantidad,
                "subtotal": subtotal
            })

    return jsonify({
        "items": items_detalle,
        "total": total
    }), 200


@app.delete('/carrito/<int:prod_id>')
def quitar_del_carrito(prod_id):
    """
    Eliminar un producto del carrito
    ---
    parameters:
      - name: prod_id
        in: path
        type: integer
        required: true
        description: ID del producto a eliminar
    responses:
      200:
        description: Producto eliminado exitosamente
      404:
        description: Producto no encontrado en el carrito
    """
    if prod_id in carrito:
        del carrito[prod_id]
        return jsonify({"mensaje": "Producto eliminado del carrito"}), 200
    else:
        return jsonify({"error": "El producto no está en el carrito"}), 404

if __name__ == '__main__':
    app.run(debug=True)
