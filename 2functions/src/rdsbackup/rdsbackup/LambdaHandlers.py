import rdsbackup.Commands


def add_database_details_to_backup_queue(event, context):
    rdsbackup.Commands.add_database_details_to_backup_queue_impl("Dev-PayGlobalOnline")


def backup_database_from_queue(event, context):
    rdsbackup.Commands.backup_database_from_queue_impl("Dev-PayGlobalOnline")


def on_database_backup_upload(event, context):
    # rdsbackup.Commands.on_database_backup_upload_impl("Dev-PayGlobalOnline")
    pass