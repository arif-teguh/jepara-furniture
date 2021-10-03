from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class ChairModel(Models.models):
#     nama = models.varchar(default = "test")
#     harga = models.BigIntegerField(null = False)
#     tipe = models.varchar()

class FurnitureModels(models.Model):
    nama = models.CharField(max_length=200)
    harga = models.IntegerField(null=False)
    gambar = models.FileField()
    kategori = models.CharField(max_length=30)



class ReviewModels(models.Model):
    futniture = models.ForeignKey(FurnitureModels, on_delete=models.CASCADE)
    user =  models.ForeignKey(User,on_delete=models.CASCADE,
         null=False, blank=False)
    rating = models.IntegerField(null=False)
    notes = models.CharField(max_length=200)


class ChatTopicModels(models.Model):
    user =  models.OneToOneField(User,on_delete=models.CASCADE,
         null=False, blank=False)
    

class ChatContentModels(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,
         null=False, blank=False)
    content = models.CharField(max_length=200)
    topic = models.ForeignKey(ChatTopicModels,on_delete=models.CASCADE,
         null=False, blank=False)