from django.contrib import admin
from geo.models import GeoArea, GeoStyle


# @admin.register(GeoStyle)
class GeoStyleAdmin(admin.ModelAdmin):
    search_fields = ('title', 'file', 'geoarea')
    list_display = ('title', 'file', 'geoarea')
    ordering = ('title', 'file', 'geoarea')
    list_filter = ('geoarea',)


class GeoStyleInline(admin.TabularInline):
    model = GeoStyle
    max_num = 1


# @admin.register(GeoArea)
class GeoAreaAdmin(admin.ModelAdmin):
    inlines = (GeoStyleInline,)
    search_fields = ('__str__', 'file',)
    list_display = ('__str__', 'file',)

    def has_add_permission(self, request, obj=None):
        if GeoArea.objects.count() >= len(GeoArea.GEO_TYPES):
            return False
        return True
