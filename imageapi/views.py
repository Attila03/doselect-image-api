import os
import base64

from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from .serializers import ImagePostSerializer, ImagePatchSerializer


# def file_exists(filename, username):
#     '''Check if a particular file exists for a given user'''
#     file_path = os.path.join(settings.MEDIA_ROOT, username, filename)
#     return os.path.isfile(file_path)


class ImageListView(APIView):

    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = ImagePostSerializer(data=request.data, context={'request': request})
        username = request.user.username
        if serializer.is_valid():
            image = serializer.validated_data['image']
            image_path = os.path.join(settings.MEDIA_ROOT, username, image.name)
            default_storage.save(image_path, ContentFile(image.read()))
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        username = request.user.username
        images = {}
        protocol = 'https://' if request.is_secure() else 'http://'
        for image_name in os.listdir(os.path.join(settings.MEDIA_ROOT, username)):
            image_url = protocol + request.get_host() + settings.MEDIA_URL + username + '/' + image_name
            images[image_name] = image_url
        return Response(images, status=status.HTTP_200_OK)


class ImageDetailView(APIView):

    permission_classes = ()

    def get(self, request, *args, **kwargs):
        username = request.user.username
        image_name = kwargs['name']
        image_path = os.path.join(settings.MEDIA_ROOT, username, image_name)
        if os.path.isfile(image_path):
            with open(image_path, 'rb') as image:
                encoded_image = base64.b64encode(image.read())
            response_content = {'image': encoded_image}
            return Response(response_content, status=status.HTTP_200_OK)
        return Response({
            "error": "No Image named {} exists. Make sure the extension is also correct.".format(image_name)
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        username = request.user.username
        image_name = kwargs['name']
        image_path = os.path.join(settings.MEDIA_ROOT, username, image_name)
        if os.path.isfile(image_path):
            default_storage.delete(image_path)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            "error": "No image named {} exists. Make sure the extension is also correct".format(image_name)
        }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        serializer = ImagePatchSerializer(data=request.data, context={'request': request})
        username = request.user.username
        if serializer.is_valid():
            image = serializer.validated_data['image']
            image_path = os.path.join(settings.MEDIA_ROOT, username, image.name)
            if os.path.isfile(image_path):
                default_storage.delete(image_path)
                default_storage.save(image_path, ContentFile(image.read()))
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                "error": "Image {} doesn't exist.Use POST request if you want to upload a new image.".format(image.name)
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




