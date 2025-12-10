# define "incident_elimination_analysis" function
def incident_elimination_analysis() -> dict[str, str]: #type: ignore
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
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        incident_dump_handler_folder_path = Path(backend_folder_path) / 'IncidentDumpHandler'
        esoar_analysis_folder_path = Path(incident_dump_handler_folder_path) / 'ESOARAnalysis'
        support_script_folder_path = Path(esoar_analysis_folder_path) / 'SupportScript'
        reference_data_folder_path = Path(support_script_folder_path) / 'ReferenceData'
        connector_down_category_keywords_file_path = Path(reference_data_folder_path) / 'ConnectorDownCategoryKeywords.txt'
        connector_down_keywords_file_path = Path(reference_data_folder_path) / 'ConnectorDownKeywords.txt'
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '7', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Elimination-Analysis', steps = '8', status = 'SUCCESS', message = '"input_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Elimination-Analysis', steps = '8', status = 'ERROR', message = '"input_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '8', 'message' : '"input_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '8', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Elimination-Analysis', steps = '9', status = 'SUCCESS', message = '"processed_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Elimination-Analysis', steps = '9', status = 'ERROR', message = '"processed_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '9', 'message' : '"processed_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '9', 'message' : str(error)}

    # load "ConnectorDownCategoryKeywords.txt" file in script:S10
    try:
        if ((connector_down_category_keywords_file_path.exists()) and (connector_down_category_keywords_file_path.is_file()) and (connector_down_category_keywords_file_path.suffix.lower() == '.txt')):
            with open(connector_down_category_keywords_file_path, 'r', encoding = 'utf-8') as connector_down_category_keywords_file:
                connector_category_keywords = [line.strip().lower() for line in connector_down_category_keywords_file if line.strip()]
                log_writer(script_name = 'Incident-Elimination-Analysis', steps = '10', status = 'SUCCESS', message = '"ConnectorDownCategoryKeywords.txt" File Is Present And Content Loaded Into Script')
        else:
            connector_category_keywords = ['monitoring']
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '10', status = 'ERROR', message = '"ConnectorDownCategoryKeywords.txt" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '10', 'message' : '"ConnectorDownCategoryKeywords.txt" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '10', 'message' : str(error)}

    # load "ConnectorDownKeywords.txt" file in script:S11
    try:
        if ((connector_down_keywords_file_path.exists()) and (connector_down_keywords_file_path.is_file()) and (connector_down_keywords_file_path.suffix.lower() == '.txt')):
            with open(connector_down_keywords_file_path, 'r', encoding = 'utf-8') as connector_down_keywords_file:
                connector_keywords = [line.strip().lower() for line in connector_down_keywords_file if line.strip()]
                log_writer(script_name = 'Incident-Elimination-Analysis', steps = '11', status = 'SUCCESS', message = '"ConnectorDownKeywords.txt" File Is Present And Content Loaded Into Script')
        else:
            connector_keywords = ['node', 'down']
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '11', status = 'ERROR', message = '"ConnectorDownKeywords.txt" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '11', 'message' : '"ConnectorDownKeywords.txt" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '11', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '11', 'message' : str(error)}

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
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '12', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '12', 'message' : str(error)}

    # define "normalized_text" function:S13
    try:
        def normalize_text(value):
            if value is None:
                return ''
            text = str(value).strip()
            if text.upper() == 'N/A':
                return ''
            return text.replace('_', '').replace('-', '').replace('.', '').replace(' ', '').lower()
    except Exception as error:
        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '13', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '13', 'message' : str(error)}

    # define constant
    total_count = 0
    elimination_analysis_rows_limiter = int(str(environment_values.get('ELIMINATION_ANALYSIS_BATCH', '1000')))
    flapping_event_timespan = int(str(environment_values.get('FLAPPING_EVENT_TIMESPAN', '120')))
    periodic_event_timespan = int(str(environment_values.get('PERIODIC_EVENT_TIMESPAN', '1440')))

    # loop through all the data
    while True:
        # define constant
        processed_data_insert_rows = []
        input_data_update_row = []

        # fetch rows for "Elimination Analysis":S14
        try:
            fetch_to_be_process_data_sql = '''
            SELECT
                iid.ticket_number,
                pid.opened_at,
                pid.cmdb_ci,
                pid.state,
                pid.category,
                iid.short_description,
                pid.ticket_mttr_days,
                pid.ticket_mttr_hours,
                pid.ticket_mttr_minutes,
                pid.ticket_mttr_minutes_bucket
            FROM
                input_incident_data AS iid
            JOIN
                processed_incident_data AS pid
                ON iid.ticket_number = pid.ticket_number
            WHERE
                iid.row_status = 7
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (elimination_analysis_rows_limiter,))
                    to_be_processed_data = database_cursor.fetchall()
                    database_column_names = [database_field_name[0] for database_field_name in database_cursor.description]
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '14', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Fetched For Elimination Analysis Process')
                    else:
                        log_writer(script_name = 'Incident-Elimination-Analysis', steps = '14', status = 'INFO', message = f'No New Rows Present For Elimination Analysis Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '14', 'message' : str(error)}

        # convert data into pandas dataframe:S15
        try:
            # define local_time_zone
            local_tz = datetime.now().astimezone().tzinfo
            # define default dates
            default_dates = [
                datetime.min.replace(tzinfo = timezone.utc),
                datetime(1970, 1, 1, tzinfo = timezone.utc)
            ]
            ticket_dataframe = pandas.DataFrame(to_be_processed_data, columns = database_column_names)
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '15', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Pandas Dataframe Created For Processing')
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '15', 'message' : str(error)}

        # generating "Cancelled Ticke" view:S16
        try:
            # normalize "state" column first
            ticket_dataframe['normalized_state'] = ticket_dataframe['state'].apply(normalize_text)
            # create "cancelled_ticket" column using inline regex
            ticket_dataframe['cancelled_ticket'] = ticket_dataframe['normalized_state'].apply(lambda x: 'Yes' if re.search(r'cancel', x, re.IGNORECASE) else 'No')
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '16', status = 'SUCCESS', message = f'Total {int(len(ticket_dataframe))}-Rows Of Data Processed For Cancelled Ticket Analysis')
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '16', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '16', 'message' : str(error)}

        # generate "Connector Down" view:S17
        try:
            # normalized all the fileds
            ticket_dataframe['normalized_category'] = ticket_dataframe['category'].apply(normalize_text)
            ticket_dataframe['normalized_short_description'] = ticket_dataframe['short_description'].apply(normalize_text)

            # compute valid mask
            connector_valid_mask = (
                (ticket_dataframe['normalized_category'] != '') &
                (ticket_dataframe['normalized_short_description'] != '')
            )
            ticket_dataframe['is_connector_valid'] = connector_valid_mask

            # make "connector_down" as "no" for all rows
            ticket_dataframe['connector_down'] = 'No'

            # process valid rows only
            connector_valid_df = ticket_dataframe.loc[connector_valid_mask].copy()

            # check if valid dataframe is not empty
            if (not connector_valid_df.empty):
                # "category" match with the keywords
                category_pattern = '|'.join(map(re.escape, connector_category_keywords))
                category_match_mask = connector_valid_df['normalized_category'].str.contains(category_pattern, case = False, na = False)

                # "shortdescription" match with the keywords
                connector_match_mask = connector_valid_df['normalized_short_description'].apply(lambda text: all(keyword in text for keyword in connector_keywords))
                connector_down_mask = (category_match_mask & connector_match_mask)
                connector_valid_df.loc[connector_down_mask, 'connector_down'] = 'Yes'

                # push results back to main dataframe
                ticket_dataframe.loc[connector_valid_df.index, 'connector_down'] = connector_valid_df['connector_down']
            log_writer(script_name='Incident-Elimination-Analysis', steps='17', status='SUCCESS', message=f'Total {int((~ticket_dataframe["is_connector_valid"]).sum())}-Rows Of Data Skipped For Connector Down Analysis')
            log_writer(script_name='Incident-Elimination-Analysis', steps='17', status='SUCCESS', message=f'Total {int(ticket_dataframe["is_connector_valid"].sum())}-Rows Of Data Processed For Connector Down Analysis')
        except Exception as error:
            log_writer(script_name='Incident-Elimination-Analysis', steps='17', status='ERROR', message=str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-Elimination-Analysis', 'step': '17', 'message': str(error)}

        # generating "Flapping Event" view:S18
        try:
            # normalized all the fileds
            ticket_dataframe['normalized_cmdb_ci'] = ticket_dataframe['cmdb_ci'].apply(normalize_text)
            ticket_dataframe['temp_opened_at'] = ticket_dataframe['opened_at'].apply(lambda x: normalize_datetime(x, local_tz).astimezone(timezone.utc))

            # compute valid mask
            valid_mask = (
                (ticket_dataframe['normalized_cmdb_ci'] != '') &
                (~ticket_dataframe['temp_opened_at'].isin(default_dates))
            )
            ticket_dataframe['is_flapping_valid'] = valid_mask

            # make "flapping_event" as "no" for all rows
            ticket_dataframe['flapping_event'] = 'No'
            # process only valid rows
            valid_df = ticket_dataframe.loc[valid_mask].copy()

            # check if valid dataframe is not empty
            if (not valid_df.empty):
                # sort valid data
                valid_df = valid_df.sort_values(by = ['normalized_cmdb_ci', 'temp_opened_at'], ascending = True) #type: ignore
                # compute "flapping_event_timespan"
                flapping_event_timespan_series = (
                    valid_df
                    .groupby('normalized_cmdb_ci')['temp_opened_at']
                    .diff()
                    .dt.total_seconds() #type: ignore
                    .div(60)
                    .le(flapping_event_timespan)
                    .fillna(False)
                )
                # generating "flapping_event" accordingly
                valid_df = valid_df.assign(flapping_event_timespan = flapping_event_timespan_series)
                valid_df['flapping_event'] = valid_df.apply(
                    lambda row: (
                        'Yes'
                        if (
                            row['flapping_event_timespan']
                            and re.search(r'(resolved|closed)', normalize_text(row['state']), re.IGNORECASE)
                        )
                        else 'No'
                    ),
                    axis = 1
                )
                # push results back to main dataframe
                ticket_dataframe.loc[valid_df.index, 'flapping_event'] = valid_df['flapping_event']
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '18', status = 'SUCCESS', message = f'Total {int((~ticket_dataframe["is_flapping_valid"]).sum())}-Rows Of Data Skipped For Flapping Event Analysis')
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '18', status = 'SUCCESS', message = f'Total {int(ticket_dataframe["is_flapping_valid"].sum())}-Rows Of Data Processed For Flapping Event Analysis')
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '18', status = 'ERROR', message = str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-Elimination-Analysis', 'step': '18', 'message': str(error)}

        # generating "Short Duration Ticket" view:S19
        try:
            # define valid "short-duration-ticket" buckets
            short_duration_ticket_buckets = {'0-5', '5-10'}
            # create "short_duration_ticket" column
            ticket_dataframe['short_duration_ticket'] = ticket_dataframe['ticket_mttr_minutes_bucket'].apply(lambda x: 'Yes' if x in short_duration_ticket_buckets else 'No')
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '19', status = 'SUCCESS', message = f'Total {int(len(ticket_dataframe))}-Rows Of Data Processed For Short Duration Ticket Analysis')
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '19', status = 'ERROR', message = str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-Elimination-Analysis', 'step': '19', 'message': str(error)}

        # generating "Sequence Event" view:S20
        try:
            # normalized all the fields
            ticket_dataframe['normalized_incident_number'] = ticket_dataframe['ticket_number'].apply(normalize_text)

            # compute valid mask
            valid_mask = (
                ~ticket_dataframe['temp_opened_at'].isin(default_dates) &
                (ticket_dataframe['normalized_incident_number'] != '') &
                (ticket_dataframe['normalized_cmdb_ci'] != '') &
                (ticket_dataframe['normalized_short_description'] != '')
            )
            ticket_dataframe['is_sequence_valis'] = valid_mask

            # make "sequence_event" as "no" for all rows
            ticket_dataframe['sequence_event'] = 'No'
            # process valid rows only
            valid_df = ticket_dataframe.loc[valid_mask].copy()

            # check if dataframe is not empty
            if (not valid_df.empty):
                valid_df.sort_values(by = ['normalized_cmdb_ci', 'temp_opened_at'], ascending = True, inplace = True) #type: ignore
                # group all the "ticket_number" with "cmdb_ci", "opened_at" and "short_description" value
                sequence_event_counts_minute = (
                    valid_df
                    .groupby(['normalized_cmdb_ci', 'normalized_short_description', 'temp_opened_at'])['normalized_incident_number']
                    .transform('count')
                )
                # generating "sequence_event" accordingly
                valid_df['sequence_event'] = ['Yes' if x > 1 else 'No' for x in sequence_event_counts_minute]
                # push results back to main dataframe
                ticket_dataframe.loc[valid_df.index, 'sequence_event'] = valid_df['sequence_event']
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '20', status = 'SUCCESS', message = f'Total {int((~ticket_dataframe["is_sequence_valis"]).sum())}-Rows Of Data Skipped For Sequence Event Analysis')
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '20', status = 'SUCCESS', message = f'Total {int(ticket_dataframe["is_sequence_valis"].sum())}-Rows Of Data Processed For Sequence Event Analysis')
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '20', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '20', 'message' : str(error)}

        # generating "Periodic Event" view:S21
        try:
            # compute valid mask only for required fields
            valid_mask = (
                (ticket_dataframe['normalized_cmdb_ci'] != '') &
                (ticket_dataframe['normalized_short_description'] != '')
            )
            ticket_dataframe['is_periodic_valid'] = valid_mask

            # make "periodic_event" as "no" for all rows
            ticket_dataframe['periodic_event'] = 'No'
            # process only valid rows
            valid_df = ticket_dataframe.loc[valid_mask].copy()

            # check if valid dataframe is not empty
            if not valid_df.empty:
                # sort by "opened_at"
                valid_df = valid_df.sort_values(by = 'opened_at', ascending = True) #type: ignore
                # compute time difference in minutes for grouped records
                periodic_event_mask = (
                    valid_df
                    .groupby(['normalized_cmdb_ci', 'normalized_short_description', 'ticket_mttr_days', 'ticket_mttr_hours', 'ticket_mttr_minutes'])['ticket_mttr_minutes']
                    .diff()
                    .div(60)
                    .le(periodic_event_timespan)
                    .fillna(False)
                )
                # generating "periodic_event" accordingly
                valid_df['periodic_event'] = periodic_event_mask.apply(lambda x: 'Yes' if x else 'No')
                # push results back to main dataframe
                ticket_dataframe.loc[valid_df.index, 'periodic_event'] = valid_df['periodic_event']
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '21', status = 'SUCCESS', message = f'Total {int((~ticket_dataframe["is_periodic_valid"]).sum())}-Rows Of Data Skipped For Periodic Event Analysis')
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '21', status = 'SUCCESS', message = f'Total {int(ticket_dataframe["is_periodic_valid"].sum())}-Rows Of Data Processed For Periodic Event Analysis')
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '21', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '21', 'message' : str(error)}

        # re-order column for data insertion:S22
        try:
            ticket_dataframe = ticket_dataframe[['ticket_number', 'cancelled_ticket', 'connector_down', 'flapping_event', 'short_duration_ticket', 'sequence_event', 'periodic_event']]
            for _, row in ticket_dataframe.iterrows():
                total_count += 1
                # appending data into "processed_data_insert_rows"
                processed_data_insert_rows.append((
                    row['ticket_number'],
                    str(row['cancelled_ticket']),
                    str(row['connector_down']),
                    str(row['flapping_event']),
                    str(row['short_duration_ticket']),
                    str(row['sequence_event']),
                    str(row['periodic_event'])
                ))
                # appending data into "input_data_update_row"
                input_data_update_row.append((
                    row['ticket_number'],
                ))
            # deleting pandas dataframe to free memory
            del ticket_dataframe
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '22', status = 'ERROR', message = str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-Elimination-Analysis', 'step': '22', 'message': str(error)}

        # inserting elimination data into "processed_incident_data" table:S23
        try:
            data_upsert_sql_for_processed_incident_data_table_sql = '''
            INSERT INTO processed_incident_data (
                ticket_number,
                cancelled_ticket,
                connector_down,
                flapping_event,
                short_duration_ticket,
                sequence_event,
                periodic_event
            )
            VALUES %s
            ON CONFLICT (ticket_number)
            DO UPDATE SET
                cancelled_ticket        = EXCLUDED.cancelled_ticket,
                connector_down          = EXCLUDED.connector_down,
                flapping_event          = EXCLUDED.flapping_event,
                short_duration_ticket   = EXCLUDED.short_duration_ticket,
                sequence_event          = EXCLUDED.sequence_event,
                periodic_event          = EXCLUDED.periodic_event;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table_sql, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Elimination-Analysis', steps = '23', status = 'SUCCESS', message = f'Total {int(len(processed_data_insert_rows))}-Rows Upserted Into "processed_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '23', status = 'ERROR', message = str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-Elimination-Analysis', 'step': '23', 'message': str(error)}

        # updating "row_status" of "input_incident_data" to "8" after normalized data:S24
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_incident_data AS t
            SET row_status = 8,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(ticket_number)
            WHERE t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_row)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Elimination-Analysis', steps = '24', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "8" Inside "input_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Elimination-Analysis', steps = '24', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '24', 'message' : str(error)}

    # sending return message to main script:S24
    return {'status' : 'SUCCESS', 'file_name' : 'Incident-Elimination-Analysis', 'step' : '24', 'message' : f'Total {total_count}-Rows Of Data Elimination Analysis Completed And Updated Into "input_incident_data" Table'}