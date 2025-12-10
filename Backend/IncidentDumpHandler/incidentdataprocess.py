# define "incident_data_process" function
def incident_data_process(file_unique_id: str, file_path: str):
    # define constant
    INCIDENT_DATA_COLUMN_PROCESS_COMPLETE_STATUS = False
    INCIDENT_DATA_FILE_TO_DB_PROCESS_COMPLETE_STATUS = False
    INCIDENT_DATA_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = False
    INCIDENT_DATA_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = False
    INCIDNET_DATA_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = False
    INCIDENT_DATA_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = False
    INCIDENT_DATA_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = False
    INCIDENT_DATA_ESOAR_ANALYSIS_PROCESS_COMPLETE_STATUS = False

    # importing python module:S1
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        import time
    except Exception as error:
        print(f'ERROR - [Incident-Data-Process:S1] - {str(error)}')

    # appending system path:S2
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        print(f'ERROR - [Incident-Data-Process:S2] - {str(error)}')

    # importing user define function:S3
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        print(f'ERROR - [Incident-Data-Process:S3] - {str(error)}')

    # define folder and file path:S4
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        log_writer(script_name = 'Incident-Data-Process', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Data-Process', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Data-Process', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S5
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-Data-Process', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-Data-Process', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Data-Process', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Data-Process', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Data-Process', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S6
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-Data-Process', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-Data-Process', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Data-Process', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S7
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-Data-Process', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Data-Process', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Data-Process', 'step' : '7', 'message' : str(error)}

    # check if "submitted_file_details" table present inside database:S8
    try:
        submitted_file_details_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'submitted_file_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(submitted_file_details_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Incident-Data-Process', steps = '8', status = 'SUCCESS', message = '"submitted_file_details" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Data-Process', steps = '8', status = 'ERROR', message = '"submitted_file_details" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Data-Process', 'step' : '8', 'message' : '"submitted_file_details" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Data-Process', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Data-Process', 'step' : '8', 'message' : str(error)}

    # check if "file_process_status" table present inside database:S9
    try:
        file_process_status_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'file_process_status'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(file_process_status_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Incident-Data-Process', steps = '9', status = 'SUCCESS', message = '"file_process_status" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Data-Process', steps = '9', status = 'ERROR', message = '"file_process_status" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Data-Process', 'step' : '9', 'message' : '"file_process_status" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Data-Process', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Data-Process', 'step' : '9', 'message' : str(error)}

    ##### starting column mapping backend process:S10 #####
    # importing "incident_column_process" function:S10-A
    try:
        from Backend.IncidentDumpHandler.FileProcess.incidentcolumnprocess import incident_column_process
    except Exception as error:
        log_writer(script_name = 'Incident-Data-Process', steps = '10-A', status = 'ERROR', message = str(error))

    # calling "incident_column_process" function to validate file:S10-B
    try:
        incident_column_mapping_process_start_time = time.time()
        incident_column_process_backend_response = incident_column_process(file_path = str(file_path))
        if (incident_column_process_backend_response != None):
            log_writer(script_name = 'Incident-Data-Process', steps = '10-B', status = 'INFO', message = f'For File: "{Path(file_path).name}" Column Name Mapping Backend Process Response Generate')
        incident_column_mapping_process_end_time = time.time()
    except Exception as error:
        log_writer(script_name = 'Incident-Data-Process', steps = '10-B', status = 'ERROR', message = str(error))

    # check the result for "ERROR":S10-D
    if (str(incident_column_process_backend_response['status']).lower() == 'error'):
        try:
            INCIDENT_DATA_COLUMN_PROCESS_COMPLETE_STATUS = False
            # converting "file_path" to Path object
            file_path_object = Path(file_path)
            # delete "file_path"
            file_path_object.unlink()
            log_writer(script_name = str(incident_column_process_backend_response['file_name']), steps = str(incident_column_process_backend_response['step']), status = 'ERROR', message = incident_column_process_backend_response['message'])
            log_writer(script_name = 'Incident-Data-Process', steps = '10-D', status = 'ERROR', message = f'Submitted File: "{file_path_object.name}" Deleted Because Column Mapping Not Complete')
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '10-D', status = 'ERROR', message=str(error))

    # check the result for "INFO":S10-E
    if (str(incident_column_process_backend_response['status']).lower() == 'info'):
        try:
            column_process_description = f"Column Mapping Process Complete, but we found {', '.join([f'{i+1}){col}' for i, col in enumerate(incident_column_process_backend_response['missing_columns'])])} these column(s) are missing from the file."
            elapsed_seconds = int((incident_column_mapping_process_end_time - incident_column_mapping_process_start_time) % 60) #type: ignore
            file_process_status_insert_sql = '''
            INSERT INTO file_process_status (
                file_unique_id,
                process_name,
                process_description,
                completion_time_seconds
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Column Mapping', str(column_process_description), int(elapsed_seconds)))
                    insert_id_result = database_cursor.fetchone()
                    # check if data inserted or not
                    if ((insert_id_result is None) or (insert_id_result[0] is None)):
                        INCIDENT_DATA_COLUMN_PROCESS_COMPLETE_STATUS = False
                        database_connection.rollback()
                        log_writer(script_name = 'Incident-Data-Process', steps = '10-E', status = 'ERROR', message = f'Column Mapping Process Not Completed For File: "{Path(file_path).name}"')
                    else:
                        INCIDENT_DATA_COLUMN_PROCESS_COMPLETE_STATUS = True
                        database_connection.commit()
                        log_writer(script_name = 'Incident-Data-Process', steps = '10-E', status = 'SUCCESS', message = f'Column Mapping Process Completed For File: "{Path(file_path).name}" With Some Missing Column')
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '10-E', status = 'ERROR', message = str(error))

    # check the result for "SUCCESS":S10-F
    if (str(incident_column_process_backend_response['status']).lower() == 'success'):
        try:
            column_process_description = 'Standardizing column names and formats for consistency.'
            elapsed_seconds = int((incident_column_mapping_process_end_time - incident_column_mapping_process_start_time) % 60) #type: ignore
            file_process_status_insert_sql = '''
            INSERT INTO file_process_status (
                file_unique_id,
                process_name,
                process_description,
                completion_time_seconds
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Column Mapping', str(column_process_description), int(elapsed_seconds)))
                    insert_id_result = database_cursor.fetchone()
                    # check if data inserted or not
                    if ((insert_id_result is None) or (insert_id_result[0] is None)):
                        INCIDENT_DATA_COLUMN_PROCESS_COMPLETE_STATUS = False
                        database_connection.rollback()
                        log_writer(script_name = 'Incident-Data-Process', steps = '10-F', status = 'ERROR', message = f'Column Mapping Process Not Completed For File: "{Path(file_path).name}"')
                    else:
                        INCIDENT_DATA_COLUMN_PROCESS_COMPLETE_STATUS = True
                        database_connection.commit()
                        log_writer(script_name = 'Incident-Data-Process', steps = '10-F', status = 'SUCCESS', message = f'Column Mapping Process Completed For File: "{Path(file_path).name}" and all the required column(s) are present')
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '10-F', status = 'ERROR', message = str(error))
    ####################################################

    ##### starting excel to db transfering process:S11 #####
    if (INCIDENT_DATA_COLUMN_PROCESS_COMPLETE_STATUS):
        # importing "incident_file_to_db" function:S11-A
        try:
            from Backend.IncidentDumpHandler.FileProcess.incidentfiletodb import incident_file_to_db
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '11-A', status = 'ERROR', message = str(error))

        # calling "incident_file_to_db" function:S11-B
        try:
            incident_file_to_db_process_start_time = time.time()
            incident_data_file_to_db_backend_response = incident_file_to_db(file_unique_id = str(file_unique_id), file_path = str(incident_column_process_backend_response['file_path']))
            if (incident_data_file_to_db_backend_response != None):
                log_writer(script_name = 'Incident-Data-Process', steps = '11-B', status = 'INFO', message = f'For File: "{Path(file_path).name}" File To DB Backend Porcess Response Generate')
            incident_file_to_db_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '11-B', status = 'ERROR', message = str(error))

        # check the result for "ERROR":S11-C
        try:
            if (str(incident_data_file_to_db_backend_response['status']).lower() == 'error'):
                INCIDENT_DATA_FILE_TO_DB_PROCESS_COMPLETE_STATUS =False
                # converting "file_path" to Path object
                file_path_object = Path(file_path)
                # delete "file_path"
                file_path_object.unlink()
                log_writer(script_name = str(incident_data_file_to_db_backend_response['file_name']), steps = str(incident_data_file_to_db_backend_response['step']), status = 'ERROR', message = str(incident_data_file_to_db_backend_response['message']))
                log_writer(script_name = 'Incident-Data-Process', steps = '11-C', status = 'SUCCESS', message = f'Submitted File: "{file_path_object.name}" Deleted Because Data Process Not Complete')
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '11-C', status = 'ERROR', message = str(error))

        # check the result for "SUCCESS":
        if (str(incident_data_file_to_db_backend_response['status']).lower() == 'success'):
            # inserting value into "file_process_status" table:S11-D
            try:
                elapsed_seconds = int((incident_file_to_db_process_end_time - incident_file_to_db_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'File To DB', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            INCIDENT_DATA_FILE_TO_DB_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Incident-Data-Process', steps = '11-D', status = 'ERROR', message = f'File To DB Process Not Completed For File: "{Path(file_path).name}"')
                        else:
                            INCIDENT_DATA_FILE_TO_DB_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Incident-Data-Process', steps = '11-D', status = 'SUCCESS', message = f'File To DB Process Completed For File: "{Path(file_path).name}"')
            except Exception as error:
                log_writer(script_name = 'Incident-Data-Process', steps = '11-D', status = 'ERROR', message = str(error))
    ######################################################

    ##### starting output data fill backend process:S12 ######
    if (INCIDENT_DATA_FILE_TO_DB_PROCESS_COMPLETE_STATUS):
        # importing "incident_output_data_fill" function:S12-A
        try:
            from Backend.IncidentDumpHandler.DataProcess.incidentoutputdatafill import incident_output_data_fill
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '12-A', status = 'ERROR', message = str(error))

        # calling "incident_output_data_fill" function:S12-B
        try:
            incident_output_data_fill_process_start_time = time.time()
            incident_output_data_fill_backend_response = incident_output_data_fill()
            if (incident_output_data_fill_backend_response != None):
                log_writer(script_name = 'Incident-Data-Process', steps = '12-B', status = 'INFO', message = f'For Account Output Table Data Fill Backend Process Response Generate')
            incident_output_data_fill_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '12-B', status = 'ERROR', message = str(error))

        # check the result for "ERROR":S12-C
        try:
            if (str(incident_output_data_fill_backend_response['status']).lower() == 'error'):
                INCIDENT_DATA_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(incident_output_data_fill_backend_response['file_name']), steps = str(incident_output_data_fill_backend_response['step']), status = 'ERROR', message = str(incident_output_data_fill_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '12-C', status = 'ERROR', message = str(error))

        # check the result for "SUCCESS":S12-D
        if (str(incident_output_data_fill_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((incident_output_data_fill_process_end_time - incident_output_data_fill_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Output Data Fill', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            INCIDENT_DATA_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Incident-Data-Process', steps = '12-D', status = 'ERROR', message = f'For Account Output Data Fill Process Not Completed')
                        else:
                            INCIDENT_DATA_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Incident-Data-Process', steps = '12-D', status = 'SUCCESS', message = f'For Account Output Data Fill Process Completed')
            except Exception as error:
                log_writer(script_name = 'Incident-Data-Process', steps = '12-D', status = 'ERROR', message = str(error))
    ######################################################

    #### starting data normalization backend process:S13 #####
    if (INCIDENT_DATA_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS):
        # importing "incident_normalized_data" function:S13-A
        try:
            from Backend.IncidentDumpHandler.DataProcess.incidentnormalizeddata import incident_normalized_data
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '13-A', status = 'ERROR', message = str(error))

        # calling "incident_normalized_data" function:S13-B
        try:
            data_normalization_process_start_time = time.time()
            normalized_data_backend_response = incident_normalized_data()
            if (normalized_data_backend_response != None):
                log_writer(script_name = 'Incident-Data-Process', steps = '13-B', status = 'INFO', message = f'For Account Data Normalization Backend Process Response Generate')
            data_normalization_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '13-B', status = 'ERROR', message = str(error))

        # check the result for "ERROR":S13-C
        try:
            if (str(normalized_data_backend_response['status']).lower() == 'error'):
                INCIDENT_DATA_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(normalized_data_backend_response['file_name']), steps = str(normalized_data_backend_response['step']), status = 'ERROR', message = str(normalized_data_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '13-C', status = 'ERROR', message = str(error))

        # check the result for "SUCCESS":S13-D
        if (str(normalized_data_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((data_normalization_process_end_time - data_normalization_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Data Normalization', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            INCIDENT_DATA_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Incident-Data-Process', steps = '13-D', status = 'ERROR', message = f'For Account Data Normalization Process Not Completed')
                        else:
                            INCIDENT_DATA_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Incident-Data-Process', steps = '13-D', status = 'SUCCESS', message = f'For Account Data Normalization Process Completed')
            except Exception as error:
                log_writer(script_name = 'Incident-Data-Process', steps = '13-D', status = 'ERROR', message = str(error))
    ######################################################

    ##### starting information clean backend process:S14 #####
    if (INCIDENT_DATA_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS):
        # importing "incident_information_clean" function:S14-A
        try:
            from Backend.IncidentDumpHandler.DataProcess.incidentinformationclean import incident_information_clean
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '14-A', status = 'ERROR', message = str(error))

        # calling "incident_information_clean" function:S14-B
        try:
            information_clean_process_start_time = time.time()
            information_clean_backend_response = incident_information_clean()
            if (information_clean_backend_response != None):
                log_writer(script_name = 'Incident-Data-Process', steps = '14-B', status = 'SUCCESS', message = f'For Account Information Clean Process Backend Response Generated')
            information_clean_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '14-B', status = 'ERROR', message = str(error))

        # check the result for "ERROR":S14-C
        try:
            if (str(information_clean_backend_response['status']).lower() == 'error'):
                INCIDNET_DATA_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(information_clean_backend_response['file_name']), steps = str(information_clean_backend_response['step']), status = 'ERROR', message = str(information_clean_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '14-C', status = 'ERROR', message = str(error))

        # check the result for "SUCCESS":S14-D
        if (str(information_clean_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((information_clean_process_end_time - information_clean_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Information Cleaning', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            INCIDNET_DATA_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Incident-Data-Process', steps = '14-D', status = 'ERROR', message = f'For Account Information Clean Process Not Completed')
                        else:
                            INCIDNET_DATA_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Incident-Data-Process', steps = '14-D', status = 'SUCCESS', message = f'For Account Information Clean Process Completed')
            except Exception as error:
                log_writer(script_name = 'Incident-Data-Process', steps = '14-D', status = 'ERROR', message = str(error))
    ######################################################

    ##### starting keywords analysis backend process:S15 #####
    if (INCIDNET_DATA_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS):
        # importing "incident_keyword_analysis" function:S15-A
        try:
            from Backend.IncidentDumpHandler.TicketAnalysis.incidentkeywordanalysis import incident_keyword_analysis
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '15-A', status = 'ERROR', message = str(error))

        # calling "incident_keyword_analysis" function:S15-B
        try:
            keyword_analysis_process_start_time = time.time()
            keywords_analysis_backend_response = incident_keyword_analysis()
            if (keywords_analysis_backend_response != None):
                log_writer(script_name = 'Incident-Data-Process', steps = '15-B', status = 'INFO', message = f'For Account Keyword Analysis Backend Process Response Generate')
            keyword_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '15-B', status = 'ERROR', message = str(error))

        # check the result for "ERROR":S15-C
        try:
            if (str(keywords_analysis_backend_response['status']).lower() == 'error'):
                INCIDENT_DATA_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(keywords_analysis_backend_response['file_name']), steps = str(keywords_analysis_backend_response['step']), status = 'ERROR', message = str(keywords_analysis_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '15-C', status = 'ERROR', message = str(error))

        # check the result for "SUCCESS":S15-D
        if (str(keywords_analysis_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((keyword_analysis_process_end_time - keyword_analysis_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Keywords Analysis', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            INCIDENT_DATA_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Incident-Data-Process', steps = '15-D', status = 'ERROR', message = f'For Account Keywords Analysis Process Not Completed')
                        else:
                            INCIDENT_DATA_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Incident-Data-Process', steps = '15-D', status = 'SUCCESS', message = f'For Account Keywords Analysis Process Completed')
            except Exception as error:
                log_writer(script_name = 'Incident-Data-Process', steps = '15-D', status = 'ERROR', message = str(error))
    ######################################################

    #### starting automation mapping backend process:S16 #####
    if (INCIDENT_DATA_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "incident_automation_mapping" function:S16-A
        try:
            from Backend.IncidentDumpHandler.TicketAnalysis.incidentautomationmapping import incident_automation_mapping
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '16-A', status = 'ERROR', message = str(error))

        # calling "incident_automation_mapping" function:S16-B
        try:
            automation_mapping_process_start_time = time.time()
            automation_mapping_backend_response = incident_automation_mapping()
            if (automation_mapping_backend_response != None):
                log_writer(script_name = 'Incident-Data-Process', steps = '16-B', status = 'INFO', message = f'For Account Automation Mapping Backend Process Response Generate')
            automation_mapping_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '16-B', status = 'ERROR', message = str(error))

        # check the result for "ERROR":S16-C
        try:
            if (str(automation_mapping_backend_response['status']).lower() == 'error'):
                INCIDENT_DATA_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(automation_mapping_backend_response['file_name']), steps = str(automation_mapping_backend_response['step']), status = 'ERROR', message = str(automation_mapping_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '16-C', status = 'ERROR', message = str(error))

        # check the result for "SUCCESS":S16-D
        if (str(automation_mapping_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((automation_mapping_process_end_time - automation_mapping_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Automation Mapping', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            INCIDENT_DATA_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Incident-Data-Process', steps = '16-D', status = 'ERROR', message = f'For Account Automation Mapping Process Not Completed')
                        else:
                            INCIDENT_DATA_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Incident-Data-Process', steps = '16-D', status = 'SUCCESS', message = f'For Account Automation Mapping Process Completed')
            except Exception as error:
                log_writer(script_name = 'Incident-Data-Process', steps = '16-D', status = 'ERROR', message = str(error))
    ######################################################

    ##### starting "incident_esoar_process" backend process:S17 #####
    if (INCIDENT_DATA_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS):
        # importing "incident_esoar_process" fucntion:S17-A
        try:
            from Backend.IncidentDumpHandler.ESOARAnalysis.incidentesoarprocess import incident_esoar_process
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '17-A', status = 'ERROR', message = str(error))

        # calling "incident_esoar_process" function:S17-B
        try:
            esoar_analysis_function_response = incident_esoar_process(file_unique_id = str(file_unique_id))
            if (esoar_analysis_function_response != None):
                log_writer(script_name = 'Incident-Data-Process', steps = '17-B', status = 'INFO', message = f'For Account ESO Analysis Backend Process Response Generate')
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '17-B', status = 'ERROR', message = str(error))

        # check the result for "ERROR":S17-C
        try:
            if (str(esoar_analysis_function_response['status']).lower() == 'error'):
                INCIDENT_DATA_ESOAR_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(esoar_analysis_function_response['file_name']), steps = str(esoar_analysis_function_response['step']), status = 'ERROR', message = str(esoar_analysis_function_response['message']))
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '17-C', status = 'ERROR', message = str(error))

        # check the result for "SUCCESS":S17-D
        try:
            if (str(esoar_analysis_function_response['status']).lower() == 'success'):
                INCIDENT_DATA_ESOAR_ANALYSIS_PROCESS_COMPLETE_STATUS = True
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '17-D', status = 'ERROR', message = str(error))
    #####################################################

    # updating final "process_name" and "completion_time_seconds" inside "file_process_status":S18
    if (INCIDENT_DATA_ESOAR_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # fetching total "completion_time_seconds":S18-A
        try:
            fetch_process_total_completion_seconds_sql = '''
            SELECT SUM(completion_time_seconds) AS total_completion_seconds
            FROM file_process_status
            WHERE file_unique_id = %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_process_total_completion_seconds_sql, (str(file_unique_id),))
                    all_process_total_completion_seconds = database_cursor.fetchone()[0]
                    # check result
                    if ((all_process_total_completion_seconds is not None) and (int(all_process_total_completion_seconds) > 0)):
                        log_writer(script_name = 'Incident-Data-Process', steps = '18-A', status = 'SUCCESS', message = f'For Account: "{file_unique_id}" All Process Completion Seconds Fetched')
                    else:
                        log_writer(script_name = 'Incident-Data-Process', steps = '18-A', status = 'ERROR', message = f'For Account: "{file_unique_id}" All Process Completion Seconds Not Fetched')
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '18-A', status = 'ERROR', message = str(error))

        # updating "process_name" to "Analysis Complete":S18-B
        try:
            file_process_status_insert_sql = '''
            INSERT INTO file_process_status (
                file_unique_id,
                process_name,
                completion_time_seconds
            )
            VALUES (%s, %s, %s)
            RETURNING id;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Analysis Complete', int(all_process_total_completion_seconds)))
                    insert_id_result = database_cursor.fetchone()
                    # check if data inserted or not
                    if ((insert_id_result is None) or (insert_id_result[0] is None)):
                        database_connection.rollback()
                        log_writer(script_name = 'Incident-Data-Process', steps = '18-B', status = 'ERROR', message = f'For Account Whole Analysis Complete')
                    else:
                        database_connection.commit()
                        log_writer(script_name = 'Incident-Data-Process', steps = '18-B', status = 'SUCCESS', message = f'For Account Whole Analysis Not Completed')
        except Exception as error:
            log_writer(script_name = 'Incident-Data-Process', steps = '18-B', status = 'ERROR', message = str(error))
    #####################################################