from django.contrib import admin
from django.db import models
from .models import Careers, Tag, Category, Applicants





class TagInline(admin.TabularInline):
    model = Careers.tags.through

@admin.register(Careers)
class CareersAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'type','created_on')
    list_filter = ("type",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TagInline]
    
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Applicants)

