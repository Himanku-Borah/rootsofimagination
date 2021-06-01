from account.account_service import AccountService
from django.contrib import admin
from .models import Academic, Account, Student
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'last_login', 'is_active', 'date_joined')
    list_display_links = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'father_name', 'mailing_address',
                    'dob', 'course', 'created_at', AccountService.linkToForeignKey(column_name="academic"))
    ordering = ('created_at',)


class AcademicAdmin(admin.ModelAdmin):
    list_display = ('x_board', 'x_year', 'x_percentage',
                    'xii_board', 'xii_year', 'xii_percentage', 'student_name')
    def student_name(self, obj):
        return obj.student.name


admin.site.register(Account, AccountAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Academic, AcademicAdmin)
