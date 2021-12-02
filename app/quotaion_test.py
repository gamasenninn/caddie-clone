from app import db, app
from models import *
import unittest
from datetime import datetime
from seeder import seeder


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

    def test_get_quotaions(self):
        print('---Quotaion全件読み込み---')
        quotations = Quotaion.query.all()
        quotationCount = len(quotations)
        self.assertTrue(quotationCount)

        # Customerまで全件取得
        print('Quotation→Customer全件取得')
        customerCount = 0
        for quotation in quotations:
            if(quotation.customer is not None):
                customerCount += 1
        self.assertGreaterEqual(customerCount, 1)

        # Quotation_Itemまで取得
        print('Quotation→Quotation_Item全件取得')
        quotationItemCount = 0
        for quotation in quotations:
            for quotationItem in quotation.quotaion_items:
                quotationItemCount += 1
        self.assertGreaterEqual(quotationItemCount, 1)

    def test_get_quotations_dict(self):
        print('---Quotation全件読込→Dict---')
        quotations = Quotaion.query.all()
        sch = QuotaionSchema(many=True).dump(quotations)
        self.assertEqual(sch[0]['title'], '○○株式会社への見積書')

    def test_get_quotaion_byId(self):
        print('---Quotaion一件読み込み---')
        quotaion = Quotaion.query.filter(Quotaion.id == 1).first()
        self.assertTrue(quotaion)
        self.assertEqual(quotaion.title, '○○株式会社への見積書')

        print('---Quotaion一件読み込み失敗---')
        quotaions = Quotaion.query.filter(Quotaion.id == 9999).all()
        self.assertFalse(quotaions)
        self.assertEqual(len(quotaions), 0)

    def test_update_quotaion(self):
        print('---Quotaion一件更新---')
        quotaion = Quotaion.query.filter(Quotaion.id == 2).first()
        quotaion.title = '××株式会社への見積書'
        db.session.commit()
        quotaion = Quotaion.query.filter(Quotaion.id == 2).first()
        self.assertEqual(quotaion.title, "××株式会社への見積書")

    def test_create_quotaion(self):
        print('---Quotaion新規作成---')
        quotaions = [
            Quotaion(customerId=1, applyNumber=1000004, applyDate=datetime.now(), expiry=datetime.now(),
                     title='○○建設への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', isTaxExp=True),
            Quotaion(customerId=1, applyNumber=1000005, applyDate=datetime.now(), expiry=datetime.now(),
                     title='○○商店への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', isTaxExp=True),
        ]
        db.session.add_all(quotaions)
        db.session.commit()
        self.assertGreaterEqual(len(Quotaion.query.all()), 2)

    def test_delete_quotaion(self):
        print('---Quotaion一件削除---')
        quotaion = Quotaion(customerId=1, applyNumber=1000006, applyDate=datetime.now(), expiry=datetime.now(),
                            title='○○株式会社への見積書', memo='これは見積書のメモです', remarks='これは見積書の備考です', isTaxExp=True)
        db.session.add(quotaion)
        db.session.commit()
        newId = quotaion.id
        quotaion = Quotaion.query.filter(Quotaion.id == newId).delete()
        db.session.commit()

        quotaion = Quotaion.query.filter(Quotaion.id == newId).all()
        self.assertEqual(len(quotaion), 0)


if __name__ == '__main__':
    unittest.main()
