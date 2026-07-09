from django.contrib import admin
from .models import (
    Department,
    Employee,
    Author,
    Book,
    Club,
    Student,
    Revenue,
    Wallet,
    ClinicPatient,
    Appointment,
)

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Club)
admin.site.register(Student)
admin.site.register(Revenue)
admin.site.register(Wallet)
admin.site.register(ClinicPatient)
admin.site.register(Appointment)
