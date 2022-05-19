from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
# from contacts.models import Contact
from django.contrib.auth.decorators import login_required
from contacts.models import Contact
from proposals.models import Proposal
from tasks.models import Task
from invoices.models import Invoice

from .models import Contract, ContractTimeline
from .forms import ContractForm

from invoices.forms  import InvoiceForm

from tasks.forms import TaskForm
from tasks.models import Task


# from .forms import proposalForm
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Q, Max

from app.views import get_client_ip
from app.views import cost_base_cal
from app.views import get_currency_rate

from comments.forms import CommentForm
from comments.models import Comment


from files.forms import FileForm
from files.models import File
from datetime import datetime


# Create your views here.


@login_required(login_url='login')
def contracts(request):

	if request.method == 'POST':
		ContractFormTemplate = ContractForm(request.POST, request.FILES)
		
		if ContractFormTemplate.is_valid():
			obj = ContractFormTemplate.save(commit=False)
			currency = ContractFormTemplate.cleaned_data['currency']
			account_in_contract = ContractFormTemplate.cleaned_data['account']



			if currency == 'USD':
				azn_usd = get_currency_rate(request, currency)
				obj.rate = azn_usd
				obj.save()
			elif currency == 'EUR':
				azn_eur = get_currency_rate(request, currency)
				obj.rate = azn_eur
				obj.save()
			elif currency == 'RUB':
				azn_rub = get_currency_rate(request, currency)
				obj.rate = azn_rub
		
				obj.save()

			else:
				obj.rate = 1
				obj.save()

			the_contract = Contract.objects.aggregate(pk=Max('pk'))
			the_contract_id = the_contract['pk']
			contract = Contract.objects.get(id=the_contract_id)
			inv_amnt = contract.amount / contract.planned_invoices
			time_step = (contract.date_end - contract.date_start)/contract.planned_invoices
			n = 1
			for invoice in range(contract.planned_invoices):
				inv_start_date = contract.date_start + (time_step*n)
				inv_end_date = contract.date_start + time_step
				invoice = Invoice(
						title= "invoice " + str(n) + " for " + contract.title,
						status= "new",
						contract = contract,
						date_start = inv_start_date,
						date_end = inv_end_date,
						amount = inv_amnt,
						rate = contract.rate,	
						currency = contract.currency,
						invoice_add_by = contract.contract_add_by)
				invoice.save()
				n = n + 1
			
			count_contracts = Contract.objects.all().filter(account=account_in_contract).count()
			if count_contracts != 0:
				account_in_contract.is_client = True
				account_in_contract.save()
			else:
				account_in_contract.is_client = False
				account_in_contract.save()


			messages.success(request, 'The record is successfully created')
		else:
			messages.error(request, 'check Your form')

		return redirect('contract_view', the_contract_id)
	else:

		ContractFormTemplate = ContractForm()
		
		contracts_all = Contract.objects.order_by('-id')
		contracts_signed = Contract.objects.all().filter(status='signed').order_by('-id')
		contracts_completed = Contract.objects.all().filter(status='completed').order_by('-id')
		contracts_planned = Contract.objects.all().filter(status='planned').order_by('-id')
		contracts_cancelled = Contract.objects.all().filter(status='cancelled').order_by('-id')



		current_year_str = str(datetime.now().year)
		scbcss = []

		ytd_sales = Contract.objects.filter(date_start__range=[current_year_str+"-01-01", current_year_str+"-12-31"])
		
		ytd_sum_cost_base = cost_base_cal(ytd_sales)
		sum_cost_base = cost_base_cal(contracts_all)


		quaterlysold = Contract.objects.filter(date_start__range=["2020-01-01", "2020-03-31"]).aggregate(qs=Sum('amount'))

		qsold = quaterlysold['qs']

		all_contracts = Contract.objects.all().aggregate(ts=Sum('amount'))
		
		ts_contracts = all_contracts['ts']

		ContractFormTemplate = ContractForm(
			initial={
			'contract_add_by': request.user.id,
			'rate': 0,
			'status': 'signed'

			}
		)
		context = {
		'contracts_all': contracts_all,
		'contracts_signed': contracts_signed,
		'contracts_completed':contracts_completed,
		'contracts_planned': contracts_planned,
		'contracts_cancelled':contracts_cancelled,
		'ContractFormTemplate': ContractFormTemplate,
		'ts_contracts': ts_contracts,
		'all_contracts': all_contracts,
		'sum_cost_base': sum_cost_base,
		'ytd_sum_cost_base':ytd_sum_cost_base,
		}

		return render(request, 'contracts/contracts.html', context)

