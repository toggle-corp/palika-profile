from django.contrib import admin

from .models import Export, Generator


class ExportInline(admin.TabularInline):
    model = Export
    max_num = 0

    def has_change_permission(self, *args, **kwargs):
        return False


class GeneratorInline(admin.TabularInline):
    model = Generator
    max_num = 0

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(Generator)
class GeneratorAdmin(admin.ModelAdmin):
    change_list_template = 'admin/generator_change_list.html'
    inlines = (ExportInline,)
    search_fields = ('file',)
    list_display = ('__str__', 'file', 'created_at', 'updated_at', 'status',)
    ordering = ('file', 'created_at', 'updated_at',)
    list_filter = ('created_at', 'updated_at', 'status',)
    readonly_fields = ('status',)
    exclude = ('data', 'errors',)


@admin.register(Export)
class ExportAdmin(admin.ModelAdmin):
    search_fields = ('file',)
    list_display = ('title', 'file', 'palika_code', 'language',)
    list_filter = ('language',)
