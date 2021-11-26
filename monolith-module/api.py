from app import app
from models import *
from flask import jsonify, request
import json


@app.route('/')
def index():
    return 'HelloWorld!'


@app.route('/customers', methods=['GET'])
def customer_index():
    return jsonify(
        [customer.to_dict() for customer in Customer.query.all()]
    )


@app.route('/customer/<id>', methods=['GET'])
def customer_show(id):
    customerCount = Customer.query.filter(Customer.id == id).count()
    if customerCount:
        return jsonify(Customer.query.filter(Customer.id == id).first().to_dict())
    else:
        return jsonify([])


@app.route('/customers', methods=['POST'])
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


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010)
