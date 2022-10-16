from django.db import models


class Server(models.Model):
    """ Basic properties of monitoring database """
    server_id = models.PositiveIntegerField(primary_key=True)
    max_sample_age = models.PositiveIntegerField(null=True, verbose_name='')
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
    sample_id = models.PositiveIntegerField(primary_key=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "samples"

