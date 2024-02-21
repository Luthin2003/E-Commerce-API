from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)
api = Api(app)

# Define Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

# Define CartItem model
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# API resource for products
class ProductsResource(Resource):
    def get(self):
        products = Product.query.all()
        return jsonify([{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price, 'image_url': p.image_url} for p in products])
    
    def post(self):
        data = request.get_json()
        if 'product_id' not in data or 'price' not in data  or 'name' not in data or 'description' not in data  or 'image_url' not in data:
            abort(400)

        price = data['price']
        name = data["name"]
        image_url = data["image_url"]
        description = data["description"]
        product_id = data['product_id']

        product_item = Product(price=price, name=name , image_url=image_url ,description = description , product_id=product_id )
        db.session.add(product_item )

        db.session.commit()
        return {'message': 'new Product added successfully to store'}, 201


class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            abort(404)
        return jsonify({'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'image_url': product.image_url})

# API resource for cart
class CartResource(Resource):
    def get(self):
        cart_items = CartItem.query.all()
        cart = [{'id': item.id, 'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]
        return jsonify(cart)

    def post(self):
        data = request.get_json()
        if 'product_id' not in data or 'quantity' not in data:
            abort(400)
        product_id = data['product_id']
        quantity = data['quantity']
        cart_item = CartItem(product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        return {'message': 'Cart item added successfully'}, 201

class CartItemResource(Resource):
    def delete(self, item_id):
        cart_item = CartItem.query.get(item_id)
        if not cart_item:
            abort(404)
        db.session.delete(cart_item)
        db.session.commit()
        return '', 204

# Add resources to API
api.add_resource(ProductsResource, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')
api.add_resource(CartResource, '/cart')
api.add_resource(CartItemResource, '/cart/<int:item_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
