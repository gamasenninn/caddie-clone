from logging import captureWarnings
from app import db, app
from models import *
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

    def test_get_costomers(self):
        print('---Customer全件読み込み---')
        customers = Customer.query.all()
        c_count = len(customers)
        self.assertTrue(c_count)

    def test_get_coustomer_byId(self):
        print('---Customer一件読み込み---')
        customer = Customer.query.filter(Customer.id == 1).first()
        self.assertTrue(customer)
        self.assertEqual(customer.customerName, '○○株式会社')

        print('---Customer一件読み込み失敗---')
        customers = Customer.query.filter(Customer.id == 9999).all()
        self.assertFalse(customers)
        self.assertEqual(len(customers), 0)

    def test_update_customer(self):
        print('---Customer一件更新---')
        customer = Customer.query.filter(Customer.id == 2).first()
        customer.customerName = 'テスト株式会社'
        db.session.commit()
        customer = Customer.query.filter(Customer.id == 2).first()
        self.assertEqual(customer.customerName, "テスト株式会社")

    def test_create_customer(self):
        print('---Customer新規作成---')
        custoemrs = [
            Customer(customerName='テストクリエイト株式会社', honorificTitle='御中', postNumber='000-0000', address='鹿沼市板荷000', telNumber='000-0000-0000',
                     faxNumber='000-0000-0000', url='example.com', email='example@co.jp', manager='田中太郎', representative='田中代表', memo='これは○○株式会社のメモです'),
            Customer(customerName='テストクリエイト株式会社2', honorificTitle='御中', postNumber='000-0000', address='鹿沼市板荷000', telNumber='000-0000-0000',
                     faxNumber='000-0000-0000', url='example.com', email='example@co.jp', manager='田中太郎', representative='田中代表', memo='これは○○株式会社のメモです'),
        ]
        db.session.add_all(custoemrs)
        db.session.commit()
        self.assertGreaterEqual(len(Customer.query.all()), 2)

    def test_delete_customer(self):
        print('---Customer一件削除---')
        customer = Customer.query.filter(Customer.id == 3).delete()
        db.session.commit()

        customer = Customer.query.filter(Customer.id == 3).all()
        self.assertGreaterEqual(len(customer), 0)


if __name__ == '__main__':
    unittest.main()
