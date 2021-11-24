from app import db, app
from models import Memo
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

    def test_get_memos(self):
        print('---Memo全件読み込み---')
        memos = Memo.query.all()
        memoCount = len(memos)
        self.assertTrue(memoCount)

    def test_get_memo_byId(self):
        print('---Memo一件読み込み---')
        memo = Memo.query.filter(Memo.id == 1).first()
        self.assertTrue(memo)
        self.assertEqual(memo.title, 'メモのタイトル１')

        print('---Memo一件読み込み失敗---')
        memos = Memo.query.filter(Memo.id == 9999).all()
        self.assertFalse(memos)
        self.assertEqual(len(memos), 0)

    def test_update_memo(self):
        print('---Memo一件更新---')
        memo = Memo.query.filter(Memo.id == 2).first()
        memo.title = 'メモのタイトル変更'
        db.session.commit()
        memo = Memo.query.filter(Memo.id == 2).first()
        self.assertEqual(memo.title, "メモのタイトル変更")

    def test_create_memo(self):
        print('---Memo新規作成---')
        memos = [
            Memo(title='メモのタイトル４', content='メモの内容４'),
            Memo(title='メモのタイトル５', content='メモの内容５'),
        ]
        db.session.add_all(memos)
        db.session.commit()
        self.assertGreaterEqual(len(Memo.query.all()), 2)

    def test_delete_memo(self):
        print('---Memo一件削除---')
        memo = Memo.query.filter(Memo.id == 3).delete()
        db.session.commit()

        memo = Memo.query.filter(Memo.id == 3).all()
        self.assertGreaterEqual(len(memo), 0)


if __name__ == '__main__':
    unittest.main()
