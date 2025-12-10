# define "incident_output_data_fill" function
def incident_output_data_fill() -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-Output-Data-Fill', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-Output-Data-Fill', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '7', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Output-Data-Fill', steps = '8', status = 'SUCCESS', message = '"input_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Output-Data-Fill', steps = '8', status = 'ERROR', message = '"input_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '8', 'message' : '"input_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '8', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Output-Data-Fill', steps = '9', status = 'SUCCESS', message = '"processed_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Output-Data-Fill', steps = '9', status = 'ERROR', message = '"processed_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '9', 'message' : '"processed_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '9', 'message' : str(error)}

    # define constant
    total_count = 0
    output_data_fill_rows_limiter = int(str(environment_values.get('OUTPUT_DATA_FILL_BATCH', '1000')))

    # loop through all the available data
    while True:
        # define empty list
        processed_data_insert_rows = []
        input_data_update_rows = []

        # fetching rows for data fill:S10
        try:
            fetch_to_be_process_data_sql = '''
            SELECT "ticket_number", "ticket_type", "opened_at", "resolved_at"
            FROM input_incident_data
            WHERE "row_status" = 1
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (output_data_fill_rows_limiter,))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '10', status = 'SUCCESS', message = f'Total {len(to_be_processed_data)}-Rows Fetched For Output Table Fill Process')
                    else:
                        log_writer(script_name = 'Incident-Output-Data-Fill', steps = '10', status = 'INFO', message = f'No New Rows Present For Output Table Fill Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Incident-Output-Data-Fill', steps = '10', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '10', 'message' : str(error)}

        # re-order column for data insertion:S11
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "processed_data_insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0], # ticket_number
                    str(data_row[1]), # ticket_type
                    data_row[2], # opened_at
                    data_row[3] # resolved_at
                ))
                # input_data_update_rows will hold single-column tuples (ticket_number,)
                input_data_update_rows.append((data_row[0],))
        except Exception as error:
            log_writer(script_name = 'Incident-Output-Data-Fill', steps = '11', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '11', 'message' : str(error)}

        # inserting data into "processed_incident_data":S12
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_incident_data (
                ticket_number,
                ticket_type,
                opened_at,
                resolved_at
            )
            VALUES %s
            ON CONFLICT (ticket_number)
            DO UPDATE SET
                ticket_type     = EXCLUDED.ticket_type,
                opened_at       = EXCLUDED.opened_at,
                resolved_at     = EXCLUDED.resolved_at;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Output-Data-Fill', steps = '12', status = 'SUCCESS', message = f'Total {int(len(processed_data_insert_rows))}-Rows Upserted Into "processed_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Output-Data-Fill', steps = '12', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '12', 'message' : str(error)}

        # updating "row_status" of "input_incident_data" to "2" after output data fill process:S13
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_incident_data AS t
            SET row_status = 2,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(ticket_number)
            WHERE t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Output-Data-Fill', steps = '13', status = 'SUCCESS', message = f'Total {int(len(processed_data_insert_rows))}-Rows Updated "row_status" To "2" Inside "input_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Output-Data-Fill', steps = '13', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '13', 'message' : str(error)}

    # sending return message to main script:S14
    log_writer(script_name = 'Incident-Output-Data-Fill', steps = '14', status = 'SUCCESS', message = f'Total {total_count}-Rows Of Output Data Filled And Updated Into "input_incident_data" Table')
    return {'status' : 'SUCCESS', 'file_name' : 'Incident-Output-Data-Fill', 'step' : '14', 'message' : f'Total {total_count}-Rows Of Output Data Filled And Updated Into "input_incident_data" Table'}