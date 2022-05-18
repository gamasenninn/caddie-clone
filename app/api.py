import sqlite3
from app import app
from models import *
from flask import jsonify, request
import json
from datetime import date, datetime
from dateutil import relativedelta
from sqlalchemy import desc, or_, and_, extract
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash


_LIMIT_NUM = 100

# -----ユーザー(Users)-----


@app.route('/users', methods=['GET'])
def user_index():
    users = User.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='User',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(UserSchema(many=True).dump(users))


@app.route('/user/<id>', methods=['GET'])
def user_show(id):
    userCount = User.query.filter(User.id == id).count()
    if userCount:
        user = User.query.filter(User.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='User',
            modelId=id,
            action='get'
        )
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(UserSchema().dump(user))
    else:
        return jsonify([])


@app.route('/user', methods=['POST'])
def user_create():
    data = request.json
    anyNum = User.query.filter(User.anyNumber == data.get('anyNumber'))
    anyName = User.query.filter(User.anyName == data.get('anyName'))
    if db.session.query(anyNum.exists()).scalar():
        return jsonify({"result": "error", "message": "入力した任意番号は既に存在します。存在しない値を入力してください。"}), 500
    if db.session.query(anyName.exists()).scalar():
        return jsonify({"result": "error", "message": "入力した任意名は既に存在します。存在しない値を入力してください。"}), 500
    if data.get('anyNumber') is None or data.get('anyName') is None or data.get('name') is None or data.get('password') is None or data.get('anyNumber') == '' or data.get('anyName') == '' or data.get('name') == '' or data.get('password') == '':
        return jsonify({"result": "error", "message": "必須項目に空欄があります。値を入力してください。"}), 500
    newUser = User(
        anyNumber=data.get('anyNumber'),
        anyName=data.get('anyName'),
        name=data.get('name'),
        password=generate_password_hash(data.get('password')),
        group=data.get('group'),
        role=data.get('role'),
    )
    db.session.add(newUser)
    db.session.commit()
    id = newUser.id
    newHistory = History(
        userName=current_user.id,
        modelName='User',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/user/<id>', methods=['PUT'])
def user_update(id):
    data = request.json
    anyNum = User.query.filter(User.anyNumber == data.get('anyNumber'))
    anyName = User.query.filter(User.anyName == data.get('anyName'))
    user = User.query.filter(User.id == id).one()
    if db.session.query(anyNum.exists()).scalar() and user.anyNumber != data.get('anyNumber'):
        return jsonify({"result": "error", "message": "入力した任意番号は既に存在します。存在しない値を入力してください。"}), 500
    if db.session.query(anyName.exists()).scalar() and user.anyName != data.get('anyName'):
        return jsonify({"result": "error", "message": "入力した任意名は既に存在します。存在しない値を入力してください。"}), 500
    if data.get('anyNumber') is None or data.get('anyName') is None or data.get('name') is None or data.get('password') is None or data.get('anyNumber') == '' or data.get('anyName') == '' or data.get('name') == '' or data.get('password') == '':
        return jsonify({"result": "error", "message": "必須項目に空欄があります。値を入力してください。"}), 500

    user.anyNumber = data.get('anyNumber')
    user.anyName = data.get('anyName')
    user.name = data.get('name')
    user.password = generate_password_hash(data.get('password'))
    user.group = data.get('group')
    user.role = data.get('role')

    newHistory = History(
        userName=current_user.id,
        modelName='User',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/user/<id>', methods=['DELETE'])
def user_destroy(id):
    user = User.query.filter(User.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='User',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# -----得意先(Customers)-----
@app.route('/v1/customers', methods=['GET'])
@app.route('/customers', methods=['GET'])
def customer_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    # テスト的に300に
    limit = int(req.get('limit')) if req.get('limit') else 300
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        customers = Customer.query.filter(or_(
            Customer.customerName.like('%'+searchWord+'%'),
            Customer.customerKana.like('%'+searchWord+'%'),
            Customer.anyNumber == searchWord,
        ))
    else:
        customers = Customer.query
    if offset:
        customers = customers.offset(offset)
    if limit:
        customers = customers.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Customer',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    return jsonify(CustomerSchema(many=True).dump(customers))


@app.route('/v1/customer/<id>', methods=['GET'])
@app.route('/customer/<id>', methods=['GET'])
def customer_show(id):
    customerCount = Customer.query.filter(Customer.id == id).count()
    if customerCount:
        customer = Customer.query.filter(Customer.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Customer',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(CustomerSchema().dump(customer))
    else:
        return jsonify([])


@app.route('/v1/customer', methods=['POST'])
@app.route('/customer', methods=['POST'])
def customer_create():
    data = request.json
    query = Customer.query.filter(Customer.anyNumber == data.get('anyNumber'))
    if db.session.query(query.exists()).scalar():
        return jsonify({"result": "error", "message": "入力した任意番号は既に存在します。存在しない値を入力してください。"}), 500
    if data.get('anyNumber') is None or data.get('anyNumber') == '':
        return jsonify({"result": "error", "message": "必須項目に空欄があります。値を入力してください。"}), 500
    newCustomer = Customer(
        anyNumber=data.get('anyNumber'),
        customerName=data.get('customerName'),
        customerKana=data.get('customerKana'),
        honorificTitle=data.get('honorificTitle'),
        department=data.get('department'),
        postNumber=data.get('postNumber'),
        address=data.get('address'),
        addressSub=data.get('addressSub'),
        telNumber=data.get('telNumber'),
        faxNumber=data.get('faxNumber'),
        url=data.get('url'),
        email=data.get('email'),
        manager=data.get('manager'),
        representative=data.get('representative'),
        customerCategory=data.get('customerCategory'),
        isHide=data.get('isHide'),
        isFavorite=data.get('isFavorite'),
        memo=data.get('memo'),
    )
    db.session.add(newCustomer)
    db.session.commit()
    id = newCustomer.id
    newHistory = History(
        userName=current_user.id,
        modelName='Customer',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/customer/<id>', methods=['PUT'])
@app.route('/customer/<id>', methods=['PUT'])
def customer_update(id):
    data = request.json
    query = Customer.query.filter(Customer.anyNumber == data.get('anyNumber'))
    customer = Customer.query.filter(Customer.id == id).one()
    if db.session.query(query.exists()).scalar() and customer.anyNumber != data.get('anyNumber'):
        return jsonify({"result": "error", "message": "入力した任意番号は既に存在します。存在しない値を入力してください。"}), 500
    if data.get('anyNumber') is None or data.get('anyNumber') == '':
        return jsonify({"result": "error", "message": "必須項目に空欄があります。値を入力してください。"}), 500

    customer.anyNumber = data.get('anyNumber')
    customer.customerName = data.get('customerName')
    customer.customerKana = data.get('customerKana')
    customer.honorificTitle = data.get('honorificTitle')
    customer.department = data.get('department')
    customer.postNumber = data.get('postNumber')
    customer.address = data.get('address')
    customer.addressSub = data.get('addressSub')
    customer.telNumber = data.get('telNumber')
    customer.faxNumber = data.get('faxNumber')
    customer.url = data.get('url')
    customer.email = data.get('email')
    customer.manager = data.get('manager')
    customer.representative = data.get('representative')
    customer.customerCategory = data.get('customerCategory')if data.get(
        'customerCategory') else 'corporation'  # ページリロード後、更新時のエラー防止
    customer.isHide = data.get('isHide')if data.get(
        'isHide') else False  # ページリロード後、更新時のエラー防止
    customer.isFavorite = data.get('isFavorite')if data.get(
        'isFavorite') else False  # ページリロード後、更新時のエラー防止
    customer.memo = data.get('memo')

    newHistory = History(
        userName=current_user.id,
        modelName='Customer',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/customer/<id>', methods=['DELETE'])
@app.route('/customer/<id>', methods=['DELETE'])
def customer_destroy(id):
    customer = Customer.query.filter(Customer.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Customer',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# -----商品(Items)-----
@app.route('/v1/items', methods=['GET'])
@app.route('/items', methods=['GET'])
def item_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    limit = int(req.get('limit')) if req.get('limit') else _LIMIT_NUM
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        items = Item.query.filter(or_(
            Item.itemName.like('%'+searchWord+'%'),
            Item.itemCode.like('%'+searchWord+'%'),
            Item.model.like('%'+searchWord+'%'),
        ))
    else:
        items = Item.query
    if offset:
        items = items.offset(offset)
    if limit:
        items = items.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Item',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    return jsonify(ItemSchema(many=True).dump(items))


@app.route('/v1/item/<id>', methods=['GET'])
@app.route('/item/<id>', methods=['GET'])
def item_show(id):
    itemCount = Item.query.filter(Item.id == id).count()
    if itemCount:
        item = Item.query.filter(Item.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Item',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(ItemSchema().dump(item))
    else:
        return jsonify({})


@app.route('/v1/item', methods=['POST'])
def item_create():
    data = request.json
    query = Item.query.filter(Item.itemCode == data.get('itemCode'))
    if db.session.query(query.exists()).scalar() and data.get('itemCode') != None and data.get('itemCode') != '':
        return jsonify({"result": "error", "message": "入力した商品コードは既に存在します。存在しない値を入力してください。"}), 500
    newItem = Item(
        itemName=data.get('itemName'),
        itemCode=data.get('itemCode'),
        model=data.get('model'),
        category=data.get('category'),
        maker=data.get('maker'),
        supplier=data.get('supplier'),
        unit=data.get('unit'),
        basePrice=data.get('basePrice'),
        baseCost=data.get('baseCost'),
        isHide=data.get('isHide'),
        memo=data.get('memo'),
        numberOfAttachments=data.get('numberOfAttachments'),
    )
    db.session.add(newItem)
    db.session.commit()
    id = newItem.id
    newHistory = History(
        userName=current_user.id,
        modelName='Item',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/item/<id>', methods=['PUT'])
def item_update(id):
    data = request.json
    item = Item.query.filter(Item.id == id).one()
    query = Item.query.filter(Item.itemCode == data.get('itemCode'))
    if db.session.query(query.exists()).scalar() and item.itemCode != data.get('itemCode') and (data.get('itemCode') != None and data.get('itemCode') != ''):
        return jsonify({"result": "error", "message": "入力した商品コードは既に存在します。存在しない値を入力してください。"}), 500

    item.itemName = data.get('itemName')
    item.itemCode = data.get('itemCode')
    item.model = data.get('model')
    item.category = data.get('category')
    item.maker = data.get('maker')
    item.supplier = data.get('supplier')
    item.unit = data.get('unit')
    item.basePrice = data.get('basePrice')
    item.baseCost = data.get('baseCost')
    item.isHide = data.get('isHide')if data.get(
        'isHide') else False  # ページリロード後、更新時のエラー防止
    item.memo = data.get('memo')
    item.numberOfAttachments = data.get('numberOfAttachments')

    newHistory = History(
        userName=current_user.id,
        modelName='Item',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/item/<id>', methods=['DELETE'])
def item_destroy(id):
    item = Item.query.filter(Item.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Item',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# -----請求書(Invoices)-----
@app.route('/v1/invoices', methods=['GET'])
@app.route('/invoices', methods=['GET'])
def invoice_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    # テスト的に300に
    limit = int(req.get('limit')) if req.get('limit') else 300
    offset = int(req.get('offset')) if req.get('offset') else 0
    reqMonth = int(req.get('month')) if req.get('month') else None
    reqYear = int(req.get('year')) if req.get('year') else None
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            invoices = Invoice.query.filter(and_(Invoice.isDelete == False, or_(
                extract('year', Invoice.applyDate) == searchWord, Invoice.customerName.like('%'+searchWord+'%'))))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            invoices = Invoice.query.filter(and_(Invoice.isDelete == False, or_(
                Invoice.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Invoice.applyDate) == year, extract('month', Invoice.applyDate) == month))))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            invoices = Invoice.query.filter(and_(Invoice.isDelete == False, or_(
                Invoice.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Invoice.applyDate) == year, extract('month', Invoice.applyDate) == month, extract('day', Invoice.applyDate) == day))))
        else:
            invoices = Invoice.query.filter(
                and_(Invoice.isDelete == False, Invoice.customerName.like('%'+searchWord+'%')))
    if reqYear and reqMonth:
        beforeDate = date(reqYear, reqMonth, 1)
        afterDate = beforeDate + \
            relativedelta.relativedelta(
                years=1)-relativedelta.relativedelta(days=1)
        invoices = Invoice.query.filter(and_(
            Invoice.isDelete == False, Invoice.applyDate.between(beforeDate, afterDate)))
    else:
        invoices = Invoice.query.filter(Invoice.isDelete == False)
    if offset:
        invoices = invoices.offset(offset)
    if limit:
        invoices = invoices.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(InvoiceSchema(many=True).dump(invoices))


@app.route('/v1/dust-invoices', methods=['GET'])
@app.route('/dust-invoices', methods=['GET'])
def dust_invoice_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    # テスト的に300に
    limit = int(req.get('limit')) if req.get('limit') else 300
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            invoices = Invoice.query.filter(and_(Invoice.isDelete == True, or_(
                extract('year', Invoice.applyDate) == searchWord, Invoice.customerName.like('%'+searchWord+'%'))))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            invoices = Invoice.query.filter(and_(Invoice.isDelete == True, or_(
                Invoice.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Invoice.applyDate) == year, extract('month', Invoice.applyDate) == month))))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            invoices = Invoice.query.filter(and_(Invoice.isDelete == True, or_(
                Invoice.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Invoice.applyDate) == year, extract('month', Invoice.applyDate) == month, extract('day', Invoice.applyDate) == day))))
        else:
            invoices = Invoice.query.filter(
                and_(Invoice.isDelete == True, Invoice.customerName.like('%'+searchWord+'%')))
    else:
        invoices = Invoice.query.filter(Invoice.isDelete == True)
    if offset:
        invoices = invoices.offset(offset)
    if limit:
        invoices = invoices.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Invoice(dust)',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()

    return jsonify(InvoiceSchema(many=True).dump(invoices))


@app.route('/v1/invoice/<id>', methods=['GET'])
@app.route('/invoice/<id>', methods=['GET'])
def invoice_show(id):
    invoiceCount = Invoice.query.filter(Invoice.id == id).count()
    if invoiceCount:
        invoice = Invoice.query.filter(Invoice.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Invoice',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(InvoiceSchema().dump(invoice))
    else:
        return jsonify([])


@app.route('/v1/invoice', methods=['POST'])
@app.route('/invoice', methods=['POST'])
def invoice_create():
    data = request.json
    newInvoiceItems = []
    if data.get('invoice_items'):
        for item in data.get('invoice_items'):
            if item.get('isDelete'):
                if item['isDelete']:
                    continue
            newInvoiceItems.append(
                Invoice_Item(
                    invoiceId=item.get('invoiceId'),
                    itemId=item.get('itemId'),
                    any=item.get('any'),
                    itemName=item.get('itemName'),
                    price=item.get('price'),
                    count=item.get('count'),
                    unit=item.get('unit'),
                    remarks=item.get('remarks'),
                )
            )

        # newInvoiceItems = [
        #    Invoice_Item(
        #        invoiceId=item.get('invoiceId'),
        #        itemId=item.get('itemId'),
        #        price=item.get('price'),
        #        count=item.get('count'),
        #        unit=item.get('unit'),
        #        itemName=item.get('itemName'),
        #    )
        #    for item in data.get('invoice_items')
        # ]

    newInvoice = Invoice(
        customerId=data.get('customerId'),
        customerName=data.get('customerName'),
        customerAnyNumber=data.get('customerAnyNumber'),
        honorificTitle=data.get('honorificTitle'),
        department=data.get('department'),
        manager=data.get('manager'),
        otherPartyManager=data.get('otherPartyManager'),
        applyDate=datetime.strptime(
            data.get('applyDate'), "%Y-%m-%d") if data.get('applyDate') else None,
        deadLine=datetime.strptime(
            data.get('deadLine'), "%Y-%m-%d") if data.get('deadLine') else None,
        paymentDate=datetime.strptime(
            data.get('paymentDate'), "%Y-%m-%d") if data.get('paymentDate') else None,
        isPaid=data.get('isPaid'),
        title=data.get('title'),
        memo=data.get('memo'),
        remarks=data.get('remarks'),
        tax=data.get('tax'),
        isTaxExp=data.get('isTaxExp'),
        numberOfAttachments=data.get('numberOfAttachments'),
        invoice_items=newInvoiceItems,
    )
    db.session.add(newInvoice)
    db.session.commit()
    id = newInvoice.id
    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/invoice/<id>', methods=['PUT'])
@app.route('/invoice/<id>', methods=['PUT'])
def invoice_update(id):
    data = request.json

    invoice = Invoice.query.filter(Invoice.id == id).one()
    if not invoice:
        return jsonify({"result": "No Data", "id": id, "data": data})

    invoice.customerId = data.get('customerId')
    invoice.customerName = data.get('customerName')
    invoice.customerAnyNumber = data.get('customerAnyNumber')
    invoice.honorificTitle = data.get('honorificTitle')
    invoice.department = data.get('department')
    invoice.manager = data.get('manager')
    invoice.otherPartyManager = data.get('otherPartyManager')
    invoice.applyNumber = data.get('applyNumber')
    invoice.applyDate = datetime.strptime(
        data.get('applyDate'), "%Y-%m-%d") if data.get('applyDate') else None
    invoice.deadLine = datetime.strptime(
        data.get('deadLine'), "%Y-%m-%d") if data.get('deadLine') else None
    invoice.paymentDate = datetime.strptime(
        data.get('paymentDate'), "%Y-%m-%d") if data.get('paymentDate') else None
    invoice.isPaid = data.get('isPaid')
    invoice.title = data.get('title')
    invoice.memo = data.get('memo')
    invoice.remarks = data.get('remarks')
    invoice.tax = data.get('tax')
    invoice.isTaxExp = data.get('isTaxExp')
    invoice.numberOfAttachments = data.get('numberOfAttachments')

    if data.get('invoice_items'):
        update_list = []
        insert_list = []
        delete_in_list = []
        for item in data['invoice_items']:
            if 'createdAt' in item:
                del(item['createdAt'])
            if 'updatedAt' in item:
                del(item['updatedAt'])

            if item.get('id'):
                if item.get('isDelete'):
                    delete_in_list.append(item['id'])
                else:
                    update_list.append(item)
            else:
                if item.get('isDelete'):
                    pass
                else:
                    insert_list.append(item)

        db.session.bulk_update_mappings(Invoice_Item, update_list)
        db.session.bulk_insert_mappings(Invoice_Item, insert_list)
        db.session.query(Invoice_Item).filter(Invoice_Item.id.in_(
            delete_in_list)).delete(synchronize_session='fetch')

    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/invoice_delete/<id>', methods=['PUT'])
@app.route('/invoice_delete/<id>', methods=['PUT'])
def invoice_destroy(id):
    invoice = Invoice.query.filter(Invoice.id == id).one()
    invoice.isDelete = True
    newHistory = History(
        userName=current_user.id,
        modelName='Invoice',
        modelId=id,
        action='put(dust)'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ""})


# 請求書＿商品(Invoice_Items)
@app.route('/invoice_items', methods=['GET'])
def invoice_item_index():
    invoiceItems = Invoice_Item.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Invoice_ItemSchema(many=True).dump(invoiceItems))


@app.route('/invoice_item/<id>', methods=['GET'])
def invoice_item_show(id):
    invoiceItemCount = Invoice_Item.query.filter(Invoice_Item.id == id).count()
    if invoiceItemCount:
        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='InvoiceItems',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(Invoice_ItemSchema().dump(invoiceItem))
    else:
        return jsonify([])


@app.route('/invoice_items/<hid>', methods=['GET'])
def invoice_item_show_by_invoiceId(hid):
    invoiceItems = Invoice_Item.query.filter(
        Invoice_Item.invoiceId == hid).all()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=hid,
        action='gets')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Invoice_ItemSchema(many=True).dump(invoiceItems))


