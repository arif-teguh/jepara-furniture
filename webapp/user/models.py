from django.db import models

# Create your models here.
# class ChairModel(Models.models):
#     nama = models.varchar(default = "test")
#     harga = models.BigIntegerField(null = False)
#     tipe = models.varchar()

class chairModels(models.Model):
    nama = models.CharField(max_length=200)
    harga = models.IntegerField(null=False)
    gambar = models.FileField()


