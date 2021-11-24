from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

import app.models as models
import app.serializers as serializers

class BandViewSet(viewsets.ModelViewSet):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer

    @action(detail=False, url_path="active", methods=["GET"])
    def active_bands(self, request):
        active_bands = models.Band.active.all()
        serializer = self.get_serializer(active_bands, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)