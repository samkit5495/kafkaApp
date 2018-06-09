from mongoengine import *
from datetime import datetime


class Transaction(Document):
    user = IntField(required=True)
    date = DateTimeField(required=True)
    amount = FloatField(required=True)
    alert = BooleanField(default=False)