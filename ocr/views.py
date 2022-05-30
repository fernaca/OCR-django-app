import base64

import numpy as np
import pytesseract
from django.contrib import messages
from django.shortcuts import render
from PIL import Image

# you have to install tesseract module too from here - https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Path to tesseract.exe
)


def homepage(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No se seleccionó ninguna imagen."
            )
            return render(request, "home.html")
        lang = request.POST["language"]
        typetext = request.POST["typetext"]
        img = np.array(Image.open(image))

        original_image = Image.open(image)
        text = pytesseract.image_to_string(img , lang=lang)

        if typetext == 'inv':
#        w, h = original_image.size
            img_invoice_to = original_image.crop((50, 144, 262, 232)) #left, top, right, bottom
            img_invoice = original_image.crop((428, 144, 530, 163)) #left, top, right, bottom
            img_invoice_date = original_image.crop((412, 163, 523, 186)) #left, top, right, bottom
            img_table = original_image.crop((44, 320, 606, 464)) #left, top, right, bottom
            # original_image =  original_image.crop((25, 25, 50, 50))

            invoice_to = pytesseract.image_to_string(img_invoice_to , lang=lang)
            invoice_date = pytesseract.image_to_string(img_invoice_date , lang=lang)
            invoice = pytesseract.image_to_string(img_invoice , lang=lang)
            table = pytesseract.image_to_string(img_table , lang=lang)
        else:
            invoice_to = invoice_date = invoice = table = None

        # return text to html
        return render(request, "home.html", {
            "ocr": text, 
            "image": image_base64,
            "invoice_to":invoice_to,
            "invoice":invoice,
            "invoice_date":invoice_date,
            "table":table,
            })

    return render(request, "home.html")
