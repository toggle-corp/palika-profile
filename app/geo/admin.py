from django.contrib import admin
from geo.models import (
    GeoArea,
    GeoStyle,
    GeoStyleFile,
    Province,
    District,
    Palika,
)


@admin.register(GeoArea)
class GeoAreaAdmin(admin.ModelAdmin):
    search_fields = ('geo_type', 'file',)
    list_display = ('geo_type', 'file',)
    readonly_fields = ('geo_type',)

    def has_add_permission(self, request, obj=None):
        if GeoArea.objects.count() >= len(GeoArea.GEO_TYPES):
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class GeoStyleFileInline(admin.TabularInline):
    model = GeoStyleFile
    max_num = 2

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GeoStyle)
class GeoStyleAdmin(admin.ModelAdmin):
    inlines = (GeoStyleFileInline,)
    search_fields = ('title', 'style_type',)
    list_display = ('title', 'style_type',)
    ordering = ('title', 'style_type',)
    readonly_fields = ('style_type',)

    def has_add_permission(self, request, obj=None):
        if GeoStyle.objects.count() >= len(GeoStyle.STYLE_TYPES):
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


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
