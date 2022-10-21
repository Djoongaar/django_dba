from django.db import transaction, connection
from django.http import HttpResponse
from dbadmin.models import Server, Sample, LastStatDatabase, SampleStatDatabase
from rest_framework import status
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

        # New Sample
        new_sample = Sample(sample_id=new_last_sample_id, server=server)
        new_sample.save()

        # Database statistics
        db_name = connection.get_connection_params()['database']
        data_last = LastStatDatabase.objects.get(datname=db_name)
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW last_stat_database;")
        data_cur = LastStatDatabase.objects.get(datname=db_name)
        if data_cur.stats_reset == data_last.stats_reset:
            db_stat = SampleStatDatabase(
                server=server,
                sample=new_sample,
                datid=data_cur.datid,
                datname=data_cur.datname,
                xact_commit=((data_cur.xact_commit or 0) - (data_last.xact_commit or 0)),
                xact_rollback=((data_cur.xact_rollback or 0) - (data_last.xact_rollback or 0)),
                blks_read=((data_cur.blks_read or 0) - (data_last.blks_read or 0)),
                blks_hit=((data_cur.blks_hit or 0) - (data_last.blks_hit or 0)),
                tup_returned=((data_cur.tup_returned or 0) - (data_last.tup_returned or 0)),
                tup_fetched=((data_cur.tup_fetched or 0) - (data_last.tup_fetched or 0)),
                tup_inserted=((data_cur.tup_inserted or 0) - (data_last.tup_inserted or 0)),
                tup_updated=((data_cur.tup_updated or 0) - (data_last.tup_updated or 0)),
                tup_deleted=((data_cur.tup_deleted or 0) - (data_last.tup_deleted or 0)),
                conflicts=((data_cur.conflicts or 0) - (data_last.conflicts or 0)),
                temp_files=((data_cur.temp_files or 0) - (data_last.temp_files or 0)),
                temp_bytes=((data_cur.temp_bytes or 0) - (data_last.temp_bytes or 0)),
                deadlocks=((data_cur.deadlocks or 0) - (data_last.deadlocks or 0)),
                blk_read_time=((data_cur.blk_read_time or 0) - (data_last.blk_read_time or 0)),
                blk_write_time=((data_cur.blk_write_time or 0) - (data_last.blk_write_time or 0)),
                stats_reset=data_cur.stats_reset,
                datsize=data_cur.datsize,
                datsize_delta=((data_cur.datsize or 0) - (data_last.datsize or 0)),
                datistemplate=data_cur.datistemplate,
                session_time=((data_cur.session_time or 0) - (data_last.session_time or 0)),
                active_time=((data_cur.active_time or 0) - (data_last.active_time or 0)),
                idle_in_transaction_time=((data_cur.idle_in_transaction_time or 0) - (data_last.idle_in_transaction_time or 0)),
                sessions=((data_cur.sessions or 0) - (data_last.sessions or 0)),
                sessions_abandoned=((data_cur.sessions_abandoned or 0) - (data_last.sessions_abandoned or 0)),
                sessions_fatal=((data_cur.sessions_fatal or 0) - (data_last.sessions_fatal or 0)),
                sessions_killed=((data_cur.sessions_killed or 0) - (data_last.sessions_killed or 0)),
                checksum_failures=((data_cur.checksum_failures or 0) - (data_last.checksum_failures or 0)),
                checksum_last_failure=data_cur.checksum_last_failure
            )
        else:
            # In case of statistics reset
            db_stat = SampleStatDatabase(
                server=server,
                sample=new_sample,
                datid=data_cur.datid,
                datname=data_cur.datname,
                xact_commit=(data_cur.xact_commit or 0),
                xact_rollback=(data_cur.xact_rollback or 0),
                blks_read=(data_cur.blks_read or 0),
                blks_hit=(data_cur.blks_hit or 0),
                tup_returned=(data_cur.tup_returned or 0),
                tup_fetched=(data_cur.tup_fetched or 0),
                tup_inserted=(data_cur.tup_inserted or 0),
                tup_updated=(data_cur.tup_updated or 0),
                tup_deleted=(data_cur.tup_deleted or 0),
                conflicts=(data_cur.conflicts or 0),
                temp_files=(data_cur.temp_files or 0),
                temp_bytes=(data_cur.temp_bytes or 0),
                deadlocks=(data_cur.deadlocks or 0),
                blk_read_time=(data_cur.blk_read_time or 0),
                blk_write_time=(data_cur.blk_write_time or 0),
                stats_reset=data_cur.stats_reset,
                datsize=data_cur.datsize,
                datsize_delta=((data_cur.datsize or 0) - (data_last.datsize or 0)),
                datistemplate=data_cur.datistemplate,
                session_time=(data_cur.session_time or 0),
                active_time=(data_cur.active_time or 0),
                idle_in_transaction_time=(data_cur.idle_in_transaction_time or 0),
                sessions=(data_cur.sessions or 0),
                sessions_abandoned=(data_cur.sessions_abandoned or 0),
                sessions_fatal=(data_cur.sessions_fatal or 0),
                sessions_killed=(data_cur.sessions_killed or 0),
                checksum_failures=((data_cur.checksum_failures or 0) - (data_last.checksum_failures or 0)),
                checksum_last_failure=data_cur.checksum_last_failure
            )
        db_stat.save()

        # Tablespace statistics

    return Response('OK', status=status.HTTP_200_OK)
