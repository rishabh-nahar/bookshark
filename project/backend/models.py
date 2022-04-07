from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class register_user_manager(BaseUserManager):
    def create_user(self,username,mail,first_name,mid_name,last_name,gender,password=None):
        # if not mail:
        #     raise ValueError("Email required")
        
        if not username:
            raise ValueError("username required")

        user = self.model(
            mail = mail,
            first_name=first_name,
            mid_name=mid_name,
            last_name=last_name,
            gender=gender,
            username = username,
            password = password,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self,username,mail,first_name,mid_name,last_name,gender,password=None):
        user = self.create_user(
            mail = mail,
            first_name=first_name,
            mid_name=mid_name,
            last_name=last_name,
            gender=gender,
            username = username,
            password = password,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using = self._db)
        return user      

class user_details(AbstractBaseUser):
    unique_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30,null=False)
    last_name = models.CharField(max_length=30,null=False)
    gender = models.CharField(max_length=6,null = False)
    
    mail = models.CharField(max_length=50,null = False,unique=True)
    phone = models.BigIntegerField(null = False,default=None)

    username = models.CharField(max_length=30,null=False,unique=True,default=None)
    password = models.CharField(max_length=1000,null=False)

    is_active = models.BooleanField(default = False,null=False)
    is_admin = models.BooleanField(default = False,null=False)
    is_faculty = models.BooleanField(default = False,null=False)
    is_student = models.BooleanField(default = False,null=False)
    is_content_writer = models.BooleanField(default = False,null=False)

    MAIL_FIELD = 'mail'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mail','first_name','mid_name','last_name','gender']
    objects = register_user_manager()

    def __str__(self):
        return self.mail
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perm(self , app_label):
        return True

    class Meta:
        db_table = "users"


class file_upload(models.Model):
    file_type = models.CharField(max_length=6,null=False,default=None)
    file_name = models.CharField(max_length=50,null = False,default=None)
    file_url = models.CharField(max_length=200,default=None)
    category = models.CharField(max_length=40,default=None)
    is_appropriate = models.BooleanField(default=False)

    user_id = models.ForeignKey(user_details,on_delete=models.CASCADE,default=None,verbose_name='user_unique_id')
    class Meta:
        db_table = "file_details"

class listing_books(models.Model):
    book_name = models.CharField(max_length=70,null=False,default=None)
    book_author = models.CharField(max_length=70,null=False,default=None)
    book_publisher = models.CharField(max_length=70,null=False,default=None)
    book_year_edition = models.IntegerField(null=True,default=None)
    book_selling_price = models.CharField(max_length=70,null=False,default=None)
    book_description = models.CharField(max_length=1000,null=False,default=None)
    book_seller = models.ForeignKey(user_details,on_delete=models.CASCADE,default=None,verbose_name='book_seller_id')
    class Meta:
        db_table = "book_details"