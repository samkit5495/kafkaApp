# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.views import View
from dashboard.models import Transaction
# Create your views here.
from datetime import datetime

class DashboardView(View):
    
    def get(self, request):
        return render(request, "dashboard/index.html", {
            'usersCount': len(Transaction.objects.distinct('user')),
            'transactionsCount': Transaction.objects.count(),
            'alertsCount': Transaction.objects(alert=True).count(),
            'latestTransactions': Transaction.objects.order_by('-id').limit(20),
            'now': datetime.now()
        })


class UsersView(View):

    def get(self, request):
        pipeline = [
            {
                '$group':{
                    '_id':'$user',
                    'accountBalance':{'$sum':'$amount'}
                }
            },
            {
                '$project':{
                    'id':'$_id',
                    'accountBalance':'$accountBalance'
                }
            }
        ]
        return render(request, "dashboard/users.html", {
            'users': list(Transaction.objects.aggregate(*pipeline))
        })

    def userTransactions(self, request, id):
        return render(request, "dashboard/transactions.html", {
            'transactions': Transaction.objects(user=id)
        })


class TransactionView(View):

    def get(self, request):
        return render(request, "dashboard/transactions.html", {
            'transactions': Transaction.objects.order_by('-id')
        })


class AlertView(View):

    def get(self, request):
        return render(request, "dashboard/alerts.html", {
            'transactions': Transaction.objects(alert=True).order_by('-id')
        })
