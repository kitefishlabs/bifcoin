from django.contrib import admin

from .models import MinedTransaction, BifTransaction, EarnedTransaction, NetworkStateLog


class BifTransactionAdmin(admin.ModelAdmin):
    pass


class MinedTransactionAdmin(admin.ModelAdmin):
    pass


class EarnedTransactionAdmin(admin.ModelAdmin):
    pass


class NetworkStateLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(MinedTransaction, MinedTransactionAdmin)
admin.site.register(BifTransaction, BifTransactionAdmin)
admin.site.register(EarnedTransaction, EarnedTransactionAdmin)
admin.site.register(NetworkStateLog, NetworkStateLogAdmin)
