from django import forms
from accounts.models import Account
from contacts.models import Contact
from proposals.models import Proposal
from .models import Contract


class ContractForm(forms.ModelForm):
	class Meta:
		model = Contract
		fields = ('title', 'status', 'account', 'amount', 'date_start', 'date_end', 'planned_invoices', 'currency', 'rate', 'contract_add_by', 'service')
		widgets = {
		'title': forms.TextInput(attrs={'class': 'form-control'}),
		'amount': forms.TextInput(attrs={'class': 'form-control'}),
		'service': forms.Select(attrs={'class': 'form-control'}),
		'status': forms.Select(choices={
				('planned', 'planned'),
				('signed', 'signed'),
				('completed', 'completed'),
				('cancelled', 'cancelled'),},
				attrs={'class': 'form-control'}),
		'contract_add_by': forms.HiddenInput(),
		'rate': forms.HiddenInput(),
		'currency': forms.Select(
					choices={
					('AZN', 'AZN'),
					('EUR', 'EUR'),
					('RUB', 'RUB'),
					('USD', 'USD'),},
					attrs={'class': 'form-control'}),
		'date_start': forms.DateInput(attrs={
					'class': 'form-control datetimepicker-input',
					'type': 'date'}),
		'date_end': forms.DateInput(attrs={
					'class': 'form-control datetimepicker-input',
					'type': 'date'}),
		'planned_invoices': forms.TextInput(attrs={'class': 'form-control'}),
		'account': forms.Select(attrs={'class': 'form-control'})}






