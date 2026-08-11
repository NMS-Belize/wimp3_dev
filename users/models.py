from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone       = models.CharField(max_length=20, blank=True)
    department  = models.ForeignKey("system_core.DepartmentSection", on_delete=models.SET_NULL, blank=True, null=True)
    office_location = models.ForeignKey("system_core.OfficeLocation", on_delete=models.SET_NULL, blank=True, null=True)
    job_title   = models.ForeignKey("system_core.JobTitle", on_delete=models.SET_NULL, blank=True, null=True)
    photo       = models.ImageField(upload_to="images/users/profile", blank=True, null=True)

    def __str__(self):
        return self.user.username

class Employee(models.Model):

    first_name  = models.CharField(max_length=20, blank=True)
    last_name   = models.CharField(max_length=20, blank=True)

    email       = models.CharField(max_length=60, blank=True)
    phone       = models.CharField(max_length=20, blank=True)
    department  = models.ForeignKey("system_core.DepartmentSection", on_delete=models.SET_NULL, blank=True, null=True)
    office_location = models.ForeignKey("system_core.OfficeLocation", on_delete=models.SET_NULL, blank=True, null=True)
    job_title   = models.ForeignKey("system_core.JobTitle", on_delete=models.SET_NULL, blank=True, null=True)

    #photo       = models.ImageField(upload_to="images/users/profile", blank=True, null=True)
    has_user_account = models.BooleanField(default=False)
    #user        = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)
    
    def __str__(self):
        return self.user.first_name