@app.route('/invoice_item', methods=['POST'])
def invoice_item_create():
    data = request.json
    newInvoiceItem = Invoice_Item(
        invoiceId=data.get('invoiceId'),
        itemId=data.get('itemId'),
        itemName=data.get('itemName'),
        price=data.get('price'),
        cost=data.get('cost'),
        count=data.get('count'),
        unit=data.get('unit'),
        remarks=data.get('remarks'),
    )
    db.session.add(newInvoiceItem)
    db.session.commit()
    id = newInvoiceItem.id
    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=id,
        action='post')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/invoice_item/<id>', methods=['PUT'])
def invoice_item_update(id):
    data = request.json
    invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == id).one()
    invoiceItem.invoiceId = data.get('invoiceId')
    invoiceItem.itemId = data.get('itemId')
    invoiceItem.itemName = data.get('itemName')
    invoiceItem.price = data.get('price')
    invoiceItem.cost = data.get('cost')
    invoiceItem.count = data.get('count')
    invoiceItem.unit = data.get('unit')
    invoiceItem.remarks = data.get('remarks')

    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/invoice_item/<id>', methods=['DELETE'])
def invoice_item_destroy(id):
    invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoiceItems',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# 請求書＿入金(Invoice_Payments)
@app.route('/invoice_payments', methods=['GET'])
def invoice_payment_index():
    invoicePayments = Invoice_Payment.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Invoice_PaymentSchema(many=True).dump(invoicePayments))


