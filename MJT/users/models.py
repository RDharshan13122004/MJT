from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user_id = models.CharField(max_length=8)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    role = [
        ('Storekeeper', 'Storekeeper'),
        ('ProductionPlanner', 'Production Planner'),
        ('MachineOperator', 'Machine Operator'),
        ('DispatchClerk', 'Dispatch Clerk'),
        ('Admin', 'Admin'),
        ('Supervisor', 'Supervisor'),
        ('AccountsClerk', 'Accounts Clerk'),
    ]
    role = models.CharField(max_length=20, choices=role, null=False)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name
    