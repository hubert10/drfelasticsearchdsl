from django.urls import re_path
from enterprisesapp.views import EnterpriseView

urlpatterns = [
    re_path(
        "create/$",
        EnterpriseView.as_view(),
        name="enterprises-create",
    ),
]