@app.route('/invoice_payment/<id>', methods=['GET'])
def invoice_payment_show(id):
    invoicePaymentCount = Invoice_Payment.query.filter(
        Invoice_Payment.id == id).count()
    if invoicePaymentCount:
        invoicePayment = Invoice_Payment.query.filter(
            Invoice_Payment.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='InvoicePayments',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(Invoice_PaymentSchema().dump(invoicePayment))
    else:
        return jsonify([])


@app.route('/invoice_payments/<hid>', methods=['GET'])
def invoice_payment_show_by_invoiceId(hid):
    invoicePayments = Invoice_Payment.query.filter(
        Invoice_Payment.invoiceId == hid).all()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=hid,
        action='gets')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Invoice_PaymentSchema(many=True).dump(invoicePayments))


@app.route('/invoice_payment', methods=['POST'])
def invoice_payment_create():
    data = request.json
    newInvoiceItem = Invoice_Payment(
        invoiceId=data.get('invoiceId'),
        paymentDate=data.get('paymentDate'),
        paymentMethod=data.get('paymentMethod'),
        paymentAmount=data.get('paymentAmount'),
        remarks=data.get('remarks'),
    )
    db.session.add(newInvoiceItem)
    db.session.commit()
    id = newInvoiceItem.id
    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=id,
        action='post')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/invoice_payment/<id>', methods=['PUT'])
