import json
import data
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self, arg):
        return {
            "id": arg.id,
            "first_name": arg.first_name,
            "last_name": arg.last_name,
            "age": arg.age,
            "email": arg.email,
            "role": arg.role,
            "phone": arg.phone
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self, arg):
        return {
            "id": arg.id,
            "order_id": arg.order_id,
            "executor_id": arg.executor_id
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self, arg):
        return {
            "id": arg.id,
            "name": arg.name,
            "description": arg.description,
            "start_date": arg.start_date,
            "end_date": arg.end_date,
            "address": arg.address,
            "price": arg.price,
            "customer_id": arg.customer_id,
            "executor_id": arg.executor_id
        }
@app.route('/users', methods=["GET"])
def get_users():
    result = []
    users = User.query.all()
    for user in users:
        result.append(user.to_dict(user))
    return json.dumps(result), 200

@app.route('/users/<int:uid>', methods=["GET"])
def get_user(uid):
    result = []
    user = User.query.get(uid)
    result.append(user.to_dict(user))
    return result, 200

@app.route('/users', methods=["POST"])
def add_user():
    user = json.loads(request.data)
    new_user = User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    )
    db.session.add(new_user)
    db.session.commit()
    return "", 201


@app.route('/users/<int:uid>', methods=['PUT'])
def edit_user(uid):
    user_data = json.loads(request.data)
    user = User.query.get(uid)
    user.first_name = user_data["first_name"]
    user.last_name = user_data["last_name"]
    user.age = user_data["age"]
    user.email = user_data["email"]
    user.role = user_data["role"]
    user.phone = user_data["phone"]

    db.session.add(user)
    db.session.commit()
    return "", 204
@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    user = User.query.get(uid)
    db.session.delete(user)
    db.session.commit()
    return "", 204

@app.route('/offers', methods=['GET'])
def get_offers():
    result = []
    offers = Offer.query.all()
    for offer in offers:
        result.append(offer.to_dict(offer))
    return json.dumps(result), 200

@app.route('/offers/<int:oid>', methods=['GET'])
def get_offer(oid):
    result = []
    offer = Offer.query.get(oid)
    result.append(offer.to_dict(offer))
    return result, 200
@app.route('/offers', methods=["POST"])
def add_offer():
    offer = json.loads(request.data)
    new_offer = Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id']
    )

    db.session.add(new_offer)
    db.session.commit()
    return "", 201

@app.route('/offers/<int:oid>', methods=['PUT'])
def edit_offer(oid):
    offer_data = json.loads(request.data)
    offer = Offer.query.get(oid)
    offer.order_id = offer_data["order_id"]
    offer.executor_id = offer_data["executor_id"]

    db.session.add(offer)
    db.session.commit()
    return "", 204

@app.route('/offers/<int:ofid>', methods=['DELETE'])
def delete_offer(ofid):
    offer = Offer.query.get(ofid)
    db.session.delete(offer)
    db.session.commit()
    return "", 204

@app.route('/orders', methods=["GET"])
def get_orders():
    result = []
    orders = Order.query.all()
    for order in orders:
         result.append(order.to_dict(order))
    return json.dumps(result), 200

@app.route('/orders/<int:oid>', methods=["GET"])
def get_order(oid):
    result = []
    order = Order.query.get(oid)
    result.append(order.to_dict(order))
    return result, 200

@app.route('/orders', methods=["POST"])
def add_order():
    order = json.loads(request.data)
    new_order = Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    )

    db.session.add(new_order)
    db.session.commit()
    return "", 201


@app.route('/orders/<int:oid>', methods=['PUT'])
def edit_order(oid):
    order_data = json.loads(request.data)
    order = Order.query.get(oid)
    order.description = order_data["description"]
    order.start_date = order_data["start_date"]
    order.end_date = order_data["end_date"]
    order.address = order_data["address"]
    order.price = order_data["price"]
    order.customer_id = order_data["customer_id"]
    order.executor_id = order_data["executor_id"]

    db.session.add(order)
    db.session.commit()
    return "", 204


@app.route('/orders/<int:oid>', methods=['DELETE'])
def delete_order(oid):
    order = Order.query.get(oid)
    db.session.delete(order)
    db.session.commit()
    return "", 204

def create_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
    for user in data.users:
        user = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        )

        db.session.add(user)
        db.session.commit()

    for order in data.orders:
        order = Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=order['start_date'],
            end_date=order['end_date'],
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        )

        db.session.add(order)
        db.session.commit()

    for offer in data.offers:
        offer = Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )

        db.session.add(offer)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_database()
    app.run(debug=True)
