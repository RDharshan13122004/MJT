from django.db import models


class InwardEntry(models.Model):
    sl_no = models.IntegerField()
    date = models.DateField()
    inward_slip_no = models.CharField(max_length=50)
    yellow_white = models.CharField(max_length=1)
    customer_dc_no = models.CharField(max_length=50)
    wo_no = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    material_type = models.CharField(max_length=50)
    thickness_mm = models.FloatField()
    width_mm = models.FloatField()
    length_mm = models.FloatField()
    quantity = models.IntegerField()
    density = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sl_no}"


class ProgramDetail(models.Model):
    inward_entry = models.ForeignKey(InwardEntry, on_delete=models.CASCADE, related_name='programs')
    prg_no = models.CharField(max_length=50)
    prg_date = models.DateField()
    planned_qty = models.IntegerField()
    balance_qty = models.IntegerField()
    used_weight_kg = models.FloatField()
    components_per_sheet = models.IntegerField()
    cut_length_per_sheet = models.FloatField()
    pierce_per_sheet = models.FloatField()
    planned_mins_per_sheet = models.FloatField()

    def __str__(self):
        return f"{self.prg_no}"


class ProcessingLog(models.Model):
    program_detail = models.ForeignKey(ProgramDetail, on_delete=models.CASCADE, related_name='process_logs')
    processed_date = models.DateField()
    shift = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')])
    sheets_processed = models.IntegerField()
    cycle_time_per_sheet = models.FloatField()
    total_cycle_time = models.FloatField()
    machine = models.CharField(max_length=100)
    operator = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.program_detail.prg_no}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
    ]
    program_detail = models.ForeignKey(ProgramDetail, on_delete=models.CASCADE, related_name='invoices')
    invoice_no = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.invoice_no}"