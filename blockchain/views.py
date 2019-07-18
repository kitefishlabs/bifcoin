from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import MinedTransaction, BifTransaction


def explorer(request):
    all_transactions = BifTransaction.objects.all()
    return render(request, 'blockchain/explorer.html', {})


class TransactionsView(generic.ListView):
    template_name = 'blockchain/transactions.html'
    context_object_name = 'latest_bif_transactions_list'

    def get_queryset(self):
        return BifTransaction.objects.order_by('-timestamp')[:20]


class TransactionDetailView(generic.DetailView):
    model = BifTransaction
    template_name = 'blockchain/transaction_detail.html'


class MinedTransactionDetailView(generic.DetailView):
    model = MinedTransaction
    template_name = 'blockchain/transaction_detail.html'


class MinedTransactionsView(generic.ListView):
    template_name = 'blockchain/transactions.html'
    context_object_name = 'latest_mined_transactions_list'

    def get_queryset(self):
        return MinedTransaction.objects.order_by('-timestamp')[:20]


class PendingTransactionsView(generic.ListView):
    template_name = 'blockchain/transactions.html'
    context_object_name = 'latest_pending_transactions_list'

    def get_queryset(self):
        return BifTransaction.objects.filter(pending=True).order_by('-timestamp')[:20]
