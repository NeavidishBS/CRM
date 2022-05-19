from django.db import models

from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings

from accounts.models import Account
from contacts.models import Contact
from proposals.models import Proposal
from servicelist.models import Servicelist

from django.utils.timezone import utc
from django.db.models import Sum, Q

from simple_history.models import HistoricalRecords
from django.utils import timezone

class Contract(models.Model):
	title = models.CharField(max_length=200, blank=True)
	contract_add_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='contract_owner')
	status = models.CharField(max_length=50, blank=True)
	date_start = models.DateTimeField(default=timezone.now, blank=True)
	date_end = models.DateTimeField(default=timezone.now, blank=True)
	account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, blank=True)
	service = models.ForeignKey(Servicelist, on_delete=models.DO_NOTHING, blank=True)	
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=20)
	rate = models.DecimalField(max_digits=10, decimal_places=7)
	add_date = models.DateTimeField(default=timezone.now)
	planned_invoices = models.IntegerField(default=1)
	history = HistoricalRecords()

	@property
	def _history_user(self):
		return self.changed_by

	def invoice_count(self):
		return self.invoice_set.count()

	def invoice_paid(self):
		paid = self.invoice_set.filter(Q(contract=self.pk) & Q(status='paid')).aggregate(ta=Sum('amount'))
		ta_paid = paid['ta']
		return ta_paid 

	def invoice_issued(self):
		issued = self.invoice_set.filter(Q(contract=self.pk) & Q(status='issued')).aggregate(ta=Sum('amount'))
		ta_issued = issued['ta']
		return ta_issued

	def invoice_new(self):
		new = self.invoice_set.filter(Q(contract=self.pk) & Q(status='new')).aggregate(ta=Sum('amount'))
		ta_new = new['ta']
		return ta_new

	def invoices_sum(self):
		invoice_sum = self.invoice_set.filter(contract=self.pk).aggregate(ta=Sum('amount'))
		total = invoice_sum['ta']
		return total


	def contract_completion(self):
		paid = self.invoice_set.filter(Q(contract=self.pk) & Q(status='paid')).aggregate(ta=Sum('amount'))
		ta_paid = paid['ta']
		if ta_paid is not None:
			completion_not = ta_paid/self.amount * 100
			completion = round(completion_not, 2)
		else:
			completion = 'no paid invoices'
		
		return completion
	
	def contract_audit(self):

		paid = self.invoice_set.filter(Q(contract=self.pk) & Q(status='paid')).aggregate(ta=Sum('amount'))
		ta_paid = paid['ta']

		if ta_paid is None:
			ta_paid = 0
		else:
			ta_paid = paid['ta']

		issued = self.invoice_set.filter(Q(contract=self.pk) & Q(status='issued')).aggregate(ta=Sum('amount'))
		ta_issued = issued['ta']

		if ta_issued is None:
			ta_issued = 0
		else:
			ta_issued = issued['ta']

		new = self.invoice_set.filter(Q(contract=self.pk) & Q(status='new')).aggregate(ta=Sum('amount'))
		ta_new = new['ta']

		if ta_new is None:
			ta_new = 0
		else:
			ta_new = new['ta']
		
		total_invoices = ta_paid + ta_issued + ta_new

		if self.invoice_set.count() is None:
			invoice_count = 0
		else:
			invoice_count = self.invoice_set.count()
		

		if self.planned_invoices  is  None:
				planned_invoices  = 0
		else:
			planned_invoices = self.planned_invoices
			
			
			
		left_invoices = planned_invoices - invoice_count
		
		if planned_invoices == 0:
			audit = 'please add number of planned invoices'

		elif invoice_count == 0 :
			audit = 'please add planned invoices to the contract'

		elif planned_invoices > invoice_count:
			audit = 'please add the rest ' + str(left_invoices)  + ' invoices'
		
		elif planned_invoices < invoice_count:
			audit = 'check the planned invoices ' + str(left_invoices)
		
		elif invoice_count != planned_invoices :
			audit = 'the number of planned invoices and actual invoices are not matching'

		
	
		else:
			if total_invoices != self.amount:
				audit = 'check amounts of invoices'
			else:
				audit = "ok"
			

		return audit
	
	def cost_base(self):
		r = self.rate
		c = self.amount
		cost_base_b = r * c
		cost_base = round(cost_base_b, 2)
		return cost_base

	# def sum_cost_base(self):
	# 	scbcss = []
	# 	for c in contracts:
	# 		base = round(c.rate * c.amount, 2)
	# 		scbcss.append(base)
	# 	sum_cost_base = sum(scbcss)
	# 	return sum_cost_base

	def __str__(self):
		return self.title


class ContractTimeline(models.Model):

	changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1,
    	)
	timestamp = models.DateTimeField(auto_now=True)
	contract_id = models.IntegerField(default=0)
	field_name = models.CharField(max_length=200, blank=True)
	old_value  = models.CharField(max_length=200, blank=True)
	new_value  = models.CharField(max_length=200, blank=True)
	ip  = models.GenericIPAddressField()
