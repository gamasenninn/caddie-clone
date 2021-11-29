from app import db, app
from models import Quotaion_Item
import unittest
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

    def test_get_quotaion_items(self):
        print('---Quotaion_Item全件読み込み---')
        quotaionItems = Quotaion_Item.query.all()
        quotaionItemCount = len(quotaionItems)
        self.assertTrue(quotaionItemCount)
        print('---Quotaion_Item→Customer全件取得---')
        customerCount = 0
        for quotaionItem in quotaionItems:
            if quotaionItem.quotaion.customer is not None:
                customerCount += 1
        self.assertGreaterEqual(customerCount, 1)

    def test_get_quotaion_item_byId(self):
        print('---Quotaion_Item一件読み込み---')
        quotaionItem = Quotaion_Item.query.filter(
            Quotaion_Item.id == 1).first()
        self.assertTrue(quotaionItem)
        self.assertEqual(quotaionItem.count, 5)

        print('---Quotaion_Item一件読み込み失敗---')
        quotaionItems = Quotaion_Item.query.filter(
            Quotaion_Item.id == 9999).all()
        self.assertFalse(quotaionItems)
        self.assertEqual(len(quotaionItems), 0)

    def test_update_quotaion_item(self):
        print('---Quotaion_Item一件更新---')
        quotaionItem = Quotaion_Item.query.filter(
            Quotaion_Item.id == 2).first()
        quotaionItem.count = 20
        db.session.commit()
        quotaionItem = Quotaion_Item.query.filter(
            Quotaion_Item.id == 2).first()
        self.assertEqual(quotaionItem.count, 20)

    def test_create_quotaion_item(self):
        print('---Quotaion_Item新規作成---')
        quotaionItems = [
            Quotaion_Item(quotaionId=3, itemId=2, count=20),
            Quotaion_Item(quotaionId=3, itemId=3, count=10),
        ]
        db.session.add_all(quotaionItems)
        db.session.commit()
        self.assertGreaterEqual(len(Quotaion_Item.query.all()), 2)

    def test_delete_quotaion_item(self):
        print('---Quotaion_Item一件削除---')
        quotaionItem = Quotaion_Item(quotaionId=1, itemId=1, count=10)
        db.session.add(quotaionItem)
        db.session.commit()
        newId = quotaionItem.id
        quotaionItem = Quotaion_Item.query.filter(
            Quotaion_Item.id == newId).delete()
        db.session.commit()

        quotaionItem = Quotaion_Item.query.filter(
            Quotaion_Item.id == newId).all()
        self.assertEqual(len(quotaionItem), 0)


if __name__ == '__main__':
    unittest.main()
