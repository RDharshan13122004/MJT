from .models import *
from users.models import UserProfile
from django import forms

class InwardsEntryForm(forms.ModelForm):
    class Meta:
        model = InwardEntry
        fields = ['sl_no', 
                  'date', 
                  'inward_slip_no', 
                  'yellow_white', 
                  'customer_dc_no', 
                  'wo_no', 
                  'customer_name', 
                  'material_type', 
                  'thickness_mm', 
                  'width_mm', 
                  'length_mm', 
                  'quantity', 
                  'density']
        
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
    

class ProgramDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inward_entry'].label_from_instance = (
            lambda obj: f"{obj.id}"
        )
    class Meta:
        model = ProgramDetail
        fields = ['inward_entry',
                  'prg_no',
                  'prg_date',
                  'planned_qty',
                  'balance_qty',
                  'used_weight_kg',
                  'components_per_sheet',
                  'cut_length_per_sheet',
                  'pierce_per_sheet',
                  'planned_mins_per_sheet']
        
        widgets = {
            "prg_date": forms.DateInput(attrs={"type": "date"}),
        }   
        
class ProcessingLogForm(forms.ModelForm):
    class Meta:
        model = ProcessingLog
        fields = ['program_detail',
                  'processed_date',
                  'shift',
                  'sheets_processed',
                  'cycle_time_per_sheet',
                  'total_cycle_time',
                  'machine',
                  'operator']
        widgets = {
            "processed_date": forms.DateInput(attrs={"type": "date"}),
            "shift": forms.Select(attrs={}, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')]),
        }
        
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['program_detail',
                  'invoice_no',
                  'status',
                  'remarks']
        widgets = {
            "program_detail": forms.Select(attrs={"class": "form-control"}),
            "invoice_no": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),  # NO CHOICES HERE
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }