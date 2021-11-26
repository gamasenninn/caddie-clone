from app import app
from models import *
from flask import jsonify, request
import json


@app.route('/')
def index():
    return 'HelloWorld!'


# -----得意先(Customer)-----
@app.route('/customer', methods=['GET'])
def customer_index():
    customer = Customer.query.all()
    return jsonify(CustomerSchema(many=True).dump(customer))


@app.route('/customer/<id>', methods=['GET'])
def customer_show(id):
    customerCount = Customer.query.filter(Customer.id == id).count()
    if customerCount:
        customer = Customer.query.filter(Customer.id == id).first()
        return jsonify(CustomerSchema().dump(customer))
    else:
        return jsonify([])


@app.route('/customer', methods=['POST'])
def customer_create():
    data = request.json
    newCustomer = Customer(
        customerName=data['customerName'],
        honorificTitle=data['honorificTitle'],
        postNumber=data['postNumber'],
        address=data['address'],
        telNumber=data['telNumber'],
        faxNumber=data['faxNumber'],
        url=data['url'],
        email=data['email'],
        manager=data['manager'],
        representative=data['representative'],
        memo=data['memo'],
    )
    db.session.add(newCustomer)
    db.session.commit()
    id = newCustomer.id
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/customer/<id>', methods=['PUT'])
def customer_update(id):
    data = request.json
    customer = Customer.query.filter(Customer.id == id).one()

    customer.customerName = data['customerName']
    customer.honorificTitle = data['honorificTitle']
    customer.postNumber = data['postNumber']
    customer.address = data['address']
    customer.telNumber = data['telNumber']
    customer.faxNumber = data['faxNumber']
    customer.url = data['url']
    customer.email = data['email']
    customer.manager = data['manager']
    customer.representative = data['representative']
    customer.memo = data['memo']

    db.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/customer/<id>', methods=['DELETE'])
def customer_destroy(id):
    customer = Customer.query.filter(Customer.id == id).delete()
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# -----商品(item)-----
@app.route('/item', methods=['GET'])
def item_index():
    return jsonify(
        [item.to_dict() for item in Item.query.all()]
    )


@app.route('/item/<id>', methods=['GET'])
def item_show(id):
    itemCount = Item.query.filter(Item.id == id).count()
    if itemCount:
        return jsonify(Item.query.filter(Item.id == id).first().to_dict())
    else:
        return jsonify([])


@app.route('/item', methods=['POST'])
def item_create():
    data = request.json
    newItem = Customer(
        itemName=data['itemName'],
        unit=data['unit'],
        price=data['price'],
        cost=data['cost'],
        costRate=data['costRate'],
        memo=data['memo'],
    )
    db.session.add(newItem)
    db.session.commit()
    id = newItem.id
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/item/<id>', methods=['PUT'])
def item_update(id):
    data = request.json
    item = Item.query.filter(Item.id == id).one()

    item.itemName = data['itemName']
    item.unit = data['unit']
    item.price = data['price']
    item.cost = data['cost']
    item.costRate = data['costRate']
    item.memo = data['memo']

    db.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/item/<id>', methods=['DELETE'])
def item_destroy(id):
    item = Item.query.filter(Item.id == id).delete()
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010)
