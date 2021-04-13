from django.shortcuts import render

from django.http import request, JsonResponse, Http404
from .models import User
from .models import Survey
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer
from .serializer import SurveySerializer

class ListSurvey(APIView):
    def get(self,request):
        obj = Survey.objects.all()
        serializer_obj = SurveySerializer(obj, many=True)
        return Response(serializer_obj.data)

    def post(self,request):
        data = request.data
        serializer_obj = SurveySerializer(data=data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        return Response(serializer_obj.error)


class ListUser(APIView):
    def get(self,request):
        obj = User.objects.all()
        serializer_obj = UserSerializer(obj, many=True)
        return Response(serializer_obj.data)

    def post(self,request):
        data = request.data
        serializer_obj = UserSerializer(data=data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        return Response(serializer_obj.error)
