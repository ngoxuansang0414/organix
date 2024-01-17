from django.core.checks.messages import Error
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, name, phone, email, gender, password=None):
        if not email:
            raise ValueError('Email address is required')

        # Tạo đối tượng user mới
        user = self.model(
            name=name,
            phone=phone,
            email=self.normalize_email(email=email),  # Chuyển email về dạng bình thường
            gender=gender,
            is_active=False,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(
            email=self.normalize_email(email=email),
            name=name,
            password=password,
            phone='',
            gender=Gender.not_specified
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
class Gender(models.TextChoices):
	male = 'Nam'
	female = 'Nữ'
	not_specified = 'Không xác định'

class Account(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=15, choices = Gender.choices, default = Gender.not_specified)
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    # Trường quyêt định khi login
    REQUIRED_FIELDS = ['name']    # Các trường yêu cầu khi đk tài khoản (mặc định đã có email), mặc định có password

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin    # Admin có tất cả quyền trong hệ thống

    def has_module_perms(self, add_label):
        return True
    
class Address(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    specific_address = models.CharField(default="", max_length=200)
    ward = models.CharField(default="", max_length=100)
    district = models.CharField(default="", max_length=100)
    city = models.CharField(default="", max_length=100)

    class Meta:
        verbose_name_plural = 'Address'
