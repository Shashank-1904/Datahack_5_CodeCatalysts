from django.db import models


class PDFDocument1(models.Model):
    file = models.FileField(upload_to='pdfs/')
    extracted_text = models.TextField(blank=True)
    
   

