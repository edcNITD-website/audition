from django.contrib import admin

from .models import *

from import_export.admin import ImportExportModelAdmin

admin.site.register(Student)
admin.site.register(CQuestion)
admin.site.register(NCQuestion)
admin.site.register(ClubMember)
admin.site.register(MemberFeedback)
admin.site.register(Result)

@admin.register(Response)
class Response(ImportExportModelAdmin):
    pass

# Register your models here.
