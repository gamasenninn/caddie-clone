from app import db, app, ma
from datetime import datetime


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)


class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String)
    honorificTitle = db.Column(db.String)
    postNumber = db.Column(db.String(20))
    address = db.Column(db.String)
    telNumber = db.Column(db.String(30))
    faxNumber = db.Column(db.String(30))
    url = db.Column(db.String)
    email = db.Column(db.String)
    manager = db.Column(db.String)
    representative = db.Column(db.String)
    memo = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)
    invoices = db.relationship('Invoice', backref='customer')
    quotaions = db.relationship('Quotaion', backref='customer')

    def to_dict(self):
        return {
            'id': self.id,
            'customerName': self.customerName,
            'honorificTitle': self.honorificTitle,
            'postNumber': self.postNumber,
            'address': self.address,
            'telNumber': self.telNumber,
            'faxNumber': self.faxNumber,
            'url': self.url,
            'email': self.email,
            'manager': self.manager,
            'representative': self.representative,
            'memo': self.memo,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
        }


class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String)
    unit = db.Column(db.String)
    price = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    costRate = db.Column(db.Float)
    memo = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'itemName': self.itemName,
            'unit': self.unit,
            'price': self.price,
            'cost': self.cost,
            'costRate': self.costRate,
            'memo': self.memo,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
        }
    # invoice_items=db.relationship('Invoice_Item',backref='items')
    # quotaion_items=db.relationship('Quotaion_Item',backref='items')


class Invoice(db.Model):

    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'))
    applyNumber = db.Column(db.Integer)
    applyDate = db.Column(db.DateTime)
    expiry = db.Column(db.DateTime)
    title = db.Column(db.String)
    memo = db.Column(db.String)
    remarks = db.Column(db.String)
    isTaxExp = db.Column(db.Boolean, nullable=False, default=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)
    invoice_items = db.relationship('Invoice_Item', backref='invoice')


class Invoice_Item(db.Model):

    __tablename__ = 'invoice_items'

    id = db.Column(db.Integer, primary_key=True)
    invoiceId = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    count = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Quotaion(db.Model):

    __tablename__ = 'quotaions'

    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'))
    applyNumber = db.Column(db.Integer)
    applyDate = db.Column(db.DateTime)
    expiry = db.Column(db.DateTime)
    title = db.Column(db.String)
    memo = db.Column(db.String)
    remarks = db.Column(db.String)
    isTaxExp = db.Column(db.Boolean, nullable=False, default=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)
    quotaion_items = db.relationship('Quotaion_Item', backref='quotaion')


class Quotaion_Item(db.Model):

    __tablename__ = 'quotaion_items'

    id = db.Column(db.Integer, primary_key=True)
    quotaionId = db.Column(db.Integer, db.ForeignKey('quotaions.id'))
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    count = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Memo(db.Model):

    __tablename__ = 'memos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Unit(db.Model):

    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    unitName = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Setting(db.Model):

    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String)
    representative = db.Column(db.String)
    postNumber = db.Column(db.String(20))
    address = db.Column(db.String)
    telNumber = db.Column(db.String(30))
    faxNumber = db.Column(db.String(30))
    url = db.Column(db.String)
    email = db.Column(db.String)
    logoFilePath = db.Column(db.String)
    stampFilePath = db.Column(db.String)
    isDisplayQuotationLogo = db.Column(
        db.Boolean, nullable=False, default=True)
    isDisplayInvoiceLogo = db.Column(db.Boolean, nullable=False, default=True)
    isDisplayDeliveryLogo = db.Column(db.Boolean, nullable=False, default=True)
    isDisplayQuotationStamp = db.Column(
        db.Boolean, nullable=False, default=True)
    isDisplayInvoiceStamp = db.Column(db.Boolean, nullable=False, default=True)
    isDisplayDeliveryStamp = db.Column(
        db.Boolean, nullable=False, default=True)
    updatedAt = updatedAt = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


# -----Json変換-----

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item

class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice

class Invoice_ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice_Item

class QuotaionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quotaion

class Quotaion_ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quotaion_Item

class MemoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Memo

class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit

class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Setting