def invoice_payment_update(id):
    data = request.json
    req = request.args
    priceIncludingTax = int(req.get('priceIncludingTax'))
    paymentSum = int(req.get('paymentSum'))
    invoice = Invoice.query.filter(Invoice.id == id).one()
    invoicePaymentIds = db.session.query(Invoice_Payment.id).filter(
        Invoice_Payment.invoiceId == id).all()
    if not invoice:
        return jsonify({"result": "No Data", "id": id, "data": data})

    if data.get('invoice_payments'):
        update_list = []
        insert_list = []
        delete_in_list = []
        for i in invoicePaymentIds:
            delete_in_list.append(i.id)
        for item in data['invoice_payments']:
            if 'createdAt' in item:
                del(item['createdAt'])
            if 'updatedAt' in item:
                del(item['updatedAt'])
            if item.get('paymentDate'):
                item['paymentDate'] = datetime.strptime(
                    item.get('paymentDate'), "%Y-%m-%d")
            if not item.get('paymentAmount'):
                item['paymentAmount'] = None

            if item.get('id'):
                update_list.append(item)
                index = next((i for i, x in enumerate(
                    delete_in_list) if x == item['id']), None)
                if index != None:
                    delete_in_list.pop(index)
            else:
                insert_list.append(item)

        db.session.bulk_update_mappings(Invoice_Payment, update_list)
        db.session.bulk_insert_mappings(Invoice_Payment, insert_list)
        db.session.query(Invoice_Payment).filter(Invoice_Payment.id.in_(
            delete_in_list)).delete(synchronize_session='fetch')

    else:
        db.session.query(Invoice_Payment).filter(
            Invoice_Payment.invoiceId == id).delete()

    # 入金合計額が上回れば入金済みに（変動）
    if paymentSum >= priceIncludingTax:
        invoice.isPaid = True
    else:
        invoice.isPaid = False

    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/invoice_payment/<id>', methods=['DELETE'])
