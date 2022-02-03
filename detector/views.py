from django.shortcuts import render
from django.shortcuts import redirect
from detector.models import Patients
from detector.models import Report
from oralDetector import settings
from .form import DetailsForm
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "home.html", {})


def details(request):
    if request.method == 'POST':
        form = DetailsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            response = redirect('/OralDetective/detection')
            return response
    else:
        form = DetailsForm()
    return render(request, 'details.html', {'form': form})

def report(request):
    key = Patients.objects.raw(
        'SELECT * FROM detector_patients WHERE id=(SELECT MAX(id) FROM detector_patients)')
    for i in key:
        id = str(i.id)
    key2 = Patients.objects.raw(
        'SELECT * FROM detector_report WHERE report_id='+id)
    return render(request, "report.html", {'data': key,'data2':key2})

def detection (request):
    key = Patients.objects.raw(
        'SELECT * FROM detector_patients WHERE id=(SELECT MAX(id) FROM detector_patients)')
    for y in key:
        image=y.image.url

    path = "D:\canDetec\oralDetector"+image
    diagnosis=cancerDetection(path)
    if (diagnosis == 'Cancer'):
        lesion=lesionType(path)
        saverecord = Report()
        for i in key:
            id = i.id
        saverecord.report_id = id
        saverecord.diagnosis = diagnosis
        saverecord.lesionType = lesion
        saverecord.save()
    else:
        lesion = 'None'
        saverecord = Report()
        for i in key:
            id = i.id
        saverecord.report_id = id
        saverecord.diagnosis = diagnosis
        saverecord.lesionType = lesion
        saverecord.save()
    response = redirect('/OralDetective/report')
    return response

def cancerDetection(path):
    model = load_model('D:\canDetec\oralDetector\models\cancerDetector.hdf5')
    model_labels = {0: 'Cancer', 1: 'Non-Cancer'}
    image = cv2.imread(path)
    image_to_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_detected = cv2.resize(image_to_gray, (48, 48), interpolation=cv2.INTER_AREA)
    if np.sum([image_detected]) != 0.0:
        arry = image_detected.astype("float") / 255.0
        arry = img_to_array(arry)
        arry = np.expand_dims(arry, axis=0)
        preds = model.predict(arry)[0]
        diagnose = model_labels[preds.argmax()]
        return diagnose

def lesionType(path):
    model = load_model('D:\canDetec\oralDetector\models\lesionType.hdf5')
    model_labels = {0: 'Squamous cell carcinoma', 1: 'Varrucous Carcinoma', 2: 'Leukoplakia ', 3: 'Erythroplakia'}
    image = cv2.imread(path)
    image_to_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_detected = cv2.resize(image_to_gray, (48, 48), interpolation=cv2.INTER_AREA)
    if np.sum([image_detected]) != 0.0:
        arry = image_detected.astype("float") / 255.0
        arry = img_to_array(arry)
        arry = np.expand_dims(arry, axis=0)
        preds = model.predict(arry)[0]
        lesion = model_labels[preds.argmax()]
        return lesion