# define "service_desk_kb_details_analysis" function
def service_desk_kb_details_analysis(account_unique_id: str) -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
        import re
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '7', 'message' : str(error)}

    # check if "input_sd_data" table present inside database:S08
    try:
        input_incident_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'input_sd_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(input_incident_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '8', status = 'SUCCESS', message = '"input_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '8', status = 'ERROR', message = '"input_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '8', 'message' : '"input_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '8', 'message' : str(error)}

    # check if "processed_sd_data" table present inside database:S09
    try:
        processed_incident_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'processed_sd_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(processed_incident_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '9', status = 'SUCCESS', message = '"processed_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '9', status = 'ERROR', message = '"processed_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '9', 'message' : '"processed_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '9', 'message' : str(error)}

    # define constant
    total_count = 0
    kb_details_analysis_rows_limiter = int(str(environment_values.get('SERVICE_DESK_KB_DETAILS_ANALYSIS_BATCH')))

    # loop through all the data
    while True:
        # define constant
        processed_data_insert_rows = []
        input_data_update_row = []

        # fetching rows for "MTTR" and "Aging" analysis:S10
        try:
            fetch_to_be_process_data_sql = '''
            SELECT
                isdd.account_unique_id,
                isdd.ticket_number,
                isdd.work_notes,
                isdd.resolution_notes,
                psdd.kb_present,
                psdd.kb_reference,
                psdd.kb_number
            FROM
                input_sd_data isdd
            JOIN
                processed_sd_data psdd
                ON isdd.account_unique_id = psdd.account_unique_id
                AND isdd.ticket_number = psdd.ticket_number
            WHERE
                isdd.account_unique_id = %s
                AND isdd.row_status = 8
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (str(account_unique_id), kb_details_analysis_rows_limiter))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '10', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Fetched For Service-Desk-KB-Details-Analysis Process')
                    else:
                        log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '10', status = 'INFO', message = f'For Account: "{account_unique_id}" No New Rows Present For Service-Desk-KB-Details-Analysis Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '10', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '10', 'message' : str(error)}

        # generating "kb_present", "kb_reference" and "kb_number":S11
        try:
            # define column index
            work_notes_index = 2
            resolution_notes_index = 3
            kb_present_index = 4
            kb_reference_index = 5
            kb_number_index = 6

            # pre-compiled regex
            referred_kb_pattern = re.compile(r'\bKB\d{7}\b')
            attached_kb_pattern = re.compile(r'\[code\]<a title(.*?)\[/code\]', re.DOTALL)

            # loop through all the rows
            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)
                # define constant
                attached_kbs = set()

                # extracting "attached" KB from "work_notes"
                for code_block in attached_kb_pattern.findall(str(row_list[work_notes_index] or '')):
                    attached_kbs.update(referred_kb_pattern.findall(code_block))

                # extracting "referred" KB from both "work_notes" and "resolution_notes"
                referred_kbs = set(referred_kb_pattern.findall(str(attached_kb_pattern.sub('', str(row_list[work_notes_index] or ''))) + ' ' +str(row_list[resolution_notes_index] or ''))) - attached_kbs
                all_kbs = attached_kbs | referred_kbs

                # creating all the details related KB
                if not all_kbs:
                    row_list[kb_present_index]   = 'No'
                    row_list[kb_reference_index] = 'N/A'
                    row_list[kb_number_index]    = 'N/A'
                else:
                    if attached_kbs and referred_kbs:
                        row_list[kb_present_index]   = 'Yes'
                        row_list[kb_reference_index] = 'Both'
                        row_list[kb_number_index]    = ', '.join(sorted(all_kbs))
                    elif attached_kbs:
                        row_list[kb_present_index]   = 'Yes'
                        row_list[kb_reference_index] = 'Attached'
                        row_list[kb_number_index]    = ', '.join(sorted(all_kbs))
                    else:
                        row_list[kb_present_index]   = 'Yes'
                        row_list[kb_reference_index] = 'Referred'
                        row_list[kb_number_index]    = ', '.join(sorted(all_kbs))
                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '11', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Of Data KB Details Analysis Completed')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '11', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '11', 'message' : str(error)}

        # re-order column for data insertion:S12
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "processed_data_insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0], # account_unique_id
                    data_row[1], # ticket_number
                    data_row[4], # kb_present
                    data_row[5], # kb_reference
                    data_row[6] # kb_number
                ))
                # appending data into "input_data_update_row" empty list
                input_data_update_row.append((
                    data_row[0], # account_unique_id
                    data_row[1] # ticket_number
                ))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '12', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '12', 'message' : str(error)}

        # inserting normalize data into "processed_sd_data":S13
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_sd_data (
                account_unique_id,
                ticket_number,
                kb_present,
                kb_reference,
                kb_number
            )
            VALUES %s
            ON CONFLICT (account_unique_id, ticket_number)
            DO UPDATE SET
                kb_present   = EXCLUDED.kb_present,
                kb_reference = EXCLUDED.kb_reference,
                kb_number    = EXCLUDED.kb_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '13', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_sd_data" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '13', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '13', 'message' : str(error)}

        # updating "row_status" of "input_sd_data" to "9" after normalized data:S14
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_sd_data AS t
            SET row_status = 9,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(account_unique_id, ticket_number)
            WHERE t.account_unique_id = v.account_unique_id
            AND t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_row)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '14', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "9" Inside "input_sd_data" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-KB-Details-Analysis', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '14', 'message' : str(error)}

    # sending return message to main script:S15
    return {'status' : 'SUCCESS', 'file_name' : 'Service-Desk-KB-Details-Analysis', 'step' : '15', 'message' : f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data KB Details Analysis Completed And Updated Into "input_sd_data" Table'}