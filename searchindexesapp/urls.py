from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views.skill import SkillDocumentView
from .views.sector import SectorDocumentView
from .views.enterprise import EnterpriseDocumentViewSet


router = DefaultRouter()

router.register(r"skills", SkillDocumentView, basename="skill_document")

router.register(r"sectors", SectorDocumentView, basename="sector_document")

router.register(
    r"enterprises", EnterpriseDocumentViewSet, basename="enterprise_document"
)


urlpatterns = [
    url(r"^", include(router.urls)),
]
