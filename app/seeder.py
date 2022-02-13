from datetime import date
from app import db, app
from models import *


def seeder():

    models = [User, Customer, Item, Invoice,
              Invoice_Item, Quotation, Quotation_Item, Memo, Unit, Category, Maker, Setting]

    for model in models:
        db.session.query(model).delete()
        db.session.commit()

    # -----Users-----
    print('----Users----')
    users = [
        User(id=1, name='tanaka_taro', password='password',
             group='operator', role='crescom_support'),
        User(id=2, name='suzuki_jiro', password='password',
             group='guest', role='admin'),
        User(id=3, name='satou_saburo', password='password',
             group='guest', role='user'),
    ]
    db.session.add_all(users)
    db.session.commit()

    users = User.query.all()
    for user in users:
        print(user.name)

    # -------------Customers---------------
    print('----Customers----')
    customers = [
        Customer(id=1, customerName="○○株式会社", honorificTitle='御中', department='部署名', postNumber='000-0000',
                 address='鹿沼市板荷', addressSub='000', telNumber='000-0000-0000', faxNumber='000-0000-0000', url='example.com',
                 email='example@co.jp', manager='田中太郎', representative='田中代表', customerCategory='corporation', isHide=False,
                 memo='これは○○株式会社のメモです',),
        Customer(id=2, customerName="○○有限会社", honorificTitle='御中', department='部署名', postNumber='111-1111',
                 address='鹿沼市板荷', addressSub='111', telNumber='111-1111-1111', faxNumber='111-1111-1111', url='example.com',
                 email='example@co.jp', manager='田中次郎', representative='田中代表', customerCategory='corporation', isHide=False,
                 memo='これは○○有限会社のメモです',),
        Customer(id=3, customerName="○○商事", honorificTitle='御中', department='部署名', postNumber='222-2222',
                 address='鹿沼市板荷', addressSub='222', telNumber='222-2222-2222', faxNumber='222-2222-2222', url='example.com',
                 email='example@co.jp', manager='田中三郎', representative='田中代表', customerCategory='corporation', isHide=False,
                 memo='これは○○商事のメモです',)
    ]
    db.session.add_all(customers)
    db.session.commit()

    customers = Customer.query.all()
    for customer in customers:
        print(customer.customerName)

    # -----Items-----
    print('----Items----')
    items = [
        Item(id=1, itemName='りんご', itemCode='11111', model='APP001', category='食料品', maker='apple青果店', unit='個', basePrice=100,
             baseCost=50, memo='これはりんごのメモです'),
        Item(id=2, itemName='鉛筆', itemCode='22222', model='PEN001', category='事務用品', maker='トンビ鉛筆', unit='本', basePrice=20,
             baseCost=5, memo='これは鉛筆のメモです'),
        Item(id=3, itemName='ラジオ', itemCode='33333', model='RAD001', category='家電', maker='zony', unit='台', basePrice=1000,
             baseCost=300, memo='これはラジオのメモです'),
    ]
    db.session.add_all(items)
    db.session.commit()

    items = Item.query.all()
    for item in items:
        print(item.itemName)

    # -----Invoices-----
    print('----Invoices-----')
    invoices = [
        Invoice(customerId=1, customerName='○○株式会社',  applyDate=date(2022, 1, 1), deadLine=date(2022, 1, 1),
                title='○○株式会社への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', isTaxExp=True),
        Invoice(customerId=2, customerName="○○有限会社",  applyDate=date(2022, 1, 1), deadLine=date(2022, 1, 1),
                title='○○有限会社への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', isTaxExp=True),
        Invoice(customerId=3, customerName="○○商事",  applyDate=date(2022, 1, 1), deadLine=date(2022, 1, 1),
                title='○○商事への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', isTaxExp=True),
    ]
    db.session.add_all(invoices)
    db.session.commit()

    invoices = Invoice.query.all()
    for invoice in invoices:
        print(invoice.title)

    # -----Invoice_Items-----
    print('----Invoice_Items----')
    invoice_items = [
        Invoice_Item(id=1, invoiceId=1, itemId=1,
                     itemName='りんご', price=100, cost=50, count=5, unit="個"),
        Invoice_Item(id=2, invoiceId=1, itemId=2,
                     itemName='鉛筆', price=20, cost=5, count=10, unit="本"),
        Invoice_Item(id=3, invoiceId=2, itemId=2,
                     itemName='鉛筆', price=30, cost=5, count=15, unit="本"),
        Invoice_Item(id=4, invoiceId=2, itemId=3,
                     itemName='ラジオ', price=1100, cost=300, count=2, unit="台"),
        Invoice_Item(id=5, invoiceId=3, itemId=1,
                     itemName='りんご', price=120, cost=50, count=30, unit="個"),
    ]
    db.session.add_all(invoice_items)
    db.session.commit()

    invoice_items = Invoice_Item.query.all()
    for invoice_item in invoice_items:
        print(invoice_item.count)

    # -----Quotations-----
    print('----Quotations----')
    quotations = [
        Quotation(customerId=1, customerName='○○株式会社', applyDate=date(2022, 1, 1), expiry=date(2022, 1, 1),
                  title='○○株式会社への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', isTaxExp=True),
        Quotation(customerId=2, customerName="○○有限会社", applyDate=date(2022, 1, 1), expiry=date(2022, 1, 1),
                  title='○○有限会社への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', isTaxExp=True),
        Quotation(customerId=3, customerName="○○商事", applyDate=date(2022, 1, 1), expiry=date(2022, 1, 1),
                  title='○○商事への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', isTaxExp=True),
    ]
    db.session.add_all(quotations)
    db.session.commit()

    quotations = Quotation.query.all()
    for quotation in quotations:
        print(quotation.title)

    # -----Quotation_Items-----
    print('----Quotation_Items----')
    quotation_items = [
        Quotation_Item(id=1, quotationId=1, itemId=1,
                       itemName='りんご', price=100, cost=50, count=5, unit="個"),
        Quotation_Item(id=2, quotationId=1, itemId=2,
                       itemName='鉛筆', price=20, cost=5, count=10, unit="本"),
        Quotation_Item(id=3, quotationId=2, itemId=2,
                       itemName='鉛筆', price=30, cost=5, count=15, unit="本"),
        Quotation_Item(id=4, quotationId=2, itemId=3,
                       itemName='ラジオ', price=1100, cost=300, count=2, unit="台"),
        Quotation_Item(id=5, quotationId=3, itemId=1,
                       itemName='りんご', price=120, cost=50, count=30, unit="個"),
    ]
    db.session.add_all(quotation_items)
    db.session.commit()

    quotation_items = Quotation_Item.query.all()
    for quotation_item in quotation_items:
        print(quotation_item.count)

    # -----Memos-----
    print('----Memos----')
    memos = [
        Memo(id=1, title='メモのタイトル１', content='メモの内容１'),
        Memo(id=2, title='メモのタイトル２', content='メモの内容２'),
        Memo(id=3, title='メモのタイトル３', content='メモの内容３'),
    ]
    db.session.add_all(memos)
    db.session.commit()

    memos = Memo.query.all()
    for memo in memos:
        print(memo.title)

    # -----Units-----
    print('----Units----')
    units = [
        Unit(id=1, unitName='個'),
        Unit(id=2, unitName='本'),
        Unit(id=3, unitName='台'),
    ]
    db.session.add_all(units)
    db.session.commit()

    units = Unit.query.all()
    for unit in units:
        print(unit.unitName)

    # -----Categories-----
    print('----Categories----')
    categories = [
        Category(id=1, categoryName='食料品'),
        Category(id=2, categoryName='事務用品'),
        Category(id=3, categoryName='家電'),
    ]
    db.session.add_all(categories)
    db.session.commit()

    categories = Category.query.all()
    for category in categories:
        print(category.categoryName)

    # -----Makers-----
    print('----Makers----')
    makers = [
        Maker(id=1, makerName='apple青果店'),
        Maker(id=2, makerName='トンビ鉛筆'),
        Maker(id=3, makerName='zony'),
    ]
    db.session.add_all(makers)
    db.session.commit()

    makers = Maker.query.all()
    for maker in makers:
        print(maker.makerName)

    # -----Setting-----
    print('----Setting----')
    setting = [
        Setting(id=1, companyName='自社株式会社', representative='自社代表者', postNumber='000-0000', address='宇都宮市北若松原', telNumber='000-0000-0000', faxNumber='000-0000-0000', url='mypage.com', email='mymail@co.jp', logoFilePath='sohoweb/images/logo.png',
                stampFilePath='sohoweb/images/stamp.png', isDisplayQuotationLogo=True, isDisplayInvoiceLogo=True, isDisplayDeliveryLogo=True, isDisplayQuotationStamp=True, isDisplayInvoiceStamp=True, isDisplayDeliveryStamp=True)
    ]
    db.session.add_all(setting)
    db.session.commit()

    setting = Setting.query.all()
    print(setting[0].companyName)


if __name__ == '__main__':
    seeder()
