from app import db, app
from models import Unit
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

    def test_get_units(self):
        print('---Unit全件読み込み---')
        units = Unit.query.all()
        unitCount = len(units)
        self.assertTrue(unitCount)

    def test_get_unit_byId(self):
        print('---Unit一件読み込み---')
        unit = Unit.query.filter(Unit.id == 1).first()
        self.assertTrue(unit)
        self.assertEqual(unit.unitName, '個')

        print('---Unit一件読み込み失敗---')
        units = Unit.query.filter(Unit.id == 9999).all()
        self.assertFalse(units)
        self.assertEqual(len(units), 0)

    def test_update_unit(self):
        print('---Unit一件更新---')
        unit = Unit.query.filter(Unit.id == 2).first()
        unit.unitName = '丁'
        db.session.commit()
        unit = Unit.query.filter(Unit.id == 2).first()
        self.assertEqual(unit.unitName, "丁")

    def test_create_unit(self):
        print('---Unit新規作成---')
        units = [
            Unit(unitName='式'),
            Unit(unitName='枚'),
        ]
        db.session.add_all(units)
        db.session.commit()
        self.assertGreaterEqual(len(Unit.query.all()), 2)

    def test_delete_unit(self):
        print('---Unit一件削除---')
        unit = Unit.query.filter(Unit.id == 3).delete()
        db.session.commit()

        unit = Unit.query.filter(Unit.id == 3).all()
        self.assertGreaterEqual(len(unit), 0)


if __name__ == '__main__':
    unittest.main()
