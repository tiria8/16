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

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }

@app.route('/users', methods=["GET"])
def get_users():
    id = request.args.get("id")
    result = []
    if not id:
        users = User.query.all()
        for user in users:
            result.append(user.to_dict(user))
        return json.dumps(result)
    users = User.query.filter_by(id=id)
    for user in users:
        result.append(user.to_dict(user))
    return json.dumps(result)


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


@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    user = User.query.get(uid)
    db.session.delete(user)
    db.session.commit()

class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }

@app.route('/offers', methods=['GET'])
def get_offers():
    id = request.args.get("id")
    result = []
    if not id:
        offers = Offer.query.all()
        for offer in offers:
            result.append(offers.to_dict(offer))
        return json.dumps(result)
    offers = Offer.query.filter_by(id=id)
    for offer in offers:
        result.append(offers.to_dict(offer))
    return json.dumps(result)


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


@app.route('/offers/<int:oid>', methods=['PUT'])
def edit_offer(oid):
    offer_data = json.loads(request.data)
    offer = Offer.query.get(oid)
    offer.order_id = offer_data["order_id"]
    offer.executor_id = offer_data["executor_id"]

    db.session.add(offer)
    db.session.commit()


@app.route('/offers/<int:ofid>', methods=['DELETE'])
def delete_offer(ofid):
    offer = Offer.query.get(ofid)
    db.session.delete(offer)
    db.session.commit()


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }

@app.route('/orders', methods=["GET"])
def get_orders():
    id = request.args.get("id")
    result = []
    if not id:
        orders = Order.query.all()
        for order in orders:
            result.append(orders.to_dict(order))
        return json.dumps(result)
    orders = Order.query.filter_by(id=id)
    for order in orders:
        result.append(orders.to_dict(order))
    return json.dumps(result)


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


@app.route('/orders/<int:oid>', methods=['DELETE'])
def delete_order(oid):
    order = Order.query.get(oid)
    db.session.delete(order)
    db.session.commit()

def create_database():
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
    create_database()
    app.run(debug=True)
