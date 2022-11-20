from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from compost.models import CompostCategory, Composter, Household, ComposterAction
from compost.serializers import HouseholdSerializer, CompostCategorySerializer, ComposterSerializer, \
    ComposterActionSerializer


class HouseholdViewSet(viewsets.ModelViewSet):
    serializer_class = HouseholdSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Household.objects.all()
        return Household.objects.filter(
            user=self.request.user
        )


class CompostCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CompostCategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = CompostCategory.objects.all()


class ComposterViewSet(viewsets.ModelViewSet):
    serializer_class = ComposterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Composter.objects.all()
        user_households = Household.objects.filter(
            user=self.request.user
        )
        return Composter.objects.filter(
            household__in=user_households
        )


class ComposterActionView(generics.CreateAPIView):
    queryset = ComposterAction.objects.all()
    serializer_class = ComposterActionSerializer

