from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView

from .forms import EmailUserCreationForm
from .models import BifCoinUser, ClaimedProposal


class RegistrationView(CreateView):
    form_class = EmailUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/register.html'


def dashboard(request):
    user = request.user
    linked_email = ''
    claimable = False
    claimed = False
    possible_bifcoin_users = BifCoinUser.objects.filter(
        proposal_email=user.email)
    if (len(possible_bifcoin_users) == 1) and (possible_bifcoin_users[0].state == 'claimed'):
        linked_email = possible_bifcoin_users[0].proposal_email
        claimed = True
    elif (len(possible_bifcoin_users) == 1):
        linked_email = possible_bifcoin_users[0].proposal_email
        claimable = True
    else:
        pass
    proposals = ClaimedProposal.objects.filter(proposal_email=user.email)
    return render(request, 'user/dashboard.html', {'claimable': claimable, 'claimed': claimed, 'linked_email': linked_email, 'linked_proposals': list(proposals), })


def claim_proposals(request):
    if request.method == 'POST':
        linking_email = request.user.email
        possible_bifcoin_users = BifCoinUser.objects.filter(
            proposal_email=linking_email)
        proposals = ClaimedProposal.objects.filter(
            proposal_email=linking_email)
        if (len(possible_bifcoin_users) == 1) and (len(proposals) > 0):
            user = possible_bifcoin_users[0]
            user.state = 'claimed'
            user.save()
            for proposal in proposals:
                proposal.state = 'claimed'
                proposal.save()

    return HttpResponseRedirect('/user')


def unclaim_proposals(request):
    if request.method == 'POST':
        linking_email = request.user.email
        possible_bifcoin_users = BifCoinUser.objects.filter(
            proposal_email=linking_email)
        proposals = ClaimedProposal.objects.filter(
            proposal_email=linking_email)
        if (len(possible_bifcoin_users) == 1) and (len(proposals) > 0):
            user = possible_bifcoin_users[0]
            user.state = 'unclaimed'
            user.save()
            for proposal in proposals:
                proposal.state = 'unclaimed'
                proposal.save()

    return HttpResponseRedirect('/user')
