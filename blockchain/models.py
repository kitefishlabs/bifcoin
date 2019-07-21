from django.db import models

from users.models import BifCoinUser, ClaimedProposal, BifUserAction


class MinedTransaction(models.Model):
    recipient = models.ForeignKey(
        BifCoinUser, on_delete=models.SET_NULL, null=True, related_name='transactions_mined')
    amount = models.IntegerField()
    proposal = models.OneToOneField(
        ClaimedProposal, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.DateTimeField(auto_now_add=True)
    pending = models.BooleanField()

    def __str__(self):
        # recip = self.recipient
        return ' - '.join([self.timestamp.strftime("%Y-%m-%d %H:%M"), str(self.recipient), str(self.amount), str(self.pending)])


class BifTransaction(models.Model):
    """
    hint: this is altruistic part
    """
    sender = models.ForeignKey(
        BifCoinUser, on_delete=models.SET_NULL, null=True, related_name='transactions_sent')
    recipient = models.ForeignKey(
        BifCoinUser, on_delete=models.SET_NULL, null=True, related_name='transactions_received')
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.DateTimeField(auto_now_add=True)
    pending = models.BooleanField()

    def __str__(self):
        return ' - '.join([self.timestamp.strftime("%Y-%m-%d %H:%M"), str(self.amount), self.sender.user.email, self.recipient.user.email, str(self.pending)])


class EarnedTransaction(models.Model):
    recipient = models.ForeignKey(
        BifCoinUser, on_delete=models.SET_NULL, null=True, related_name='transactions_earned')
    amount = models.IntegerField()
    action = models.OneToOneField(to=BifUserAction, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.DateTimeField(auto_now_add=True)
    pending = models.BooleanField()

    def __str__(self):
        return ' - '.join([self.timestamp.strftime("%Y-%m-%d %H:%M"), str(self.amount), self.recipient.user.email, self.action.action, str(self.pending)])


#     ART_CHOICES = [
#         ('random poetry', 'poetry'),
#         ('random ascii art', 'art'),
#     ]
#     art = models.CharField(max_length=15, choices=ART_CHOICES)
#     art_payload = models.TextField()  # text or social media


class NetworkStateLog(models.Model):
    last_network_update = models.DateTimeField(auto_now_add=True)
    approved_transactions = models.IntegerField()
    mining_reward = models.IntegerField(default=10)
    social_reward = models.IntegerField(default=1)
    note_reward = models.IntegerField(default=3)
    feedback_reward = models.IntegerField(default=2)
