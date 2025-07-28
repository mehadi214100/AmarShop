from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,password= None,**extra_fields):
        if not email:
            raise ValueError('Email must be needed')
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_admin',True)

        return self.create_user(email,password,**extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique= True,max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150,blank=True)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=150)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated= models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def has_perm(self,perm,obj=None):
        return self.is_superuser

    def has_module_perms(self,app_label):
        return True
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

choices = (
    ('male','Male'),
    ('female','Female'),
    ('others','Others'),
) 
class userProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    city = models.CharField(blank=True,null=True,max_length=150)
    postcode = models.CharField(blank=True,null=True,max_length=150)
    gender = models.CharField(choices=choices,max_length=50,default='male')
    address_line_1 = models.TextField(blank=True,null=True)
    address_line_2 = models.TextField(blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile_picture/')


    def __str__(self):
            return self.user.email

