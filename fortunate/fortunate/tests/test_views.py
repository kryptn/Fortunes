from fortunate import db, models, views

from fortunate.tests.base import Base

class ViewsTest(Base):

    def test_test(self):
        self.assertEqual(True, True)