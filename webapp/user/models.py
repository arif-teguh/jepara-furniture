from django.db import models
from django.contrib.auth.models import User

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your models here.
# class ChairModel(Models.models):
#     nama = models.varchar(default = "test")
#     harga = models.BigIntegerField(null = False)
#     tipe = models.varchar()

class FurnitureModels(models.Model):
    nama = models.CharField(max_length=200)
    harga = models.IntegerField(null=False)
    gambar = models.FileField(upload_to = 'static/uploaded')
    kategori = models.CharField(max_length=30)
    info = models.TextField()
    stock = models.IntegerField(null=False)


class ShoppingCartModels(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,
         null=False, blank=False) 
    total = models.IntegerField(null=False , default= 0)   
    total_furnitur = models.IntegerField(null=False , default = 0)   





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

class ProfileModels(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,
         null=False, blank=False)
    alamat = models.TextField( null= True)
    gender =  models.CharField(max_length=20 , null= True)
    full_name = models.TextField(null= True)
    phone = models.CharField(max_length=20 , null= True)
    birth_date = models.DateField(auto_now_add=True, blank=True)
    profile_pic = models.FileField(upload_to = 'static/uploaded/profile', null= True , default="static/uploaded/profile/profile.png")

class ComplainModels(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,
         null=False, blank=False)
    alamat = models.TextField()
    nama =  models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    deskripsi =  models.TextField()
    picture = models.FileField(upload_to = 'static/uploaded/complain', null= True)


class PreOrderModels(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,
         null=False, blank=False)
    alamat = models.TextField()
    nama =  models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    jenis_furniture =  models.TextField()
    picture = models.FileField(upload_to = 'static/uploaded/preorder', null= True)

class PaymentModels(models.Model):
     user =  models.ForeignKey(User,on_delete=models.CASCADE,
          null=False, blank=False) 
     total = models.IntegerField(null=False , default= 0)   
     total_furnitur = models.IntegerField(null=False)   
     status = models.CharField(max_length=50)
     alamat =  models.TextField()
     bukti_pembayaran = models.FileField(upload_to = 'static/uploaded/payment', null= False)
     keranjang_deleted_id = models.IntegerField(null=False)
     tanggal_bayar = models.DateTimeField(null=True,auto_now_add= True)
     tanggal_selesai = models.DateTimeField(null=True)



class OrderModels(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,
         null=False, blank=False)
    furnitur = models.ForeignKey(FurnitureModels, on_delete=models.CASCADE)
    jumlah = models.IntegerField(null=False)
    keranjang =  models.ForeignKey(ShoppingCartModels ,on_delete=models.SET_NULL, null= True)  
    total = models.IntegerField(null=False, default= 0)
    keranjang_deleted_id = models.IntegerField(null=True, default= None)