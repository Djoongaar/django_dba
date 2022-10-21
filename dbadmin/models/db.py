from django.db import models

from dbadmin.models.core import Server, Sample


class SampleStatDatabase(models.Model):
    """
    Model for storing differentials between old and new
    sample of database statistics from pg_stat_database
    """
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    datid = models.IntegerField()
    datname = models.CharField(max_length=16)
    xact_commit = models.BigIntegerField(null=True)
    xact_rollback = models.BigIntegerField(null=True)
    blks_read = models.BigIntegerField(null=True)
    blks_hit = models.BigIntegerField(null=True)
    tup_returned = models.BigIntegerField(null=True)
    tup_fetched = models.BigIntegerField(null=True)
    tup_inserted = models.BigIntegerField(null=True)
    tup_updated = models.BigIntegerField(null=True)
    tup_deleted = models.BigIntegerField(null=True)
    conflicts = models.BigIntegerField(null=True)
    temp_files = models.BigIntegerField(null=True)
    temp_bytes = models.BigIntegerField(null=True)
    deadlocks = models.BigIntegerField(null=True)
    blk_read_time = models.FloatField(null=True)
    blk_write_time = models.FloatField(null=True)
    stats_reset = models.DateTimeField(null=True)
    datsize = models.BigIntegerField(null=True)
    datsize_delta = models.BigIntegerField(null=True)
    datistemplate = models.BigIntegerField(null=True)
    session_time = models.FloatField(null=True)
    active_time = models.FloatField(null=True)
    idle_in_transaction_time = models.FloatField(null=True)
    sessions = models.BigIntegerField(null=True)
    sessions_abandoned = models.BigIntegerField(null=True)
    sessions_fatal = models.BigIntegerField(null=True)
    sessions_killed = models.BigIntegerField(null=True)
    checksum_failures = models.BigIntegerField(null=True)
    checksum_last_failure = models.DateTimeField(null=True)

    class Meta:
        db_table = "sample_stat_database"
        unique_together = ("server", "sample", "datid")


class LastStatDatabase(models.Model):
    """ Connection model to View pg_catalog.pg_stat_database """
    datid = models.IntegerField(primary_key=True)
    datname = models.CharField(max_length=16)
    xact_commit = models.BigIntegerField(null=True)
    xact_rollback = models.BigIntegerField(null=True)
    blks_read = models.BigIntegerField(null=True)
    blks_hit = models.BigIntegerField(null=True)
    tup_returned = models.BigIntegerField(null=True)
    tup_fetched = models.BigIntegerField(null=True)
    tup_inserted = models.BigIntegerField(null=True)
    tup_updated = models.BigIntegerField(null=True)
    tup_deleted = models.BigIntegerField(null=True)
    conflicts = models.BigIntegerField(null=True)
    temp_files = models.BigIntegerField(null=True)
    temp_bytes = models.BigIntegerField(null=True)
    deadlocks = models.BigIntegerField(null=True)
    blk_read_time = models.FloatField(null=True)
    blk_write_time = models.FloatField(null=True)
    stats_reset = models.DateTimeField(null=True)
    datsize = models.BigIntegerField(null=True)
    datsize_delta = models.BigIntegerField(null=True)
    datistemplate = models.BigIntegerField(null=True)
    session_time = models.FloatField(null=True)
    active_time = models.FloatField(null=True)
    idle_in_transaction_time = models.FloatField(null=True)
    sessions = models.BigIntegerField(null=True)
    sessions_abandoned = models.BigIntegerField(null=True)
    sessions_fatal = models.BigIntegerField(null=True)
    sessions_killed = models.BigIntegerField(null=True)
    checksum_failures = models.BigIntegerField(null=True)
    checksum_last_failure = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = "last_stat_database"
