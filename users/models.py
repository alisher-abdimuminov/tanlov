from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


APPLICATION_TYPE = (
    ("waiting", "Ko'rib chiqilmoqda"),
    ("approved", "Qabul qilindi"),
    ("rejected", "Rad etildi"),
)


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Telefon raqami")

    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")

    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Viloyat")
    town = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tuman")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


class Criteria(models.Model):
    name = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def applications(self, user):
        return Application.objects.filter(criteria=self, author=user)


class Application(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    file = models.FileField(upload_to="applications")
    status = models.CharField(max_length=100, choices=APPLICATION_TYPE, default="waiting")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.criteria.name
    