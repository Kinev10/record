from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BandSerializer

from .models.band import Band


class ActiveBandsList(APIView):
    def get(self, request, format=None):
        active_bands = Band.active.all()
        serializer = BandSerializer(active_bands, many = True)
        return Response(serializer.data)
