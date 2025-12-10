# define "incident_standardization_analysis" function
def incident_standardization_analysis() -> dict[str, str]: #type: ignore
    # importing python module:S1
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S2
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S3
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S4
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        incident_dump_handler_folder_path = Path(backend_folder_path) / 'IncidentDumpHandler'
        esoar_analysis_folder_path = Path(incident_dump_handler_folder_path) / 'ESOARAnalysis'
        support_script_folder_path = Path(esoar_analysis_folder_path) / 'SupportScript'
        reference_data_folder_path = Path(support_script_folder_path) / 'ReferenceData'
        blank_ci_keywords_file_path = Path(reference_data_folder_path) / 'BlankCIKeywords.txt'
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S5
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-Standardization-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-Standardization-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S6
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S7
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '7', 'message' : str(error)}

    # check if "input_incident_data" table present inside database:S8
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
                    log_writer(script_name = 'Incident-Standardization-Analysis', steps = '8', status = 'SUCCESS', message = '"input_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Standardization-Analysis', steps = '8', status = 'ERROR', message = '"input_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '8', 'message' : '"input_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '8', 'message' : str(error)}

    # check if "processed_incident_data" table present inside database:S9
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
                    log_writer(script_name = 'Incident-Standardization-Analysis', steps = '9', status = 'SUCCESS', message = '"processed_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Standardization-Analysis', steps = '9', status = 'ERROR', message = '"processed_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '9', 'message' : '"processed_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '9', 'message' : str(error)}

    # load "BlankCIKeywords.txt" file in script:S10
    try:
        if ((blank_ci_keywords_file_path.exists()) and (blank_ci_keywords_file_path.is_file()) and (blank_ci_keywords_file_path.suffix.lower() == '.txt')):
            with open(blank_ci_keywords_file_path, 'r', encoding = 'utf-8') as blank_ci_keywords_file:
                blank_ci_keywords = [line.strip().lower() for line in blank_ci_keywords_file if line.strip()]
                log_writer(script_name = 'Incident-Standardization-Analysis', steps = '10', status = 'SUCCESS', message = '"BlankCIKeywords.txt" File Is Present And Content Loaded Into Script')
        else:
            blank_ci_keywords = ['nocifound', 'splunkdefaultci']
            log_writer(script_name = 'Incident-Standardization-Analysis', steps = '10', status = 'ERROR', message = '"BlankCIKeywords.txt" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '10', 'message' : '"BlankCIKeywords.txt" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '10', 'message' : str(error)}

    # define constant
    total_count = 0
    standardization_analysis_rows_limiter = int(str(environment_values.get('STANDARDIZATION_ANALYSIS_BATCH', '1000')))

    # loop through all the data
    while True:
        # define constant
        processed_data_insert_rows = []
        input_data_update_row = []

        # fetch rows for "blank_ci" analysis:S11
        try:
            fetch_to_be_process_data_sql = '''
            SELECT
                iid.ticket_number,
                pid.cmdb_ci,
                pid.blank_ci
            FROM
                input_incident_data iid
            JOIN
                processed_incident_data pid
                ON iid.ticket_number = pid.ticket_number
            WHERE
                iid.row_status = 8
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (standardization_analysis_rows_limiter,))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '11', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Fetched For Standardization Analysis Process')
                    else:
                        log_writer(script_name = 'Incident-Standardization-Analysis', steps = '11', status = 'INFO', message = f'No New Rows Present For Standardization Analysis Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Incident-Standardization-Analysis', steps = '11', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '11', 'message' : str(error)}

        # generating "blank_ci" view:S12
        try:
            # define column index
            cmdb_ci_index = 1
            blank_ci_index = 2

            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)

                # normalize for keyword comparison
                normalized_ci = (str(row_list[cmdb_ci_index]).strip().lower().replace(' ', '').replace('.', '').replace('-', '').replace('_', ''))

                # check for "N/A" or keywords
                if ((str(row_list[cmdb_ci_index]).strip().upper() == 'N/A') or (normalized_ci in blank_ci_keywords)):
                    row_list[blank_ci_index] = 'Yes'
                else:
                    row_list[blank_ci_index] = 'No'

                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Incident-Standardization-Analysis', steps = '12', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Standardization Analysis Complete')
        except Exception as error:
            log_writer(script_name = 'Incident-Standardization-Analysis', steps = '12', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '12', 'message' : str(error)}

        # re-order column for data insertion:S13
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "processed_data_insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0],  # ticket_number
                    data_row[2],  # blank_ci
                ))
                # appending data into "input_data_update_row" empty list
                input_data_update_row.append((
                    data_row[0], # ticket_number
                ))
        except Exception as error:
            log_writer(script_name = 'Incident-Standardization-Analysis', steps = '13', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '13', 'message' : str(error)}

        # inserting normalize data into "processed_incident_data":S14
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_incident_data (
                ticket_number,
                blank_ci
            )
            VALUES %s
            ON CONFLICT (ticket_number)
            DO UPDATE SET
                blank_ci = EXCLUDED.blank_ci;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Standardization-Analysis', steps = '14', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Standardization-Analysis', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '14', 'message' : str(error)}

        # updating "row_status" of "input_incident_data" to "9" after normalized data:S15
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_incident_data AS t
            SET row_status = 9,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(ticket_number)
            WHERE t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_row)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Standardization-Analysis', steps = '15', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "9" Inside "input_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Standardization-Analysis', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '15', 'message' : str(error)}

    # sending return message to main script:S16
    return {'status' : 'SUCCESS', 'file_name' : 'Incident-Standardization-Analysis', 'step' : '16', 'message' : f'Total {total_count}-Rows Of Data Standardization Analysis Completed And Updated Into "input_incident_data" Table'}