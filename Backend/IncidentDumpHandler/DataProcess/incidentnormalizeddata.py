# define "incident_normalized_data" function
def incident_normalized_data(account_unique_id: str) -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
        import re
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        log_writer(script_name = 'Incident-Normalized-Data', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Normalized-Data', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-Normalized-Data', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-Normalized-Data', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Normalized-Data', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-Normalized-Data', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-Normalized-Data', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-Normalized-Data', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Normalized-Data', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '7', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Normalized-Data', steps = '8', status = 'SUCCESS', message = '"input_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Normalized-Data', steps = '8', status = 'ERROR', message = '"input_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '8', 'message' : '"input_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Normalized-Data', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '8', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Normalized-Data', steps = '9', status = 'SUCCESS', message = '"processed_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Normalized-Data', steps = '9', status = 'ERROR', message = '"processed_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '9', 'message' : '"processed_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Normalized-Data', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '9', 'message' : str(error)}

    # define constant
    total_count = 0
    normalize_data_rows_limiter = int(str(environment_values.get('DATA_NORMALIZE_BATCH', '1000')))
    priority_map = {
        '1': 'Critical',
        '2': 'High',
        '3': 'Medium',
        '4': 'Low',
        '5': 'Planning'
    }

    # loop through all the available data
    while True:
        # define empty list
        processed_data_insert_rows = []
        input_data_update_row = []

        # fetching rows to for normalizing:S10
        try:
            fetch_to_be_process_data_sql = '''
            SELECT "account_unique_id", "ticket_number", "cmdb_ci", "state", "priority", "category", "channel", "assignment_group", "parent_ticket", "assigned_to", "resolved_by"
            FROM input_incident_data
            WHERE "row_status" = 2
            AND "account_unique_id" = %s
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (account_unique_id, normalize_data_rows_limiter))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Incident-Normalized-Data', steps = '10', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Fetched For Data Normalization Process')
                    else:
                        log_writer(script_name = 'Incident-Normalized-Data', steps = '10', status = 'INFO', message = f'For Account: "{account_unique_id}" No New Rows Present For Data Normalization Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Incident-Normalized-Data', steps = '10', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '10', 'message' : str(error)}

        # normalize "cmdb_ci", "state", "priority", "category", "channel", "assignment_group", "parent_ticket", "assigned_to", "resolved_by" columns:S11
        try:
            # define column index
            cmdb_ci_index = 2
            state_index = 3
            priority_index = 4
            category_index = 5
            channel_index = 6
            assignment_group_index = 7
            parent_ticket_index = 8
            assigned_to_index = 9
            resolved_by_index = 10

            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)

                # normalize cmdb_ci
                if (cmdb_ci_value := str(row_list[cmdb_ci_index]).strip()) and cmdb_ci_value.upper() != 'N/A':
                    row_list[cmdb_ci_index] = re.sub(r'[^A-Z0-9]+', '_', cmdb_ci_value.upper()).strip('_')

                # normalize "state"
                if (str(row_list[state_index]).strip() != 'N/A'):
                    row_list[state_index] = "_".join(
                        state_word.title()
                        for state_word in str(row_list[state_index]).strip().split()
                    )

                # normalize "priority"
                if (raw_priority := str(row_list[priority_index]).strip()) and raw_priority.upper() != 'N/A':
                    priority_number_match = re.search(r'(\d+)', raw_priority)
                    if priority_number_match:
                        num = priority_number_match.group(1)
                        row_list[priority_index] = priority_map.get(num, 'Unknown')
                    else:
                        row_list[priority_index] = raw_priority

                # normalize "category"
                if (str(row_list[category_index]).strip() != 'N/A'):
                    row_list[category_index] = re.sub(r'[\s\W]+', '_', str(row_list[category_index]).strip()).strip('_')

                # normalize "channel"
                if (str(row_list[channel_index]).strip() != 'N/A'):
                    row_list[channel_index] = re.sub(r'[\s\W]+', '_', str(row_list[channel_index]).strip()).strip('_').upper()

                # normalize "assignment_group"
                if (str(row_list[assignment_group_index]).strip() != 'N/A'):
                    row_list[assignment_group_index] = re.sub(r'[\s\W]+', '_', str(row_list[assignment_group_index]).strip()).strip('_').upper()

                # normalize "parent_ticket"
                if (str(row_list[parent_ticket_index]).strip() != 'N/A'):
                    row_list[parent_ticket_index] = str(row_list[parent_ticket_index]).strip().upper()

                # normalize "assigned_to"
                if (str(row_list[assigned_to_index]).strip() != 'N/A'):
                    row_list[assigned_to_index] = " ".join(str(row_list[assigned_to_index]).strip().split()).title()

                # normalize "resolved_by"
                if (str(row_list[resolved_by_index]).strip() != 'N/A'):
                    row_list[resolved_by_index] = " ".join(str(row_list[resolved_by_index]).strip().split()).title()

                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Incident-Normalized-Data', steps = '11', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows "state", "priority", "category", "assignment_group", "parent_ticket" Data Normalized')
        except Exception as error:
            log_writer(script_name = 'Incident-Normalized-Data', steps = '11', status = 'ERROR', message = str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-Normalized-Data', 'step': '11', 'message': str(error)}

        # re-order column for data insertion:S12
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "processed_data_insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0], # account_unique_id
                    data_row[1], # ticket_number
                    data_row[2], # cmdb_ci
                    data_row[3], # state
                    data_row[4], # priority
                    data_row[5], # category
                    data_row[6], # channel
                    data_row[7], # assignment_group
                    data_row[8], # parent_ticket
                    data_row[9], # assigned_to
                    data_row[10], # resolved_by
                ))
                # appending data into "input_data_update_row" empty list
                input_data_update_row.append((
                    data_row[0], # account_unique_id
                    data_row[1] # ticket_number
                ))
        except Exception as error:
            log_writer(script_name = 'Incident-Normalized-Data', steps = '12', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '12', 'message' : str(error)}

        # inserting normalize data into "processed_incident_data":S13
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_incident_data (
                account_unique_id,
                ticket_number,
                cmdb_ci,
                state,
                priority,
                category,
                channel,
                assignment_group,
                parent_ticket,
                assigned_to,
                resolved_by
            )
            VALUES %s
            ON CONFLICT (account_unique_id, ticket_number)
            DO UPDATE SET
                cmdb_ci          = EXCLUDED.cmdb_ci,
                state            = EXCLUDED.state,
                priority         = EXCLUDED.priority,
                category         = EXCLUDED.category,
                channel          = EXCLUDED.channel,
                assignment_group = EXCLUDED.assignment_group,
                parent_ticket    = EXCLUDED.parent_ticket,
                assigned_to      = EXCLUDED.assigned_to,
                resolved_by      = EXCLUDED.resolved_by;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Normalized-Data', steps = '13', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Normalized-Data', steps = '13', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '13', 'message' : str(error)}

        # updating "row_status" of "input_incident_data" to "3" after normalized data:S14
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_incident_data AS t
            SET row_status = 3,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(account_unique_id, ticket_number)
            WHERE t.account_unique_id = v.account_unique_id
            AND t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_row)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Normalized-Data', steps = '14', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "3" Inside "input_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Normalized-Data', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Normalized-Data', 'step' : '14', 'message' : str(error)}

    # sending return message to main script:S15
    log_writer(script_name = 'Incident-Normalized-Data', steps = '15', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data Normalized And Updated Into "input_incident_data" Table')
    return {'status' : 'SUCCESS', 'file_name' : 'Incident-Normalized-Data', 'step' : '15', 'message' : f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data Normalized And Updated Into "input_incident_data" Table'}