import json
from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from searchindexesapp.documents.sector import SectorDocument


class SectorDocumentSerializer(DocumentSerializer):
    """Serializer for the Book document."""

    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    created = serializers.DateField(read_only=True)

    class Meta(object):
        """Meta options."""

        # Specify the correspondent document class
        document = SectorDocument

        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            "id",
            "name",
            "created",
        )
