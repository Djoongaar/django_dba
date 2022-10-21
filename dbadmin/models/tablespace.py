from django.db import models
from dbadmin.models import Sample


class Tablespaces(models.Model):
    """ Tablespaces, captured in samples """
    tablespace_id = models.IntegerField(primary_key=True)
    tablespace_name = models.CharField(max_length=16)
    tablespace_path = models.TextField()
    last_sample_id = models.IntegerField(default=0)

    class Meta:
        db_table = "tablespaces_list"


class SampleStatTablespace(models.Model):
    sample_id = models.ForeignKey(Sample, on_delete=models.CASCADE)
    tablespace = models.ForeignKey(Tablespaces, on_delete=models.CASCADE)
    size = models.IntegerField()
    size_delta = models.IntegerField()

    class Meta:
        db_table = "sample_stat_tablespaces"
        unique_together = ('sample_id', 'tablespace')


class LastStatTablespace(models.Model):
    tablespace_id = models.IntegerField(primary_key=True)
    tablespace_name = models.CharField(max_length=16)
    tablespace_path = models.TextField()
    size = models.IntegerField()
    size_delta = models.IntegerField()

    class Meta:
        managed = False
        db_table = "last_stat_tablespaces"
