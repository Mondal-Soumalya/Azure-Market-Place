# define "incident_information_clean" function
def incident_information_clean() -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import re
        import json
        import psycopg2
        from psycopg2.extras import execute_values
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        incident_dump_handler_folder_path = Path(backend_folder_path) / 'IncidentDumpHandler'
        data_process_folder_path = Path(incident_dump_handler_folder_path) / 'DataProcess'
        reference_data_folder_path = Path(data_process_folder_path) / 'ReferenceData'
        information_clean_pattern_json_file_path = Path(reference_data_folder_path) / 'InformationCleanPattern.json'
        log_writer(script_name = 'Incident-Information-Clean', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Information-Clean', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-Information-Clean', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-Information-Clean', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Information-Clean', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-Information-Clean', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-Information-Clean', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-Information-Clean', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Information-Clean', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '7', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Information-Clean', steps = '8', status = 'SUCCESS', message = '"input_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Information-Clean', steps = '8', status = 'ERROR', message = '"input_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '8', 'message' : '"input_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Information-Clean', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '8', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Information-Clean', steps = '9', status = 'SUCCESS', message = '"processed_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Information-Clean', steps = '9', status = 'ERROR', message = '"processed_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '9', 'message' : '"processed_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Information-Clean', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '9', 'message' : str(error)}

    # check if "InformationCleanPattern.json" file is present:S10
    try:
        if ((information_clean_pattern_json_file_path.exists()) and (information_clean_pattern_json_file_path.is_file()) and (information_clean_pattern_json_file_path.suffix.lower() == '.json')):
            log_writer(script_name = 'Incident-Information-Clean', steps = '10', status = 'SUCCESS', message = '"InformationCleanPattern.json" File Is Present')
        else:
            log_writer(script_name = 'Incident-Information-Clean', steps = '10', status = 'ERROR', message = '"InformationCleanPattern.json" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '10', 'message' : '"InformationCleanPattern.json" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Information-Clean', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '10', 'message' : str(error)}

    # load "InformationCleanPattern.json" file and compile with regexs:S11
    try:
        with open(str(information_clean_pattern_json_file_path), 'r') as pattern_file:
            json_file_pattern_dict = json.load(pattern_file)
            log_writer(script_name = 'Incident-Information-Clean', steps = '11', status = 'SUCCESS', message = '"InformationCleanPattern.json" File Loaded Into Script')
        # check if any pattern present
        if (json_file_pattern_dict):
            log_writer(script_name = 'Incident-Information-Clean', steps = '11', status = 'SUCCESS', message = f'Total: {len(json_file_pattern_dict)} Information Clean Pattern Present Inside "InformationCleanPattern.json" File')
            regexes_flag_map = {
                'IGNORECASE' : re.IGNORECASE,
                'DOTALL' : re.DOTALL,
                'MULTILINE' : re.MULTILINE
            }
            # define empty "information_clean_pattern" dict
            information_clean_pattern = {}
            for name, data in json_file_pattern_dict.items():
                pattern_string = data.get('pattern')
                regexes_flag_list = data.get('flags', [])
                regexes_flag_value = 0
                for flag_name in regexes_flag_list:
                    regexes_flag_value |= regexes_flag_map.get(flag_name, 0)
                information_clean_pattern[name] = re.compile(pattern_string, regexes_flag_value)
        else:
            log_writer(script_name = 'Incident-Information-Clean', steps = '11', status = 'ERROR', message = 'No Information Clean Pattern Present Inside "InformationCleanPattern.json" File')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '11', 'message' : 'No Information Clean Pattern Present Inside "InformationCleanPattern.json" File'}
    except json.JSONDecodeError as json_error:
        log_writer(script_name = 'Incident-Information-Clean', steps = '11', status = 'ERROR', message = str(json_error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '11', 'message' : str(json_error)}
    except Exception as error:
        log_writer(script_name = 'Incident-Information-Clean', steps = '11', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '11', 'message' : str(error)}

    # define constant
    total_count = 0
    information_clean_rows_limiter = int(str(environment_values.get('DATA_CLEAN_BATCH', '1000')))

    # loop through all the available data
    while True:
        # define empty list
        processed_data_insert_rows= []
        input_data_update_rows = []

        # fetching rows to for information clean:S12
        try:
            fetch_to_be_process_data_sql = '''
            SELECT "ticket_number", "cmdb_ci", "assigned_to", "resolved_by", "short_description", "description", "work_notes", "resolution_notes"
            FROM input_incident_data
            WHERE "row_status" = 3
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: # type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (information_clean_rows_limiter,))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Incident-Information-Clean', steps = '12', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Fetched For Information Clean Process')
                    else:
                        log_writer(script_name = 'Incident-Information-Clean', steps = '12', status = 'INFO', message = f'No New Rows Present For Information Clean Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Incident-Information-Clean', steps = '12', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '12', 'message' : str(error)}

        # remove information from "short_description", "description", "work_notes", "resolution_notes" and mask "cmdb_ci", "assigned_to", "resolved_by" columns:S13
        try:
            # masking priority for block wise pattern
            structural_patterns = ['HTML_BODY', 'HTML_TAG', 'KB_ATTACH_BLOCK', 'CODE_BLOCK']
            # define index matching with column name
            cmdb_ci_index = 1
            assigned_to_index = 2
            resolved_by_index = 3
            short_description_index = 4
            description_index = 5
            work_notes_index = 6
            resolution_notes_index = 7
            # column for patter search and masking
            text_field_indexes = [
                short_description_index,
                description_index,
                work_notes_index,
                resolution_notes_index
            ]

            # loop through all rows
            for i, row in enumerate(to_be_processed_data):
                row_list = list(row)

                # creating pattern for "cmdb_ci"
                cmdb_ci_value = str(row_list[cmdb_ci_index]).strip()
                cmdb_ci_pattern = re.compile(re.escape(cmdb_ci_value), re.IGNORECASE) if cmdb_ci_value and cmdb_ci_value.lower() != 'n/a' else None

                # creating pattern for "assigned_to"
                assigned_to_value = str(row_list[assigned_to_index]).strip()
                assigned_to_pattern = re.compile(re.escape(assigned_to_value), re.IGNORECASE) if assigned_to_value else None

                # creating pattern for "resolved_by"
                resolved_by_value = str(row_list[resolved_by_index]).strip()
                resolved_by_pattern = re.compile(re.escape(resolved_by_value), re.IGNORECASE) if resolved_by_value else None

                # loop through every required clean text field
                for j in text_field_indexes:
                    original_text = str(row_list[j])
                    if not original_text or original_text.strip().lower() in ['n/a', 'none', 'null']:
                        continue
                    cleaned_text = original_text

                    # structural blocks first
                    for pattern_name in structural_patterns:
                        cleaned_text = information_clean_pattern[pattern_name].sub(f'<{pattern_name}>', cleaned_text)

                    # row-specific masking
                    if cmdb_ci_pattern:
                        cleaned_text = cmdb_ci_pattern.sub('<CMDB_CI>', cleaned_text)
                    if assigned_to_pattern:
                        cleaned_text = assigned_to_pattern.sub('<ASSIGNED_TO>', cleaned_text)
                    if resolved_by_pattern:
                        cleaned_text = resolved_by_pattern.sub('<RESOLVED_BY>', cleaned_text)

                    # remaining patterns
                    for pattern_name, pattern_regex in information_clean_pattern.items():
                        if pattern_name not in structural_patterns:
                            cleaned_text = pattern_regex.sub(f'<{pattern_name}>', cleaned_text)

                    # normalize whitespace and newlines
                    cleaned_text = re.sub(r'\s*\n\s*', '; ', cleaned_text)
                    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

                    # update fields
                    row_list[j] = cleaned_text

                # replaced modified rows
                to_be_processed_data[i] = tuple(row_list)
        except Exception as error:
            log_writer(script_name='Incident-Information-Clean', steps='13', status='ERROR', message=str(error))
            return {'status': 'ERROR', 'file_name': 'Incident-Information-Clean', 'step': '13', 'message': str(error)}

        # re-order column for data insertion:S14
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0], # ticket_number
                    str(data_row[4]), # short_description
                    str(data_row[5]), # description
                    str(data_row[6]), # work_notes
                    str(data_row[7]) # resolution_notes
                ))
                # appending data into "input_data_update_rows" empty list
                input_data_update_rows.append((
                    data_row[0], # ticket_number
                ))
        except Exception as error:
            log_writer(script_name = 'Incident-Information-Clean', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '14', 'message' : str(error)}

        # inserting normalize data into "processed_incident_data":S15
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_incident_data (
                ticket_number,
                short_description,
                description,
                work_notes,
                resolution_notes
            )
            VALUES %s
            ON CONFLICT (ticket_number)
            DO UPDATE SET
                short_description= EXCLUDED.short_description,
                description      = EXCLUDED.description,
                work_notes       = EXCLUDED.work_notes,
                resolution_notes = EXCLUDED.resolution_notes;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Information-Clean', steps = '15', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Information-Clean', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '15', 'message' : str(error)}

        # updating "row_status" of "input_incident_data" to "4" after normalized data:S16
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_incident_data AS t
            SET row_status = 4,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(ticket_number)
            WHERE t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Information-Clean', steps = '16', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "4" Inside "input_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Information-Clean', steps = '16', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '16', 'message' : str(error)}

        # inserting "ticket_number" into "token_count_details" table:S17
        try:
            token_count_details_upsert_sql = '''
            INSERT INTO token_count_details (
                ticket_number,
                prompt_token,
                output_token
            )
            SELECT v.ticket_number, 0 AS prompt_token, 0 AS output_token
            FROM (VALUES %s) AS v(ticket_number)
            ON CONFLICT (ticket_number)
            DO UPDATE
            SET
                prompt_token = token_count_details.prompt_token + 0,
                output_token = token_count_details.output_token + 0;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, token_count_details_upsert_sql, input_data_update_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Information-Clean', steps = '17', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Upserted Into "token_count_details" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Information-Clean', steps = '17', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Information-Clean', 'step' : '17', 'message' : str(error)}

    # sending return message to main script:S18
    log_writer(script_name = 'Incident-Information-Clean', steps = '18', status = 'SUCCESS', message = f'Total {total_count}-Rows Of Data Information Clean And Updated Into "input_incident_data" Table')
    return {'status' : 'SUCCESS', 'file_name' : 'Incident-Information-Clean', 'step' : '18', 'message' : f'Total {total_count}-Rows Of Data Information Clean And Updated Into "input_incident_data" Table'}