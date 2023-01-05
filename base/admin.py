from django.contrib import admin

from .models import Student, CQuestion, NCQuestion , Response

from import_export.admin import ImportExportModelAdmin

admin.site.register(Student)
admin.site.register(CQuestion)
admin.site.register(NCQuestion)

@admin.register(Response)
class Response(ImportExportModelAdmin):
    pass

# Register your models here.