def invoice_payment_destroy(id):
    invoicePayment = Invoice_Payment.query.filter(
        Invoice_Payment.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='InvoicePayments',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# 見積書(Quotations)
@app.route('/v1/quotations', methods=['GET'])
@app.route('/quotations', methods=['GET'])
def quotation_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    limit = int(req.get('limit')) if req.get('limit') else _LIMIT_NUM
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            quotations = Quotation.query.filter(and_(Invoice.isDelete == False, or_(
                extract('year', Quotation.applyDate) == searchWord, Quotation.customerName.like('%'+searchWord+'%'))))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            quotations = Quotation.query.filter(and_(Invoice.isDelete == False, or_(
                Quotation.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Quotation.applyDate) == year, extract('month', Quotation.applyDate) == month))))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            quotations = Quotation.query.filter(and_(Invoice.isDelete == False, or_(
                Quotation.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Quotation.applyDate) == year, extract('month', Quotation.applyDate) == month, extract('day', Quotation.applyDate) == day))))
        else:
            quotations = Quotation.query.filter(
                and_(Quotation.isDelete == False, Quotation.customerName.like('%'+searchWord+'%')))
    else:
        quotations = Quotation.query.filter(Quotation.isDelete == False)
    if offset:
        quotations = quotations.offset(offset)
    if limit:
        quotations = quotations.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Quotation',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(QuotationSchema(many=True).dump(quotations))


@app.route('/v1/dust-quotations', methods=['GET'])
@app.route('/dust-quotations', methods=['GET'])
def dust_quotation_index_v1():
    # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    limit = int(req.get('limit')) if req.get('limit') else _LIMIT_NUM
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            quotations = Quotation.query.filter(and_(Quotation.isDelete == True, or_(
                extract('year', Quotation.applyDate) == searchWord, Quotation.customerName.like('%'+searchWord+'%'))))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            quotations = Quotation.query.filter(and_(Quotation.isDelete == True, or_(
                Quotation.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Quotation.applyDate) == year, extract('month', Quotation.applyDate) == month))))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            quotations = Quotation.query.filter(and_(Quotation.isDelete == True, or_(
                Quotation.customerName.like('%'+searchWord+'%'), and_(
                    extract('year', Quotation.applyDate) == year, extract('month', Quotation.applyDate) == month, extract('day', Quotation.applyDate) == day))))
        else:
            quotations = Quotation.query.filter(
                and_(Quotation.isDelete == True, Quotation.customerName.like('%'+searchWord+'%')))
    else:
        quotations = Quotation.query.filter(Quotation.isDelete == True)
    if offset:
        quotations = quotations.offset(offset)
    if limit:
        quotations = quotations.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Quotation(dust)',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(QuotationSchema(many=True).dump(quotations))


