# define "incident_mttr_aging_analysis" function
def incident_mttr_aging_analysis(account_unique_id: str) -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
        from datetime import datetime, timedelta, timezone
        import math
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '7', 'message' : str(error)}

    # check if "input_incident_data" table present inside database:S08
    try:
        input_incident_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'input_incident_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(input_incident_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '8', status = 'SUCCESS', message = '"input_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '8', status = 'ERROR', message = '"input_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '8', 'message' : '"input_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '8', 'message' : str(error)}

    # check if "processed_incident_data" table present inside database:S09
    try:
        processed_incident_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'processed_incident_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(processed_incident_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '9', status = 'SUCCESS', message = '"processed_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '9', status = 'ERROR', message = '"processed_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '9', 'message' : '"processed_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '9', 'message' : str(error)}

    # define "calculate_mttr_excluding_weekends" function:S10
    try:
        def calculate_mttr_excluding_weekends(temp_opened_at, temp_resolved_at):
            if (temp_resolved_at < temp_opened_at):
                return timedelta(0)
            total_seconds = 0
            tzinfo = temp_opened_at.tzinfo  # preserve timezone awareness
            while temp_opened_at < temp_resolved_at:
                # skip weekends directly
                if temp_opened_at.weekday() >= 5:
                    # move to next Monday
                    days_to_monday = 7 - temp_opened_at.weekday()
                    temp_opened_at = datetime(temp_opened_at.year, temp_opened_at.month, temp_opened_at.day, tzinfo = tzinfo) + timedelta(days = days_to_monday)
                    continue
                # end of the current working day
                next_day = datetime(temp_opened_at.year, temp_opened_at.month, temp_opened_at.day, tzinfo=tzinfo) + timedelta(days=1)
                next_point = min(next_day, temp_resolved_at)
                total_seconds += (next_point - temp_opened_at).total_seconds()
                temp_opened_at = next_point
            return timedelta(seconds=total_seconds)
    except Exception as error:
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '10', 'message' : str(error)}

    # define "normalized_datetime" function:S11
    try:
        def normalize_datetime(value, local_tz):
            # if value is not a datetime object -> use default minimum UTC
            if not isinstance(value, datetime):
                return datetime.min.replace(tzinfo = timezone.utc)
            # if tzinfo missing -> attach local timezone
            if value.tzinfo is None:
                return value.replace(tzinfo = local_tz)
            # already valid datetime with timezone
            return value
    except Exception as error:
        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '11', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '11', 'message' : str(error)}

    # define constant
    total_count = 0
    skipped_rows = 0
    mttr_aging_analysis_rows_limiter = int(str(environment_values.get('INCIDENT_MTTR_AGING_ANALYSIS_BATCH')))

    # loop through all the data
    while True:
        # define constant
        processed_data_insert_rows = []
        input_data_update_row = []

        # fetching rows for "MTTR" and "Aging" analysis:S12
        try:
            fetch_to_be_process_data_sql = '''
            SELECT
                pid.account_unique_id,
                pid.ticket_number,
                pid.opened_at,
                pid.resolved_at,
                pid.ticket_mttr_days,
                pid.ticket_mttr_hours,
                pid.ticket_mttr_minutes,
                pid.ticket_mttr_seconds,
                pid.ticket_mttr_minutes_bucket,
                pid.ticket_aging_days,
                pid.ticket_aging_hours,
                pid.ticket_aging_minutes,
                pid.ticket_aging_seconds,
                pid.ticket_aging_minutes_bucket
            FROM
                input_incident_data iid
            JOIN
                processed_incident_data pid
                ON iid.account_unique_id = pid.account_unique_id
                AND iid.ticket_number = pid.ticket_number
            WHERE
                iid.account_unique_id = %s
                AND iid.row_status = 6
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (str(account_unique_id), mttr_aging_analysis_rows_limiter))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '12', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Fetched For Incident-MTTR-Aging-Analysis Process')
                    else:
                        log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '12', status = 'INFO', message = f'For Account: "{account_unique_id}" No New Rows Present For Incident-MTTR-Aging-Analysis Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '12', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '12', 'message' : str(error)}

        # generating "MTTR" and "Aging" view:S13
        try:
            # define local_time_zone
            local_tz = datetime.now().astimezone().tzinfo
            # define column index
            opened_at_index = 2
            resolved_at_index = 3
            ticket_mttr_days_index = 4
            ticket_mttr_hours_index = 5
            ticket_mttr_minutes_index = 6
            ticket_mttr_seconds_index = 7
            ticket_mttr_minutes_bucket_index = 8
            ticket_aging_days_index = 9
            ticket_aging_hours_index = 10
            ticket_aging_minutes_index = 11
            ticket_aging_seconds_index = 12
            ticket_aging_minutes_bucket_index = 13

            # loop through all the rows
            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)

                # define default dates
                default_dates = [
                    datetime.min.replace(tzinfo = timezone.utc),
                    datetime(1970, 1, 1, tzinfo = timezone.utc)
                ]
                # normalize timezone to UTC
                temp_opened_at = normalize_datetime(row_list[opened_at_index], local_tz).astimezone(timezone.utc)
                temp_resolved_at = normalize_datetime(row_list[resolved_at_index], local_tz).astimezone(timezone.utc)

                # check if both "opened_at" and "resolved_at" are not "default_dates"
                if ((temp_opened_at in default_dates) or (temp_resolved_at in default_dates) or (temp_resolved_at < temp_opened_at)):
                    skipped_rows += 1
                    continue
                else:
                    # ==================== "MTTR" Calculation ==================== #
                    # calculate "MTTR" excluding weekends
                    mttr_in_seconds = (calculate_mttr_excluding_weekends(temp_opened_at, temp_resolved_at)).total_seconds()

                    # store all the "MTTR" value
                    row_list[ticket_mttr_days_index] = max(0, (int(math.ceil(mttr_in_seconds / 86400))))
                    row_list[ticket_mttr_hours_index] = max(0, (int(math.ceil(mttr_in_seconds / 3600))))
                    row_list[ticket_mttr_minutes_index] = max(0, (int(math.ceil(mttr_in_seconds / 60))))
                    row_list[ticket_mttr_seconds_index] = max(0, int(mttr_in_seconds))

                    # "MTTR" bucket categorization with minutes
                    if (0 <= int(row_list[ticket_mttr_minutes_index]) <= 5):
                        row_list[ticket_mttr_minutes_bucket_index] = '0-5'
                    elif (5 < int(row_list[ticket_mttr_minutes_index]) <= 10):
                        row_list[ticket_mttr_minutes_bucket_index] = '5-10'
                    elif (10 < int(row_list[ticket_mttr_minutes_index]) <= 20):
                        row_list[ticket_mttr_minutes_bucket_index] = '10-20'
                    elif (20 < int(row_list[ticket_mttr_minutes_index]) <= 30):
                        row_list[ticket_mttr_minutes_bucket_index] = '20-30'
                    else:
                        row_list[ticket_mttr_minutes_bucket_index] = '>30'

                    # ==================== "Aging" Calculation ==================== #
                    # calculate "Ageing" excluding weekends
                    ageing_in_seconds = (temp_resolved_at - temp_opened_at).total_seconds()

                    # store all the "Ageing" value
                    row_list[ticket_aging_days_index] = max(0 , (int(math.ceil(ageing_in_seconds / 86400))))
                    row_list[ticket_aging_hours_index] = max(0, (int(math.ceil(ageing_in_seconds / 3600))))
                    row_list[ticket_aging_minutes_index] = max(0, (int(math.ceil(ageing_in_seconds / 60))))
                    row_list[ticket_aging_seconds_index] = max(0, int(ageing_in_seconds))

                    # "Aging" bucket categorization with minutes
                    if (0 <= int(row_list[ticket_aging_minutes_index]) <= 5):
                        row_list[ticket_aging_minutes_bucket_index] = '0-5'
                    elif (5 < int(row_list[ticket_aging_minutes_index]) <= 10):
                        row_list[ticket_aging_minutes_bucket_index] = '5-10'
                    elif (10 < int(row_list[ticket_aging_minutes_index]) <= 20):
                        row_list[ticket_aging_minutes_bucket_index] = '10-20'
                    elif (20 < int(row_list[ticket_aging_minutes_index]) <= 30):
                        row_list[ticket_aging_minutes_bucket_index] = '20-30'
                    else:
                        row_list[ticket_aging_minutes_bucket_index] = '>30'

                    # replace modified row
                    to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '13', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Of Data "MTTR" And "Aging" Analysis Completed')
        except Exception as error:
            log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '13', status = 'ERROR', message = str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-MTTR-Aging-Analysis', 'step': '13', 'message': str(error)}

        # re-order column for data insertion:S14
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "processed_data_insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0], # account_unique_id
                    data_row[1], # ticket_number
                    data_row[4], # ticket_mttr_days
                    data_row[5], # ticket_mtrr_hours
                    data_row[6], # ticket_mttr_minutes
                    data_row[7], # ticket_mttr_seconds
                    data_row[8], # ticket_mttr_minutes_bucket
                    data_row[9], # ticket_aging_days
                    data_row[10], # ticket_aging_hours
                    data_row[11], # ticket_aging_minutes
                    data_row[12], # ticket_aging_seconds
                    data_row[13] # ticket_aging_minutes_bucket
                ))
                # appending data into "input_data_update_row" empty list
                input_data_update_row.append((
                    data_row[0], # account_unique_id
                    data_row[1] # ticket_number
                ))
        except Exception as error:
            log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '14', 'message' : str(error)}

        # inserting normalize data into "processed_incident_data":S15
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_incident_data (
                account_unique_id,
                ticket_number,
                ticket_mttr_days,
                ticket_mttr_hours,
                ticket_mttr_minutes,
                ticket_mttr_seconds,
                ticket_mttr_minutes_bucket,
                ticket_aging_days,
                ticket_aging_hours,
                ticket_aging_minutes,
                ticket_aging_seconds,
                ticket_aging_minutes_bucket
            )
            VALUES %s
            ON CONFLICT (account_unique_id, ticket_number)
            DO UPDATE SET
                ticket_mttr_days            = EXCLUDED.ticket_mttr_days,
                ticket_mttr_hours           = EXCLUDED.ticket_mttr_hours,
                ticket_mttr_minutes         = EXCLUDED.ticket_mttr_minutes,
                ticket_mttr_seconds         = EXCLUDED.ticket_mttr_seconds,
                ticket_mttr_minutes_bucket  = EXCLUDED.ticket_mttr_minutes_bucket,
                ticket_aging_days           = EXCLUDED.ticket_aging_days,
                ticket_aging_hours          = EXCLUDED.ticket_aging_hours,
                ticket_aging_minutes        = EXCLUDED.ticket_aging_minutes,
                ticket_aging_seconds        = EXCLUDED.ticket_aging_seconds,
                ticket_aging_minutes_bucket = EXCLUDED.ticket_aging_minutes_bucket;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '15', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '15', 'message' : str(error)}

        # updating "row_status" of "input_incident_data" to "7" after normalized data:S16
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_incident_data AS t
            SET row_status = 7,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(account_unique_id, ticket_number)
            WHERE t.account_unique_id = v.account_unique_id
            AND t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_row)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '16', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "7" Inside "input_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '16', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '16', 'message' : str(error)}

    # sending return message to main script:S17
    log_writer(script_name = 'Incident-MTTR-Aging-Analysis', steps = '17', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {skipped_rows}-Rows Of Data MTTR And Aging Analysis Skipped')
    return {'status' : 'SUCCESS', 'file_name' : 'Incident-MTTR-Aging-Analysis', 'step' : '17', 'message' : f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data MTTR And Aging Analysis Completed And Updated Into "input_incident_data" Table'}