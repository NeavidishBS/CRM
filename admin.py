from django.contrib import admin

# Register your models here.

from .models import Contract, ContractTimeline

class ContractAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'status', 'account', 'amount', 'date_start', 'date_end', 'planned_invoices', 'contract_add_by',)
	list_display_links = ('id',)
	
	list_per_page = 25

admin.site.register(Contract, ContractAdmin)

class ContractTimelineAdmin(admin.ModelAdmin):
	list_display = ('id', 'changed_by', 'timestamp', 'contract_id', 'field_name', 'old_value', 'new_value', 'ip',)
	list_display_links = ('id',)
	
	list_per_page = 25

admin.site.register(ContractTimeline, ContractTimelineAdmin)