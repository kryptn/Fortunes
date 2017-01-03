from flask_testing import TestCase
from fortunate.utils import make_app
from fortunate import db

class Base(TestCase):
    
    def create_app(self):
        return make_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
