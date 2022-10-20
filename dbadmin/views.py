from django.db import transaction, connection
from django.http import HttpResponse
from dbadmin.models import Server, Sample, LastStatDatabase, StatDatabase
from dbadmin.serializers import LastStatDatabaseSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer


def index(request):
    return HttpResponse('Awesome app!')


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def take_sample(request):
    """ Take sample of database statistics """

    with transaction.atomic():

        # Only one running take_sample() function allowed per server! Explicitly lock server in servers table
        server = Server.objects.select_for_update(nowait=True).get(server_id=1)
        new_last_sample_id = server.last_sample_id + 1
        server.last_sample_id = new_last_sample_id
        server.save()

        # Creating a new sample record
        new_sample = Sample(sample_id=new_last_sample_id, server=server)
        new_sample.save()

        # Refreshing Materialized Views
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW last_stat_database")

        # Get data
        db_name = connection.get_connection_params()['database']
        data = LastStatDatabase.objects.get(datname=db_name)
        db_stat = StatDatabase(
            server=server,
            sample=new_sample,
            datid=data.datid,
            datname=data.datname,
            xact_commit=data.xact_commit,
            xact_rollback=data.xact_rollback,
            blks_read=data.blks_read,
            blks_hit=data.blks_hit,
            tup_returned=data.tup_returned,
            tup_fetched=data.tup_fetched,
            tup_inserted=data.tup_inserted,
            tup_updated=data.tup_updated,
            tup_deleted=data.tup_deleted,
            conflicts=data.conflicts,
            temp_files=data.temp_files,
            temp_bytes=data.temp_bytes,
            deadlocks=data.deadlocks,
            blk_read_time=data.blk_read_time,
            blk_write_time=data.blk_write_time,
            stats_reset=data.stats_reset,
            datsize=data.datsize,
            datsize_delta=data.datsize_delta,
            datistemplate=data.datistemplate,
            session_time=data.session_time,
            active_time=data.active_time,
            idle_in_transaction_time=data.idle_in_transaction_time,
            sessions=data.sessions,
            sessions_abandoned=data.sessions_abandoned,
            sessions_fatal=data.sessions_fatal,
            sessions_killed=data.sessions_killed,
            checksum_failures=data.checksum_failures,
            checksum_last_failure=data.checksum_last_failure
        )
        db_stat.save()

    return Response(LastStatDatabaseSerializer(data).data)
