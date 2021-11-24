from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

import app.models as models
import app.serializers as serializers

class ActiveBandsList(APIView):
    def get(self, request, format=None):
        active_bands = models.Band.active.all()
        serializer = serializers.BandSerializer(active_bands, many = True)
        return Response(serializer.data)
