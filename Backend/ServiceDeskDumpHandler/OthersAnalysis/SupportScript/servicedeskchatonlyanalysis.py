# define "service_desk_chat_only_analysis" function
def service_desk_chat_only_analysis(account_unique_id: str) -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
        import re
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        service_desk_dump_handler_folder_path = Path(backend_folder_path) / 'ServiceDeskDumpHandler'
        others_analysis_folder_path = Path(service_desk_dump_handler_folder_path) / 'OthersAnalysis'
        support_script_folder_path = Path(others_analysis_folder_path) / 'SupportScript'
        reference_data_folder_path = Path(support_script_folder_path) / 'ReferenceData'
        chat_only_analysis_file_path = Path(reference_data_folder_path) / 'ChatOnlyAnalysisKeywords.txt'
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '7', 'message' : str(error)}

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
                    log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '8', status = 'SUCCESS', message = '"input_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '8', status = 'ERROR', message = '"input_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '8', 'message' : '"input_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '8', 'message' : str(error)}

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
                    log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '9', status = 'SUCCESS', message = '"processed_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '9', status = 'ERROR', message = '"processed_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '9', 'message' : '"processed_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '9', 'message' : str(error)}

    # load "ChatOnlyAnalysisKeywords.txt" file in script:S10
    try:
        if ((chat_only_analysis_file_path.exists()) and (chat_only_analysis_file_path.is_file()) and (chat_only_analysis_file_path.suffix.lower() == '.txt')):
            with open(chat_only_analysis_file_path, 'r', encoding = 'utf-8') as blank_ci_keywords_file:
                chat_only_keywords = [line.strip().lower() for line in blank_ci_keywords_file if line.strip()]
                log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '10', status = 'SUCCESS', message = '"ChatOnlyAnalysisKeywords.txt" File Is Present And Content Loaded Into Script')
        else:
            chat_only_keywords = ['chat']
            log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '10', status = 'ERROR', message = '"ChatOnlyAnalysisKeywords.txt" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '10', 'message' : '"ChatOnlyAnalysisKeywords.txt" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Serivce-Desk-Chat-Only-Analysis', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Serivce-Desk-Chat-Only-Analysis', 'step' : '10', 'message' : str(error)}

    # define constant
    total_count = 0
    kb_details_analysis_rows_limiter = int(str(environment_values.get('SERVICE_DESK_CHAT_ONLY_TICKET_ANALYSIS_BATCH')))

    # loop through all the data
    while True:
        # define constant
        processed_data_insert_rows = []
        input_data_update_row = []

        # fetching rows for "MTTR" and "Aging" analysis:S11
        try:
            fetch_to_be_process_data_sql = '''
            SELECT
                isdd.account_unique_id,
                isdd.ticket_number,
                psdd.contact_type,
                psdd.chat_only_ticket
            FROM
                input_sd_data isdd
            JOIN
                processed_sd_data psdd
                ON isdd.account_unique_id = psdd.account_unique_id
                AND isdd.ticket_number = psdd.ticket_number
            WHERE
                isdd.account_unique_id = %s
                AND isdd.row_status = 9
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (str(account_unique_id), kb_details_analysis_rows_limiter))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Service-Desk-Chat-Only-Analysis', steps = '11', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Fetched For Service-Desk-Chat-Only-Analysis Process')
                    else:
                        log_writer(script_name = 'Service-Desk-Chat-Only-Analysis', steps = '11', status = 'INFO', message = f'For Account: "{account_unique_id}" No New Rows Present For Service-Desk-Chat-Only-Analysis Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chat-Only-Analysis', steps = '11', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chat-Only-Analysis', 'step' : '11', 'message' : str(error)}

        # generating "chat_only_ticket":S12
        try:
            # define column index
            contact_type_index = 2
            chat_only_ticket_index = 3
            # escape each keyword to avoid regex injection
            escaped_keywords = [re.escape(keyword) for keyword in chat_only_keywords]
            # build pattern with keywords
            chat_only_pattern = re.compile(r'\b(?:' + '|'.join(escaped_keywords) + r')\b', re.IGNORECASE)

            # loop through all the rows
            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)
                # creating all the details related chat only ticket
                if chat_only_pattern.search(str(row_list[contact_type_index] or '')):
                    row_list[chat_only_ticket_index] = 'Yes'
                else:
                    row_list[chat_only_ticket_index] = 'No'
                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name='Service-Desk-Chat-Only-Analysis', steps='12', status='SUCCESS', message=f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Of Data Chat-Only Analysis Completed')
        except Exception as error:
            log_writer(script_name='Service-Desk-Chat-Only-Analysis', steps='12', status='ERROR', message=str(error))
            return {'status': 'ERROR', 'file_name': 'Service-Desk-Chat-Only-Analysis', 'step': '12', 'message': str(error)}

        # re-order column for data insertion:S13
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "processed_data_insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0], # account_unique_id
                    data_row[1], # ticket_number
                    data_row[3] # chat_only_ticket
                ))
                # appending data into "input_data_update_row" empty list
                input_data_update_row.append((
                    data_row[0], # account_unique_id
                    data_row[1] # ticket_number
                ))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chat-Only-Analysis', steps = '13', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chat-Only-Analysis', 'step' : '13', 'message' : str(error)}

        # inserting normalize data into "processed_sd_data":S14
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_sd_data (
                account_unique_id,
                ticket_number,
                chat_only_ticket
            )
            VALUES %s
            ON CONFLICT (account_unique_id, ticket_number)
            DO UPDATE SET
                chat_only_ticket = EXCLUDED.chat_only_ticket;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-Chat-Only-Analysis', steps = '14', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_sd_data" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chat-Only-Analysis', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chat-Only-Analysis', 'step' : '14', 'message' : str(error)}

        # updating "row_status" of "input_sd_data" to "10" after normalized data:S15
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_sd_data AS t
            SET row_status = 10,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(account_unique_id, ticket_number)
            WHERE t.account_unique_id = v.account_unique_id
            AND t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_row)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-Chat-Only-Analysis', steps = '15', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "10" Inside "input_sd_data" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chat-Only-Analysis', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chat-Only-Analysis', 'step' : '15', 'message' : str(error)}

    # sending return message to main script:S16
    return {'status' : 'SUCCESS', 'file_name' : 'Service-Desk-Chat-Only-Analysis', 'step' : '16', 'message' : f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Chat Only Ticket Analysis Completed And Updated Into "input_sd_data" Table'}