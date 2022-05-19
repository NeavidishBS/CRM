from django.urls import path

from . import views

urlpatterns = [

    path('', views.contracts, name='contracts'),
    path('contract/<int:contract_view_id>', views.contract_view_id, name='contract_view'),
    path('add_invoice/<int:contract_view_id>', views.add_invoice, name='add_contract_invoice'),
    path('add_file/<int:contract_view_id>', views.add_contract_file, name='add_contract_file'),
    path('contract/tasks/<int:contract_view_id>', views.contract_view_id, name='contract_view_tasks'),
    path('add_task/<int:contract_view_id>', views.add_task, name='add_contract_task'),
    path('contract_task_on_off/<int:contract_task_on_off_id>', views.contract_task_on_off, name='contract_task_on_off'),
    path('add_comment/<int:contract_view_id>', views.add_comment, name='add_contract_comment'),
    path('contract/comments/<int:contract_view_id>', views.contract_view_id, name='contract_view_comments'),
    path('signed', views.contracts, name='contracts_signed'),
    path('completed', views.contracts, name='contracts_completed'),
    path('planned', views.contracts, name='contracts_planned'),
    path('cancelled', views.contracts, name='contracts_cancelled'),
    path('all', views.contracts, name='contracts_all'),
    


]

