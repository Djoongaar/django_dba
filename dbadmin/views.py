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

        # Creating a new sample record
        new_sample = Sample(sample_id=new_last_sample_id, server=server)
        new_sample.save()

        # Get data
        db_name = connection.get_connection_params()['database']
        data_old = LastStatDatabase.objects.get(datname=db_name)
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW last_stat_database;")
        data_new = LastStatDatabase.objects.get(datname=db_name)
        if data_new.stats_reset == data_old.stats_reset:
            db_stat = SampleStatDatabase(
                server=server,
                sample=new_sample,
                datid=data_new.datid,
                datname=data_new.datname,
                xact_commit=((data_new.xact_commit or 0) - (data_old.xact_commit or 0)),
                xact_rollback=((data_new.xact_rollback or 0) - (data_old.xact_rollback or 0)),
                blks_read=((data_new.blks_read or 0) - (data_old.blks_read or 0)),
                blks_hit=((data_new.blks_hit or 0) - (data_old.blks_hit or 0)),
                tup_returned=((data_new.tup_returned or 0) - (data_old.tup_returned or 0)),
                tup_fetched=((data_new.tup_fetched or 0) - (data_old.tup_fetched or 0)),
                tup_inserted=((data_new.tup_inserted or 0) - (data_old.tup_inserted or 0)),
                tup_updated=((data_new.tup_updated or 0) - (data_old.tup_updated or 0)),
                tup_deleted=((data_new.tup_deleted or 0) - (data_old.tup_deleted or 0)),
                conflicts=((data_new.conflicts or 0) - (data_old.conflicts or 0)),
                temp_files=((data_new.temp_files or 0) - (data_old.temp_files or 0)),
                temp_bytes=((data_new.temp_bytes or 0) - (data_old.temp_bytes or 0)),
                deadlocks=((data_new.deadlocks or 0) - (data_old.deadlocks or 0)),
                blk_read_time=((data_new.blk_read_time or 0) - (data_old.blk_read_time or 0)),
                blk_write_time=((data_new.blk_write_time or 0) - (data_old.blk_write_time or 0)),
                stats_reset=data_new.stats_reset,
                datsize=data_new.datsize,
                datsize_delta=((data_new.datsize or 0) - (data_old.datsize or 0)),
                datistemplate=data_new.datistemplate,
                session_time=((data_new.session_time or 0) - (data_old.session_time or 0)),
                active_time=((data_new.active_time or 0) - (data_old.active_time or 0)),
                idle_in_transaction_time=((data_new.idle_in_transaction_time or 0) - (data_old.idle_in_transaction_time or 0)),
                sessions=((data_new.sessions or 0) - (data_old.sessions or 0)),
                sessions_abandoned=((data_new.sessions_abandoned or 0) - (data_old.sessions_abandoned or 0)),
                sessions_fatal=((data_new.sessions_fatal or 0) - (data_old.sessions_fatal or 0)),
                sessions_killed=((data_new.sessions_killed or 0) - (data_old.sessions_killed or 0)),
                checksum_failures=((data_new.checksum_failures or 0) - (data_old.checksum_failures or 0)),
                checksum_last_failure=data_new.checksum_last_failure
            )
        else:
            db_stat = SampleStatDatabase(
                server=server,
                sample=new_sample,
                datid=data_new.datid,
                datname=data_new.datname,
                xact_commit=(data_new.xact_commit or 0),
                xact_rollback=(data_new.xact_rollback or 0),
                blks_read=(data_new.blks_read or 0),
                blks_hit=(data_new.blks_hit or 0),
                tup_returned=(data_new.tup_returned or 0),
                tup_fetched=(data_new.tup_fetched or 0),
                tup_inserted=(data_new.tup_inserted or 0),
                tup_updated=(data_new.tup_updated or 0),
                tup_deleted=(data_new.tup_deleted or 0),
                conflicts=(data_new.conflicts or 0),
                temp_files=(data_new.temp_files or 0),
                temp_bytes=(data_new.temp_bytes or 0),
                deadlocks=(data_new.deadlocks or 0),
                blk_read_time=(data_new.blk_read_time or 0),
                blk_write_time=(data_new.blk_write_time or 0),
                stats_reset=data_new.stats_reset,
                datsize=data_new.datsize,
                datsize_delta=((data_new.datsize or 0) - (data_old.datsize or 0)),
                datistemplate=data_new.datistemplate,
                session_time=(data_new.session_time or 0),
                active_time=(data_new.active_time or 0),
                idle_in_transaction_time=(data_new.idle_in_transaction_time or 0),
                sessions=(data_new.sessions or 0),
                sessions_abandoned=(data_new.sessions_abandoned or 0),
                sessions_fatal=(data_new.sessions_fatal or 0),
                sessions_killed=(data_new.sessions_killed or 0),
                checksum_failures=((data_new.checksum_failures or 0) - (data_old.checksum_failures or 0)),
                checksum_last_failure=data_new.checksum_last_failure
            )
        db_stat.save()

    return Response('OK', status=status.HTTP_200_OK)
