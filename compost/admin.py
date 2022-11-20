from django.contrib import admin

from compost.models import Household, Composter, CompostCategory, CompostAudit


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    pass


@admin.register(Composter)
class ComposterAdmin(admin.ModelAdmin):
    pass


@admin.register(CompostCategory)
class CompostCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(CompostAudit)
class CompostAuditAdmin(admin.ModelAdmin):
    pass
