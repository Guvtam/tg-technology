from django.contrib import admin

from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "service",
        "email",
        "created_at",
        "is_contacted",
    )

    list_filter = (
        "service",
        "is_contacted",
        "created_at",
    )

    search_fields = (
        "name",
        "company",
        "email",
        "phone",
        "message",
    )

    list_editable = (
        "is_contacted",
    )

    readonly_fields = (
        "created_at",
    )