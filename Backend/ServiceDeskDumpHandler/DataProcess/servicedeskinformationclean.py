# define "servicedesk_information_clean" function
def servicedesk_information_clean(account_unique_id: str) -> dict[str, str]: #type: ignore
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
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        servcie_desk_dump_handler_folder_path = Path(backend_folder_path) / 'ServiceDeskDumpHandler'
        data_process_folder_path = Path(servcie_desk_dump_handler_folder_path) / 'DataProcess'
        reference_data_folder_path = Path(data_process_folder_path) / 'ReferenceData'
        information_clean_pattern_json_file_path = Path(reference_data_folder_path) / 'InformationCleanPattern.json'
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '7', status = 'SUCCESS', message = 'PostgreSQL Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '7', 'message' : str(error)}

    # check if "input_sd_data" table present inside database:S08
    try:
        input_sd_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'input_sd_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(input_sd_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Service-Desk-Information-Clean', steps = '8', status = 'SUCCESS', message = '"input_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Information-Clean', steps = '8', status = 'ERROR', message = '"input_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '8', 'message' : '"input_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '8', 'message' : str(error)}

    # check if "processed_sd_data" table present inside database:S09
    try:
        processed_sd_data_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'processed_sd_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(processed_sd_data_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Service-Desk-Information-Clean', steps = '9', status = 'SUCCESS', message = '"processed_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Information-Clean', steps = '9', status = 'ERROR', message = '"processed_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '9', 'message' : '"processed_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '9', 'message' : str(error)}

    # check if "InformationCleanPattern.json" file is present:S10
    try:
        if ((information_clean_pattern_json_file_path.exists()) and (information_clean_pattern_json_file_path.is_file()) and (information_clean_pattern_json_file_path.suffix.lower() == '.json')):
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '10', status = 'SUCCESS', message = '"InformationCleanPattern.json" File Is Present')
        else:
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '10', status = 'ERROR', message = '"InformationCleanPattern.json" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '10', 'message' : '"InformationCleanPattern.json" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '10', 'message' : str(error)}

    # load "InformationCleanPattern.json" file and compile with regexs:S11
    try:
        with open(str(information_clean_pattern_json_file_path), 'r') as pattern_file:
            json_file_pattern_dict = json.load(pattern_file)
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '11', status = 'SUCCESS', message = '"InformationCleanPattern.json" File Loaded Into Script')
        # check if any pattern present
        if (json_file_pattern_dict):
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '11', status = 'SUCCESS', message = f'Total: {len(json_file_pattern_dict)} Information Clean Pattern Present Inside "InformationCleanPattern.json" File')
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
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '11', status = 'ERROR', message = 'No Information Clean Pattern Present Inside "InformationCleanPattern.json" File')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '11', 'message' : 'No Information Clean Pattern Present Inside "InformationCleanPattern.json" File'}
    except json.JSONDecodeError as json_error:
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '11', status = 'ERROR', message = str(json_error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '11', 'message' : str(json_error)}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '11', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '11', 'message' : str(error)}

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
            SELECT "account_unique_id", "ticket_number", "created_by", "opened_by", "resolved_by", "short_description", "description", "work_notes", "resolution_notes"
            FROM input_sd_data
            WHERE "row_status" = 3
            AND "account_unique_id" = %s
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (account_unique_id, information_clean_rows_limiter))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '12', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Fetched For Information Clean Process')
                    else:
                        log_writer(script_name = 'Service-Desk-Information-Clean', steps = '12', status = 'INFO', message = f'For Account: "{account_unique_id}" No New Rows Present For Information Clean Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '12', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '12', 'message' : str(error)}

        # remove information from "short_description", "description", "work_notes", "resolution_notes" and mask "created_by", "opened_by", "resolved_by" columns:S13
        try:
            # masking priority for block wise pattern
            structural_patterns = ['HTML_BODY', 'HTML_TAG', 'KB_ATTACH_BLOCK', 'CODE_BLOCK']
            # define index matching with column name
            created_by_index = 2
            opened_by_index = 3
            resolved_by_index = 4
            short_description_index = 5
            description_index = 6
            work_notes_index = 7
            resolution_notes_index = 8
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

                # creating "created_by" pattern
                created_by_value = str(row_list[created_by_index]).strip()
                created_by_pattern = re.compile(re.escape(created_by_value), re.IGNORECASE) if created_by_value else None

                # creating "opened_by" pattern
                opened_by_value = str(row_list[opened_by_index]).strip()
                opened_by_pattern = re.compile(re.escape(opened_by_value), re.IGNORECASE) if opened_by_value else None

                # creating "resolved_by" pattern
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
                    if created_by_pattern:
                        cleaned_text = created_by_pattern.sub('<CREATED_BY>', cleaned_text)
                    if opened_by_pattern:
                        cleaned_text = opened_by_pattern.sub('<OPENED_BY>', cleaned_text)
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
            log_writer(script_name='Service-Desk-Information-Clean', steps='13', status='ERROR', message=str(error))
            return {'status': 'ERROR', 'file_name': 'Service-Desk-Information-Clean', 'step': '13', 'message': str(error)}

        # re-order column for data insertion:S14
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0], # account_unique_id
                    data_row[1], # ticket_number
                    str(data_row[5]), # short_description
                    str(data_row[6]), # description
                    str(data_row[7]), # work_notes
                    str(data_row[8]) # resolution_notes
                ))
                # appending data into "input_data_update_rows" empty list
                input_data_update_rows.append((
                    data_row[0], # account_unique_id
                    data_row[1] # ticket_number
                ))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '14', 'message' : str(error)}

        # inserting normalize data into "processed_sd_data":S15
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_sd_data (
                account_unique_id,
                ticket_number,
                short_description,
                description,
                work_notes,
                resolution_notes
            )
            VALUES %s
            ON CONFLICT (ticket_number, account_unique_id)
            DO UPDATE SET
                short_description= EXCLUDED.short_description,
                description      = EXCLUDED.description,
                work_notes       = EXCLUDED.work_notes,
                resolution_notes = EXCLUDED.resolution_notes;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-Information-Clean', steps = '15', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_sd_data" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '15', 'message' : str(error)}

        # updating "row_status" of "input_sd_data" to "4" after normalized data:S16
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_sd_data AS t
            SET row_status = 4,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(account_unique_id, ticket_number)
            WHERE t.account_unique_id = v.account_unique_id
            AND t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-Information-Clean', steps = '16', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "4" Inside "input_sd_data" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '16', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '16', 'message' : str(error)}

        # inserting "account_unique_id" and "ticket_number" into "token_count_details" table:S17
        try:
            token_count_details_upsert_sql = '''
            INSERT INTO token_count_details (
                account_unique_id,
                ticket_number,
                prompt_token,
                output_token
            )
            SELECT v.account_unique_id, v.ticket_number, 0 AS prompt_token, 0 AS output_token
            FROM (VALUES %s) AS v(account_unique_id, ticket_number)
            ON CONFLICT (account_unique_id, ticket_number)
            DO UPDATE
            SET
                prompt_token = token_count_details.prompt_token + 0,
                output_token = token_count_details.output_token + 0;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, token_count_details_upsert_sql, input_data_update_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-Information-Clean', steps = '17', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Upserted Into "token_count_details" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Information-Clean', steps = '17', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '17', 'message' : str(error)}

    # sending return message to main script:S18
    log_writer(script_name = 'Service-Desk-Information-Clean', steps = '18', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data Information Clean And Updated Into "input_sd_data" Table')
    return {'status' : 'SUCCESS', 'file_name' : 'Service-Desk-Information-Clean', 'step' : '18', 'message' : f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data Information Clean And Updated Into "input_sd_data" Table'}


# # old information clean pattern
# information_clean_pattern = {
#     # Matches any HTML tags like <div>, <p>, <span>, etc.
#     "HTML_TAG": re.compile(r"<[^>]+>", re.IGNORECASE | re.DOTALL),

#     # Matches entire <html> or <body> sections, including nested content
#     "HTML_BODY": re.compile(r"<html.*?>.*?</html>|<body.*?>.*?</body>", re.IGNORECASE | re.DOTALL),

#     # Matches timestamps like "12/31/2023", "12-31-2023", "12/31/23 10:30 AM", etc.
#     "TIMESTAMP": re.compile(
#         r"\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}[\sT,]*(\d{1,2}[:]\d{2}([:]\d{2})?\s?(AM|PM)?)?\b",
#         re.IGNORECASE | re.MULTILINE
#     ),

#     # Matches ISO formatted timestamps like "2023-12-31 14:30:00"
#     "TIMESTAMP_ISO": re.compile(r"\b\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\b"),

#     # Matches datestamps with month names and optional time, e.g., "December 31, 2023 10:30 AM"
#     "DATESTAMP_ISO": re.compile(
#         r"\b(?:Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|"
#         r"Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December) "
#         r"\d{1,2},\s\d{4}\s\d{1,2}:\d{2}\s?(?:AM|PM)\b",
#         re.IGNORECASE
#     ),

#     # Matches datestamps like "10:30 (UTC) 31.12.2023"
#     "DATESTAMP_UTC": re.compile(r"\b\d{1,2}:\d{2}\s*\(UTC\)\s*\d{1,2}\.\d{1,2}\.\d{4}\b", re.IGNORECASE),

#     # Matches short datestamps like "31-Dec-23"
#     "DATESTAMP": re.compile(r"\b\d{1,2}-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{2}\b", re.IGNORECASE),

#     # Matches full datetimes with day of week and month name, e.g., "Monday, December 31, 2023 10:30 AM"
#     "DATETIMEFULL_STAMP": re.compile(
#         r"\b(?:Mon|Monday|Tue|Tuesday|Wed|Wednesday|Thu|Thursday|Fri|Friday|Sat|Saturday|Sun|Sunday),\s*"
#         r"(?:Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)\s+"
#         r"\d{1,2},\s\d{4}\s\d{1,2}:\d{2}\s?(?:AM|PM)\b",
#         re.IGNORECASE
#     ),

#     # Matches ticket IDs like "NC12345", "REQ67890", "TASK54321", etc.
#     "TICKET_ID": re.compile(r"\b(?:INC|REQ|TASK|CHG|PRB|SCTASK|RITM)\d{5,}\b", re.IGNORECASE),

#     # Matches email addresses
#     "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", re.IGNORECASE),

#     # Matches IPv4 addresses like "192.168.1.1"
#     "IPv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),

#     # Matches IPv6 addresses like "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
#     "IPv6": re.compile(r"\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b", re.IGNORECASE),

#     # Matches MAC addresses like "00:1A:2B:3C:4D:5E" or "00-1A-2B-3C-4D-5E"
#     "MAC": re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b", re.IGNORECASE),

#     # Matches URLs starting with "http(s)://" or "www."
#     "URL": re.compile(r"\b(?:https?://|www\.)[^\s/$.?#].[^\s]*\b", re.IGNORECASE),

#     # Matches Microsoft KB article numbers like "KB1234567"
#     "KB_NUMBER": re.compile(r"\bKB\d{7}\b", re.IGNORECASE),

#     # Matches KB attachment links in code blocks like "[code]<a title ... [/code]"
#     "KB_ATTACH_BLOCK": re.compile(r"\[code\]<a title(.*?)\[/code\]", re.DOTALL),

#     # Matches code blocks wrapped in "[code]...[/code]", including any HTML, text, or links inside
#     "CODE_BLOCK": re.compile(r"\[code\](.*?)\[/code\]", re.IGNORECASE | re.DOTALL),

#     # Matches lines of repeated decoration characters like ===, --- or ***
#     "DECORATION": re.compile(r"^[=\-*]{3,}$", re.MULTILINE),

#     # Matches SHA-1 hash values (40 hex characters)
#     "SHA1": re.compile(r"\b[a-fA-F0-9]{40}\b"),

#     # Matches SHA-256 hash values (64 hex characters)
#     "SHA256": re.compile(r"\b[a-fA-F0-9]{64}\b"),

#     # Matches base64-encoded SHA-1 keys (27-28 chars + optional padding)
#     "SHA1_KEY_B64": re.compile(r"\b[A-Za-z0-9+/]{27,28}={0,2}\b"),

#     # Matches base64-encoded SHA-256 keys (43-44 chars + optional padding)
#     "SHA256_KEY_B64": re.compile(r"\b[A-Za-z0-9+/]{43,44}={0,2}\b"),

#     # Matches hexadecimal numbers like "0x1A2B3C"
#     "HEX": re.compile(r"\b0x[a-fA-F0-9]+\b", re.IGNORECASE),

#     # Matches domain names like "example.com", "sub.example.co.uk"
#     "DOMAIN_NAME": re.compile(r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b", re.IGNORECASE)
# }