from rest_framework import serializers

from compost.models import Household, CompostCategory, Composter, ComposterAction


class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = ("uuid", "user", "members_count", "green_land_size")


class CompostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompostCategory
        fields = ("uuid", "name")


class ComposterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composter
        fields = ("uuid", "household", "name", "capacity", "fill_amount", "categories")


class ComposterActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComposterAction
        fields = ("composter", "fill_amount", "category", "action_type")