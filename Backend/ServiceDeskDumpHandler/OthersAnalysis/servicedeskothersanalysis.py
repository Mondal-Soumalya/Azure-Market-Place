# define "service_desk_others_analysis" function
# def service_desk_others_analysis(account_unique_id: str, ticket_number: str, ticket_sys_id: str) -> dict[str, str]: #type: ignore
def service_desk_others_analysis(account_unique_id: str, file_unique_id: str, user_unique_id: str) -> dict[str, str]: #type: ignore
    # define constant
    MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = False
    KB_DETAILS_ANALYSIS_PROCESS_COMPLETE_STATUS = False
    CHAT_ONLY_ANALYSIS_PROCESS_COMPLETE_STATUS = False
    BUDDYBOT_ANALYSIS_PROCESS_COMPLETE_STATUS = False

    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        import time
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '2', 'message' : str(error)}

    # importing user define function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
        # from Backend.SnowHandler.createworknotes import create_worknotes
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '7', 'message' : str(error)}

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
                    log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '8', status = 'SUCCESS', message = '"file_process_status" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '8', status = 'ERROR', message = '"file_process_status" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '8', 'message' : '"file_process_status" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '8', 'message' : str(error)}

    #### starting mttr and aging analysis backend process:S09 #####
    # importing "service_desk_mttr_aging_analysis" function:S09-A
    try:
        from Backend.ServiceDeskDumpHandler.OthersAnalysis.SupportScript.servicedeskmttrandaginganalysis import service_desk_mttr_aging_analysis
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '9-A', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '9-A', 'message' : str(error)}

    # calling "service_desk_mttr_aging_analysis" function:S09-B
    try:
        mttr_aging_analysis_process_start_time = time.time()
        mttr_aging_analysis_backend_response = service_desk_mttr_aging_analysis(account_unique_id = str(account_unique_id))
        if (mttr_aging_analysis_backend_response != None):
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '9-B', status = 'INFO', message = f'For Account: "{account_unique_id}" MTTR And Aging Backend Process Response Generate')
        mttr_aging_analysis_process_end_time = time.time()
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '9-B', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '9-B', 'message' : str(error)}

    # check the result for "ERROR":S09-C
    try:
        if (str(mttr_aging_analysis_backend_response['status']).lower() == 'error'):
            MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = False
            return {'status' : 'ERROR', 'file_name' : str(mttr_aging_analysis_backend_response['file_name']), 'step' : str(mttr_aging_analysis_backend_response['step']), 'message' : str(mttr_aging_analysis_backend_response['message'])}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '9-C', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '9-C', 'message' : str(error)}

    # check the result for "SUCCESS":S09-D
    if (str(mttr_aging_analysis_backend_response['status']).lower() == 'success'):
        try:
            elapsed_seconds = int((mttr_aging_analysis_process_end_time - mttr_aging_analysis_process_start_time) % 60) #type: ignore
            file_process_status_insert_sql = '''
            INSERT INTO file_process_status (
                file_unique_id,
                account_unique_id,
                file_submitted_by,
                process_name,
                completion_time_seconds
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), str(account_unique_id), str(user_unique_id), 'MTTR Analysis', int(elapsed_seconds)))
                    insert_id_result = database_cursor.fetchone()
                    # check if data inserted or not
                    if ((insert_id_result is None) or (insert_id_result[0] is None)):
                        MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                        database_connection.rollback()
                        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '9-D', 'message' : f'For Account: "{account_unique_id}" MTTR Analysis Process Not Completed'}
                    else:
                        MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                        database_connection.commit()
                        log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '9-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" MTTR Analysis Process Completed')
            # elapsed_seconds = int((mttr_aging_analysis_process_end_time - mttr_aging_analysis_process_start_time) % 60) #type: ignore
            # elapsed_minutes = int(((mttr_aging_analysis_process_end_time - mttr_aging_analysis_process_start_time) % 3600) // 60) #type: ignore
            # elapsed_hours = int((mttr_aging_analysis_process_end_time - mttr_aging_analysis_process_start_time) // 3600) #type: ignore
            # # define servicenow worknotes
            # work_notes = '~' * 33 + ' Step : 7 [MTTR And Aging Analysis] ' + '~' * 33 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : MTTR And Aging Analysis\n• Upcoming Procss : KB Article Finding' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
            # # calling "create_worknotes" function
            # mttr_aging_analysis_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
            # # check the response
            # if (((mttr_aging_analysis_create_worknotes_backend_response) != None) and (str(mttr_aging_analysis_create_worknotes_backend_response['status']).lower() == 'success')):
            #     MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = True
            #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '9-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed And Worknotes Updated Into SerivceNow')
            # else:
            #     MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS = False
            #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '9-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed But Worknotes Not Updated In ServiceNow')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '9-D', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '9-D', 'message' : str(error)}
    ######################################################

    #### starting kb details analysis backend process:S10 #####
    if (MTTR_AGING_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "service_desk_kb_details_analysis" function:S10-A
        try:
            from Backend.ServiceDeskDumpHandler.OthersAnalysis.SupportScript.servicedeskkbdetailsanalysis import service_desk_kb_details_analysis
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '10-A', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '10-A', 'message' : str(error)}

        # calling "service_desk_kb_details_analysis" function:S10-B
        try:
            kb_details_analysis_process_start_time = time.time()
            kb_details_analysis_backend_response = service_desk_kb_details_analysis(account_unique_id = str(account_unique_id))
            if (kb_details_analysis_backend_response != None):
                log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '10-B', status = 'INFO', message = f'For Account: "{account_unique_id}" MTTR And Aging Backend Process Response Generate')
            kb_details_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '10-B', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '10-B', 'message' : str(error)}

        # check the result for "ERROR":S10-C
        try:
            if (str(kb_details_analysis_backend_response['status']).lower() == 'error'):
                KB_DETAILS_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                return {'status' : 'ERROR', 'file_name' : str(kb_details_analysis_backend_response['file_name']), 'step' : str(kb_details_analysis_backend_response['step']), 'message' : str(kb_details_analysis_backend_response['message'])}
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '10-C', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '10-C', 'message' : str(error)}

        # check the result for "SUCCESS":S10-D
        if (str(kb_details_analysis_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((kb_details_analysis_process_end_time - kb_details_analysis_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    account_unique_id,
                    file_submitted_by,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), str(account_unique_id), str(user_unique_id), 'KB Details Analysis', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            KB_DETAILS_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '10-D', 'message' : f'For Account: "{account_unique_id}" KB Details Analysis Process Not Completed'}
                        else:
                            KB_DETAILS_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '10-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" KB Details Analysis Process Completed')
                # elapsed_seconds = int((kb_details_analysis_process_end_time - kb_details_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((kb_details_analysis_process_end_time - kb_details_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((kb_details_analysis_process_end_time - kb_details_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 33 + ' Step : 7 [MTTR And Aging Analysis] ' + '~' * 33 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : KB Details Analysis\n• Upcoming Procss : Chat Only Ticket Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # mttr_aging_analysis_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
                # # check the response
                # if (((mttr_aging_analysis_create_worknotes_backend_response) != None) and (str(mttr_aging_analysis_create_worknotes_backend_response['status']).lower() == 'success')):
                #     KB_DETAILS_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '10-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed And Worknotes Updated Into SerivceNow')
                # else:
                #     KB_DETAILS_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '10-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '10-D', status = 'ERROR', message = str(error))
                return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '10-D', 'message' : str(error)}
    ######################################################

    #### starting kb details analysis backend process:S11 #####
    if (KB_DETAILS_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "service_desk_chat_only_analysis" function:S11-A
        try:
            from Backend.ServiceDeskDumpHandler.OthersAnalysis.SupportScript.servicedeskchatonlyanalysis import service_desk_chat_only_analysis
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '11-A', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '11-A', 'message' : str(error)}

        # calling "service_desk_chat_only_analysis" function:S11-B
        try:
            chat_only_analysis_process_start_time = time.time()
            chat_only_analysis_backend_response = service_desk_chat_only_analysis(account_unique_id = str(account_unique_id))
            if (chat_only_analysis_backend_response != None):
                log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '11-B', status = 'INFO', message = f'For Account: "{account_unique_id}" MTTR And Aging Backend Process Response Generate')
            chat_only_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '11-B', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '11-B', 'message' : str(error)}

        # check the result for "ERROR":S11-C
        try:
            if (str(chat_only_analysis_backend_response['status']).lower() == 'error'):
                CHAT_ONLY_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                return {'status' : 'ERROR', 'file_name' : str(chat_only_analysis_backend_response['file_name']), 'step' : str(chat_only_analysis_backend_response['step']), 'message' : str(chat_only_analysis_backend_response['message'])}
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '11-C', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '11-C', 'message' : str(error)}

        # check the result for "SUCCESS":S11-D
        if (str(chat_only_analysis_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((chat_only_analysis_process_end_time - chat_only_analysis_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    account_unique_id,
                    file_submitted_by,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), str(account_unique_id), str(user_unique_id), 'Chat Only Ticket', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            CHAT_ONLY_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '11-D', 'message' : f'For Account: "{account_unique_id}" Chat Only Ticket Process Not Completed'}
                        else:
                            CHAT_ONLY_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '11-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Chat Only Ticket Process Completed')
                # elapsed_seconds = int((chat_only_analysis_process_end_time - chat_only_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((chat_only_analysis_process_end_time - chat_only_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((chat_only_analysis_process_end_time - chat_only_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 33 + ' Step : 7 [MTTR And Aging Analysis] ' + '~' * 33 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Chat Only Ticket\n• Upcoming Procss : BuddyBot Ticket Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # mttr_aging_analysis_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
                # # check the response
                # if (((mttr_aging_analysis_create_worknotes_backend_response) != None) and (str(mttr_aging_analysis_create_worknotes_backend_response['status']).lower() == 'success')):
                #     CHAT_ONLY_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '11-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed And Worknotes Updated Into SerivceNow')
                # else:
                #     CHAT_ONLY_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '11-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '11-D', status = 'ERROR', message = str(error))
                return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '11-D', 'message' : str(error)}
    ######################################################

    #### starting buddybot analysis backend process:S12 #####
    if (CHAT_ONLY_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "service_desk_buddybot_analysis" function:S12-A
        try:
            from Backend.ServiceDeskDumpHandler.OthersAnalysis.SupportScript.servicedeskbuddybotanalysis import service_desk_buddybot_analysis
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '12-A', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '12-A', 'message' : str(error)}

        # calling "service_desk_buddybot_analysis" function:S12-B
        try:
            buddybot_analysis_process_start_time = time.time()
            buddybot_analysis_backend_response = service_desk_buddybot_analysis(account_unique_id = str(account_unique_id))
            if (buddybot_analysis_backend_response != None):
                log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '12-B', status = 'INFO', message = f'For Account: "{account_unique_id}" MTTR And Aging Backend Process Response Generate')
            buddybot_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '12-B', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '12-B', 'message' : str(error)}

        # check the result for "ERROR":S12-C
        try:
            if (str(buddybot_analysis_backend_response['status']).lower() == 'error'):
                BUDDYBOT_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                return {'status' : 'ERROR', 'file_name' : str(buddybot_analysis_backend_response['file_name']), 'step' : str(buddybot_analysis_backend_response['step']), 'message' : str(buddybot_analysis_backend_response['message'])}
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '12-C', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '12-C', 'message' : str(error)}

        # check the result for "SUCCESS":S12-D
        if (str(buddybot_analysis_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((buddybot_analysis_process_end_time - buddybot_analysis_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    account_unique_id,
                    file_submitted_by,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), str(account_unique_id), str(user_unique_id), 'BuddyBot Analysis', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            BUDDYBOT_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '12-D', 'message' : f'For Account: "{account_unique_id}" BuddyBot Analysis Process Not Completed'}
                        else:
                            BUDDYBOT_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '12-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" BuddyBot Analysis Process Completed')
                # elapsed_seconds = int((buddybot_analysis_process_end_time - buddybot_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((buddybot_analysis_process_end_time - buddybot_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((buddybot_analysis_process_end_time - buddybot_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 33 + ' Step : 7 [MTTR And Aging Analysis] ' + '~' * 33 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : BuddyBot Analysis\n• Upcoming Procss : CHIP Ticket Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # mttr_aging_analysis_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
                # # check the response
                # if (((mttr_aging_analysis_create_worknotes_backend_response) != None) and (str(mttr_aging_analysis_create_worknotes_backend_response['status']).lower() == 'success')):
                #     BUDDYBOT_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '12-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed And Worknotes Updated Into SerivceNow')
                # else:
                #     BUDDYBOT_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '12-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '12-D', status = 'ERROR', message = str(error))
                return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '12-D', 'message' : str(error)}
    ######################################################

    #### starting chip analysis backend process:S13 #####
    if (BUDDYBOT_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "service_desk_chip_analysis" function:S13-A
        try:
            from Backend.ServiceDeskDumpHandler.OthersAnalysis.SupportScript.servicedeskchipanalysis import service_desk_chip_analysis
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '13-A', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '13-A', 'message' : str(error)}

        # calling "service_desk_chip_analysis" function:S13-B
        try:
            chip_analysis_process_start_time = time.time()
            chip_analysis_backend_response = service_desk_chip_analysis(account_unique_id = str(account_unique_id))
            if (chip_analysis_backend_response != None):
                log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '13-B', status = 'INFO', message = f'For Account: "{account_unique_id}" MTTR And Aging Backend Process Response Generate')
            chip_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '13-B', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '13-B', 'message' : str(error)}

        # check the result for "ERROR":S13-C
        try:
            if (str(chip_analysis_backend_response['status']).lower() == 'error'):
                return {'status' : 'ERROR', 'file_name' : str(chip_analysis_backend_response['file_name']), 'step' : str(chip_analysis_backend_response['step']), 'message' : str(chip_analysis_backend_response['message'])}
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '13-C', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '13-C', 'message' : str(error)}

        # check the result for "SUCCESS":S13-D
        if (str(chip_analysis_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((chip_analysis_process_end_time - chip_analysis_process_start_time) % 60) #type: ignore
                file_process_status_insert_sql = '''
                INSERT INTO file_process_status (
                    file_unique_id,
                    account_unique_id,
                    file_submitted_by,
                    process_name,
                    completion_time_seconds
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;'''
                with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                    with database_connection.cursor() as database_cursor:
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), str(account_unique_id), str(user_unique_id), 'CHIP Analysis', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            database_connection.rollback()
                            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '13-D', 'message' : f'For Account: "{account_unique_id}" CHIP Analysis Process Not Completed'}
                        else:
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '13-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" CHIP Analysis Process Completed')
                            return {'status' : 'SUCCESS', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '13-D', 'message' : f'For Account: "{account_unique_id}" CHIP Analysis Process Completed'}
                # elapsed_seconds = int((chip_analysis_process_end_time - chip_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((chip_analysis_process_end_time - chip_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((chip_analysis_process_end_time - chip_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 33 + ' Step : 7 [MTTR And Aging Analysis] ' + '~' * 33 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : CHIP Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # mttr_aging_analysis_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(ticket_number), ticket_sys_id = str(ticket_sys_id))
                # # check the response
                # if (((mttr_aging_analysis_create_worknotes_backend_response) != None) and (str(mttr_aging_analysis_create_worknotes_backend_response['status']).lower() == 'success')):
                #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '13-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed And Worknotes Updated Into SerivceNow')
                # else:
                #     log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '13-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" MTTR And Aging Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Others-Analysis', steps = '13-D', status = 'ERROR', message = str(error))
                return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Others-Analysis', 'step' : '13-D', 'message' : str(error)}
    ######################################################