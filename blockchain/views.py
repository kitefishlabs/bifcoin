from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import MinedTransaction, BifTransaction, EarnedTransaction


def explorer(request):
    # bif = BifTransaction.objects.all()

    return render(request, 'blockchain/explorer.html', {})


class TransactionsView(generic.ListView):
    template_name = 'blockchain/transactions.html'
    context_object_name = 'bif_transactions_list'

    def get_queryset(self):
        return BifTransaction.objects.order_by('-timestamp')


class TransactionDetailView(generic.DetailView):
    model = BifTransaction
    template_name = 'blockchain/transaction_detail.html'


class MinedTransactionDetailView(generic.DetailView):
    model = MinedTransaction
    template_name = 'blockchain/transaction_detail.html'


class EarnedTransactionDetailView(generic.DetailView):
    model = EarnedTransaction
    template_name = 'blockchain/transaction_detail.html'


class MinedTransactionsView(generic.ListView):
    template_name = 'blockchain/transactions.html'
    context_object_name = 'mined_transactions_list'

    def get_queryset(self):
        return MinedTransaction.objects.order_by('-timestamp')


class EarnedTransactionsView(generic.ListView):
    template_name = 'blockchain/transactions.html'
    context_object_name = 'earned_transactions_list'

    def get_queryset(self):
        return EarnedTransaction.objects.order_by('-timestamp')
