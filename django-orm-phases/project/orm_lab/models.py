from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=120)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=120, unique=True)


class Book(models.Model):
    title = models.CharField(max_length=160)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")


class Club(models.Model):
    name = models.CharField(max_length=120, unique=True)


class Student(models.Model):
    name = models.CharField(max_length=120, unique=True)
    clubs = models.ManyToManyField(Club, related_name="students")


class Revenue(models.Model):
    category = models.CharField(max_length=80)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Wallet(models.Model):
    owner = models.CharField(max_length=80, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


class ClinicPatient(models.Model):
    name = models.CharField(max_length=120)


class Appointment(models.Model):
    patient = models.ForeignKey(ClinicPatient, on_delete=models.CASCADE, related_name="appointments")
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="scheduled")
