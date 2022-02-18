from pyexpat import model
from app import db, app, ma
from datetime import datetime
from datetime import date
from sqlalchemy.sql import func
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import Insert


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(255))
    role = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)


class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String)
    customerKana = db.Column(db.String)
    honorificTitle = db.Column(db.String)
    department = db.Column(db.String)
    postNumber = db.Column(db.String(20))
    address = db.Column(db.String)
    addressSub = db.Column(db.String)
    telNumber = db.Column(db.String(30))
    faxNumber = db.Column(db.String(30))
    url = db.Column(db.String)
    email = db.Column(db.String)
    manager = db.Column(db.String)
    representative = db.Column(db.String)
    customerCategory = db.Column(
        db.String, nullable=False, default='corporation')
    isHide = db.Column(db.Boolean, nullable=False, default=False)
    isFavorite = db.Column(db.Boolean, nullable=False, default=False)
    memo = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)
    invoices = db.relationship('Invoice', backref='customer')
    quotations = db.relationship('Quotation', backref='customer')


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
    itemCode = db.Column(db.String)
    model = db.Column(db.String)
    category = db.Column(db.String)
    maker = db.Column(db.String)
    unit = db.Column(db.String)
    basePrice = db.Column(db.Integer)
    baseCost = db.Column(db.Integer)
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
    # quotation_items=db.relationship('Quotation_Item',backref='items')


# 請求番号自動生成
def edited_invoice_number():

    nowYearFormat = datetime.now().strftime('%y')
    nowYear = datetime.now().year
    yearStart = date(nowYear, 1, 1)
    # 年末を含めてしまうのを防ぐ
    yearEnd = date(nowYear+1, 1, 1)
    maxNumberForYear = db.session.query(
        func.max(Invoice.applyNumber)).filter(Invoice.createdAt >= yearStart, Invoice.createdAt < yearEnd).first()[0]
    if maxNumberForYear:
        maxNumberForYear_s = str(maxNumberForYear)
        maxApplyNumber_s = maxNumberForYear_s[2:]
        maxApplyNumber = int(maxApplyNumber_s)
        nextNumber = format(maxApplyNumber+1, '0>5')
    else:
        nextNumber = '00001'
    return str(nowYearFormat) + str(nextNumber)


class Invoice(db.Model):

    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customerName = db.Column(db.String)
    department = db.Column(db.String)
    manager = db.Column(db.String)
    otherPartyManager = db.Column(db.String)
    applyNumber = db.Column(db.Integer, default=edited_invoice_number)
    applyDate = db.Column(db.Date)
    deadLine = db.Column(db.Date)
    title = db.Column(db.String)
    memo = db.Column(db.String)
    remarks = db.Column(db.String)
    isTaxExp = db.Column(db.Boolean, nullable=False, default=True)
    isDelete = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)
    invoice_items = db.relationship(
        'Invoice_Item', backref='invoice', uselist=True, cascade='all, delete',)


class Invoice_Item(db.Model):

    __tablename__ = 'invoice_items'

    id = db.Column(db.Integer, primary_key=True)
    invoiceId = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    itemName = db.Column(db.String)
    price = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    count = db.Column(db.Integer)
    unit = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


# 見積番号自動生成
def edited_quotation_number():

    nowYearFormat = datetime.now().strftime('%y')
    nowYear = datetime.now().year
    yearStart = date(nowYear, 1, 1)
    # 年末を含めてしまうのを防ぐ
    yearEnd = date(nowYear+1, 1, 1)
    maxNumberForYear = db.session.query(
        func.max(Quotation.applyNumber)).filter(Quotation.createdAt >= yearStart, Quotation.createdAt < yearEnd).first()[0]
    if maxNumberForYear:
        maxNumberForYear_s = str(maxNumberForYear)
        maxApplyNumber_s = maxNumberForYear_s[2:]
        maxApplyNumber = int(maxApplyNumber_s)
        nextNumber = format(maxApplyNumber+1, '0>5')
    else:
        nextNumber = '00001'
    return str(nowYearFormat) + str(nextNumber)


class Quotation(db.Model):

    __tablename__ = 'quotations'

    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customerName = db.Column(db.String)
    department = db.Column(db.String)
    manager = db.Column(db.String)
    otherPartyManager = db.Column(db.String)
    applyNumber = db.Column(db.Integer, default=edited_quotation_number)
    applyDate = db.Column(db.Date)
    expiry = db.Column(db.Date)
    title = db.Column(db.String)
    memo = db.Column(db.String)
    remarks = db.Column(db.String)
    isTaxExp = db.Column(db.Boolean, nullable=False, default=True)
    isDelete = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)
    quotation_items = db.relationship(
        'Quotation_Item', backref='quotation', uselist=True, cascade='all, delete',)


class Quotation_Item(db.Model):

    __tablename__ = 'quotation_items'

    id = db.Column(db.Integer, primary_key=True)
    quotationId = db.Column(db.Integer, db.ForeignKey('quotations.id'))
    itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
    itemName = db.Column(db.String)
    price = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    count = db.Column(db.Integer)
    unit = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Memo(db.Model):

    __tablename__ = 'memos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    manager = db.Column(db.String)
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


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False,
                          default=datetime.now, onupdate=datetime.now)


class Maker(db.Model):

    __tablename__ = 'maker'

    id = db.Column(db.Integer, primary_key=True)
    makerName = db.Column(db.String)
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


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item


class Invoice_ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice_Item
        include_fk = True


class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        include_fk = True
    invoice_items = ma.Nested(Invoice_ItemSchema, many=True)


class Quotation_ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quotation_Item
        include_fk = True


class QuotationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quotation
        include_fk = True
    quotation_items = ma.Nested(Quotation_ItemSchema, many=True)


class MemoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Memo


class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category


class MakerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Maker


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Setting
