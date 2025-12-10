# define "incident_esoar_process" function
# def incident_esoar_process(account_unique_id: str, ticket_number: str, ticket_sys_id: str) -> dict[str, str]: #type: ignore
def incident_esoar_process(account_unique_id: str, file_unique_id: str, user_unique_id: str) -> dict[str, str]: #type: ignore
    # define constant
    MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = False
    ELIMINATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
    STANDARDIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
    OPTIMIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False

    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        import time
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '2', 'message' : str(error)}

    # importing user define function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
        # from Backend.SnowHandler.createworknotes import create_worknotes
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '7', 'message' : str(error)}

    # check if "file_process_status" table present inside database:S08
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
                    log_writer(script_name = 'Incident-ESOAR-Process', steps = '8', status = 'SUCCESS', message = '"file_process_status" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-ESOAR-Process', steps = '8', status = 'ERROR', message = '"file_process_status" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '8', 'message' : '"file_process_status" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '8', 'message' : str(error)}

    #### starting mttr and aging analysis backend process:S09 #####
    # importing "incident_mttr_aging_analysis" function:S09-A
    try:
        from Backend.IncidentDumpHandler.ESOARAnalysis.SupportScript.incidentmttrandaginganalysis import incident_mttr_aging_analysis
    except Exception as error:
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '9-A', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '9-A', 'message' : str(error)}

    # calling "incident_mttr_aging_analysis" function:S09-B
    try:
        mttr_aging_analysis_process_start_time = time.time()
        mttr_aging_analysis_backend_response = incident_mttr_aging_analysis(account_unique_id = str(account_unique_id))
        if (mttr_aging_analysis_backend_response != None):
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '9-B', status = 'INFO', message = f'For Account: "{account_unique_id}" MTTR And Aging Backend Process Response Generate')
        mttr_aging_analysis_process_end_time = time.time()
    except Exception as error:
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '9-B', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '9-B', 'message' : str(error)}

    # check the result for "ERROR":S09-C
    try:
        if (str(mttr_aging_analysis_backend_response['status']).lower() == 'error'):
            MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = False
            return {'status' : 'ERROR', 'file_name' : str(mttr_aging_analysis_backend_response['file_name']), 'step' : str(mttr_aging_analysis_backend_response['step']), 'message' : str(mttr_aging_analysis_backend_response['message'])}
    except Exception as error:
        log_writer(script_name = 'Incident-ESOAR-Process', steps = '9-C', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '9-C', 'message' : str(error)}

    # check the result for "SUCCESS":S09-D
    if (str(mttr_aging_analysis_backend_response['status']).lower() == 'success'):
        try:
            elapsed_seconds = int((mttr_aging_analysis_process_end_time - mttr_aging_analysis_process_start_time) % 60) #type: ignore
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
                    database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'MTTR Analysis', int(elapsed_seconds)))
                    insert_id_result = database_cursor.fetchone()
                    # check if data inserted or not
                    if ((insert_id_result is None) or (insert_id_result[0] is None)):
                        MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                        database_connection.rollback()
                        return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '9-D', 'message' : f'For Account: "{account_unique_id}" MTTR Analysis Process Not Completed'}
                    else:
                        MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                        database_connection.commit()
                        log_writer(script_name = 'Incident-ESOAR-Process', steps = '9-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" MTTR Analysis Process Completed')
            # elapsed_seconds = int((mttr_aging_analysis_process_end_time - mttr_aging_analysis_process_start_time) % 60) #type: ignore
            # elapsed_minutes = int(((mttr_aging_analysis_process_end_time - mttr_aging_analysis_process_start_time) % 3600) // 60) #type: ignore
            # elapsed_hours = int((mttr_aging_analysis_process_end_time - mttr_aging_analysis_process_start_time) // 3600) #type: ignore
            # # define servicenow worknotes
            # work_notes = '~' * 33 + ' Step : 7 [MTTR And Aging Analysis] ' + '~' * 33 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : MTTR And Aging Analysis\n• Upcoming Procss : Elimination Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
            # # calling "create_worknotes" function
            # mttr_aging_analysis_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
            # # check the response
            # if (((mttr_aging_analysis_create_worknotes_backend_response) != None) and (str(mttr_aging_analysis_create_worknotes_backend_response['status']).lower() == 'success')):
            #     MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = True
            #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '9-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed And Worknotes Updated Into SerivceNow')
            # else:
            #     MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = False
            #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '9-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed But Worknotes Not Updated In ServiceNow')
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '9-D', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '9-D', 'message' : str(error)}
    ######################################################

    #### starting elimination analysis backend process:S10 #####
    if (MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "incident_elimination_analysis" function:S10-A
        try:
            from Backend.IncidentDumpHandler.ESOARAnalysis.SupportScript.incidenteliminationanalysis import incident_elimination_analysis
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '10-A', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '10-A', 'message' : str(error)}

        # calling "incident_elimination_analysis" function:S10-B
        try:
            elimination_analysis_process_start_time = time.time()
            elimination_analysis_backend_process = incident_elimination_analysis(account_unique_id = str(account_unique_id))
            if (elimination_analysis_backend_process != None):
                log_writer(script_name = 'Incident-ESOAR-Process', steps = '10-B', status = 'INFO', message = f'For Account: "{account_unique_id}" Elimination Analysis Backend Process Response Generate')
            elimination_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '10-B', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '10-B', 'message' : str(error)}

        # check the result for "ERROR":S10-C
        try:
            if (str(elimination_analysis_backend_process['status']).lower() == 'error'):
                ELIMINATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                return {'status' : 'ERROR', 'file_name' : str(elimination_analysis_backend_process['file_name']), 'step' : str(elimination_analysis_backend_process['step']), 'message' : str(elimination_analysis_backend_process['message'])}
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '10-C', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '10-C', 'message' : str(error)}

        # check the result for "SUCCESS":S10-D
        if (str(elimination_analysis_backend_process['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((elimination_analysis_process_end_time - elimination_analysis_process_start_time) % 60) #type: ignore
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
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Elimination Analysis', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            ELIMINATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '10-D', 'message' : f'For Account: "{account_unique_id}" Elimination Analysis Process Not Completed'}
                        else:
                            ELIMINATION_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Incident-ESOAR-Process', steps = '10-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Elimination Analysis Process Completed')
                # elapsed_seconds = int((elimination_analysis_process_end_time - elimination_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((elimination_analysis_process_end_time - elimination_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((elimination_analysis_process_end_time - elimination_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 35 + ' Step : 8 [Elimination Analysis] ' + '~' * 34 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Elimination Analysis\n• Upcoming Procss : Standardization Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # mttr_aging_analysis_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
                # # check the response
                # if (((mttr_aging_analysis_create_worknotes_backend_response) != None) and (str(mttr_aging_analysis_create_worknotes_backend_response['status']).lower() == 'success')):
                #     ELIMINATION_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '10-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Elimination Analysis Process Completed And Worknotes Updated Into SerivceNow')
                # else:
                #     ELIMINATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '10-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Elimination Analysis Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Incident-ESOAR-Process', steps = '10-D', status = 'ERROR', message = str(error))
                return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '10-D', 'message' : str(error)}
    ######################################################

    #### starting standardization analysis backend process:S11 #####
    if (ELIMINATION_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "incident_standardization_analysis" function:S11-A
        try:
            from Backend.IncidentDumpHandler.ESOARAnalysis.SupportScript.incidentstandardizationanalysis import incident_standardization_analysis
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '11-A', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '11-A', 'message' : str(error)}

        # calling "incident_standardization_analysis" function:S11-B
        try:
            standardization_analysis_process_start_time = time.time()
            standardization_analysis_backend_process = incident_standardization_analysis(account_unique_id = str(account_unique_id))
            if (standardization_analysis_backend_process != None):
                log_writer(script_name = 'Incident-ESOAR-Process', steps = '11-B', status = 'INFO', message = f'For Account: "{account_unique_id}" Standardization Analysis Backend Process Response Generate')
            standardization_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '11-B', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '11-B', 'message' : str(error)}

        # check the result for "ERROR":S11-C
        try:
            if (str(standardization_analysis_backend_process['status']).lower() == 'error'):
                STANDARDIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                return {'status' : 'ERROR', 'file_name' : str(standardization_analysis_backend_process['file_name']), 'step' : str(standardization_analysis_backend_process['step']), 'message' : str(standardization_analysis_backend_process['message'])}
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '11-C', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '11-C', 'message' : str(error)}

        # check the result for "SUCCESS":S11-D
        if (str(standardization_analysis_backend_process['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((standardization_analysis_process_end_time - standardization_analysis_process_start_time) % 60) #type: ignore
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
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Standardization Analysis', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            STANDARDIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '11-D', 'message' : f'For Account: "{account_unique_id}" Standardization Analysis Process Not Completed'}
                        else:
                            STANDARDIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Incident-ESOAR-Process', steps = '11-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Standardization Analysis Process Completed')
                # elapsed_seconds = int((standardization_analysis_process_end_time - standardization_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((standardization_analysis_process_end_time - standardization_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((standardization_analysis_process_end_time - standardization_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 34 + ' Step : 9 [Standardization Analysis] ' + '~' * 34 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Standardization Analysis\n• Upcoming Procss : Optimization Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # standardization_analysis_create_worknotes_backend_process = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
                # # check the response
                # if (((standardization_analysis_create_worknotes_backend_process) != None) and (str(standardization_analysis_create_worknotes_backend_process['status']).lower() == 'success')):
                #     STANDARDIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '11-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Standardization Analysis Process Completed And Worknotes Updated Into SerivceNow')
                # else:
                #     STANDARDIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '11-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Standardization Analysis Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Incident-ESOAR-Process', steps = '11-D', status = 'ERROR', message = str(error))
                return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '11-D', 'message' : str(error)}
    ######################################################

    #### starting optmization analysis backend process:S12 #####
    if (STANDARDIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "incident_optimization_analysis" function:S12-A
        try:
            from Backend.IncidentDumpHandler.ESOARAnalysis.SupportScript.incidentoptimizationanalysis import incident_optimization_analysis
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '12-A', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '12-A', 'message' : str(error)}

        # calling "incident_optimization_analysis" function:S12-B
        try:
            optimization_analysis_process_start_time = time.time()
            optimization_analysis_backend_process = incident_optimization_analysis(account_unique_id = str(account_unique_id))
            if (optimization_analysis_backend_process != None):
                log_writer(script_name = 'Incident-ESOAR-Process', steps = '12-B', status = 'INFO', message = f'For Account: "{account_unique_id}" Optimization Analysis Backend Process Response Generate')
            optimization_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '12-B', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '12-B', 'message' : str(error)}

        # check the result for "ERROR":S12-C
        try:
            if (str(optimization_analysis_backend_process['status']).lower() == 'error'):
                OPTIMIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                return {'status' : 'ERROR', 'file_name' : str(optimization_analysis_backend_process['file_name']), 'step' : str(optimization_analysis_backend_process['step']), 'message' : str(optimization_analysis_backend_process['message'])}
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '12-C', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '12-C', 'message' : str(error)}

        # check the result for "SUCCESS":S12-D
        if (str(optimization_analysis_backend_process['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((optimization_analysis_process_end_time - optimization_analysis_process_start_time) % 60) #type: ignore
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
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Optimization Analysis', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            OPTIMIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '12-D', 'message' : f'For Account: "{account_unique_id}" Optimization Analysis Process Not Completed'}
                        else:
                            OPTIMIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Incident-ESOAR-Process', steps = '12-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Optimization Analysis Process Completed')
                # elapsed_seconds = int((optimization_analysis_process_end_time - optimization_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((optimization_analysis_process_end_time - optimization_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((optimization_analysis_process_end_time - optimization_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 35 + ' Step : 10 [Optimization Analysis] ' + '~' * 35 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Optimization Analysis\n• Upcoming Procss : Final Category Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # optimization_analysis_create_worknotes_backend_process = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
                # # check the response
                # if (((optimization_analysis_create_worknotes_backend_process) != None) and (str(optimization_analysis_create_worknotes_backend_process['status']).lower() == 'success')):
                #     OPTIMIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '12-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Optimization Analysis Process Completed And Worknotes Updated Into SerivceNow')
                # else:
                #     OPTIMIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '12-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Optimization Analysis Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Incident-ESOAR-Process', steps = '12-D', status = 'ERROR', message = str(error))
                return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '12-D', 'message' : str(error)}
    ######################################################

    #### starting final-category analysis backend process:S13 #####
    if (OPTIMIZATION_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "incident_final_category_analysis" function:S13-A
        try:
            from Backend.IncidentDumpHandler.ESOARAnalysis.SupportScript.incidentfinalcategoryanalysis import incident_final_category_analysis
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '13-A', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '13-A', 'message' : str(error)}

        # calling "incident_final_category_analysis" function:S13-B
        try:
            final_category_analysis_process_start_time = time.time()
            final_category_analysis_backend_process = incident_final_category_analysis(account_unique_id = str(account_unique_id))
            if (final_category_analysis_backend_process != None):
                log_writer(script_name = 'Incident-ESOAR-Process', steps = '13-B', status = 'INFO', message = f'For Account: "{account_unique_id}" Final Categroy Analysis Backend Process Response Generate')
            final_category_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '13-B', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '13-B', 'message' : str(error)}

        # check the result for "ERROR":S13-C
        try:
            if (str(final_category_analysis_backend_process['status']).lower() == 'error'):
                return {'status' : 'ERROR', 'file_name' : str(final_category_analysis_backend_process['file_name']), 'step' : str(final_category_analysis_backend_process['step']), 'message' : str(final_category_analysis_backend_process['message'])}
        except Exception as error:
            log_writer(script_name = 'Incident-ESOAR-Process', steps = '13-C', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '13-C', 'message' : str(error)}

        # check the result for "SUCCESS":S13-D
        if (str(final_category_analysis_backend_process['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((final_category_analysis_process_end_time - final_category_analysis_process_start_time) % 60) #type: ignore
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
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Final Category Analysis', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            database_connection.rollback()
                            return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '13-D', 'message' : f'For Account: "{account_unique_id}" Final Category Analysis Process Not Completed'}
                        else:
                            database_connection.commit()
                            log_writer(script_name = 'Incident-ESOAR-Process', steps = '13-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Final Category Analysis Process Completed')
                            return {'status' : 'SUCCESS', 'file_name' : 'Incident-ESOAR-Process', 'step' : '13-D', 'message' : f'For Account: "{account_unique_id}" Final Category Analysis Process Completed'}
                # elapsed_seconds = int((final_category_analysis_process_end_time - final_category_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((final_category_analysis_process_end_time - final_category_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((final_category_analysis_process_end_time - final_category_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 34 + ' Step : 11 [Final Categroy Analysis] ' + '~' * 34 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Final Categroy Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # final_category_analysis_create_worknotes_backend_process = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
                # # check the response
                # if (((final_category_analysis_create_worknotes_backend_process) != None) and (str(final_category_analysis_create_worknotes_backend_process['status']).lower() == 'success')):
                #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '13-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Final Categroy Analysis Process Completed And Worknotes Updated Into SerivceNow')
                #     return {'status' : 'SUCCESS', 'file_name' : 'Incident-ESOAR-Process', 'step' : '13-D', 'message' : f'For Account: "{account_unique_id}" Final Category Analysis Process Completed'}
                # else:
                #     log_writer(script_name = 'Incident-ESOAR-Process', steps = '13-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Final Categroy Analysis Process Completed But Worknotes Not Updated In ServiceNow')
                #     return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '13-D', 'message' : f'For Account: "{account_unique_id}" Final Category Analysis Process Not Completed'}
            except Exception as error:
                log_writer(script_name = 'Incident-ESOAR-Process', steps = '13-D', status = 'ERROR', message = str(error))
                return {'status' : 'ERROR', 'file_name' : 'Incident-ESOAR-Process', 'step' : '13-D', 'message' : str(error)}
    ######################################################