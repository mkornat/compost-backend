from django.urls import path
from rest_framework.routers import DefaultRouter

from compost.models import ComposterAction
from compost.views import HouseholdViewSet, CompostCategoryViewSet, ComposterViewSet, ComposterActionView

router = DefaultRouter()
router.register(r"households", HouseholdViewSet, basename="household")
router.register(r"compost_category", CompostCategoryViewSet, basename="compost_category")
router.register(r"composter", ComposterViewSet, basename="composter")

urlpatterns = router.urls + [
    path("composter/action", ComposterActionView.as_view(), name="composter_action"),
]
