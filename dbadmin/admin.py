from django.contrib import admin

from dbadmin.models import Server


# Register your models here.
@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    fields = (
        "server_id",
        "topn",
        "track_sample_timings",
        "max_query_length",
        "max_sample_age",
    )