@app.route('/v1/quotation/<id>', methods=['GET'])
@app.route('/quotation/<id>', methods=['GET'])
def quotation_show(id):
    quotationCount = Quotation.query.filter(Quotation.id == id).count()
    if quotationCount:
        quotation = Quotation.query.filter(Quotation.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Quotation',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(QuotationSchema().dump(quotation))
    else:
        return jsonify([])


@app.route('/v1/quotation', methods=['POST'])
@app.route('/quotation', methods=['POST'])
def quotation_create():
    data = request.json
    newQuotationItems = []
    if data.get('quotation_items'):
        for item in data.get('quotation_items'):
            if item.get('isDelete'):
                if item['isDelete']:
                    continue

            newQuotationItems.append(
                Quotation_Item(
                    quotationId=item.get('quotationId'),
                    itemId=item.get('itemId'),
                    any=item.get('any'),
                    itemName=item.get('itemName'),
                    price=item.get('price'),
                    count=item.get('count'),
                    unit=item.get('unit'),
                    remarks=item.get('remarks'),
                )
            )

    newQuotation = Quotation(
        customerId=data.get('customerId'),
        customerName=data.get('customerName'),
        customerAnyNumber=data.get('customerAnyNumber'),
        honorificTitle=data.get('honorificTitle'),
        department=data.get('department'),
        manager=data.get('manager'),
        otherPartyManager=data.get('otherPartyManager'),
        applyDate=datetime.strptime(
            data.get('applyDate'), "%Y-%m-%d") if data.get('applyDate') else None,
        expiry=data.get('expiry'),
        dayOfDelivery=data.get('dayOfDelivery'),
        termOfSale=data.get('termOfSale'),
        isConvert=data.get('isConvert') if data.get('isConvert') else False,
        title=data.get('title'),
        memo=data.get('memo'),
        remarks=data.get('remarks'),
        tax=data.get('tax'),
        isTaxExp=data.get('isTaxExp'),
        numberOfAttachments=data.get('numberOfAttachments'),
        quotation_items=newQuotationItems,
    )
    db.session.add(newQuotation)
    db.session.commit()
    id = newQuotation.id
    newHistory = History(
        userName=current_user.id,
        modelName='Quotation',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/quotation/<id>', methods=['PUT'])
@app.route('/quotation/<id>', methods=['PUT'])
def quotation_update(id):
    data = request.json

    quotation = Quotation.query.filter(Quotation.id == id).one()
    if not quotation:
        return jsonify({"result": "No Data", "id": id, "data": data})

    quotation.customerId = data.get('customerId')
    quotation.customerName = data.get('customerName')
    quotation.customerAnyNumber = data.get('customerAnyNumber')
    quotation.honorificTitle = data.get('honorificTitle')
    quotation.department = data.get('department')
    quotation.manager = data.get('manager')
    quotation.otherPartyManager = data.get('otherPartyManager')
    quotation.applyNumber = data.get('applyNumber')
    quotation.applyDate = datetime.strptime(
        data.get('applyDate'), "%Y-%m-%d") if data.get('applyDate') else None
    quotation.expiry = data.get('expiry')
    quotation.dayOfDelivery = data.get('dayOfDelivery')
    quotation.termOfSale = data.get('termOfSale')
    quotation.isConvert = data.get(
        'isConvert') if data.get('isConvert') else False
    quotation.title = data.get('title')
    quotation.memo = data.get('memo')
    quotation.remarks = data.get('remarks')
    quotation.tax = data.get('tax')
    quotation.isTaxExp = data.get('isTaxExp')
    quotation.numberOfAttachments = data.get('numberOfAttachments')

    if data.get('quotation_items'):
        update_list = []
        insert_list = []
        delete_in_list = []
        for item in data['quotation_items']:
            if 'createdAt' in item:
                del(item['createdAt'])
            if 'updatedAt' in item:
                del(item['updatedAt'])

            if item.get('id'):
                if item.get('isDelete'):
                    delete_in_list.append(item['id'])
                else:
                    update_list.append(item)
            else:
                if item.get('isDelete'):
                    pass
                else:
                    insert_list.append(item)

        db.session.bulk_update_mappings(Quotation_Item, update_list)
        db.session.bulk_insert_mappings(Quotation_Item, insert_list)
        db.session.query(Quotation_Item).filter(Quotation_Item.id.in_(
            delete_in_list)).delete(synchronize_session='fetch')

    newHistory = History(
        userName=current_user.id,
        modelName='Quotation',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/quotation_delete/<id>', methods=['PUT'])
@app.route('/quotation_delete/<id>', methods=['PUT'])
def quotation_destroy(id):
    quotation = Quotation.query.filter(Quotation.id == id).one()
    quotation.isDelete = True
    newHistory = History(
        userName=current_user.id,
        modelName='Quotation',
        modelId=id,
        action='put(dust)'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ""})


# 見積書＿商品(Quotation_Items)
@app.route('/quotation_items', methods=['GET'])
def quotation_item_index():
    quotationItems = Quotation_Item.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Quotation_ItemSchema(many=True).dump(quotationItems))


@app.route('/quotation_item/<id>', methods=['GET'])
def quotation_item_show(id):
    quotationItemCount = Quotation_Item.query.filter(
        Quotation_Item.id == id).count()
    if quotationItemCount:
        quotationItem = Quotation_Item.query.filter(
            Quotation_Item.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='QuotationItems',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(Quotation_ItemSchema().dump(quotationItem))
    else:
        return jsonify([])


@app.route('/quotation_items/<hid>', methods=['GET'])
def quotation_item_show_by_quotationId(hid):
    quotationItems = Quotation_Item.query.filter(
        Quotation_Item.quotationId == hid).all()
    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=hid,
        action='gets')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(Quotation_ItemSchema(many=True).dump(quotationItems))


@app.route('/quotation_item', methods=['POST'])
def quotation_item_create():
    data = request.json
    newQuotationItem = Quotation_Item(
        quotationId=data.get('quotationId'),
        itemId=data.get('itemId'),
        itemName=data.get('itemName'),
        price=data.get('price'),
        cost=data.get('cost'),
        count=data.get('count'),
        unit=data.get('unit'),
        remarks=data.get('remarks'),
    )
    db.session.add(newQuotationItem)
    db.session.commit()
    id = newQuotationItem.id

    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=id,
        action='post')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/quotation_item/<id>', methods=['PUT'])
