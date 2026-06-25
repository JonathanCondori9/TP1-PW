import sqlite3
import mimetypes
from flask import Flask, jsonify, request, render_template
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

BD_Nom = 'pizzeria.db'

def conetar_BD():
    con = sqlite3.connect(BD_Nom)
    con.row_factory = sqlite3.Row
    return con

def iniciar_bd():
    con = conetar_BD()
    con.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            imagen_url TEXT
        )
    ''')
    con.execute('''
        CREATE TABLE IF NOT EXISTS carrito (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
    ''')
    
    count = con.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
    if count == 0:
        productos_iniciales = [
            (1, 'Muzzarella', 'Clásica con salsa de tomate, abundante muzzarella, orégano y aceitunas verdes.', 8000.0, '/static/img/muzzarella.png'),
            (2, 'Napolitana', 'Muzzarella, rodajas de tomate fresco, ajo, perejil y aceitunas.', 9500.0, '/static/img/napolitana.jpg'),
            (3, 'Fugazzetta', 'Masa esponjosa cubierta con abundante queso muzzarella y cebolla en juliana.', 10000.0, '/static/img/fugazzetta.jpg'),
            (4, 'Jamón y Morrones', 'Salsa de tomate, muzzarella, jamón cocido, morrones asados y aceitunas.', 11500.0, '/static/img/jamon_morrones.jpg'),
            (5, 'Calabresa', 'Salsa de tomate, muzzarella, rodajas de longaniza calabresa y aceitunas.', 11000.0, 'https://images.unsplash.com/photo-1628840042765-356cda07504e?q=80&w=600&auto=format&fit=crop'),
            (6, 'Caprese', 'Muzzarella, rodajas de tomate fresco, albahaca y un toque de aceite de oliva.', 10500.0, '/static/img/caprese.jpg')
        ]
        con.executemany('INSERT INTO productos (id, nombre, descripcion, precio, imagen_url) VALUES (?, ?, ?, ?, ?)', productos_iniciales)
    
    con.commit()
    con.close()

iniciar_bd()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_productos():
    """
    Productos disponibles
    ---
    responses:
      200:
        description: Una lista de productos
    """
    con = conetar_BD()
    productos = con.execute('SELECT * FROM productos').fetchall()
    con.close()
    return jsonify([dict(ix) for ix in productos]), 200

@app.route('/api/cart', methods=['POST'])
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
            productId:
              type: integer
              example: 1
    responses:
      200:
        description: Producto agregado exitosamente
      400:
        description: Faltan datos o error de validación
      404:
        description: Producto no encontrado
    """
    datos = request.get_json()
    if not datos or 'productId' not in datos:
        return jsonify({"error": "Se requiere el 'productId'"}), 400

    prod_id = datos['productId']

    con = conetar_BD()

    producto = con.execute('SELECT id FROM productos WHERE id = ?', (prod_id,)).fetchone()
    if not producto:
        con.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    item = con.execute('SELECT id, cantidad FROM carrito WHERE producto_id = ?', (prod_id,)).fetchone()
    if item:
        con.execute('UPDATE carrito SET cantidad = cantidad + 1 WHERE id = ?', (item['id'],))
    else:
        con.execute('INSERT INTO carrito (producto_id, cantidad) VALUES (?, 1)', (prod_id,))
    
    con.commit()
    con.close()

    return jsonify({"mensaje": "Producto agregado al carrito exitosamente"}), 200

@app.route('/api/cart', methods=['GET'])
def get_carrito():
    """
    Obtener el estado actual del carrito
    ---
    responses:
      200:
        description: Detalles del carrito de compras
    """
    con = conetar_BD()
    items = con.execute('''
        SELECT c.producto_id, p.nombre, p.precio, p.imagen_url, c.cantidad 
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
    ''').fetchall()
    con.close()

    resultado = []
    total = 0.0
    
    for item in items:
        subtotal = item['precio'] * item['cantidad']
        total += subtotal
        resultado.append({
            "productId": item['producto_id'],
            "name": item['nombre'],
            "price": item['precio'],
            "image": item['imagen_url'],
            "quantity": item['cantidad']
        })

    return jsonify({
        "items": resultado,
        "total": total
    }), 200

@app.route('/api/cart/<int:prod_id>', methods=['DELETE'])
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
        description: Producto no encontrado
    """
    con = conetar_BD()
    item = con.execute('SELECT id FROM carrito WHERE producto_id = ?', (prod_id,)).fetchone()
    
    if item:
        con.execute('DELETE FROM carrito WHERE id = ?', (item['id'],))
        con.commit()
        con.close()
        return jsonify({"mensaje": "Producto eliminado del carrito"}), 200
    else:
        con.close()
        return jsonify({"error": "El producto no está en el carrito"}), 404

if __name__ == '__main__':
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('application/javascript', '.js')
    app.run(debug=True, port=5000)
