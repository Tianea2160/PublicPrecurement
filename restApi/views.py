from rest_framework import generics
from .serializers import CorporationSerializer
from .models import Corporation
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .functions import run_data

class CorporationCreate(APIView):
    def get(self, request):
        queryset = Corporation.objects.all()
        serializer = CorporationSerializer(queryset,many=True)
        return Response(serializer.data)

    def post(self, request):
        data = dict(request.data)

        output = run_data(data)
        item = Corporation(data, bidOrNot=output)
        print(item)
        item.save()
        return Response(status=status.HTTP_201_CREATED)

# Class Based View
class CorporationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Corporation.objects.all()
    serializer_class = CorporationSerializer