@login_required
def contract_view_id(request, contract_view_id):


	contract = get_object_or_404(Contract, pk=contract_view_id)
	tasks = Task.objects.all().filter(Q(parent_id=contract_view_id) & Q(parent='contract')).order_by('-id')
	invoices_paid = Invoice.objects.all().filter(Q(contract=contract_view_id) & Q(status='paid'))
	invoices_issued = Invoice.objects.all().filter(Q(contract=contract_view_id) & Q(status='issued'))
	invoices_new = Invoice.objects.all().filter(Q(contract=contract_view_id) & Q(status='new'))

	invoices = Invoice.objects.all().filter(contract=contract_view_id)

	comments = Comment.objects.all().filter(Q(parent_id=contract_view_id) & Q(parent='contract')).order_by('-id')

	files = File.objects.all().filter(Q(parent_id=contract_view_id) & Q(parent='contract')).order_by('-id')
	files_count = File.objects.all().filter(Q(parent_id=contract_view_id) & Q(parent='contract')).order_by('-id').count()


	ip = get_client_ip(request)

	if request.method == 'POST':
		form = ContractForm(request.POST or None, request.FILES, instance=contract)
	

		if form.is_valid():
			obj = form.save(commit=False)
			currency = form.cleaned_data['currency']

			if currency == 'USD':
				azn_usd = get_currency_rate(request, currency)
				obj.rate = azn_usd

				obj.save()
			elif currency == 'EUR':
				azn_eur = get_currency_rate(request, currency)
				obj.rate = azn_eur
				obj.save()
			elif currency == 'RUB':
				azn_rub = get_currency_rate(request, currency)
				obj.rate = azn_rub
	
				obj.save()

			else:
				obj.rate = 1
				obj.save()

			cnrct = Contract.history.all().filter(id=contract_view_id)
			changes = []
			last = cnrct.first()
			new_record, old_record = last, last.prev_record
			delta = new_record.diff_against(old_record)
			changes.append(delta)
			for change in delta.changes:
						field_name = change.field
						old_value  = change.old
						new_value  = change.new

						cnrcttl = ContractTimeline(
								changed_by = request.user,
								contract_id = contract_view_id,
								field_name = field_name,
								old_value  = old_value,
								new_value  = new_value,
								ip         = ip
								)
						cnrcttl.save()

			messages.success(request, 'The record is successfully created')
		else:
			messages.error(request, 'check Your form')

		return redirect('contract_view', contract_view_id)

	else:

		ContractUpdateForm = ContractForm(
			initial={

			'title': contract.title,
			'contract_add_by': contract.contract_add_by,
			'status': contract.status,
			'date_start': contract.date_start,
			'date_end': contract.date_end,
			'account': contract.account, 
			'amount': contract.amount,
			'rate': contract.rate,
			'currency': contract.currency,
			'planned_invoices': contract.planned_invoices,
			'service': contract.service
			}
			)


		TaskFormTemplate = TaskForm(
			initial={
			'add_by': request.user.id,
			'parent_id': contract_view_id,
			'parent': "contract",
			# 'tasks': tasks,
			}
		)

		InvoiceFormTemplate = InvoiceForm(
			initial={
			'invoice_add_by': request.user.id,
			'contract': contract_view_id,
			'rate': 0

			}
		)

		CommentFormTemplate = CommentForm(
			initial={
			'added_by': request.user.id,
			'parent_id': contract_view_id,
			'parent': "contract",
			'comments': comments,
			}
		)

		ContractFilesFormTemplate = FileForm(
			initial={
			
			'file_add_by': request.user.id,
			'parent': 'contract',
			'parent_id': contract_view_id
			
			}
		)

		contract_history = Contract.history.all().filter(id=contract_view_id)
		contract_hist_time = ContractTimeline.objects.all().filter(contract_id=contract_view_id).order_by('-timestamp')
		contact_last_updated = ContractTimeline.objects.aggregate(last_updated_time=Max('timestamp'))

	context ={
        'contract': contract,
		'TaskFormTemplate': TaskFormTemplate,
		'ContractUpdateForm': ContractUpdateForm,
		'tasks': tasks,
		'invoices_issued': invoices_issued,
		'invoices_paid': invoices_paid,
		'invoices_new': invoices_new,
		'invoices': invoices,
		'InvoiceFormTemplate': InvoiceFormTemplate,
		'contract_history': contract_history,
		'contract_hist_time': contract_hist_time,
		'contact_last_updated ': contact_last_updated,
		'comments': comments,
		'CommentFormTemplate':CommentFormTemplate,
		'ContractFilesFormTemplate':ContractFilesFormTemplate,
		'files': files,
		'files_count':files_count,
		# 'tasks_count':tasks_count,


    }
	return render(request, 'contracts/contract_view.html', context)


@login_required(login_url='login')
def add_invoice(request, contract_view_id):
	from invoices.views import invoices
	invoices(request)

	return redirect('contract_view', contract_view_id)


@login_required(login_url='login')
def add_comment(request, contract_view_id):
	from comments.views import comment
	comment(request)

	return redirect('contract_view_comments', contract_view_id)

@login_required(login_url='login')
def add_contract_file(request, contract_view_id):
	from files.views import files
	files(request)
	return redirect('contract_view', contract_view_id)

@login_required(login_url='login')
def add_task(request, contract_view_id):
	from tasks.views import tasks
	tasks(request)
	return redirect('contract_view', contract_view_id)

@login_required(login_url='login')
def add_task(request, contract_view_id):
	from tasks.views import tasks
	tasks(request)
	return redirect('contract_view', contract_view_id)


@login_required
def contract_task_on_off(request, contract_task_on_off_id):

	task = Task.objects.get(pk=contract_task_on_off_id)

	contract_view_id = task.parent_id
	from tasks.views import task_on_off
	task_on_off(request, contract_task_on_off_id )


	return redirect('contract_view', contract_view_id)