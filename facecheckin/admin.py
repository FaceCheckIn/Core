from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'sentiment', 'status', 'created_at')
    list_filter = ('user', 'status',)


admin.site.register(Transaction, TransactionAdmin)
