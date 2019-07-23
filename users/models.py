from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import EmailUserManager


class EmailUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = EmailUserManager()

    def __str__(self):
        return self.email


STATE_CHOICES = [
    ('unclaimed', 'unclaimed'),
    ('claimed', 'claimed'),
    ('abandoned', 'abandoned'),
]


class BifCoinUser(models.Model):
    """
    when registered, user = NULL -> EmailUser + claimed = True
    if unregistered, user = EmailUser -> NULL + claimed = False
    users without proposals have NULL proposal_emails
    unclaimed users' proposal emails are generated one time by scraping and should never change
    """
    user = models.OneToOneField(
        EmailUser, on_delete=models.SET_NULL, null=True)
    proposal_email = models.EmailField(max_length=100, null=True, unique=True)
    balance = models.IntegerField()
    # pending bal. can be negative
    pending_balance = models.IntegerField()
    state = models.CharField(max_length=9, choices=STATE_CHOICES)

    def __str__(self):
        return (self.proposal_email + '|' + self.state + '|' + str(self.balance))


class ClaimedProposal(models.Model):
    """
    each proposal is associated with a bifcoin user (claimed or not) and a proposal id
    if the bifcoin user disappears, the owner field reverts to NULL in all owned proposals
    (in this case, these objects should also be reassociated with a BCUser)
    should not matter whether the proposal's claimed state is tracked
    if cancelled, this should cause any transactions to be reversed
    """
    owner = models.ForeignKey(
        BifCoinUser, on_delete=models.SET_NULL, null=True, blank=True)
    proposal_id = models.IntegerField()
    proposal_name = models.CharField(max_length=100)
    proposal_datetime = models.DateTimeField()
    proposal_email = models.EmailField(max_length=100, null=True)
    state = models.CharField(max_length=9, choices=STATE_CHOICES)
    cancelled = models.BooleanField()

    def __str__(self):
        return (self.proposal_name + '|' + self.proposal_datetime.strftime("%Y-%m-%d %H:%M"))


class BifUserAction(models.Model):
    actor = models.ForeignKey(
        BifCoinUser, on_delete=models.SET_NULL, null=True, related_name='user_action')
    ACTION_CHOICES = [
        ('social media', 'social'),
        ('note', 'note'),
        ('feedback', 'feedback'),
    ]
    action = models.CharField(max_length=12, choices=ACTION_CHOICES)
    action_payload = models.TextField()  # text or social media
