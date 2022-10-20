from rest_framework import serializers
from dbadmin.models import LastStatDatabase


class LastStatDatabaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = LastStatDatabase
        fields = '__all__'

