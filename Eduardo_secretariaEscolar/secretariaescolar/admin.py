from django.contrib import admin
from .models import Guardian, Student, Professor, Contract, Class, Matter, Grade, Falta, Advertencia, Suspensao, Evento
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import path
from django.utils.safestring import mark_safe


class StudentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "registration_number",
        "phone_number",
        "email",
        "adress",
        "cpf",
        "birthday",
        "class_choice",      
    )
    list_display_links = (
        "full_name",
        "email",
        "adress",
    )
    search_fields = (
        "full_name",
        "registration_number",
    )
    list_filter = ("full_name",)


class GuardiansAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "student",
        "phone_number",
        "email",
        "cpf",
        "birthday",
        "adress",
    )
    list_display_links = (
        "full_name",
        "email",
        "adress",
    )
    search_fields = ("full_name",)
    list_filter = ("full_name",)


class ProfessorsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",  # Mostra o usuário vinculado
        "full_name",
        "phone_number",
        "email",
        "cpf",
        "birthday",
        "adress",
        "class_choice",
        "matter_choice",
    )
    list_display_links = (
        "full_name",
        "email",
        "adress",
    )
    search_fields = ("full_name", "user__username", "user__email")  # Permite buscar pelo usuário
    list_filter = ("full_name", "user")  # Filtro por usuário
    autocomplete_fields = ["user"]  # Facilita seleção do usuário
    # Torna o campo user obrigatório no admin
    def save_model(self, request, obj, form, change):
        if not obj.user:
            from django.core.exceptions import ValidationError
            raise ValidationError("O campo Usuário é obrigatório para o Professor.")
        super().save_model(request, obj, form, change)


class ContractsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "guardian",
        "student",
        "download_contract",
    )
    list_display_links = (
        "guardian",
        "student",
    )
    search_fields = (
        "guardian",
        "student",
    )
    readonly_fields = ("gerar_pdf",)
    fieldsets = (
        (None, {
            'fields': ('guardian', 'student', 'gerar_pdf', 'uploaded_pdf')
        }),
    )

    def gerar_pdf(self, obj):
        if obj and obj.pk:
            url = f"/admin/secretariaescolar/contract/{obj.pk}/generate-pdf/"
            return format_html('<a class="button" href="{}" target="_blank">Gerar PDF</a>', url)
        return "Salve o contrato antes de gerar o PDF."
    gerar_pdf.short_description = "Gerar PDF"

    def download_contract(self, obj):
        # Botão para gerar e baixar o PDF do contrato
        return format_html(
            '<a class="button" href="{}">Gerar PDF</a>',
            f"/admin/secretariaescolar/contract/{obj.id}/generate-pdf/",
        )

    download_contract.short_description = "Gerar PDF"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:contract_id>/generate-pdf/",
                self.admin_site.admin_view(self.generate_pdf),
                name="contract-generate-pdf",
            ),
        ]
        return custom_urls + urls

    def generate_pdf(self, request, contract_id):
        try:
            contract = Contract.objects.get(pk=contract_id)
            return contract.generate_contract_pdf()
        except Contract.DoesNotExist:
            self.message_user(request, "Contrato não encontrado.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['gerar_pdf_url'] = f"/admin/secretariaescolar/contract/{object_id}/generate-pdf/"
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def render_change_form(self, request, context, *args, **kwargs):
        if 'gerar_pdf_url' in context:
            context['adminform'].form.fields['uploaded_pdf'].help_text = mark_safe(
                f'<a class="button" href="{context["gerar_pdf_url"]}" target="_blank">Gerar PDF</a>'
            )
        return super().render_change_form(request, context, *args, **kwargs)


class ClassesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "class_choices",
        "itinerary_choices",
    )
    list_display_links = (
        "class_choices",
        "itinerary_choices",
    )
    search_fields = (
        "class_choices",
        "itinerary_choices",
    )
    list_filter = ("itinerary_choices",)

class MattersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "matter_choices",

    )
    list_display_links = (
        "matter_choices",
    )
    search_fields = (
        "matter_choices",
    )
    list_filter = ("matter_choices",)



class GradesAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "classs",
        "matter",
        "grade_presence",
        "grade_activity",
        "grade_evaluative",  # Corrected field name
        "grade_final",
    )
    search_fields = (
        "student__full_name",  # Corrected to reference the related field
        "classs__class_choices",  # Corrected to reference the related field
        "matter__matter_choices",  # Corrected to reference the related field
    )
    list_filter = ("classs", "matter",)  # Corrected field name

class FaltasAdmin(admin.ModelAdmin):
    list_display = ("student", "data", "motivo")
    search_fields = ("student__full_name", "motivo")
    list_filter = ("data",)

class AdvertenciasAdmin(admin.ModelAdmin):
    list_display = ("student", "data", "motivo")
    search_fields = ("student__full_name", "motivo")
    list_filter = ("data",)

class SuspensoesAdmin(admin.ModelAdmin):
    list_display = ("student", "data", "motivo", "dias")
    search_fields = ("student__full_name", "motivo")
    list_filter = ("data",)

class EventosAdmin(admin.ModelAdmin):
    list_display = ("titulo", "data", "tipo", "turma", "professor", "publico_alvo")
    search_fields = ("titulo", "descricao")
    list_filter = ("tipo", "data", "publico_alvo")


admin.site.register(
    Guardian,
    GuardiansAdmin,
)

admin.site.register(
    Student,
    StudentsAdmin,
)

admin.site.register(
    Professor,
    ProfessorsAdmin,
)

admin.site.register(
    Contract,
    ContractsAdmin,
)

admin.site.register(
    Class,
    ClassesAdmin,
)
admin.site.register(
    Matter,
    MattersAdmin,
)
admin.site.register(
    Grade,
    GradesAdmin,
)
admin.site.register(Falta, FaltasAdmin)
admin.site.register(Advertencia, AdvertenciasAdmin)
admin.site.register(Suspensao, SuspensoesAdmin)
admin.site.register(Evento, EventosAdmin)
