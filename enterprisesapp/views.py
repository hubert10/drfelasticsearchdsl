"""
This file provides an APIView classes that are the used for all views in Wutiko opportunitiesapp Application.
These views are basically Generic Views which provided some basic functionality: render a template, redirect, create or edit a model, etc.
"""
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework import generics
from enterprisesapp.models.enterprise import Enterprise
from searchindexesapp.serializers.enterprise import EnterpriseDocumentSerializer


class EnterpriseView(generics.ListAPIView):
    queryset = Enterprise.objects.filter()
    serializer_class = EnterpriseDocumentSerializer

    def list(self, request, *args, **kwargs):

        for i in range(0, 100000):
            Enterprise.objects.create(name="test" + str(i))
        return Response("ok")
