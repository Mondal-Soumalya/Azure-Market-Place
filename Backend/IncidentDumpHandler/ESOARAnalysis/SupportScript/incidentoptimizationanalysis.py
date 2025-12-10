# define "incident_optimization_analysis" function
def incident_optimization_analysis() -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
        from datetime import datetime, timezone
        import pandas
        import re
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        incident_dump_handler_folder_path = Path(backend_folder_path) / 'IncidentDumpHandler'
        esoar_analysis_folder_path = Path(incident_dump_handler_folder_path) / 'ESOARAnalysis'
        support_script_folder_path = Path(esoar_analysis_folder_path) / 'SupportScript'
        reference_data_folder_path = Path(support_script_folder_path) / 'ReferenceData'
        deduplicate_event_state_keywords_file_path = Path(reference_data_folder_path) / 'DeDuplicateEventStateKeywords.txt'
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '7', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Optimization-Analysis', steps = '8', status = 'SUCCESS', message = '"input_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Optimization-Analysis', steps = '8', status = 'ERROR', message = '"input_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '8', 'message' : '"input_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '8', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Optimization-Analysis', steps = '9', status = 'SUCCESS', message = '"processed_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Optimization-Analysis', steps = '9', status = 'ERROR', message = '"processed_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '9', 'message' : '"processed_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '9', 'message' : str(error)}

    # load "DeDuplicateEventStateKeywords.txt" file in script:S10
    try:
        if ((deduplicate_event_state_keywords_file_path.exists()) and (deduplicate_event_state_keywords_file_path.is_file()) and (deduplicate_event_state_keywords_file_path.suffix.lower() == '.txt')):
            with open(deduplicate_event_state_keywords_file_path, 'r', encoding = 'utf-8') as deduplicate_event_state_keywords_file:
                state_keywords = [line.strip().lower() for line in deduplicate_event_state_keywords_file if line.strip()]
                log_writer(script_name = 'Incident-Optimization-Analysis', steps = '10', status = 'SUCCESS', message = '"DeDuplicateEventStateKeywords.txt" File Is Present And Content Loaded Into Script')
        else:
            state_keywords = ['inprogress', 'onhold', 'new', 'assigned']
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '10', status = 'ERROR', message = '"DeDuplicateEventStateKeywords.txt" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '10', 'message' : '"DeDuplicateEventStateKeywords.txt" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '10', 'message' : str(error)}

    # define "normalized_text" function:S11
    try:
        def normalize_text(value):
            if value is None:
                return ''
            text = str(value).strip()
            if text.upper() == 'N/A':
                return ''
            return text.replace('_', '').replace('-', '').replace('.', '').replace(' ', '').lower()
    except Exception as error:
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '11', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '11', 'message' : str(error)}

    # define "normalized_datetime" function:S12
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
        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '12', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '12', 'message' : str(error)}

    # define constant
    total_count = 0
    optimization_analysis_rows_limiter = int(str(environment_values.get('OPTIMIZATION_ANALYSIS_BATCH', '1000')))
    duplicate_event_timespan = int(str(environment_values.get('DUPLICATE_EVENT_TIMESPAN', '10')))

    # loop through all the data
    while True:
        # define constant
        processed_data_insert_rows = []
        input_data_update_row = []

        # fetch rows for "Optimization Analysis":S13
        try:
            fetch_to_be_process_data_sql = '''
            SELECT
                iid.ticket_number,
                pid.ticket_opened_day,
                pid.ticket_opened_hours,
                pid.ticket_opened_minutes,
                pid.opened_at,
                pid.cmdb_ci,
                pid.state,
                pid.parent_ticket,
                iid.short_description,
                iid.work_notes
            FROM
                input_incident_data AS iid
            JOIN
                processed_incident_data AS pid
                ON iid.ticket_number = pid.ticket_number
            WHERE
                iid.row_status = 9
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (optimization_analysis_rows_limiter,))
                    to_be_processed_data = database_cursor.fetchall()
                    database_column_names = [database_field_name[0] for database_field_name in database_cursor.description]
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '13', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Fetched For Optimization Analysis Process')
                    else:
                        log_writer(script_name = 'Incident-Optimization-Analysis', steps = '13', status = 'INFO', message = f'No New Rows Present For Optimization Analysis Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '13', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '13', 'message' : str(error)}

        # convert data into pandas dataframe:S14
        try:
            # define local_time_zone
            local_tz = datetime.now().astimezone().tzinfo
            # define default dates
            default_dates = [
                datetime.min.replace(tzinfo = timezone.utc),
                datetime(1970, 1, 1, tzinfo = timezone.utc)
            ]
            ticket_dataframe = pandas.DataFrame(to_be_processed_data, columns = database_column_names)
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '14', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Pandas Dataframe Created For Processing')
        except Exception as error:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '14', 'message' : str(error)}

        # generating "Parent Child" view:S15
        try:
            # define regex for "parent incident: INCxxxx"
            parent_child_event_pattern = re.compile(r'parent incident:\s*INC\d+', re.IGNORECASE)
            # combine both conditions
            mask_combined = (
                ticket_dataframe['parent_ticket'].astype(str).str.upper().str.startswith('INC') |
                ticket_dataframe['work_notes'].astype(str).str.contains(parent_child_event_pattern, na = False)
            )
            # generating "parent_child_event" accordingly
            ticket_dataframe['parent_child_event'] = 'No'
            ticket_dataframe['parent_child_event'] = ticket_dataframe['parent_child_event'].mask(mask_combined, 'Yes')
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '15', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Processed For Parent Child Event')
        except Exception as error:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '15', 'message' : str(error)}

        # generating "Duplicate Event" view:S16
        try:
            # normalized all the fields
            ticket_dataframe['temp_opened_at'] = ticket_dataframe['opened_at'].apply(lambda x: normalize_datetime(x, local_tz))
            ticket_dataframe['normalized_cmdb_ci'] = ticket_dataframe['cmdb_ci'].apply(normalize_text)
            ticket_dataframe['normalized_state'] = ticket_dataframe['state'].apply(normalize_text)

            # compute valid mask
            valid_mask = (
                ~ticket_dataframe['temp_opened_at'].isin(default_dates) &
                (ticket_dataframe['normalized_cmdb_ci'] != '')
            )
            ticket_dataframe['is_duplicate_valid'] = valid_mask

            # initialize column
            ticket_dataframe['duplicate_event'] = 'No'
            # process valid rows only
            valid_df = ticket_dataframe.loc[valid_mask].copy()

            # check if dataframe is not empty
            if (not valid_df.empty):
                valid_df.sort_values(by = ['normalized_cmdb_ci', 'temp_opened_at'], ascending = True, inplace = True) #type: ignore
                valid_df['duplicate_event_timespan'] = (
                    valid_df.groupby(['normalized_cmdb_ci'])['temp_opened_at']
                    .diff()
                    .dt.total_seconds() #type: ignore
                    .div(60)
                )
                # generating "duplicate_event" accordingly
                valid_df['duplicate_event'] = valid_df['duplicate_event_timespan'].apply(lambda x: 'Yes' if pandas.notnull(x) and x <= duplicate_event_timespan else 'No')
                # push results back to main dataframe
                ticket_dataframe.loc[valid_df.index, ['duplicate_event']] = valid_df['duplicate_event']
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '16', status = 'SUCCESS', message = f'Total {int((~ticket_dataframe["is_duplicate_valid"]).sum())}-Rows Of Data Skipped For Duplicate Event Analysis')
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '16', status = 'SUCCESS', message = f'Total {int(ticket_dataframe["is_duplicate_valid"].sum())}-Rows Of Data Processed For Duplicate Event Analysis')
        except Exception as error:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '16', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '16', 'message' : str(error)}

        # generating "Deduplicate Event" view:S17
        try:
            # normalized all the fields
            ticket_dataframe['normalized_short_description'] = ticket_dataframe['short_description'].apply(normalize_text)
            ticket_dataframe['normalized_incident_number'] = ticket_dataframe['ticket_number'].apply(normalize_text)
            # compute valid mask
            valid_mask = (
                (ticket_dataframe['normalized_cmdb_ci'] != '') &
                (ticket_dataframe['normalized_short_description'] != '')
            )
            ticket_dataframe['is_deduplicate_valid'] = valid_mask

            # initialize column
            ticket_dataframe['deduplicate_event'] = 'No'
            ticket_dataframe['deduplicate_counts'] = 0
            # process valid rows only
            valid_df = ticket_dataframe.loc[valid_mask].copy()

            if (not valid_df.empty):
                valid_df.sort_values(by=['temp_opened_at'], ascending = True, inplace = True) #type: ignore
                # calculate "duplicate_counts"
                valid_df['deduplicate_counts'] = (
                    valid_df.groupby(['normalized_short_description', 'normalized_cmdb_ci'])['normalized_incident_number']
                    .transform('count')
                )
                # generating "deduplicate_event" accordingly
                valid_df['deduplicate_event'] = valid_df.apply(
                    lambda row: (
                        'Yes'
                        if row['deduplicate_counts'] > 1 and row['normalized_state'] in state_keywords
                        else 'No'
                    ),
                    axis=1
                )
                # push results back to main dataframe
                ticket_dataframe.loc[valid_df.index, ['deduplicate_event']] = valid_df['deduplicate_event']
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '17', status = 'SUCCESS', message = f'Total {int((~ticket_dataframe["is_deduplicate_valid"]).sum())}-Rows Of Data Skipped For Deduplicate Event Analysis')
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '17', status = 'SUCCESS', message = f'Total {int(ticket_dataframe["is_deduplicate_valid"].sum())}-Rows Of Data Processed For Deduplicate Event Analysis')
        except Exception as error:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '17', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '17', 'message' : str(error)}

        # generating "Correlated Event" view:S18
        try:
            # compute valid mask (only normalized_cmdb_ci is required)
            valid_mask = (ticket_dataframe['normalized_cmdb_ci'] != '')
            ticket_dataframe['is_correlated_valid'] = valid_mask

            # initialize default column
            ticket_dataframe['correlated_event'] = 'No'
            # process valid rows only
            valid_df = ticket_dataframe.loc[valid_mask].copy()

            if (not valid_df.empty):
                valid_df.sort_values(by = ['temp_opened_at'], ascending = True, inplace = True) #type: ignore
                correlated_event_counts_minute = (
                    valid_df.groupby(['ticket_opened_day', 'ticket_opened_hours', 'ticket_opened_minutes', 'normalized_short_description'])['normalized_cmdb_ci'].transform('count'))
                # generating "correlated_event" accordingly
                valid_df['correlated_event'] = correlated_event_counts_minute.apply(lambda x: 'Yes' if x > 1 else 'No')
                # push results back to main dataframe
                ticket_dataframe.loc[valid_df.index, 'correlated_event'] = valid_df['correlated_event']
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '18', status = 'SUCCESS', message = f'Total {int((~ticket_dataframe["is_correlated_valid"]).sum())}-Rows Of Data Skipped For Correlated Event Analysis')
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '18', status = 'SUCCESS', message = f'Total {int(ticket_dataframe["is_correlated_valid"].sum())}-Rows Of Data Processed For Correlated Event Analysis')
        except Exception as error:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '18', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '18', 'message' : str(error)}

        # re-order column for data insertion:S19
        try:
            ticket_dataframe = ticket_dataframe[['ticket_number', 'parent_child_event', 'duplicate_event', 'deduplicate_event', 'correlated_event']]
            for _, row in ticket_dataframe.iterrows():
                total_count += 1
                # appending data into "processed_data_insert_rows"
                processed_data_insert_rows.append((
                    row['ticket_number'],
                    str(row['parent_child_event']),
                    str(row['duplicate_event']),
                    str(row['deduplicate_event']),
                    str(row['correlated_event']),
                ))
                # appending data into "input_data_update_row"
                input_data_update_row.append((
                    row['ticket_number'],
                ))
            # deleting pandas dataframe to free memory
            del ticket_dataframe
        except Exception as error:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '19', status = 'ERROR', message = str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-Optimization-Analysis', 'step': '19', 'message': str(error)}

        # inserting elimination data into "processed_incident_data" table:S20
        try:
            data_upsert_sql_for_processed_incident_data_table_sql = '''
            INSERT INTO processed_incident_data (
                ticket_number,
                parent_child_event,
                duplicate_event,
                deduplicate_event,
                correlated_event
            )
            VALUES %s
            ON CONFLICT (ticket_number)
            DO UPDATE SET
                parent_child_event  = EXCLUDED.parent_child_event,
                duplicate_event     = EXCLUDED.duplicate_event,
                deduplicate_event   = EXCLUDED.deduplicate_event,
                correlated_event    = EXCLUDED.correlated_event;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table_sql, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Optimization-Analysis', steps = '20', status = 'SUCCESS', message = f'Total {int(len(processed_data_insert_rows))}-Rows Upserted Into "processed_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '20', status = 'ERROR', message = str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-Optimization-Analysis', 'step': '20', 'message': str(error)}

        # updating "row_status" of "input_incident_data" to "10" after normalized data:S21
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_incident_data AS t
            SET row_status = 10,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(ticket_number)
            WHERE t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_row)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Optimization-Analysis', steps = '21', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "10" Inside "input_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Optimization-Analysis', steps = '21', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '21', 'message' : str(error)}

    # sending return message to main script:S21
    return {'status' : 'SUCCESS', 'file_name' : 'Incident-Optimization-Analysis', 'step' : '21', 'message' : f'Total {total_count}-Rows Of Data Optimization Analysis Completed And Updated Into "input_incident_data" Table'}