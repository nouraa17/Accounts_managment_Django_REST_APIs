import base64
import PIL
import numpy as np
from keras.backend import set_session
from keras.utils import img_to_array, load_img
from .models import Patient
from .serializers import UserSerializer, RegisterSerializer, PatientSerializer
from django.conf import settings
from django.contrib.auth import login
from django.core.files.storage import FileSystemStorage, default_storage
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from ultralytics import YOLO
import cv2
import pandas as pd
import json

# load a custom model
model = YOLO('C:/Users/NOURA/Downloads/best model ever yolov8 seg medium.pt')


fs = FileSystemStorage(location='patients/')
# ui = FileSystemStorage(location='predicted_implants/')


class ImageUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        model = YOLO(
            'C:/Users/NOURA/Downloads/best model ever yolov8 seg medium.pt')
        image_file = request.FILES['image']
        image_data = image_file.read()
        img_np = cv2.imdecode(np.frombuffer(
            image_data, np.uint8), cv2.IMREAD_COLOR)
        results = model.predict(img_np, save=True, conf=0.5, iou=0.7)
        df = pd.DataFrame(results.pandas().xyxy[0])
        response_data = df.to_json(orient='records')
        return Response(response_data)


# class ImageUploadView(APIView):
#     parser_class = (FileUploadParser,)

#     def post(self, request, *args, **kwargs):
#         image_file = request.data['file']
#         file_name = default_storage.save(image_file.name, image_file)
#         file_url = default_storage.path(file_name)
#         image = load_img(file_url)
#         numpy_array = img_to_array(image)
#         image_batch = np.expand_dims(numpy_array, axis=0)
#         processed_image = image_batch.copy()
#         with settings.GRAPH1.as_default():
#             set_session(settings.SESS)
#             predictions = settings.IMAGE_MODEL.predict(
#                 processed_image)
#         # Output/Return data
#         if predictions[0][0] > predictions[0][1] and predictions[0][0] > predictions[0][2]:
#             result = 'ROOT'
#             return Response(result)
#         elif predictions[0][1] > predictions[0][0] and predictions[0][1] > predictions[0][2]:
#             result = 'Straumann'
#             return Response(result)
#         else:
#             result = 'Zimmer'
#             return Response(result)


# ////////////////////////////*****************************///////////////////////////

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# ////////////////////////////*****************************///////////////////////////


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# ////////////////////////////*****************************///////////////////////////


@api_view(['POST'])
def patient_create(request):
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            filename = fs.save(image.name, image)
            serializer.save(image=filename)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ////////////////////////////*****************************///////////////////////////


# @api_view(['GET', 'POST'])
# def patient_List(request):
#     # GET
#     if request.method == 'GET':
#         patients = Patient.objects.all()
#         serializer = PatientSerializer(patients, many=True)
#         return Response(serializer.data)
#     # POST
#     elif request.method == 'POST':
#         serializer = PatientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ////////////////////////////*****************************///////////////////////////

# @api_view(['GET', 'PUT', 'DELETE'])
# def patient_pk(request, pk):
#     try:
#         patient = Patient.objects.get(pk=pk)
#     except Patient.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     # GET
#     if request.method == 'GET':
#         serializer = PatientSerializer(patient)
#         return Response(serializer.data)
#     # PUT
#     elif request.method == 'PUT':
#         serializer = PatientSerializer(patient, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # DELETE
#     if request.method == 'DELETE':
#         patient.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
