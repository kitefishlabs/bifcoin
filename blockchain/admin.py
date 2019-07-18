from django.contrib import admin

from .models import MinedTransaction, BifTransaction, EarnedTransaction


class BifTransactionAdmin(admin.ModelAdmin):
    pass


class MinedTransactionAdmin(admin.ModelAdmin):
    pass


class EarnedTransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(MinedTransaction, MinedTransactionAdmin)
admin.site.register(BifTransaction, BifTransactionAdmin)
admin.site.register(EarnedTransaction, EarnedTransactionAdmin)
