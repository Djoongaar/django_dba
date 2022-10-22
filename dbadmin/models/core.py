from django.db import models


class Server(models.Model):
    """
    Basic properties of monitoring database:
        topn:  Number of top objects (statements, relations, etc.), to be reported in each sorted report table.
            Also, this parameter affects size of a sample - the more objects you want to appear in your report,
            the more objects we need to keep in a sample;
        max_sample_age: Retention time of samples in days. Samples, aged _pg_profile.max_sample_age_ days and
            more will be automatically deleted on next _take_sample()_ call;
        track_sample_timings: when this parameter is on, _pg_profile_ will track detailed sample taking timing;
        max_query_length: query length limit for reports. All queries in a report will be truncated to this length.
            This setting does not affect query text collection - during a sample full query texts are collected,
            thus can be obtained;
        frequency: frequency of taking samples.
    """
    server_id = models.PositiveSmallIntegerField(primary_key=True)
    topn = models.PositiveSmallIntegerField(default=20)
    max_sample_age = models.PositiveIntegerField(default=7)
    track_sample_timings = models.BooleanField(default=False)
    max_query_length = models.PositiveIntegerField(default=20_000)
    frequency = models.PositiveIntegerField(default=60*30)
    last_sample_id = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Server, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        db_table = "servers"


class Sample(models.Model):
    """ Taken samples of statistics """
    sample_id = models.PositiveSmallIntegerField(primary_key=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "samples"
        unique_together = ("sample_id", "server")

