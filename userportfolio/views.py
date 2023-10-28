from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PDFDocument1
from django.http import FileResponse
from django.core.files import File
from wsgiref.util import FileWrapper
import os
import PyPDF2
from PyPDF2 import PdfReader
import spacy
import re

def upload_pdf1(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            # Create a PDFDocument object and save the uploaded file
            pdf_document = PDFDocument1(file=pdf_file)
            pdf_document.save()

            # Extract text from the PDF
            text = ""
            pdf_file = pdf_document.file.path
            pdf_reader = PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            

            text = ' '.join(re.findall(r'\b\w+\b', text))

            print(text)
            # Load the English NLP model from spaCy
            nlp = spacy.load(text)

            # Assuming you have the extracted text stored in a variable named 'text'
            doc = nlp(text)

            # Tokenization
            tokens = [token.text for token in doc]
            # Specialization determination
            specialization = determine_specialization(doc)

            # Keyword extraction
            keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]

            # Save the extracted text in the database
            pdf_document.extracted_text = text
            pdf_document.save()
            print("******************************")
            print(specialization)

            return HttpResponse("Here's the text of the web page.") # Redirect to a success page

    return render(request, 'upload.html')  # Render the upload form
# Add a URL pattern for the view in your urls.py
# You'll also need to create an HTML template for the upload form.


def determine_specialization(doc):
    specialization = "Unknown"  # Default specialization
    try:
       
        # Define a list of keywords or key phrases related to different specializations
        data_science_keywords = ["data science", "machine learning", "data analysis", "AI"]
        web_dev_keywords = ["web development", "full stack", "front-end", "back-end", "web design","react","java","django","nodejs","mysql","mongodb","html","css","javascript","bootstrap","tailwind","figma"]
        software_eng_keywords = ["software engineering", "coding", "programming", "software development","linux"]

        # Check for the presence of keywords in the resume text
        text = doc.text.lower()  # Convert text to lowercase for case-insensitive matching
        if any(keyword in text for keyword in data_science_keywords):
            specialization = "Data Science"
        elif any(keyword in text for keyword in web_dev_keywords):
            specialization = "Web Development"
        elif any(keyword in text for keyword in software_eng_keywords):
            specialization = "Software Engineering"
    except Exception as e:
        print(f"Error processing resume: {str(e)}")
        specialization = "Error"  # Handle the error

    return specialization


