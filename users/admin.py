from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import EmailUserCreationForm, EmailUserChangeForm
from .models import EmailUser, BifCoinUser, ClaimedProposal


class EmailUserAdmin(UserAdmin):
    add_form = EmailUserCreationForm
    form = EmailUserChangeForm
    model = EmailUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class BifCoinUserAdmin(admin.ModelAdmin):
    pass


class ClaimedProposalAdmin(admin.ModelAdmin):
    pass


admin.site.register(EmailUser, EmailUserAdmin)
admin.site.register(BifCoinUser, BifCoinUserAdmin)
admin.site.register(ClaimedProposal, ClaimedProposalAdmin)
