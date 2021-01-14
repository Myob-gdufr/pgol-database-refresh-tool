from rdsbackup.RdsServer import RdsServer
from rdsbackup.Credentials import Credentials
from rdsbackup import Log
from rdsbackup.Utils import foreach

def update_permissions(domain, credential_creator=Credentials.generate):
    sql_template = \
        """
USE [master]

IF NOT EXISTS(SELECT * FROM sys.syslogins WHERE name = '{domain}\AG PLAT-SQL-Admin') BEGIN
	CREATE LOGIN [{domain}\AG PLAT-SQL-Admin] FROM WINDOWS WITH DEFAULT_LANGUAGE=[us_english]
END

ALTER SERVER ROLE [setupadmin] ADD MEMBER [{domain}\AG PLAT-SQL-Admin]
ALTER SERVER ROLE [processadmin] ADD MEMBER [{domain}\AG PLAT-SQL-Admin]

GRANT 
ADMINISTER BULK OPERATIONS, 
ALTER ANY SERVER AUDIT,
ALTER ANY CREDENTIAL,
ALTER ANY CONNECTION,
ALTER ANY LOGIN, 
ALTER ANY LINKED SERVER, 
ALTER ANY SERVER ROLE, 
ALTER SERVER STATE, 
ALTER TRACE, 
CONNECT SQL, 
CREATE ANY DATABASE, 
VIEW ANY DEFINITION, 
VIEW ANY DATABASE, 
VIEW SERVER STATE 
TO [{domain}\AG PLAT-SQL-Admin]

IF NOT EXISTS(SELECT * FROM sys.syslogins WHERE name = '{domain}\AG PLAT-SQL-RW') BEGIN
	CREATE LOGIN [{domain}\AG PLAT-SQL-RW] FROM WINDOWS WITH DEFAULT_LANGUAGE=[us_english]
END

GRANT 
VIEW ANY DEFINITION, 
VIEW ANY DATABASE, 
VIEW SERVER STATE 
TO [{domain}\AG PLAT-SQL-RW]

IF NOT EXISTS(SELECT * FROM sys.syslogins WHERE name = '{domain}\AG PLAT-SQL-R') BEGIN
	CREATE LOGIN [{domain}\AG PLAT-SQL-R] FROM WINDOWS WITH DEFAULT_LANGUAGE=[us_english]
END

GRANT 
VIEW ANY DEFINITION, 
VIEW ANY DATABASE, 
VIEW SERVER STATE 
TO [{domain}\AG PLAT-SQL-R]

IF NOT EXISTS(SELECT * FROM sys.syslogins WHERE name = '{domain}\AG PLAT-SQL-BACKUP') BEGIN
	CREATE LOGIN [{domain}\AG PLAT-SQL-BACKUP] FROM WINDOWS WITH DEFAULT_LANGUAGE=[us_english]
END

IF NOT EXISTS(SELECT * FROM sys.syslogins WHERE name = '{domain}\AG PLAT-SQL-RESTORE') BEGIN
	CREATE LOGIN [{domain}\AG PLAT-SQL-RESTORE] FROM WINDOWS WITH DEFAULT_LANGUAGE=[us_english]
END

GRANT
CREATE ANY DATABASE
TO [{domain}\AG PLAT-SQL-RESTORE]

USE [msdb]

IF NOT EXISTS(SELECT * FROM sys.database_principals WHERE name = '{domain}\AG PLAT-SQL-Admin') BEGIN
	CREATE USER [{domain}\AG PLAT-SQL-Admin] FOR LOGIN [{domain}\AG PLAT-SQL-Admin] WITH DEFAULT_SCHEMA=[dbo]
END

GRANT ALTER ANY USER TO [{domain}\AG PLAT-SQL-Admin]
ALTER ROLE [SQLAgentUserRole] ADD MEMBER [{domain}\AG PLAT-SQL-Admin]

GRANT EXECUTE ON [dbo].[rds_download_from_s3] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_delete_from_filesystem] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_gather_file_details] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_sqlagent_proxy] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_msbi_task] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_drop_ssrs_databases] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_drop_ssis_database] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_failover_time] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_add_profile_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_update_profile_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_delete_profile_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_upload_to_s3] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_msdtc_transaction_tracing] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_help_profile_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_add_account_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_update_account_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_delete_account_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_purge_jobhistory] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_update_profileaccount_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_delete_profileaccount_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_help_profileaccount_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_add_principalprofile_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_update_principalprofile_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_delete_principalprofile_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_help_principalprofile_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_help_status_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_help_queue_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_help_account_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_add_profileaccount_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_send_dbmail] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_delete_database_backuphistory] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_add_proxy] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_delete_proxy] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_update_proxy] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_grant_login_to_proxy] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_revoke_login_from_proxy] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_enum_proxy_for_subsystem] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sp_enum_login_for_proxy] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_sysmail_delete_mailitems_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_backup_database] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_cancel_task] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_restore_database] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_delete_mailitems_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_restore_log] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_task_status] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_finish_restore] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_shrink_tempdbfile] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[sysmail_delete_log_sp] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_cdc_disable_db] TO [{domain}\AG PLAT-SQL-Admin]
GRANT EXECUTE ON [dbo].[rds_cdc_enable_db] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[rds_fn_get_audit_file] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[sysmail_event_log] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[sysmail_faileditems] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[sysmail_mailattachments] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[rds_fn_task_status] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_progress] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[sysmail_unsentitems] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[sysmail_sentitems] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_input] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[sysmail_allitems] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[rds_fn_sysmail_event_log] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[rds_fn_sysmail_mailattachments] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[rds_fn_sysmail_allitems] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[sysjobhistory] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[sysjobs] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[sysjobactivity] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_querycolumn] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_querytable] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_queryindex] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_column] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_indexcolumn] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_querydatabase] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_index] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_query] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_tableview] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_database] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_table] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_partitionfunction] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_reports_partitionscheme] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_tuninglog] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[rds_fn_list_file_details] TO [{domain}\AG PLAT-SQL-Admin]
GRANT SELECT ON [dbo].[DTA_output] TO [{domain}\AG PLAT-SQL-Admin]

IF NOT EXISTS(SELECT * FROM sys.database_principals WHERE name = '{domain}\AG PLAT-SQL-BACKUP') BEGIN
	CREATE USER [{domain}\AG PLAT-SQL-BACKUP] FOR LOGIN [{domain}\AG PLAT-SQL-BACKUP] WITH DEFAULT_SCHEMA=[dbo]
END

GRANT EXECUTE ON [dbo].[rds_backup_database] TO [{domain}\AG PLAT-SQL-BACKUP]
GRANT EXECUTE ON [dbo].[rds_task_status] TO [{domain}\AG PLAT-SQL-BACKUP]

IF NOT EXISTS(SELECT * FROM sys.database_principals WHERE name = '{domain}\AG PLAT-SQL-RESTORE') BEGIN
	CREATE USER [{domain}\AG PLAT-SQL-RESTORE] FOR LOGIN [{domain}\AG PLAT-SQL-RESTORE] WITH DEFAULT_SCHEMA=[dbo]
END

GRANT EXECUTE ON [dbo].[rds_restore_database] TO [{domain}\AG PLAT-SQL-RESTORE]
GRANT EXECUTE ON [dbo].[rds_task_status] TO [{domain}\AG PLAT-SQL-RESTORE]
GRANT EXECUTE ON [dbo].[sp_delete_database_backuphistory] TO [{domain}\AG PLAT-SQL-RESTORE]

USE [tempdb]

IF NOT EXISTS(SELECT * FROM sys.database_principals WHERE name = '{domain}\AG PLAT-SQL-Admin') BEGIN
	CREATE USER [{domain}\AG PLAT-SQL-Admin] FOR LOGIN [{domain}\AG PLAT-SQL-Admin] WITH DEFAULT_SCHEMA=[dbo]
END

GRANT CONNECT, CONTROL TO [{domain}\AG PLAT-SQL-Admin]

--Not permissions, but server wide configuration
exec rdsadmin..rds_set_configuration 'S3 backup compression', 'true';
        """
    sql_cmd = sql_template.format(domain=domain)
    
    def update_permissions_impl(server):
        try:
            Log.info("The function update_permissions:update_permissions_impl() has been called with message='{m}'", {'m': str(server)})
            credentials = credential_creator("BackupOperator", server) #TODO replace with our own?
            server.connect(credentials)
            try:
                server.execute(sql_cmd)
                server.odbc_connection.commit()

            except Exception as ex:
                Log.warn("SQL Execution Error exception='{ex}'",
                         {'ex': str(ex)})
                raise ex

        except Exception as ex:
            Log.warn("When trying to update permissions, update_permissions_impl caught this exception='{ex}'", {'ex': ex})
            raise ex

    return update_permissions_impl

def lambda_handler(event, context):
    
    stack_name = event['stackName']
    domain = event['domain']
    
    print('Domain: ' + domain)
    print('Stack Name: ' + stack_name)
    tag_filter = RdsServer.tag_filter([
            {'Key': 'aws:cloudformation:stack-name', 'Value': stack_name}
        ])
        
    rds_servers = list(filter(tag_filter, RdsServer.find_instances()))
        
    update_permissions(domain)(rds_servers[0])