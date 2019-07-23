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
    user = BifCoinUser.objects.get(
        proposal_email=request.user.email)
    linked_email = ''
    claimable = False
    claimed = False
    proposals = []

    if (user is not None):
        linked_email = user.proposal_email
        if (user.state == 'claimed'):
            claimed = True
        else:
            claimable = True

        proposals = ClaimedProposal.objects.filter(
            proposal_email=user.proposal_email).order_by('proposal_datetime')

    return render(request, 'user/dashboard.html', {'claimable': claimable, 'claimed': claimed, 'linked_email': linked_email, 'linked_proposals': list(proposals), 'bifuser': user})


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
            # flip each proposal's state to claimed
            for proposal in proposals:
                proposal.state = 'claimed'
                proposal.owner = possible_bifcoin_users[0]
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
                proposal.owner = None
                proposal.save()
            user.save()

    return HttpResponseRedirect('/user')
