from app import db, app
from models import Invoice
import unittest
import subprocess
from datetime import datetime


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

    def test_get_invoices(self):
        print('---Invoice全件読み込み---')
        invoices = Invoice.query.all()
        invoiceCount = len(invoices)
        self.assertTrue(invoiceCount)

    def test_get_invoice_byId(self):
        print('---Invoice一件読み込み---')
        invoice = Invoice.query.filter(Invoice.id == 1).first()
        self.assertTrue(invoice)
        self.assertEqual(invoice.title, '○○株式会社への請求書')

        print('---Invoice一件読み込み失敗---')
        invoices = Invoice.query.filter(Invoice.id == 9999).all()
        self.assertFalse(invoices)
        self.assertEqual(len(invoices), 0)

    def test_update_invoice(self):
        print('---Invoice一件更新---')
        invoice = Invoice.query.filter(Invoice.id == 2).first()
        invoice.title = '××株式会社への請求書'
        db.session.commit()
        invoice = Invoice.query.filter(Invoice.id == 2).first()
        self.assertEqual(invoice.title, "××株式会社への請求書")

    def test_create_invoice(self):
        print('---Invoice新規作成---')
        invoices = [
            Invoice(customerId=1, applyNumber=1000004, applyDate=datetime.now(), expiry=datetime.now(),
                    title='○○建設への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', isTaxExp=True),
            Invoice(customerId=1, applyNumber=1000005, applyDate=datetime.now(), expiry=datetime.now(),
                    title='○○商店への請求書', memo='これは請求書のメモです', remarks='これは請求書の備考です', isTaxExp=True),
        ]
        db.session.add_all(invoices)
        db.session.commit()
        self.assertGreaterEqual(len(Invoice.query.all()), 2)

    def test_delete_invoice(self):
        print('---Invoice一件削除---')
        invoice = Invoice.query.filter(Invoice.id == 3).delete()
        db.session.commit()

        invoice = Invoice.query.filter(Invoice.id == 3).all()
        self.assertGreaterEqual(len(invoice), 0)


if __name__ == '__main__':
    unittest.main()
