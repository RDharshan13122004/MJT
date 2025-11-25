from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from users.models import UserProfile
from .forms import *
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from users.decorators import AuthenticatedUser

'''
------------------------------------
 ADD A CUSTOMER PAGE 404 ERROR FIXED
---------------------------------
'''

# Create your views here.
# def track_user(request):
#     return HttpResponse("User tracking view")
def dashboard(request):
    user_id = request.session.get('user_id')
    print(request.session.get('role'))
    if not user_id:
        return redirect('users:user_login')
    try:
        user_object = UserProfile.objects.get(user_id=user_id)
        return render(request, 'dashboard.html',
                      {
                        'user':user_object
                       })
    except UserProfile.DoesNotExist:
        return render(request, 'login.html', {'error': 'User not found. Please log in again.'})

def Invoices_view(request):
    Invoice_objects = Invoice.objects.all().order_by('-id')
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'login.html', {'error': 'Please log in to access the dashboard.'})
    try:
        user_object = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return render(request, 'login.html', {'error': 'User not found. Please log in again.'})
    
    return render(request, 'Invoices.html',{'invoices':Invoice_objects,'user':user_object})

def Inward_view(request):
    Inward_objects = InwardEntry.objects.all().order_by('-id')
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'login.html', {'error': 'Please log in to access the dashboard.'})
    try:
        user_object = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return render(request, 'login.html', {'error': 'User not found. Please log in again.'})

    return render(request, 'Inward_Entries.html',{'inward_entries':Inward_objects,'user':user_object})

def Processing_view(request):
    Processing_objects = ProcessingLog.objects.all().order_by('-id')
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'login.html', {'error': 'Please log in to access the dashboard.'})
    try:
        user_object = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return render(request, 'login.html', {'error': 'User not found. Please log in again.'})

    return render(request, 'processing_logs.html',{'processing_logs':Processing_objects,'user':user_object})

def Program_view(request):
    Program_objects = ProgramDetail.objects.all().order_by('-id')
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'login.html', {'error': 'Please log in to access the dashboard.'})
    try:
        user_object = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return render(request, 'login.html', {'error': 'User not found. Please log in again.'})

    return render(request, 'Program_Details.html',{'program_details':Program_objects,'user':user_object})


@AuthenticatedUser(allowed_roles=['Admin', 'Supervisor', 'MachineOperator'])
def Add_processs_log(request):
    if request.method == 'POST':
        form = ProcessingLogForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Processing log added successfully.')
            form = ProcessingLogForm()  # Clear the form after successful submission
            return redirect('tracking:processing')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'Add_process_log.html', {'form': form})
    form = ProcessingLogForm()
    return render(request, 'Add_process_log.html', {'form': form})

@AuthenticatedUser(allowed_roles=['Admin', 'Storekeeper'])
def Add_inward_entry(request):
    if request.method == 'POST':
        form = InwardsEntryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inward entry added successfully.')
            form = InwardsEntryForm()  # Clear the form after successful submission
            return redirect('tracking:inward')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'Add_inward_entries.html', {'form': form})
    form = InwardsEntryForm()
    return render(request, 'Add_inward_entries.html', {'form': form})

@AuthenticatedUser(allowed_roles=['Admin', 'ProductionPlanner'])
def Add_program_detail(request):
    if request.method == 'POST':
        form = ProgramDetailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program detail added successfully.')
            form = ProgramDetailForm()  # Clear the form after successful submission
            return redirect('tracking:program')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'Add_program_details.html', {'form': form})
    form = ProgramDetailForm()
    return render(request, 'Add_program_details.html', {'form': form})

@AuthenticatedUser(allowed_roles=['Admin', 'DispatchClerk', 'AccountsClerk'])
def Add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice added successfully.')
            form = InvoiceForm()  # Clear the form after successful submission
            return redirect('tracking:invoices')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'Add_invoices.html', {'form': form})
    form = InvoiceForm()
    return render(request, 'Add_invoices.html', {'form': form})

@AuthenticatedUser(allowed_roles=['Admin', 'Storekeeper'])
def Update_Inwards(request, id):
    table_entry = get_object_or_404(InwardEntry,id=id)
    if request.method == 'POST':
        form = InwardsEntryForm(request.POST, instance=table_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inward entry updated successfully.')
            return redirect('tracking:inwardentry')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'Add_inward_entries.html', {'form': form})
    else:
        form = InwardsEntryForm(instance=table_entry)
    return render(request, 'Add_inward_entries.html', {'form': form})

@AuthenticatedUser(allowed_roles=['Admin', 'ProductionPlanner'])
def Update_program_details(request, id):
    table_entry = get_object_or_404(ProgramDetail,id=id)
    if request.method == 'POST':
        form = ProgramDetailForm(request.POST, instance=table_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program detail updated successfully.')
            return redirect('tracking:programdetailentry')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'Add_program_details.html', {'form': form})
    else:
        form = ProgramDetailForm(instance=table_entry)
    return render(request, 'Add_program_details.html', {'form': form})

@AuthenticatedUser(allowed_roles=['Admin', 'Supervisor', 'MachineOperator'])
def Update_process_logs(request, id):
    table_entry = get_object_or_404(ProcessingLog,id=id)
    if request.method == 'POST':
        form = ProcessingLogForm(request.POST, instance=table_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Processing log updated successfully.')
            return redirect('tracking:processinglogentry')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'Add_process_log.html', {'form': form})
    else:
        form = ProcessingLogForm(instance=table_entry)
    return render(request, 'Add_process_log.html', {'form': form})

@AuthenticatedUser(allowed_roles=['Admin', 'DispatchClerk', 'AccountsClerk'])
def Update_Invoices(request, id):
    table_entry = get_object_or_404(Invoice,id=id)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=table_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice updated successfully.')
            return redirect('tracking:invoiceentry')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'Add_invoices.html', {'form': form})
    else:
        form = InvoiceForm(instance=table_entry)
    return render(request, 'Add_invoices.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('users:user_login')

def custom_403(request, exception=None):
    return render(request, "403.html", status=403)


'''
def test_500(request):
    # This view is only for testing the 500 error page
    raise Exception("Test 500 Error")
'''