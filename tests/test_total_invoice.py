from seeder import seeder
from models import *
from app import db, app
import unittest
import sys
import os
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))


class BasicTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # print('-----setUp-----')
        pass

    # テスト後にシーダーを流しなおす
    @classmethod
    def tearDownClass(cls):
        print("---tearDown---")
        seeder()

    def test_get_total_invoices(self):
        print('---TotalInvoice全件読み込み---')
        totalInvoices = TotalInvoice.query.all()
        totalInvoiceCount = len(totalInvoices)
        self.assertTrue(totalInvoiceCount)
        print('---TotalInvoice→Customer全件取得---')
        totalInvoiceApplyNumberCount = 0
        for totalInvoice in totalInvoices:
            if totalInvoice.totalInvoiceApplyNumber is not None:
                totalInvoiceApplyNumberCount += 1
        self.assertGreaterEqual(totalInvoiceApplyNumberCount, 1)

    def test_get_total_invoice_byTitle(self):
        print('---TotalInvoice全件取得→Dict---')
        totalInvoices = TotalInvoice.query.all()
        sch = TotalInvoiceSchema(many=True).dump(totalInvoices)
        self.assertEqual(sch[0]['title'], '合計請求書１')

    def test_get_total_invoice_byId(self):
        print('---TotalInvoice一件読み込み---')
        totalInvoice = TotalInvoice.query.filter(
            TotalInvoice.id == 1).first()
        self.assertTrue(totalInvoice)
        self.assertEqual(totalInvoice.totalInvoiceApplyNumber, 2200001)

        print('---TotalInvoice一件読み込み失敗---')
        totalInvoices = TotalInvoice.query.filter(
            TotalInvoice.id == 9999).all()
        self.assertFalse(totalInvoices)
        self.assertEqual(len(totalInvoices), 0)

    def test_update_total_invoice(self):
        print('---TotalInvoice一件更新---')
        totalInvoice = TotalInvoice.query.filter(
            TotalInvoice.id == 2).first()
        totalInvoice.title = 'テスト請求書２'
        db.session.commit()
        totalInvoice = TotalInvoice.query.filter(
            TotalInvoice.id == 2).first()
        self.assertEqual(totalInvoice.title, 'テスト請求書２')

    def test_create_total_invoice(self):
        print('---TotalInvoice新規作成---')
        totalInvoices = [
            TotalInvoice(applyNumbers='2200002', issueDate=date(2022, 1, 1),
                         title='テスト請求書４', customerId=2),
            TotalInvoice(applyNumbers='2200001', issueDate=date(2022, 1, 1),
                         title='テスト請求書５', customerId=1),
        ]
        db.session.add_all(totalInvoices)
        db.session.commit()
        self.assertGreaterEqual(len(TotalInvoice.query.all()), 2)

    def test_delete_total_invoice(self):
        print('---TotalInvoice一件削除---')
        totalInvoice = TotalInvoice(applyNumbers='2200003', issueDate=date(
            2022, 1, 1), title='削除請求書', customerId=3)
        db.session.add(totalInvoice)
        db.session.commit()
        newId = totalInvoice.id
        totalInvoice = TotalInvoice.query.filter(
            TotalInvoice.id == newId).delete()
        db.session.commit()

        totalInvoice = TotalInvoice.query.filter(
            TotalInvoice.id == newId).all()
        self.assertEqual(len(totalInvoice), 0)


if __name__ == '__main__':
    unittest.main()
