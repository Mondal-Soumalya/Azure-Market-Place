# define "service_desk_chip_analysis" function
def service_desk_chip_analysis(account_unique_id: str) -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
        import pandas as pd
        import re
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        service_desk_dump_handler_folder_path = Path(backend_folder_path) / 'ServiceDeskDumpHandler'
        others_analysis_folder_path = Path(service_desk_dump_handler_folder_path) / 'OthersAnalysis'
        support_script_folder_path = Path(others_analysis_folder_path) / 'SupportScript'
        reference_data_folder_path = Path(support_script_folder_path) / 'ReferenceData'
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '7', 'message' : str(error)}

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
                    log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '8', status = 'SUCCESS', message = '"input_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '8', status = 'ERROR', message = '"input_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '8', 'message' : '"input_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '8', 'message' : str(error)}

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
                    log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '9', status = 'SUCCESS', message = '"processed_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '9', status = 'ERROR', message = '"processed_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '9', 'message' : '"processed_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '9', 'message' : str(error)}

    # define "normalize_and_match" function:S10
    try:
        def normalize_and_match(df: pd.DataFrame, column: str, value: str):
            normalized_col = (
                df[column]
                .astype(str)
                .str.strip()
                .str.replace(r'[\s\W_/]+', '', regex=True)
                .str.lower()
            )
            normalized_value = re.sub(r'[\s\W_/]+', '', str(value).strip().lower())
            return normalized_col.eq(normalized_value)
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '10', 'message' : str(error)}

    # define constant
    total_count = 0
    buddybot_analysis_rows_limiter = int(str(environment_values.get('SERVICE_DESK_CHIP_ANALYSIS_BATCH')))

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
                psdd.opened_by,
                psdd.contact_type,
                psdd.resolved_by,
                psdd.ticket_created_by_chip,
                psdd.chip_zero_touch_ticket,
                psdd.chip_sap_automation_ticket,
                psdd.chip_human_touch_ticket
            FROM
                input_sd_data isdd
            JOIN
                processed_sd_data psdd
                ON isdd.account_unique_id = psdd.account_unique_id
                AND isdd.ticket_number = psdd.ticket_number
            WHERE
                isdd.account_unique_id = %s
                AND isdd.row_status = 11
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (str(account_unique_id), buddybot_analysis_rows_limiter))
                    to_be_processed_data = database_cursor.fetchall()
                    database_column_name = [database_field_name[0] for database_field_name in database_cursor.description]
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '11', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Fetched For Service-Desk-Chip-Analysis Process')
                    else:
                        log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '11', status = 'INFO', message = f'For Account: "{account_unique_id}" No New Rows Present For Service-Desk-Chip-Analysis Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '11', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '11', 'message' : str(error)}

        # convert data into pandas dataframe:S12
        try:
            ticket_dataframe = pd.DataFrame(to_be_processed_data, columns = database_column_name)
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '12', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Of Data Pandas Dataframe Created For Processing')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '12', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '12', 'message' : str(error)}

        # generate "ticket_created_by_chip" column:S13
        try:
            contact_type_mask_for_chip = normalize_and_match(ticket_dataframe, 'contact_type', 'chat')
            opened_by_mask_for_chip = normalize_and_match(ticket_dataframe, 'opened_by', 'dopintegration')
            ticket_dataframe['ticket_created_by_chip'] = (contact_type_mask_for_chip & opened_by_mask_for_chip).map({True: 'Yes', False: 'No'})
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '13', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Of Data Processed For Ticket Created By Chip')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '13', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '13', 'message' : str(error)}

        # generate "chip_zero_touch_ticket" column:S14
        try:
            resolved_by_mask_for_zero_touch = normalize_and_match(ticket_dataframe, 'resolved_by', 'dopintegration')
            ticket_dataframe['chip_zero_touch_ticket'] = (contact_type_mask_for_chip & opened_by_mask_for_chip & resolved_by_mask_for_zero_touch).map({True: 'Yes', False: 'No'})
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '14', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Of Data Processed For Chip Zero Touch Ticket')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '14', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '14', 'message' : str(error)}

        # generate "chip_sap_automation_ticket" column:S15
        try:
            resolved_by_mask_for_sap_automation = normalize_and_match(ticket_dataframe, 'resolved_by', 'asrengineer')
            ticket_dataframe['chip_sap_automation_ticket'] = (contact_type_mask_for_chip & opened_by_mask_for_chip & resolved_by_mask_for_sap_automation).map({True: 'Yes', False: 'No'})
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '15', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Of Data Processed For Chip SAP Automation Ticket')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '15', 'message' : str(error)}

        # generate "chip_human_touch_ticket" column:S16
        try:
            resolved_by_mask_for_human_touch = ~normalize_and_match(ticket_dataframe, 'resolved_by', 'asrengineer') & ~normalize_and_match(ticket_dataframe, 'resolved_by', 'dopintegration')
            ticket_dataframe['chip_human_touch_ticket'] = (contact_type_mask_for_chip & opened_by_mask_for_chip & resolved_by_mask_for_human_touch).map({True: 'Yes', False: 'No'})
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '16', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Of Data Processed For Chip Human Touch Ticket')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '16', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '16', 'message' : str(error)}

        # re-order column for data insertion:S17
        try:
            ticket_dataframe = ticket_dataframe[['account_unique_id', 'ticket_number', 'ticket_created_by_chip', 'chip_zero_touch_ticket', 'chip_sap_automation_ticket', 'chip_human_touch_ticket']]
            for _, row in ticket_dataframe.iterrows():
                # appending data into "processed_data_insert_rows"
                processed_data_insert_rows.append((
                    row['account_unique_id'],
                    row['ticket_number'],
                    row['ticket_created_by_chip'],
                    row['chip_zero_touch_ticket'],
                    row['chip_sap_automation_ticket'],
                    row['chip_human_touch_ticket']
                ))
                # appending data into "input_data_update_row"
                input_data_update_row.append((
                    row['account_unique_id'],
                    row['ticket_number']
                ))
            # deleting pandas dataframe to free memory
            del ticket_dataframe
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '17', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '17', 'message' : str(error)}

        # inserting normalized data into "processed_sd_data":S18
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_sd_data (
                account_unique_id,
                ticket_number,
                ticket_created_by_chip,
                chip_zero_touch_ticket,
                chip_sap_automation_ticket,
                chip_human_touch_ticket
            )
            VALUES %s
            ON CONFLICT (account_unique_id, ticket_number)
            DO UPDATE SET
                ticket_created_by_chip     = EXCLUDED.ticket_created_by_chip,
                chip_zero_touch_ticket     = EXCLUDED.chip_zero_touch_ticket,
                chip_sap_automation_ticket = EXCLUDED.chip_sap_automation_ticket,
                chip_human_touch_ticket    = EXCLUDED.chip_human_touch_ticket;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '18', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_sd_data" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '18', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '18', 'message' : str(error)}

        # updating "row_status" of "input_sd_data" to "12" after normalized data:S19
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_sd_data AS t
            SET row_status = 12,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(account_unique_id, ticket_number)
            WHERE t.account_unique_id = v.account_unique_id
            AND t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_row)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '19', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "12" Inside "input_sd_data" Table')
                    total_count += int(len(to_be_processed_data))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Chip-Analysis', steps = '19', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '19', 'message' : str(error)}

    # sending return message to main script:S20
    return {'status' : 'SUCCESS', 'file_name' : 'Service-Desk-Chip-Analysis', 'step' : '20', 'message' : f'For Account: "{account_unique_id}" Total {total_count}-Rows Of CHIP Analysis Completed And Updated Into "input_sd_data" Table'}