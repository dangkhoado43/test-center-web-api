from django.contrib import admin
from .models import (TestCategory, Test, Result)


@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at', 'category')
    list_filter = ('category',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'submitted_at')