from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register', views.RegistrationView.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('claim/proposals',
         views.claim_proposals, name='claim'),
    path('unclaim/proposals',
         views.unclaim_proposals, name='unclaim'),
    # path('proposal/<int:proposal_id>',
    #      views.proposal_detail, name='proposal-detail'),
]
