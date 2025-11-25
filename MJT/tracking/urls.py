from django.urls import path
from .views import *

app_name = 'tracking'

urlpatterns = [
    #path('track_user/', track_user, name='track_user'),
    path('dashboard/', dashboard, name='dashboard'),
    

    path('invoices/', Invoices_view, name='invoices'),
    path('inward/', Inward_view, name='inward'),
    path('processing/', Processing_view, name='processing'),
    path('program/', Program_view, name='program'),

    path('proccesslogentry/', Add_processs_log, name='processinglogentry'),
    path('proccesslogentry/<int:id>',Update_process_logs,name="Update_processinglogentry"),

    path('inwardentry/', Add_inward_entry, name='inwardentry'),
    path('inwardentry/<int:id>',Update_Inwards,name="Update_inwardentry"),

    path('programdetailentry/', Add_program_detail, name='programdetailentry'),
    path('programdetailentry/<int:id>', Update_program_details, name='Update_programdetailentry'),

    path('invoiceentry/', Add_invoice, name='invoiceentry'),
    path('invoiceentry/<int:id>',Update_Invoices, name='Update_invoiceentry'),

    path('logout/', logout_view, name='logout'),

    #path('test-500/', test_500, name='test_500'), # for testing 500 error page
]
