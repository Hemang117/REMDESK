import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import RoleCategory, Service, Testimonial, TeamMember, Lead, CandidateApplication, ContactMessage

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}.csv'
    writer = csv.writer(response)
    
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Header
    writer.writerow([field.verbose_name for field in fields])
    # Data
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export selected to CSV'

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'name', 'email', 'budget_range', 'timeline', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at', 'budget_range')
    search_fields = ('company_name', 'name', 'email')
    actions = [export_to_csv]

@admin.register(CandidateApplication)
class CandidateApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'primary_skill', 'experience_years', 'created_at')
    list_filter = ('experience_years', 'created_at')
    search_fields = ('full_name', 'email', 'primary_skill')
    actions = [export_to_csv]

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)

admin.site.register(RoleCategory)
admin.site.register(Service)
admin.site.register(Testimonial)
admin.site.register(ContactMessage)
