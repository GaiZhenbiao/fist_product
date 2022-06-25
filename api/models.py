from django.db import models
from django.dispatch import receiver
import hashlib
import random
import string
import pyotp

# Create your models here.

# hash the input string with sha256
def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

# generate random string with length of n
def random_string(n):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

class User(models.Model):
    name = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    two_auth = models.CharField(max_length=32, blank=True)
    token = models.CharField(max_length=255, blank=True)
    is_admin = models.BooleanField(default=False)

    def get_token(self, passwd, two_auth_code):
        # compare self.passwd with the hashed passwd
        if hash_string(passwd) == self.passwd and pyotp.TOTP(self.two_auth).now() == two_auth_code:
            return self.token
        else:
            return None

    def __str__(self):
        return self.name

@receiver(models.signals.post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        instance.passwd = hash_string(instance.passwd) # save passwords securely
        instance.two_auth = pyotp.random_base32()
        instance.token = random_string(255)
        instance.save()
    else:
        pass

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.CharField(max_length=255)
    stock = models.IntegerField()
    sold = models.IntegerField()
    fist = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image": self.image.url if self.image else None,
            "category": self.category,
            "stock": self.stock,
            "sold": self.sold,
            "fist": self.fist
        }

class FistProcedure(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField()
    stage = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    metting_time = models.DateTimeField(null=True)
    approved = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    def related_files(self):
        return UserUploadedFile.objects.filter(procedure=self)

    def to_dict(self):
        return {
            "name": self.name,
            "content": self.content,
            "stage": self.stage,
            "files":  [file.to_dict() for file in UserUploadedFile.objects.filter(procedure=self)] if UserUploadedFile.objects.filter(procedure=self) else None,
            "comments": [comment.to_dict() for comment in Comment.objects.filter(procedure=self)] if Comment.objects.filter(procedure=self) else None,
            "likes": self.likes,
            "metting_time": str(self.metting_time) if self.metting_time else None,
            "approved": self.approved,
            "product": self.product.to_dict()
        }


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    procedure = models.ForeignKey(FistProcedure, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    agree = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ": “"+ self.content[:10] + "“"

    def to_dict(self):
        return {
            "user": self.user.name,
            "procedure": self.procedure.name,
            "title": self.title,
            "content": self.content,
            "time": str(self.time)
        }

class UserUploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    procedure =  models.ForeignKey(FistProcedure, on_delete=models.DO_NOTHING)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return str(self.user) + str(self.procedure) + self.file.name[:10]

    def to_dict(self):
        return {
            "user": self.user.name,
            "procedure": self.procedure.name,
            "file": self.file.url
        }