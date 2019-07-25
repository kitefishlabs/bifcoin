from django.urls import path

from . import views

# app_name = 'bifcoin_blockchain'
urlpatterns = [

    path('', views.explorer, name='explorer'),
    path('explorer', views.explorer, name='explorer'),

    path('tick/forward', views.tick_forward, name='tick'),
    # path('tick/backward', views.tick_backward, name='tock'),
    path('mine/forward', views.mine_forward, name='mine'),
    # path('mine/backward', views.mine_backward, name='unmine'),

    path('transactions', views.TransactionsView.as_view(), name='transactions'),
    path('transactions/earned', views.EarnedTransactionsView.as_view(),
         name='earned-transactions'),
    path('transactions/mined', views.MinedTransactionsView.as_view(),
         name='mined-transactions'),
    path('transactions/<int:pk>', views.TransactionDetailView.as_view(),
         name='transaction-detail'),

    path('transaction/send>', views.transaction_send_view,
         name='transaction_send'),
    path('transaction/send/<int:proposal_id>', views.transaction_send,
         name='transaction_send'),
    # path('transaction/earn', views.TransactionEarnView.as_view(), name='transaction_earn'),

    path('network/log', views.NetworkStateLogView.as_view(),
         name='network-state'),
]
