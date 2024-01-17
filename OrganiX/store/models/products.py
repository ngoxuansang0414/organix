from django.db import models
from .categories import Category
import os
from datetime import datetime
from django.utils import timezone

from PIL import Image as Img
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

def get_file_path(request, filename):
	original_filename = filename
	nowTime = datetime.now().strftime("%H:%M, %d-%m-%Y")
	filename = "%s%s%s" % (nowTime,"_", original_filename)
	return os.path.join('uploads/products/', filename)

class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	slug = models.CharField(default='', max_length=150, null=False, blank=False)
	name = models.CharField(max_length=150, null=False, blank=False)
	unit = models.CharField(max_length=30, null=False, blank=False, default='sản phẩm')
	original_price = models.IntegerField(default=0, null=False, blank=False)
	sale_price = models.IntegerField(default=0, null=False, blank=False)
	stock = models.IntegerField(default=0,null=False, blank=False)
	image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
	status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
	
	def save(self):
		if self.image:
			img = Img.open(io.BytesIO(self.image.read()))
			if img.mode != 'RGB':img = img.convert('RGB')
			img.thumbnail((400,420), Img.Resampling.LANCZOS)  #(width,height)
			output = io.BytesIO()
			img.save(output, format='JPEG')
			output.seek(0)
			self.image= InMemoryUploadedFile(output,'ImageField', "%s.jpg" 
						%self.image.name.split('.')[0], 'image/jpeg',"Content-Type: charset=utf-8", None)
		super(Product, self).save()
	
