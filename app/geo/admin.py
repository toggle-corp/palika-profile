from django.contrib import admin
from geo.models import (
    GeoArea,
    GeoStyle,
    Province,
    District,
    Palika,
)


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


class DistrictInline(admin.TabularInline):
    model = District


class PalikaInline(admin.TabularInline):
    model = Palika


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    inlines = (DistrictInline,)
    search_fields = ('title',)
    list_display = ('title',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    inlines = (PalikaInline,)
    search_fields = ('title',)
    list_display = ('title',)
    list_filter = ('province',)


@admin.register(Palika)
class PalikaAdmin(admin.ModelAdmin):
    search_fields = ('title', 'code',)
    list_display = ('title', 'code',)
    list_filter = ('district',)
