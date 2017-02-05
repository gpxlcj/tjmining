from django.contrib import admin
from models import GeoMongoDBModel

class GeoMongoDBAdmin(admin.ModelAdmin):
    list_display = ('collection_name', 'db_id')

admin.site.register(GeoMongoDBModel, GeoMongoDBAdmin)