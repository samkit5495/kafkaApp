from mongoengine import *
from datetime import datetime


class Transactions(Document):
    user = IntField(required=True)
    date = DateTimeField(required=True)
    amount = FloatField(required=True)