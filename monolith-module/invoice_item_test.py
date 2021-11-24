from app import db, app
from models import Invoice_Item
import unittest
import subprocess


class BasicTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # print('-----setUp-----')
        pass

    # テスト後にシーダーを流しなおす
    @classmethod
    def tearDownClass(cls):
        print("---tearDown---")
        subprocess.call('python seeder.py', shell=True)

    def test_get_invoice_items(self):
        print('---Invoice_Item全件読み込み---')
        invoiceItems = Invoice_Item.query.all()
        invoiceItemCount = len(invoiceItems)
        self.assertTrue(invoiceItemCount)

    def test_get_invoice_item_byId(self):
        print('---Invoice_Item一件読み込み---')
        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == 1).first()
        self.assertTrue(invoiceItem)
        self.assertEqual(invoiceItem.count, 5)

        print('---Invoice_Item一件読み込み失敗---')
        invoiceItems = Invoice_Item.query.filter(Invoice_Item.id == 9999).all()
        self.assertFalse(invoiceItems)
        self.assertEqual(len(invoiceItems), 0)

    def test_update_invoice_item(self):
        print('---Invoice_Item一件更新---')
        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == 2).first()
        invoiceItem.count = 20
        db.session.commit()
        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == 2).first()
        self.assertEqual(invoiceItem.count, 20)

    def test_create_invoice_item(self):
        print('---Invoice_Item新規作成---')
        invoiceItems = [
            Invoice_Item(invoiceId=3, itemId=2, count=20),
            Invoice_Item(invoiceId=3, itemId=3, count=10),
        ]
        db.session.add_all(invoiceItems)
        db.session.commit()
        self.assertGreaterEqual(len(Invoice_Item.query.all()), 2)

    def test_delete_invoice_item(self):
        print('---Invoice_Item一件削除---')
        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == 3).delete()
        db.session.commit()

        invoiceItem = Invoice_Item.query.filter(Invoice_Item.id == 3).all()
        self.assertGreaterEqual(len(invoiceItem), 0)


if __name__ == '__main__':
    unittest.main()
