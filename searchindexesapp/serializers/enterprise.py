from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from searchindexesapp.documents.enterprise import EnterpriseDocument

__all__ = ("EnterpriseDocumentSerializer",)


class EnterpriseDocumentSerializer(serializers.Serializer):
    """Serializer for the Book document."""

    # id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    summary = serializers.CharField(read_only=True)

    created = serializers.DateTimeField(read_only=True)
    # skills = serializers.SerializerMethodField()

    class Meta(object):
        """Meta options."""

        fields = (
            # 'id',
            "name",
            "description",
            "summary",
            # 'skills',
            "sectors",
            "created",
        )
        # read_only_fields = fields

    # def get_skills(self, obj):
    #     """Get tags."""
    #     if obj.skills:
    #         return list(obj.skills)
    #     else:
    #         return []
