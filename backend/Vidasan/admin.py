from .models import *
from django.contrib import admin
from django.shortcuts import redirect
from django import forms

class SiparisFileInline(admin.TabularInline):
    model = SiparisFile
    extra = 0  # No extra empty fields
    fields = ['title', 'file']  # Fields to display in the inline
    can_delete = True  # This allows the deletion of files in the inline

class SiparisFileUploadForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(), required=False)

    def save_files(self, siparis):
        files = self.files.getlist('files')  # Get the list of uploaded files
        if files:
            for file in files:
                SiparisFile.objects.create(siparis=siparis, file=file)  # Create a new SiparisFile object for each file

class SiparisActivityInline(admin.StackedInline):
    model = SiparisActivity
    extra = 0  # No extra empty fields

class SiparisAdmin(admin.ModelAdmin):
    inlines = [SiparisFileInline, SiparisActivityInline]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        siparis = self.get_object(request, object_id)
        extra_context = extra_context or {}
        extra_context['files'] = siparis.files.all()  # Pass existing files to the template
        upload_form = SiparisFileUploadForm(request.POST or None, request.FILES or None)
        extra_context['upload_form'] = upload_form  # Pass the upload form to the template

        if request.method == 'POST' and upload_form.is_valid() and 'files' in request.FILES:
            upload_form.files = request.FILES  # Set the uploaded files from request.FILES
            upload_form.save_files(siparis)  # Save the uploaded files
            return redirect(request.path_info)  # Redirect to the same page after successful file upload

        return super(SiparisAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def get_inline_instances(self, request, obj=None):
        # Show the inline only when editing an existing `Siparis` (i.e., not during creation)
        if obj is not None:
            return super(SiparisAdmin, self).get_inline_instances(request, obj)
        return []

admin.site.register(Machine)
admin.site.register(Siparis, SiparisAdmin)
admin.site.register(SiparisActivity)
admin.site.register(SiparisFile)
admin.site.register(SiparisLog)
