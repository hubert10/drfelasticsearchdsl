from django.contrib import admin
from enterprisesapp.models.enterprise import Enterprise
from enterprisesapp.models.sector import Sector
from enterprisesapp.models.skill import Skill
from enterprisesapp.models.enterprise_saved_search import EnterpriseSavedSearch


class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = [
        "name",
    ]
    list_per_page = 50
    list_filter = [
        "created",
    ]


class SectorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = [
        "name",
    ]
    list_per_page = 50
    list_filter = [
        "created",
    ]


class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = [
        "name",
    ]
    list_per_page = 5000
    list_filter = [
        "created",
    ]


class EnterpriseSavedSearchAdmin(admin.ModelAdmin):
    list_display = ("enterprise_id", "order")
    search_fields = [
        "enterprise_id",
    ]
    list_per_page = 5000
    list_filter = [
        "created",
    ]


admin.site.register(Skill, SkillAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(EnterpriseSavedSearch, EnterpriseSavedSearchAdmin)