def quotation_item_update(id):
    data = request.json
    quotationItem = Quotation_Item.query.filter(Quotation_Item.id == id).one()
    quotationItem.quotationId = data.get('quotationId')
    quotationItem.itemId = data.get('itemId')
    quotationItem.itemName = data.get('itemName')
    quotationItem.price = data.get('price')
    quotationItem.cost = data.get('cost')
    quotationItem.count = data.get('count')
    quotationItem.unit = data.get('unit')
    quotationItem.remarks = data.get('remarks')

    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/quotation_item/<id>', methods=['DELETE'])
def quotation_item_destroy(id):
    quotationItem = Quotation_Item.query.filter(
        Quotation_Item.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='QuotationItems',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# メモ(Memos)
@app.route('/v1/memos', methods=['GET'])
@app.route('/memos', methods=['GET'])
def memo_index_v1():
   # パラメータを準備
    req = request.args
    searchWord = req.get('search')
    limit = int(req.get('limit')) if req.get('limit') else _LIMIT_NUM
    offset = int(req.get('offset')) if req.get('offset') else 0
    # 各種フィルタリング処理
    if searchWord:
        if len(searchWord) == 4:
            memos = Memo.query.filter(or_(
                extract('year', Memo.createdAt) == searchWord, Memo.manager.like('%'+searchWord+'%')))
        elif len(searchWord) == 6:
            year = searchWord[:4]
            month = searchWord[4:]
            memos = Memo.query.filter(or_(Memo.manager.like('%'+searchWord+'%'), and_(
                extract('year', Memo.createdAt) == year, extract('month', Memo.createdAt) == month)))
        elif len(searchWord) == 8:
            year = searchWord[:4]
            month = searchWord[4:6]
            day = searchWord[6:]
            memos = Memo.query.filter(or_(Memo.manager.like('%'+searchWord+'%'), and_(
                extract('year', Memo.createdAt) == year, extract('month', Memo.createdAt) == month, extract('day', Memo.createdAt) == day)))
        else:
            memos = Memo.query.filter(
                Memo.manager.like('%'+searchWord+'%'))
    else:
        memos = Memo.query
    if offset:
        memos = memos.offset(offset)
    if limit:
        memos = memos.limit(limit)

    newHistory = History(
        userName=current_user.id,
        modelName='Memo',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(MemoSchema(many=True).dump(memos))


@app.route('/v1/memo/<id>', methods=['GET'])
@app.route('/memo/<id>', methods=['GET'])
def memo_show(id):
    memoCount = Memo.query.filter(Memo.id == id).count()
    if memoCount:
        memo = Memo.query.filter(Memo.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Memo',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(MemoSchema().dump(memo))
    else:
        return jsonify([])


@app.route('/v1/memo', methods=['POST'])
@app.route('/memo', methods=['POST'])
def memo_create():
    data = request.json
    newMemo = Memo(
        title=data.get('title'),
        manager=data.get('manager'),
        isFavorite=data.get('isFavorite'),
        content=data.get('content'),
    )
    db.session.add(newMemo)
    db.session.commit()
    id = newMemo.id
    newHistory = History(
        userName=current_user.id,
        modelName='Memo',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/memo/<id>', methods=['PUT'])
@app.route('/memo/<id>', methods=['PUT'])
def memo_update(id):
    data = request.json
    memo = Memo.query.filter(Memo.id == id).one()

    memo.title = data.get('title')
    memo.manager = data.get('manager')
    memo.isFavorite = data.get('isFavorite') if data.get(
        'isFavorite') else False  # ページリロード後、更新時のエラー防止
    memo.content = data.get('content')

    newHistory = History(
        userName=current_user.id,
        modelName='Memo',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/v1/memo/<id>', methods=['DELETE'])
@app.route('/memo/<id>', methods=['DELETE'])
def memo_destroy(id):
    memo = Memo.query.filter(Memo.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Memo',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# 単位(Units)
@app.route('/units', methods=['GET'])
def unit_index():
    units = Unit.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='Unit',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(UnitSchema(many=True).dump(units))


@app.route('/unit/<id>', methods=['GET'])
def unit_show(id):
    unitCount = Unit.query.filter(Unit.id == id).count()
    if unitCount:
        unit = Unit.query.filter(Unit.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Unit',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(UnitSchema().dump(unit))
    else:
        return jsonify([])


@app.route('/unit', methods=['POST'])
def unit_create():
    data = request.json
    newUnit = Unit(
        unitName=data.get('unitName'),
    )
    db.session.add(newUnit)
    db.session.commit()
    id = newUnit.id
    newHistory = History(
        userName=current_user.id,
        modelName='Unit',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/unit/<id>', methods=['PUT'])
def unit_update(id):
    data = request.json
    unit = Unit.query.filter(Unit.id == id).one()

    unit.unitName = data.get('unitName')
    newHistory = History(
        userName=current_user.id,
        modelName='Unit',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/unit/<id>', methods=['DELETE'])
def unit_destroy(id):
    unit = Unit.query.filter(Unit.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Unit',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# カテゴリー(categories)
@app.route('/categories', methods=['GET'])
def category_index():
    categories = Category.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='Category',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(CategorySchema(many=True).dump(categories))


@app.route('/category/<id>', methods=['GET'])
def category_show(id):
    categoryCount = Category.query.filter(Category.id == id).count()
    if categoryCount:
        category = Category.query.filter(Category.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Category',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(CategorySchema().dump(category))
    else:
        return jsonify([])


@app.route('/category', methods=['POST'])
def category_create():
    data = request.json
    newCategory = Category(
        categoryName=data.get('categoryName'),
    )
    db.session.add(newCategory)
    db.session.commit()
    id = newCategory.id

    newHistory = History(
        userName=current_user.id,
        modelName='Category',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/category/<id>', methods=['PUT'])
def category_update(id):
    data = request.json
    category = Category.query.filter(Category.id == id).one()

    category.categoryName = data.get('categoryName')

    newHistory = History(
        userName=current_user.id,
        modelName='Category',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/category/<id>', methods=['DELETE'])
def category_destroy(id):
    category = Category.query.filter(Category.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Category',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


# メーカー(Makers)
@app.route('/makers', methods=['GET'])
def maker_index():
    makers = Maker.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='Maker',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(MakerSchema(many=True).dump(makers))


@app.route('/maker/<id>', methods=['GET'])
def maker_show(id):
    makerCount = Maker.query.filter(Maker.id == id).count()
    if makerCount:
        maker = Maker.query.filter(Maker.id == id).first()
        newHistory = History(
            userName=current_user.id,
            modelName='Maker',
            modelId=id,
            action='get')
        db.session.add(newHistory)
        db.session.commit()
        return jsonify(MakerSchema().dump(maker))
    else:
        return jsonify([])


@app.route('/maker', methods=['POST'])
def maker_create():
    data = request.json
    newMaker = Maker(
        makerName=data.get('makerName'),
    )
    db.session.add(newMaker)
    db.session.commit()
    id = newMaker.id

    newHistory = History(
        userName=current_user.id,
        modelName='Maker',
        modelId=id,
        action='post'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/maker/<id>', methods=['PUT'])
def maker_update(id):
    data = request.json
    maker = Maker.query.filter(Maker.id == id).one()

    maker.makerName = data.get('makerName')

    newHistory = History(
        userName=current_user.id,
        modelName='Maker',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


@app.route('/maker/<id>', methods=['DELETE'])
def maker_destroy(id):
    maker = Maker.query.filter(Maker.id == id).delete()
    newHistory = History(
        userName=current_user.id,
        modelName='Maker',
        modelId=id,
        action='delete'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": ''})


@app.route('/setting', methods=['GET'])
def setting_show():
    setting = Setting.query.filter(Setting.id == 1).first()
    newHistory = History(
        userName=current_user.id,
        modelName='Setting',
        modelId=1,
        action='get')
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(SettingSchema().dump(setting))


@app.route('/setting/<id>', methods=['PUT'])
def setting_update(id):
    data = request.json
    setting = Setting.query.filter(Setting.id == id).one()

    setting.companyName = data.get('companyName')
    setting.representative = data.get('representative')
    setting.postNumber = data.get('postNumber')
    setting.address = data.get('address')
    setting.telNumber = data.get('telNumber')
    setting.faxNumber = data.get('faxNumber')
    setting.url = data.get('url')
    setting.email = data.get('email')
    setting.payee = data.get('payee')
    setting.accountHolder = data.get('accountHolder')
    setting.accountHolderKana = data.get('accountHolderKana')
    setting.logoFilePath = data.get('logoFilePath')
    setting.logoHeight = data.get('logoHeight')
    setting.logoWidth = data.get('logoWidth')
    setting.stampFilePath = data.get('stampFilePath')
    setting.stampHeight = data.get('stampHeight')
    setting.stampWidth = data.get('stampWidth')
    setting.isDisplayQuotationLogo = data.get('isDisplayQuotationLogo')
    setting.isDisplayInvoiceLogo = data.get('isDisplayInvoiceLogo')
    setting.isDisplayDeliveryLogo = data.get('isDisplayDeliveryLogo')
    setting.isDisplayQuotationStamp = data.get('isDisplayQuotationStamp')
    setting.isDisplayInvoiceStamp = data.get('isDisplayInvoiceStamp')
    setting.isDisplayDeliveryStamp = data.get('isDisplayDeliveryStamp')
    setting.defaultTax = data.get('defaultTax')

    newHistory = History(
        userName=current_user.id,
        modelName='Setting',
        modelId=id,
        action='put'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify({"result": "OK", "id": id, "data": data})


# 操作履歴(Histories)
@app.route('/histories', methods=['GET'])
def history_index():
    histories = History.query.all()
    newHistory = History(
        userName=current_user.id,
        modelName='History',
        modelId=None,
        action='gets'
    )
    db.session.add(newHistory)
    db.session.commit()
    return jsonify(HistorySchema(many=True).dump(histories))


@app.route('/login-histories', methods=['GET'])
def login_history_index():
    loginHistories = History.query.order_by(desc(History.id)).limit(_LIMIT_NUM)
    return jsonify(HistorySchema(many=True).dump(loginHistories))


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010, debug=True)
