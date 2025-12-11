# define "incident_final_category_analysis" function
def incident_final_category_analysis() -> dict[str, str]: #type: ignore
    # importing python module:S1
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
        import re
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S2
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S3
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S4
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        incident_dump_handler_folder_path = Path(backend_folder_path) / 'IncidentDumpHandler'
        esoar_analysis_folder_path = Path(incident_dump_handler_folder_path) / 'ESOARAnalysis'
        support_script_folder_path = Path(esoar_analysis_folder_path) / 'SupportScript'
        reference_data_folder_path = Path(support_script_folder_path) / 'ReferenceData'
        auto_resolved_keywords_file_path = Path(reference_data_folder_path) / 'AutoResolvedKeywords.txt'
        autoheal_assigned_to_keywords_file_path = Path(reference_data_folder_path) / 'AutoHealAssignedToKeywords.txt'
        autoheal_description_keywords_file_path = Path(reference_data_folder_path) / 'AutoHealDescriptionKeyword.txt'
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined.')
    except Exception as error:
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S5
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present.')
        else:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present.')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '5', 'message' : '".env" File Not Present.'}
    except Exception as error:
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S6
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script.')
    except Exception as error:
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S7
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined.')
    except Exception as error:
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '7', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '8', status = 'SUCCESS', message = '"input_incident_data" Table Present Inside Database.')
                else:
                    log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '8', status = 'ERROR', message = '"input_incident_data" Table Not Present.')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '8', 'message' : '"input_incident_data" Table Not Present.'}
    except Exception as error:
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '8', 'message' : str(error)}

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
                    log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '9', status = 'SUCCESS', message = '"processed_incident_data" Table Present Inside Database.')
                else:
                    log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '9', status = 'ERROR', message = '"processed_incident_data" Table Not Present.')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '9', 'message' : '"processed_incident_data" Table Not Present.'}
    except Exception as error:
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '9', 'message' : str(error)}

    # load "AutoResolvedKeywords.txt" file in script:S10
    try:
        if ((auto_resolved_keywords_file_path.exists()) and (auto_resolved_keywords_file_path.is_file()) and (auto_resolved_keywords_file_path.suffix.lower() == '.txt')):
            with open(auto_resolved_keywords_file_path, 'r', encoding = 'utf-8') as blank_ci_keywords_file:
                auto_resolved_keywords = [line.strip().lower() for line in blank_ci_keywords_file if line.strip()]
                log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '10', status = 'SUCCESS', message = '"AutoResolvedKeywords.txt" File Is Present And Content Loaded Into Script.')
        else:
            auto_resolved_keywords = ['splunk', 'asrengineer', 'awsautomation', 'dopintegration', 'rmiautomationuser']
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '10', status = 'ERROR', message = '"AutoResolvedKeywords.txt" File Not Present.')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '10', 'message' : '"AutoResolvedKeywords.txt" File Not Present.'}
    except Exception as error:
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '10', 'message' : str(error)}

    # load "AutoHealAssignedToKeywords.txt" file in script:S11
    try:
        if ((autoheal_assigned_to_keywords_file_path.exists()) and (autoheal_assigned_to_keywords_file_path.is_file()) and (autoheal_assigned_to_keywords_file_path.suffix.lower() == '.txt')):
            with open(autoheal_assigned_to_keywords_file_path, 'r', encoding = 'utf-8') as blank_ci_keywords_file:
                autoheal_assigned_to_keywords = [line.strip().lower() for line in blank_ci_keywords_file if line.strip()]
                log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '11', status = 'SUCCESS', message = '"AutoHealAssignedToKeywords.txt" File Is Present And Content Loaded Into Script.')
        else:
            autoheal_assigned_to_keywords = ['rbaautoheal']
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '11', status = 'ERROR', message = '"AutoHealAssignedToKeywords.txt" File Not Present.')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '11', 'message' : '"AutoHealAssignedToKeywords.txt" File Not Present.'}
    except Exception as error:
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '11', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '11', 'message' : str(error)}

    # load "AutoHealDescriptionKeyword.txt" file in script:S12
    try:
        if ((autoheal_description_keywords_file_path.exists()) and (autoheal_description_keywords_file_path.is_file()) and (autoheal_description_keywords_file_path.suffix.lower() == '.txt')):
            with open(autoheal_description_keywords_file_path, 'r', encoding = 'utf-8') as blank_ci_keywords_file:
                autoheal_description_keywords = [line.strip().lower() for line in blank_ci_keywords_file if line.strip()]
                log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '12', status = 'SUCCESS', message = '"AutoHealDescriptionKeyword.txt" File Is Present And Content Loaded Into Script.')
        else:
            autoheal_description_keywords = ['AHDFC', 'AHDF', 'AHDFOM', 'AHDFSNF', 'AHDFSNFWFHNC', 'AHDP', 'AHDRCF', 'AHDRFCNO', 'AHDRFNO', 'AHDRNO', 'AHDSD', 'AHP', 'AHDSR', 'AHDSDWFHNC', 'ARIP', 'AHLE']
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '12', status = 'ERROR', message = '"AutoHealDescriptionKeyword.txt" File Not Present.')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '12', 'message' : '"AutoHealDescriptionKeyword.txt" File Not Present.'}
    except Exception as error:
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '12', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '12', 'message' : str(error)}

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
        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '13', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '13', 'message' : str(error)}

    # define constant
    total_count = 0
    final_category_analysis_rows_limiter = int(str(environment_values.get('FINAL_CATEGORY_ANALYSIS_BATCH', '1000')))

    # loop through all the data
    while True:
        # define constant
        processed_data_insert_rows = []
        input_data_update_row = []

        # fetch rows for "Final Category Analysis":S14
        try:
            fetch_to_be_process_data_sql = '''
            SELECT
                iid.ticket_number,
                pid.state,
                pid.assignment_group,
                pid.assignment_group_category,
                pid.assigned_to,
                pid.resolved_by,
                pid.resolved_type,
                iid.short_description,
                pid.bot_availability,
                pid.cancelled_ticket,
                pid.connector_down,
                pid.flapping_event,
                pid.short_duration_ticket,
                pid.sequence_event,
                pid.periodic_event,
                pid.blank_ci,
                pid.parent_child_event,
                pid.duplicate_event,
                pid.deduplicate_event,
                pid.correlated_event,
                pid.autoheal_category,
                pid.eso_analysis,
                pid.eso_category,
                pid.final_category
            FROM
                input_incident_data AS iid
            JOIN
                processed_incident_data AS pid
                ON iid.ticket_number = pid.ticket_number
            WHERE
                iid.row_status = 10
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (final_category_analysis_rows_limiter,))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '14', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Fetched For Final Category Analysis Process')
                    else:
                        log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '14', status = 'INFO', message = f'No New Rows Present For Final Category Analysis Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '14', 'message' : str(error)}

        # generating "assignment_group_category" view:S15
        try:
            # define column index
            assignment_group_index = 2
            assignment_group_category_index = 3

            # loop through all the rows
            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)

                # normalize "assignment_group" value
                assignment_group_normalized = normalize_text(row_list[assignment_group_index])

                # match all possible "L1/L2/L3 "combinations
                if assignment_group_normalized == '':
                    row_list[assignment_group_category_index] = 'Others'
                elif re.search(r'(level\s*1|l\s*1|lvl\s*1)', assignment_group_normalized, re.IGNORECASE):
                    row_list[assignment_group_category_index] = 'L1'
                elif re.search(r'(level\s*2|l\s*2|lvl\s*2)', assignment_group_normalized, re.IGNORECASE):
                    row_list[assignment_group_category_index] = 'L2'
                elif re.search(r'(level\s*3|l\s*3|lvl\s*3)', assignment_group_normalized, re.IGNORECASE):
                    row_list[assignment_group_category_index] = 'L3'
                else:
                    row_list[assignment_group_category_index] = 'Others'

                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '15', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Assignment Group Category Processed.')
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '15', 'message' : str(error)}

        # generating "resolved_type" view:S16
        try:
            # define column index
            resolved_by_index = 5
            resolved_type_index = 6

            # lopp through all the data
            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)

                # normalize "resolved_by" column
                normalized_resolved_by = normalize_text(row_list[resolved_by_index])

                # determine "resolved_type"
                if (normalized_resolved_by == ''):
                    row_list[resolved_type_index] = 'Others'
                elif any(re.search(keyword, normalized_resolved_by, re.IGNORECASE) for keyword in auto_resolved_keywords):
                    row_list[resolved_type_index] = 'Auto'
                else:
                    row_list[resolved_type_index] = 'User'

                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '16', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Resolved Type Processed.')
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '16', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '16', 'message' : str(error)}

        # generating "autoheal_category" view:S17
        try:
            # define column index
            state_index = 1
            assigned_to_index = 4
            short_description_index = 7
            autoheal_category_index = 20

            # loop through all the rows
            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)

                # normalize "state", "assigned_to" and "short_description" column
                normalized_state = normalize_text(row_list[state_index])
                normalized_assigned_to = normalize_text(row_list[assigned_to_index])
                normalized_short_description = str(row_list[short_description_index]).upper().strip()

                # determine "autoheal_category"
                if normalized_state in ('closed', 'resolved'):
                    if (
                        any(keyword in normalized_short_description for keyword in autoheal_description_keywords)
                        or normalized_short_description.startswith('AH')
                        or normalized_assigned_to in autoheal_assigned_to_keywords
                    ):
                        row_list[autoheal_category_index] = 'AutoHeal'
                    else:
                        row_list[autoheal_category_index] = 'Non_AutoHeal'
                else:
                    row_list[autoheal_category_index] = 'Non_AutoHeal'

                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '17', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data Autoheal Category Processed.')
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '17', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '17', 'message' : str(error)}

        # generating "eso_analysis_category" view:S18
        try:
            # define column indexes
            cancelled_ticket_index = 9
            conector_down_index = 10
            flapping_event_index = 11
            short_duration_ticket_index = 12
            sequence_event_index = 13
            periodic_event_index = 14
            blank_ci_index = 15
            parent_child_event_index = 16
            duplicate_event_index = 17
            deduplicate_event_index = 18
            correlated_event_index = 19
            eso_analysis_index = 21

            # mapping column names to indexes for cleaner iteration
            eso_columns_mapping = {
                'cancelled_ticket': cancelled_ticket_index,
                'conector_down': conector_down_index,
                'flapping_event': flapping_event_index,
                'short_duration_ticket': short_duration_ticket_index,
                'sequence_event': sequence_event_index,
                'periodic_event': periodic_event_index,
                'blank_ci': blank_ci_index,
                'parent_child_event': parent_child_event_index,
                'duplicate_event': duplicate_event_index,
                'deduplicate_event': deduplicate_event_index,
                'correlated_event': correlated_event_index
            }

            # loop through all the rows
            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)

                # collect all flags with value "Yes"
                eso_analysis_flags = [
                    eso_column_name for eso_column_name, eso_column_index in eso_columns_mapping.items()
                    if str(row_list[eso_column_index]).strip().lower() == 'yes'
                ]

                # join the value accordingly
                if (not eso_analysis_flags):
                    row_list[eso_analysis_index] = 'N/A'
                else:
                    row_list[eso_analysis_index] = ', '.join(eso_analysis_flags)

                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '18', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data ESO-Analysis Processed.')
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '18', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '18', 'message' : str(error)}

        # generating "eso_category" view:S19
        try:
            # define column index for "eso_category"
            eso_category_index = 22

            # define priority order for "eso_category"
            priority_columns = [
                ('cancelled_ticket', cancelled_ticket_index),
                ('parent_child_event', parent_child_event_index),
                ('sequence_event', sequence_event_index),
                ('duplicate_event', duplicate_event_index),
                ('deduplicate_event', deduplicate_event_index),
                ('periodic_event', periodic_event_index),
                ('flapping_event', flapping_event_index),
                ('correlated_event', correlated_event_index),
                ('connector_down', conector_down_index),
                ('short_duration_ticket', short_duration_ticket_index),
                ('blank_ci', blank_ci_index)
            ]

            # loop through all rows
            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)

                # check priority columns in order
                category_found = False
                for column_name, column_index in priority_columns:
                    if str(row_list[column_index]).strip().lower() == 'yes':
                        row_list[eso_category_index] = column_name
                        category_found = True
                        break

                # if no priority column has "Yes", set to 'N/A'
                if not category_found:
                    row_list[eso_category_index] = 'N/A'

                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '19', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Of Data ESO-Category Processed.')
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '19', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '19', 'message' : str(error)}

        # generating "final_category" view:S20
        try:
            # define column indexes
            bot_availability_index = 8
            final_category_index = 23

            # define required sets for "elimination" and "standardization" columns
            elimination_columns = [
                cancelled_ticket_index,
                parent_child_event_index,
                sequence_event_index,
                deduplicate_event_index,
                correlated_event_index,
                conector_down_index,
                short_duration_ticket_index
            ]
            standardization_columns = [blank_ci_index]

            # loop through all rows
            for i, data_row in enumerate(to_be_processed_data):
                # convert tuple to list to modify
                row_list = list(data_row)

                # check "Elimination"
                if any(str(row_list[idx]).strip().lower() == 'yes' for idx in elimination_columns):
                    row_list[final_category_index] = 'Elimination'
                # check "Standardization"
                elif any(str(row_list[idx]).strip().lower() == 'yes' for idx in standardization_columns):
                    row_list[final_category_index] = 'Standardization'
                # check "Automation"
                elif (((str(row_list[resolved_type_index]).strip().lower()) == 'user') and ((str(row_list[bot_availability_index]).strip().lower()) == 'yes')):
                    row_list[final_category_index] = 'Automation'
                # check "Exploratory"
                else:
                    row_list[final_category_index] = 'Exploratory'

                # replace modified row
                to_be_processed_data[i] = tuple(row_list)
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '20', status = 'SUCCESS', message = f'For Account Total {int(len(to_be_processed_data))}-Rows Of Data Final Category Processed')
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '20', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '20', 'message' : str(error)}

        # re-order column for data insertion:S21
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "processed_data_insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0],  # ticket_number
                    data_row[3],  # assignment_group_category
                    data_row[6],  # resolved_type
                    data_row[20], # autoheal_category
                    data_row[21], # eso_analysis
                    data_row[22], # eso_category
                    data_row[23]  # final_category
                ))
                # appending data into "input_data_update_row" empty list
                input_data_update_row.append((
                    data_row[0], # ticket_number
                ))
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '21', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Prepared For Upsert Into "processed_incident_data" Table.')
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '21', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '21', 'message' : str(error)}

        # inserting normalize data into "processed_incident_data":S22
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_incident_data (
                ticket_number,
                assignment_group_category,
                resolved_type,
                autoheal_category,
                eso_analysis,
                eso_category,
                final_category
            )
            VALUES %s
            ON CONFLICT (ticket_number)
            DO UPDATE SET
                assignment_group_category   = EXCLUDED.assignment_group_category,
                resolved_type               = EXCLUDED.resolved_type,
                autoheal_category           = EXCLUDED.autoheal_category,
                eso_analysis                = EXCLUDED.eso_analysis,
                eso_category                = EXCLUDED.eso_category,
                final_category              = EXCLUDED.final_category;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '22', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_incident_data" Table.')
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '22', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '22', 'message' : str(error)}

        # updating "row_status" of "input_incident_data" to "11" after normalized data:S23
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_incident_data AS t
            SET row_status = 11,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(ticket_number)
            WHERE t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_row)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '23', status = 'SUCCESS', message = f'Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "11" Inside "input_incident_data" Table.')
        except Exception as error:
            log_writer(script_name = 'Incident-Final-Category-Analysis', steps = '23', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '23', 'message' : str(error)}

    # sending return message to main script:S24
    return {'status' : 'SUCCESS', 'file_name' : 'Incident-Final-Category-Analysis', 'step' : '24', 'message' : f'Total {total_count}-Rows Of Data Final Category Analysis Completed And Updated Into "input_incident_data" Table.'}