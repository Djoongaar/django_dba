from django.db import models

from dbadmin.models import Sample


class SampleStatCluster(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    checkpoints_timed = models.BigIntegerField(null=True)
    checkpoints_req = models.BigIntegerField(null=True)
    checkpoint_write_time = models.FloatField(null=True)
    checkpoint_sync_time = models.FloatField(null=True)
    buffers_checkpoint = models.BigIntegerField(null=True)
    buffers_clean = models.BigIntegerField(null=True)
    maxwritten_clean = models.BigIntegerField(null=True)
    buffers_backend = models.BigIntegerField(null=True)
    buffers_backend_fsync = models.BigIntegerField(null=True)
    buffers_alloc = models.BigIntegerField(null=True)
    stats_reset = models.DateTimeField(null=True)
    wal_size = models.BigIntegerField(null=True)


class LastStatCluster(models.Model):
    server_id = models.BigIntegerField(primary_key=True)
    checkpoints_timed = models.BigIntegerField(null=True)
    checkpoints_req = models.BigIntegerField(null=True)
    checkpoint_write_time = models.FloatField(null=True)
    checkpoint_sync_time = models.FloatField(null=True)
    buffers_checkpoint = models.BigIntegerField(null=True)
    buffers_clean = models.BigIntegerField(null=True)
    maxwritten_clean = models.BigIntegerField(null=True)
    buffers_backend = models.BigIntegerField(null=True)
    buffers_backend_fsync = models.BigIntegerField(null=True)
    buffers_alloc = models.BigIntegerField(null=True)
    stats_reset = models.DateTimeField(null=True)
    wal_size = models.BigIntegerField(null=True)

    class Meta:
        managed = False
        db_table = "last_stat_cluster"

