from django.db import models
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
	return os.path.join('uploads/categories/', filename)

class Category(models.Model):
	slug = models.CharField(default='', max_length=150, null=False, blank=False)
	name = models.CharField(max_length=50, null=False, blank=False)
	image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
	status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
	created_at = models.DateTimeField(default=timezone.localtime)
	
	class Meta:
		verbose_name_plural = 'Categories'

	def save(self):
		if self.image:
			img = Img.open(io.BytesIO(self.image.read()))
			if img.mode != 'RGB':img = img.convert('RGB')
			img.thumbnail((400,420), Img.Resampling.LANCZOS)  #(width,height)
			output = io.BytesIO()
			img.save(output, format='JPEG')
			output.seek(0)
			self.image= InMemoryUploadedFile(output,'ImageField', "%s.jpg" 
						%self.image.name.split('.')[0], 'image/jpeg', "Content-Type: charset=utf-8", None) # type: ignore
		super(Category, self).save()
		
	def __str__(self):
		return self.name
