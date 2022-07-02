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
    weight = models.FloatField(default=1.0)
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
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grade = models.IntegerField(default=0) # 拳头产品分级，95分以上优秀，85分以上良好，60分以上一般，低于60分不及格

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
            "fist": self.fist,
            "news": [n.to_dict() for n in self.news_set.all().order_by('-time')],
            "id": self.id,
            "graphs": [g.to_dict() for g in self.graph_set.all().order_by('-time')],
            "grade":  self.grade,
            "prize": self.grade * 100 * 2.6,
            "user": self.user.id,
        }

class FistProcedure(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField()
    stage = models.IntegerField(default=0)
    likes = models.IntegerField(default=0) # 多于5票进入下一个阶段
    likers = models.CharField(max_length=255, blank=True)
    meeting_start_time = models.DateTimeField(null=True)
    meeting_end_time = models.DateTimeField(null=True)
    meeting_location = models.CharField(max_length=255, blank=True)
    approved = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    def related_files(self):
        return UserUploadedFile.objects.filter(procedure=self)

    def alter_like(self, user):
        assert isinstance(user, User)
        if self.likers != '':
            likers = [int(i) for i in self.likers.split(',')]
        else:
            likers = []
        flag = None
        if user.id in likers:
            # cancel like
            likers.remove(user.id)
            self.likes -= 1
            flag = False
        else:
            # like
            likers.append(user.id)
            self.likes += 1
            flag = True
        self.likers = ','.join([str(i) for i in likers])
        return flag

    def to_dict(self):
        return {
            "name": self.name,
            "content": self.content,
            "stage": self.stage,
            "files":  [file.to_dict() for file in UserUploadedFile.objects.filter(procedure=self)] if UserUploadedFile.objects.filter(procedure=self) else None,
            "comments": [comment.to_dict() for comment in Comment.objects.filter(procedure=self)] if Comment.objects.filter(procedure=self) else None,
            "likes": self.likes,
            "likers": [User.objects.get(pk=int(i)).name for i in self.likers.split(',')] if self.likers != '' else [],
            "meeting_start_time": str(self.meeting_start_time) if self.meeting_start_time else None,
            "meeting_end_time": str(self.meeting_end_time) if self.meeting_end_time else None,
            "meeting_location": self.meeting_location,
            "approved": self.approved,
            "product": self.product.to_dict(),
            "id": self.id,
            "finished": self.finished,
            "user": self.user.name,
            "userid": self.user.id
        }


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    procedure = models.ForeignKey(FistProcedure, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    # ratings
    profitable = models.FloatField(default=0.0) # 目前的可盈利性，和下面三个一样都是10分制
    future_proof = models.FloatField(default=0.0) # 市场前景
    market = models.FloatField(default=0.0) # 市场化程度
    branding = models.FloatField(default=0.0) # 品牌影响

    def __str__(self):
        return str(self.user) + ": “"+ self.content[:10] + "“"

    def to_dict(self):
        return {
            "user": self.user.name,
            "procedure": self.procedure.name,
            "title": self.title,
            "content": self.content,
            "time": str(self.time),
            "id": self.id,
            "profitable": self.profitable,
            "future_proof": self.future_proof,
            "market": self.market,
            "branding": self.branding
        }

    def grade(self):
        return (self.profitable + self.future_proof + self.market + self.branding) / 4

class UserUploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    procedure =  models.ForeignKey(FistProcedure, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return str(self.user) + str(self.procedure) + self.file.name[:10]

    def to_dict(self):
        return {
            "user": self.user.name,
            "procedure": self.procedure.name,
            "name": self.name,
            "file": self.file.url,
            "id": self.id
        }

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "product": self.product.name,
            "time": str(self.time),
            "author": self.author.name,
            "link": self.link,
            "id": self.id
        }

class Graph(models.Model):
    title = models.CharField(max_length=255)
    xs = models.CharField(max_length=1024) # 和 ys 都是逗号分隔格式
    ys = models.CharField(max_length=1024)
    time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(default=0) # 0: 经营额；1: 合同数；3：外省经营额
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def to_dict(self):
        if self.xs != '':
            xs = [float(i) for i in self.xs.split(',')]
        else:
            xs = []
        if self.ys != '':
            ys = self.ys.split(',')
        else:
            ys = []
        return {
            "title": self.title,
            "xs": xs,
            "ys": ys,
            "time": str(self.time),
            "type": self.type,
            "id": self.id
        }