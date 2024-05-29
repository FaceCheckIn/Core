from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'sentiment', 'status', 'datetime')
    readonly_fields = ('user', 'sentiment', 'status', 'datetime')


admin.site.register(Transaction, TransactionAdmin)
