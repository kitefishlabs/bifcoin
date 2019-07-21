from django.urls import path

from . import views

# app_name = 'bifcoin_blockchain'
urlpatterns = [
    path('', views.explorer, name='explorer'),
    #     path('tick/forward', views.tick_forward, name='tick'),
    # path('tick/backward', views.tick_backward, name='tock'),
    path('transactions', views.TransactionsView.as_view(), name='transactions'),
    #     path('transactions/pending', views.PendingTransactionsView.as_view(),
    #          name='pending-transactions'),
    path('transactions/mined', views.MinedTransactionsView.as_view(),
         name='mined-transactions'),
    path('transactions/<int:pk>', views.TransactionDetailView.as_view(),
         name='transaction-detail'),
]
