from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

import datetime

from .models import MinedTransaction, BifTransaction, EarnedTransaction, NetworkStateLog
from users.models import ClaimedProposal


def explorer(request):
    network_state_log_list = NetworkStateLog.objects.all().order_by(
        '-last_network_update')[:10]
    bif_transactions = BifTransaction.objects.all().order_by('-timestamp')[:10]
    mined_transactions = MinedTransaction.objects.all().order_by(
        '-timestamp')[:10]
    earned_transactions = EarnedTransaction.objects.all().order_by(
        '-timestamp')[:10]
    return render(request, 'blockchain/explorer.html', {'network_state_log_list': network_state_log_list, 'bif_transactions': bif_transactions, 'mined_transactions': mined_transactions, 'earned_transactions': earned_transactions})


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


class NetworkStateLogView(generic.ListView):
    template_name = 'blockchain/network_state.html'
    context_object_name = 'network_state_log_list'

    def get_queryset(self):
        return NetworkStateLog.objects.order_by('-last_network_update')


def mine_forward(request):
    network_state = NetworkStateLog.objects.order_by('-last_network_update')
    if len(network_state) == 0:
        network_state = NetworkStateLog(last_network_update=timezone.now())
        network_state.save()
    else:
        last_network_state = network_state[0]
        time_now = timezone.now()
        mining_delta = datetime.timedelta(
            hours=3)  # network_state.mining_window
        last_update = last_network_state.last_network_update

        network_state = NetworkStateLog(last_network_update=timezone.now())
        network_state.save()

        if (last_update < (time_now + mining_delta)) and request.method == 'POST':
            # gather the proposals that are now earlier than the current time and not attached to a mined transaction
            ready_to_mine = ClaimedProposal.objects.filter(
                proposal_datetime__lte=time_now).filter(mined_transaction=None)
            mining_reward = last_network_state.mining_reward
            for proposal in ready_to_mine:
                if proposal.proposal_datetime.hour == 6:
                    mining_reward = last_network_state.installation_reward
                mined = MinedTransaction(
                    recipient=proposal.owner, amount=mining_reward, proposal=proposal, pending=True)
                mined.save()
    # TODO: add feedback message
    return HttpResponseRedirect('/blockchain/explorer')


def tick_forward(request):
    # check that the current time is later than the time of the last network update
    time_now = timezone.now()
    last_update = NetworkStateLog.objects.order_by('-last_network_update')[0]
    # - do nothing if it is not
    if (last_update.last_network_update < time_now) and request.method == 'POST':
        # gather the transactions that are now earlier than the current time and pending
        pending_bifs = BifTransaction.objects.filter(
            timestamp__lte=time_now).exclude(pending=False)
        # subtract the pending amounts from each referenced user's pending balance
        for transaction in pending_bifs:
            amount = transaction.amount
            transaction.sender.pending_balance += amount
            transaction.recipient.pending_balance -= amount
            transaction.recipient.balance += amount
            transaction.sender.save()
            transaction.recipient.save()
            # mark them as no longer pending and bump the verified timestamp
            transaction.pending = False
            transaction.verified = timezone.now()
            transaction.save()

        pending_mined = MinedTransaction.objects.filter(
            timestamp__lte=time_now).exclude(pending=False)
        # subtract the pending amounts from each referenced user's pending balance
        for transaction in pending_mined:
            amount = transaction.amount
            transaction.recipient.pending_balance -= amount
            transaction.recipient.balance += amount
            transaction.recipient.save()
            # mark them as no longer pending and bump the verified timestamp
            transaction.pending = False
            transaction.verified = timezone.now()
            transaction.save()

        pending_earned = EarnedTransaction.objects.filter(
            timestamp__lte=time_now).exclude(pending=False)
        # subtract the pending amounts from each referenced user's pending balance
        for transaction in pending_earned:
            amount = transaction.amount
            transaction.recipient.pending_balance -= amount
            transaction.recipient.balance += amount
            transaction.recipient.save()
            # mark them as no longer pending and bump the verified timestamp
            transaction.pending = False
            transaction.verified = timezone.now()
            transaction.save()

    return HttpResponseRedirect('/blockchain/explorer')
