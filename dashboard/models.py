from mongoengine import *
from datetime import datetime


class User(Document):
    user_id = IntField(required=True)
    balance = FloatField()
    avg_transaction_amount = FloatField()
    stdev = FloatField()
    avg_monthly_balance = FloatField()

    
class Transaction(Document):
    user = ReferenceField(User,required=True)
    date = DateTimeField(required=True)
    amount = FloatField(required=True)
    alert = BooleanField(default=False)