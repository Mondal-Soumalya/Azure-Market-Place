# define "service_desk_data_process" function
def service_desk_data_process(account_unique_id: str, file_unique_id: str, user_unique_id: str, user_email: str, file_path: str):
    # define constant
    SERVICE_DESK_COLUMN_PROCESS_COMPLETE_STATUS = False
    SERVICE_DESK_FILE_TO_DB_PROCESS_COMPLETE_STATUS = False
    SERVICE_DESK_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = False
    SERVICE_DESK_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = False
    SERVICE_DESK_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = False
    SERVICE_DESK_TRANSLATE_AND_DESK_LANGUAGE_ANALYSIS_PROCESS_COMPLETE_STATUS = False
    SERVICE_DESK_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = False
    SERVICE_DESK_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = False
    SERVICE_DESK_ESOAR_ANALYSIS_PROCESS_COMPLETE_STATUS = False

    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        import time
    except Exception as error:
        print(f'ERROR - [Service-Desk-Data-Process:S01] - {str(error)}')

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        print(f'ERROR - [Service-Desk-Data-Process:S02] - {str(error)}')

    # importing user define function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
        # from Backend.MailSentHandler.mailhandler import mail_handler
        # from Backend.MailSentHandler.errormail import error_mail
        # from Backend.SnowHandler.createworknotes import create_worknotes
    except Exception as error:
        print(f'ERROR - [Service-Desk-Data-Process:S03] - {str(error)}')

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Data-Process', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Data-Process', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Data-Process', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Data-Process', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '7', status = 'SUCCESS', message = 'PostgreSQL Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Data-Process', 'step' : '7', 'message' : str(error)}

    # check if "submitted_file_details" table present inside database:S08
    try:
        submitted_file_details_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'submitted_file_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(submitted_file_details_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Service-Desk-Data-Process', steps = '8', status = 'SUCCESS', message = '"submitted_file_details" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Data-Process', steps = '8', status = 'ERROR', message = '"submitted_file_details" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Data-Process', 'step' : '8', 'message' : '"submitted_file_details" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Data-Process', 'step' : '8', 'message' : str(error)}

    # check if "file_process_status" table present inside database:S09
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
                    log_writer(script_name = 'Service-Desk-Data-Process', steps = '9', status = 'SUCCESS', message = '"file_process_status" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Data-Process', steps = '9', status = 'ERROR', message = '"file_process_status" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Data-Process', 'step' : '9', 'message' : '"file_process_status" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Data-Process', 'step' : '9', 'message' : str(error)}

    ##### starting column mapping backend process:S10 #####
    # importing "service_desk_column_process" function:S10-A
    try:
        from Backend.ServiceDeskDumpHandler.FileProcess.servicedeskcolumnprocess import service_desk_column_process
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-A', status = 'ERROR', message = str(error))
        # error_mail(file_name = 'Service-Desk-Data-Process', step = '10-A', message = str(error))

    # calling "service_desk_column_process" function to validate file:S10-B
    try:
        column_mapping_process_start_time = time.time()
        column_process_backend_response = service_desk_column_process(file_path = str(file_path))
        if (column_process_backend_response != None):
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-B', status = 'INFO', message = f'For File: "{Path(file_path).name}" Column Name Mapping Backend Process Response Generate')
        column_mapping_process_end_time = time.time()
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-B', status = 'ERROR', message = str(error))
        # error_mail(file_name = 'Service-Desk-Data-Process', step = '10-B', message = str(error))

    # # check the result for "INFO":S10-C
    # try:
    #     if (str(column_process_backend_response['status']).lower() == 'info'):
    #         SERVICE_DESK_COLUMN_PROCESS_COMPLETE_STATUS = True
    #         # define html head
    #         html_head = '''
    #         <html>
    #             <head>
    #                 <style>
    #                 body {
    #                     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    #                     color: #2c3e50;
    #                     background-color: #f9f9f9;
    #                     padding: 20px;
    #                 }
    #                 .container {
    #                     background-color: #ffffff;
    #                     border: 1px solid #ddd;
    #                     border-radius: 8px;
    #                     padding: 25px;
    #                     max-width: 600px;
    #                     margin: auto;
    #                     box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    #                 }
    #                 .highlight {
    #                     color: #27ae60;
    #                     font-weight: bold;
    #                     font-size: 22px;
    #                 }
    #                 .footer-note {
    #                     font-size: 14px;
    #                     color: #7f8c8d;
    #                     font-style: italic;
    #                     font-weight: bold;
    #                     margin-top: 30px;
    #                     text-align: center;
    #                 }
    #                 .greeting, .closing {
    #                     margin-top: 20px;
    #                 }
    #                 </style>
    #             </head>
    #                 <body>
    #                     <div class="container">
    #                     <p class="greeting"><strong>Hello Team,</strong></p>
    #                     <p><span style="color: #ffbf00; font-weight: bold;"><strong>Information!</strong></span></p>'''

    #         # check if "missing_columns" is empty
    #         if (int(len(column_process_backend_response['missing_columns'])) == 0):
    #             # define html body
    #             html_body = f'''<p><strong>Initial processing is complete.</strong> And we faced: <span style="color: red; font-weight: bold;">{column_process_backend_response['message']}</span></p><br>'''

    #         # check if "missing_columns" not empyt
    #         if (int(len(column_process_backend_response['missing_columns'])) > 0):
    #             # define html body empty string
    #             html_body = f'''<p><strong>Initial processing is complete.</strong> And we faced: <span style="color: red; font-weight: bold;">{column_process_backend_response['message']}</span></p>'''
    #             for col in column_process_backend_response['missing_columns']:
    #                 html_body += f'''<li>{col}</li>'''

    #         # define html footer
    #         html_footer = '''
    #                     <p>Be adviced rectify those errors and uplaod the Ticket Dump again; As of now you will get the incomplete analysis.</p>
    #                     <p class="closing"> <strong>Thank you</strong> for your attention.<br><br>
    #                     Best Regards,<br>
    #                     <strong>Automation ASTRA</strong></p>
    #                     <p class="footer-note">
    #                         *** This is a system-generated email. Please do not reply. ***
    #                     </p>
    #                     </div>
    #                 </body>
    #         </html>'''

    #         # define email body
    #         email_body = html_head + html_body + html_footer

    #         # calling "mail_handler"
    #         mail_handler(email_subject = 'ASTRA | ESOAR Analysis', email_to = str(user_email).lower(), email_cc = 'soumalya.mondal@capgemini.com;anurag.thakur@capgemini.com', email_body = str(email_body))
    #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-C', status = 'SUCCESS', message = f'Email Sent To User: "{str(user_email).lower()}" With Proper Description')
    # except Exception as error:
    #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-C', status = 'ERROR', message = str(error))
    #     error_mail(file_name = 'Service-Desk-Data-Process', step = '10-C', message = str(error))

    # check the result for "ERROR":S10-D
    if (str(column_process_backend_response['status']).lower() == 'error'):
        try:
            SERVICE_DESK_COLUMN_PROCESS_COMPLETE_STATUS = False
            # converting "file_path" to Path object
            file_path_object = Path(file_path)
            # delete "file_path"
            file_path_object.unlink()
            log_writer(script_name = str(column_process_backend_response['file_name']), steps = str(column_process_backend_response['step']), status = 'ERROR', message = str(column_process_backend_response['message']))
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-D', status = 'ERROR', message = f'Submitted File: "{file_path_object.name}" Deleted Because Column Process Not Complete')
            # sending error mail to developer
            # error_mail(file_name = str(column_process_backend_response['file_name']), step = str(column_process_backend_response['step']), message = str(column_process_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-D', status = 'ERROR', message=str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '10-D', message = str(error))

    # check the result for "INFO":S10-E
    if (str(column_process_backend_response['status']).lower() == 'info'):
        try:
            column_process_description = f"Column Mapping Process Complete, but we found {', '.join([f'{i+1}){col}' for i, col in enumerate(column_process_backend_response['missing_columns'])])} these column(s) are missing from the file."
            elapsed_seconds = int((column_mapping_process_end_time - column_mapping_process_start_time) % 60) #type: ignore
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
                        SERVICE_DESK_COLUMN_PROCESS_COMPLETE_STATUS = False
                        database_connection.rollback()
                        log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-E', status = 'ERROR', message = f'Column Mapping Process Not Completed For File: "{Path(file_path).name}"')
                    else:
                        SERVICE_DESK_COLUMN_PROCESS_COMPLETE_STATUS = True
                        database_connection.commit()
                        log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-E', status = 'SUCCESS', message = f'Column Mapping Process Completed For File: "{Path(file_path).name}" With Some Missing Column')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-E', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '10-E', message = str(error))

    # check the result for "SUCCESS":S10-F
    if (str(column_process_backend_response['status']).lower() == 'success'):
        try:
            column_process_description = 'Standardizing column names and formats for consistency.'
            elapsed_seconds = int((column_mapping_process_end_time - column_mapping_process_start_time) % 60) #type: ignore
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
                        SERVICE_DESK_COLUMN_PROCESS_COMPLETE_STATUS = False
                        database_connection.rollback()
                        log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-F', status = 'ERROR', message = f'Column Mapping Process Not Completed For File: "{Path(file_path).name}"')
                    else:
                        SERVICE_DESK_COLUMN_PROCESS_COMPLETE_STATUS = True
                        database_connection.commit()
                        log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-F', status = 'SUCCESS', message = f'Column Mapping Process Completed For File: "{Path(file_path).name}" and all the required column(s) are present')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '10-F', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '10-F', message = str(error))
    ####################################################

    ##### starting excel to db transfering process:S11 #####
    if (SERVICE_DESK_COLUMN_PROCESS_COMPLETE_STATUS):
        # importing "service_desk_file_to_db" function:S11-A
        try:
            from Backend.ServiceDeskDumpHandler.FileProcess.servicedeskfiletodb import service_desk_file_to_db
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-A', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '11-A', message = str(error))

        # calling "service_desk_file_to_db" function:S11-B
        try:
            file_to_db_process_start_time = time.time()
            service_desk_data_file_to_db_backend_response = service_desk_file_to_db(account_unique_id = str(account_unique_id), file_unique_id = str(file_unique_id), file_path = str(column_process_backend_response['file_path']))
            if (service_desk_data_file_to_db_backend_response != None):
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-B', status = 'INFO', message = f'For File: "{Path(file_path).name}" File To DB Backend Porcess Response Generate')
            file_to_db_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-B', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '11-B', message = str(error))

        # check the result for "ERROR":S11-C
        try:
            if (str(service_desk_data_file_to_db_backend_response['status']).lower() == 'error'):
                SERVICE_DESK_FILE_TO_DB_PROCESS_COMPLETE_STATUS =False
                # sending error mail to developer
                # error_mail(file_name = str(service_desk_data_file_to_db_backend_response['file_name']), step = str(service_desk_data_file_to_db_backend_response['step']), message = str(service_desk_data_file_to_db_backend_response['message']))
                # converting "file_path" to Path object
                file_path_object = Path(file_path)
                # delete "file_path"
                file_path_object.unlink()
                log_writer(script_name = str(service_desk_data_file_to_db_backend_response['file_name']), steps = str(service_desk_data_file_to_db_backend_response['step']), status = 'ERROR', message = str(service_desk_data_file_to_db_backend_response['message']))
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-C', status = 'ERROR', message = f'Submitted File: "{file_path_object.name}" Deleted Because Data Process Not Complete')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-C', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '11-C', message = str(error))

        # check the result for "SUCCESS"
        if (str(service_desk_data_file_to_db_backend_response['status']).lower() == 'success'):
            # inserting value into "file_process_status" table:S11-D
            try:
                elapsed_seconds = int((file_to_db_process_end_time - file_to_db_process_start_time) % 60) #type: ignore
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
                            SERVICE_DESK_FILE_TO_DB_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-D', status = 'ERROR', message = f'File To DB Process Not Completed For File: "{Path(file_path).name}"')
                        else:
                            SERVICE_DESK_FILE_TO_DB_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-D', status = 'SUCCESS', message = f'File To DB Process Completed For File: "{Path(file_path).name}"')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-D', status = 'ERROR', message = str(error))
                # error_mail(file_name = 'Service-Desk-Data-Process', step = '11-D', message = str(error))

            # # importing "create_ticket" function:S11-E
            # try:
            #     from Backend.SnowHandler.createticket import create_ticket
            # except Exception as error:
            #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-E', status = 'ERROR', message = str(error))
            #     # error_mail(file_name = 'Service-Desk-Data-Process', step = '11-E', message = str(error))

            # # calling "create_ticket" function:S11-F
            # try:
            #     servicenow_ticket_create_response = create_ticket(short_description = 'Service-Desk Ticket Analysis With PRiSM Analytics')
            #     if (servicenow_ticket_create_response != None):
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-F', status = 'SUCCESS', message = f'For File: "{Path(file_path).name}" New ServiceNow Ticket Created')
            # except Exception as error:
            #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-F', status = 'ERROR', message = str(error))
            #     error_mail(file_name = 'Service-Desk-Data-Process', step = '11-F', message = str(error))

            # # if servicenow response is "ERROR":S11-G
            # if (str(servicenow_ticket_create_response['status']).lower() == 'error'):
            #     try:
            #         SERVICE_DESK_FILE_TO_DB_PROCESS_COMPLETE_STATUS = False
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-G', status = 'SUCCESS', message = f'For File: "{Path(file_path).name}" ServiceNow Ticket Not Created Because Of Technical Issue')
            #         # define email body
            #         email_body = f'''
            #         <html>
            #             <body>
            #                 <p>Dear Team,</p>
            #                 <p>The service-desk dump file has been uploaded successfully.</p>
            #                 <p>The initial file processing completed, Due to some technical issue <strong>ServiceNow</strong> ticket not created,
            #                 Maybe You need re-upload the ticket after sometimes.</p>
            #                 <p>Thanks &amp; Regards,<br>Automation ASTRA</p>
            #                 <br>
            #                 <p style="font-size: 16px; color: gray; font-style: italic; font-weight: bold;">
            #                     *** This is a system-generated email. Please do not reply. ***
            #                 </p>
            #             </body>
            #         </html>'''
            #         # sending the email
            #         mail_handler(email_subject = 'ASTRA | ESOAR Analysis', email_to = str(user_email).lower(), email_cc = 'soumalya.mondal@capgemini.com;anurag.thakur@capgemini.com', email_body = str(email_body))
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-G', status = 'INFO', message = f'Email Sent To User: "{str(user_email).lower()}" With No ServiceNow Ticket Details')
            #     except Exception as error:
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-G', status = 'ERROR', message = str(error))
            #         error_mail(file_name = 'Service-Desk-Data-Process', step = '11-G', message = str(error))

            # # if servicenow resposne "SUCCESS":S11-H
            # if (str(servicenow_ticket_create_response['status']).lower() == 'success'):
            #     try:
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-H', status = 'SUCCESS', message = f'''New ServiceNow Ticket Created: "{servicenow_ticket_create_response['ticket_number']}" For File: "{Path(file_path).name}"''')
            #         # define email body
            #         email_body = f'''
            #         <html>
            #             <head>
            #                 <style>
            #                 body {{
            #                     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            #                     color: #2c3e50;
            #                     background-color: #f9f9f9;
            #                     padding: 20px;
            #                 }}
            #                 .container {{
            #                     background-color: #ffffff;
            #                     border: 1px solid #ddd;
            #                     border-radius: 8px;
            #                     padding: 25px;
            #                     max-width: 600px;
            #                     margin: auto;
            #                     box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            #                 }}
            #                 .highlight {{
            #                     color: #27ae60;
            #                     font-weight: bold;
            #                     font-size: 22px;
            #                 }}
            #                 .footer-note {{
            #                     font-size: 14px;
            #                     color: #7f8c8d;
            #                     font-style: italic;
            #                     font-weight: bold;
            #                     margin-top: 30px;
            #                     text-align: center;
            #                 }}
            #                 .greeting, .closing {{
            #                     margin-top: 20px;
            #                 }}
            #                 </style>
            #             </head>
            #                 <body>
            #                     <div class="container">
            #                     <p class="greeting"><strong>Hello Team,</strong></p>
            #                     <p><span style="color: green; font-weight: bold;"><strong>Success!</strong></span></p>
            #                     <p><strong>Initial processing is complete.</strong> For all future references and tracking, please use the ticket number below:</p>
            #                     <p class="highlight">{servicenow_ticket_create_response['ticket_number']}</p>
            #                     <p class="closing"> <strong>Thank you</strong> for your attention.<br><br>
            #                     Best Regards,<br>
            #                     <strong>Automation ASTRA</strong></p>
            #                     <p class="footer-note">
            #                         *** This is a system-generated email. Please do not reply. ***
            #                     </p>
            #                     </div>
            #                 </body>
            #             </html>'''
            #         # sending the email
            #         mail_handler(email_subject = 'ASTRA | ESOAR Analysis', email_to = str(user_email).lower(), email_cc = 'soumalya.mondal@capgemini.com;anurag.thakur@capgemini.com', email_body = str(email_body))
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-H', status = 'SUCCESS', message = f'''Email Sent To User: "{str(user_email).lower()}" With ServiceNow Ticket: "{servicenow_ticket_create_response['ticket_number']}" Details''')
            #     except Exception as error:
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-H', status = 'ERROR', message = str(error))
            #         error_mail(file_name = 'Service-Desk-Data-Process', step = '11-H', message = str(error))

            #     # updating "file_process_status", "itsm_tikcet_number", "itsm_global_id" into "submitted_file_details" table:S11-I
            #     try:
            #         update_status_for_submitted_file_details_sql = '''
            #         UPDATE submitted_file_details
            #         SET
            #             file_process_status = %s,
            #             itsm_ticket_number = %s,
            #             itsm_global_id = %s
            #         WHERE file_unique_id = %s
            #         AND account_unique_id = %s;'''
            #         with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            #             with database_connection.cursor() as database_cursor:
            #                 database_cursor.execute(update_status_for_submitted_file_details_sql, ('Pending', str(servicenow_ticket_create_response['ticket_number']), str(servicenow_ticket_create_response['sys_id']), str(file_unique_id), str(account_unique_id)))
            #     except Exception as error:
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-I', status = 'ERROR', message = str(error))
            #         error_mail(file_name = 'Service-Desk-Data-Process', step = '11-I', message = str(error))

            #     # check if all the details updated in "submitted_file_details" table:S11-J
            #     try:
            #         checking_status_for_submitted_file_details_sql = '''
            #         SELECT EXISTS (
            #             SELECT 1
            #             FROM submitted_file_details
            #             WHERE file_unique_id = %s
            #             AND account_unique_id = %s
            #             AND itsm_ticket_number IS NOT DISTINCT FROM %s
            #             AND itsm_global_id IS NOT DISTINCT FROM %s
            #         );'''
            #         with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            #             with database_connection.cursor() as database_cursor:
            #                 database_cursor.execute(checking_status_for_submitted_file_details_sql, (str(file_unique_id), str(account_unique_id), str(servicenow_ticket_create_response['ticket_number']), str(servicenow_ticket_create_response['sys_id'])))
            #                 if (database_cursor.fetchone()[0]):
            #                     log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-J', status = 'SUCCESS', message = f'For File: "{file_unique_id}" File Status, ITSM Ticket Number, ITSM Global ID Updated Inside "submitted_file_details" Table')
            #                 else:
            #                     log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-J', status = 'ERROR', message = f'For File: "{file_unique_id}" File Status, ITSM Ticket Number, ITSM Global ID Not Updated Inside "submitted_file_details" Table')
            #                     error_mail(file_name = 'Service-Desk-Data-Process', step = '11-J', message = f'For File: "{file_unique_id}" File Status, ITSM Ticket Number, ITSM Global ID Not Updated Inside "submitted_file_details" Table')
            #     except Exception as error:
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-J', status = 'ERROR', message = str(error))
            #         error_mail(file_name = 'Service-Desk-Data-Process', step = '11-J', message = str(error))

            #     # updaing worknotes accordingly:S11-K
            #     try:
            #         elapsed_seconds = int((file_to_db_process_end_time - file_to_db_process_start_time) % 60) #type: ignore
            #         elapsed_minutes = int(((file_to_db_process_end_time - file_to_db_process_start_time) % 3600) // 60) #type: ignore
            #         elapsed_hours = int((file_to_db_process_end_time - file_to_db_process_start_time) // 3600) #type: ignore
            #         # define servicenow worknotes
            #         work_notes = '~' * 20 + ' Step : 1 [Transferring Ticket Details From File To Database] ' + '~' * 20 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Transferring Ticket Details From File To Database\n• Upcoming Procss : Output Data Fill' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
            #         # calling "create_worknotes" function
            #         file_to_db_create_worknotes_backend_process = create_worknotes(work_notes = str(work_notes), ticket_number = str(servicenow_ticket_create_response['ticket_number']), ticket_sys_id = str(servicenow_ticket_create_response['sys_id']))
            #         # check the response
            #         if (((file_to_db_create_worknotes_backend_process) != None) and (str(file_to_db_create_worknotes_backend_process['status']).lower() == 'success')):
            #             SERVICE_DESK_FILE_TO_DB_PROCESS_COMPLETE_STATUS = True
            #             log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-K', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Transferring Ticket From File To Database Process Completed And Worknotes Updated In ServiceNow')
            #         else:
            #             SERVICE_DESK_FILE_TO_DB_PROCESS_COMPLETE_STATUS = False
            #             log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-K', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Transferring Ticket From File To Database Process Completed But Worknotes Not Updated In ServiceNow')
            #     except Exception as error:
            #         log_writer(script_name = 'Service-Desk-Data-Process', steps = '11-K', status = 'ERROR', message = str(error))
            #         error_mail(file_name = 'Service-Desk-Data-Process', step = '11-K', message = str(error))
    ######################################################

    ##### starting output data fill backend process:S12 ######
    if (SERVICE_DESK_FILE_TO_DB_PROCESS_COMPLETE_STATUS):
        # importing "servicedesk_output_data_fill" function:S12-A
        try:
            from Backend.ServiceDeskDumpHandler.DataProcess.servicedeskoutputdatafill import servicedesk_output_data_fill
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '12-A', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '12-A', message = str(error))

        # calling "servicedesk_output_data_fill" function:S12-B
        try:
            output_data_fill_porcess_start_time = time.time()
            output_data_fill_backend_response = servicedesk_output_data_fill(account_unique_id = str(account_unique_id))
            if (output_data_fill_backend_response != None):
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '12-B', status = 'INFO', message = f'For Account: "{account_unique_id}" Output Table Data Fill Backend Process Response Generate')
            output_data_fill_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '12-B', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '12-B', message = str(error))

        # check the result for "ERROR":S12-C
        try:
            if (str(output_data_fill_backend_response['status']).lower() == 'error'):
                SERVICE_DESK_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(output_data_fill_backend_response['file_name']), steps = str(output_data_fill_backend_response['step']), status = 'ERROR', message = str(output_data_fill_backend_response['message']))
                # sending error mail to developer
                # error_mail(file_name = str(output_data_fill_backend_response['file_name']), step = str(output_data_fill_backend_response['step']), message = str(output_data_fill_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '12-C', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '12-C', message = str(error))

        # check the result for "SUCCESS":S12-D
        if (str(output_data_fill_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((output_data_fill_process_end_time - output_data_fill_porcess_start_time) % 60) #type: ignore
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
                            SERVICE_DESK_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '12-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Output Data Fill Process Not Completed')
                        else:
                            SERVICE_DESK_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '12-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Output Data Fill Process Completed')
                # elapsed_seconds = int((output_data_fill_process_end_time - output_data_fill_porcess_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((output_data_fill_process_end_time - output_data_fill_porcess_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((output_data_fill_process_end_time - output_data_fill_porcess_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 37 + ' Step : 2 [Output Data Fill] ' + '~' * 36 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Output Data Fill\n• Upcoming Procss : Data Normalization' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # output_data_fill_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(servicenow_ticket_create_response['ticket_number']), ticket_sys_id = str(servicenow_ticket_create_response['sys_id']))
                # # check the response
                # if (((output_data_fill_create_worknotes_backend_response) != None) and (str(output_data_fill_create_worknotes_backend_response['status']).lower() == 'success')):
                #     SERVICE_DESK_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '12-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Output Data Fill Process Completed And Worknotes Updated In ServiceNow')
                # else:
                #     SERVICE_DESK_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '12-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Output Data Fill Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '12-D', status = 'ERROR', message = str(error))
                # error_mail(file_name = 'Service-Desk-Data-Process', step = '12-D', message = str(error))
    ######################################################

    #### starting data normalization backend process:S13 #####
    if (SERVICE_DESK_OUTPUT_DATA_FILL_PROCESS_COMPLETE_STATUS):
        # importing "servicedesk_normalized_data" function:S13-A
        try:
            from Backend.ServiceDeskDumpHandler.DataProcess.servicedesknormalizeddata import servicedesk_normalized_data
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '13-A', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '13-A', message = str(error))

        # calling "servicedesk_normalized_data" function:S13-B
        try:
            data_normalization_process_start_time = time.time()
            normalized_data_backend_response = servicedesk_normalized_data(account_unique_id = str(account_unique_id))
            if (normalized_data_backend_response != None):
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '13-B', status = 'INFO', message = f'For Account: "{account_unique_id}" Data Normalization Backend Process Response Generate')
            data_normalization_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '13-B', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '13-B', message = str(error))

        # check the result for "ERROR":S13-C
        try:
            if (str(normalized_data_backend_response['status']).lower() == 'error'):
                SERVICE_DESK_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(normalized_data_backend_response['file_name']), steps = str(normalized_data_backend_response['step']), status = 'ERROR', message = str(normalized_data_backend_response['message']))
                # sending error mail to developer
                # error_mail(file_name = str(normalized_data_backend_response['file_name']), step = str(normalized_data_backend_response['step']), message = str(normalized_data_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '13-C', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '13-C', message = str(error))

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
                            SERVICE_DESK_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '13-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Data Normalization Process Not Completed')
                        else:
                            SERVICE_DESK_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '13-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Data Normalization Process Completed')
                # elapsed_seconds = int((data_normalization_process_end_time - data_normalization_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((data_normalization_process_end_time - data_normalization_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((data_normalization_process_end_time - data_normalization_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 36 + ' Step : 3 [Data Normalization] ' + '~' * 35 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Data Normalization\n• Upcoming Procss : Information Clean' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # data_normalization_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(servicenow_ticket_create_response['ticket_number']), ticket_sys_id = str(servicenow_ticket_create_response['sys_id']))
                # # check the response
                # if (((data_normalization_create_worknotes_backend_response) != None) and (str(data_normalization_create_worknotes_backend_response['status']).lower() == 'success')):
                #     SERVICE_DESK_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '13-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Data Normalization Process Completed And Worknotes Updated In ServiceNow')
                # else:
                #     SERVICE_DESK_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '13-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Data Normalization Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '13-D', status = 'ERROR', message = str(error))
                # error_mail(file_name = 'Service-Desk-Data-Process', step = '13-D', message = str(error))
    ######################################################

    ##### starting information clean backend process:S14 #####
    if (SERVICE_DESK_DATA_NORMALIZED_PROCESS_COMPLETE_STATUS):
        # importing "servicedesk_information_clean" function:S14-A
        try:
            from Backend.ServiceDeskDumpHandler.DataProcess.servicedeskinformationclean import servicedesk_information_clean
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '14-A', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '14-A', message = str(error))

        # calling "servicedesk_information_clean" function:S14-B
        try:
            information_clean_process_start_time = time.time()
            information_clean_backend_response = servicedesk_information_clean(account_unique_id = str(account_unique_id))
            if (information_clean_backend_response != None):
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '14-B', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Information Clean Process Completed')
            information_clean_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '14-B', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '14-B', message = str(error))

        # check the result for "ERROR":S14-C
        try:
            if (str(information_clean_backend_response['status']).lower() == 'error'):
                SERVICE_DESK_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(information_clean_backend_response['file_name']), steps = str(information_clean_backend_response['step']), status = 'ERROR', message = str(information_clean_backend_response['message']))
                # sending error mail to developer
                # error_mail(file_name = str(information_clean_backend_response['file_name']), step = str(information_clean_backend_response['step']), message = str(information_clean_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '14-C', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '14-C', message = str(error))

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
                            SERVICE_DESK_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '14-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Information Clean Process Not Completed')
                        else:
                            SERVICE_DESK_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '14-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Information Clean Process Completed')
                # elapsed_seconds = int((information_clean_process_end_time - information_clean_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((information_clean_process_end_time - information_clean_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((information_clean_process_end_time - information_clean_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 35 + ' Step : 4 [Information Cleaning] ' + '~' * 34 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Information Cleaning\n• Upcoming Procss : Translate And Desk Language Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # information_clean_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(servicenow_ticket_create_response['ticket_number']), ticket_sys_id = str(servicenow_ticket_create_response['sys_id']))
                # # check the response
                # if (((information_clean_create_worknotes_backend_response) != None) and (str(information_clean_create_worknotes_backend_response['status']).lower() == 'success')):
                #     SERVICE_DESK_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '14-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Information Clean Process Completed And Worknotes Updated In ServiceNow')
                # else:
                #     SERVICE_DESK_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '14-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Information Clean Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '14-D', status = 'ERROR', message = str(error))
                # error_mail(file_name = 'Service-Desk-Data-Process', step = '14-D', message = str(error))
    ######################################################

    ##### starting desk language analysis and translate backend process:S15 #####
    if (SERVICE_DESK_INFORMATION_CLEAN_PROCESS_COMPLETE_STATUS):
        # importing "service_desk_translate_and_desk_language_analysis" function:S15-A
        try:
            from Backend.ServiceDeskDumpHandler.TicketAnalysis.servicedesktranslateanddesklanguageanalysis import service_desk_translate_and_desk_language_analysis
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '15-A', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '15-A', message = str(error))

        # calling "service_desk_translate_and_desk_language_analysis" function:S15-B
        try:
            translate_and_desk_language_analysis_process_start_time = time.time()
            translate_and_desk_language_analysis_backend_response = service_desk_translate_and_desk_language_analysis(account_unique_id = str(account_unique_id))
            if (translate_and_desk_language_analysis_backend_response != None):
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '15-B', status = 'INFO', message = f'For Account: "{account_unique_id}" Translate And Desk Language Analysis Backend Process Response Generate')
            translate_and_desk_language_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '15-B', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '15-B', message = str(error))

        # check the result for "ERROR":S15-C
        try:
            if (str(translate_and_desk_language_analysis_backend_response['status']).lower() == 'error'):
                SERVICE_DESK_TRANSLATE_AND_DESK_LANGUAGE_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(translate_and_desk_language_analysis_backend_response['file_name']), steps = str(translate_and_desk_language_analysis_backend_response['step']), status = 'ERROR', message = str(translate_and_desk_language_analysis_backend_response['message']))
                # sending error mail to developer
                # error_mail(file_name = str(translate_and_desk_language_analysis_backend_response['file_name']), step = str(translate_and_desk_language_analysis_backend_response['step']), message = str(translate_and_desk_language_analysis_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '15-C', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '15-C', message = str(error))

        # check the result for "SUCCESS":S15-D
        if (str(translate_and_desk_language_analysis_backend_response['status']).lower() == 'success'):
            try:
                elapsed_seconds = int((translate_and_desk_language_analysis_process_end_time - translate_and_desk_language_analysis_process_start_time) % 60) #type: ignore
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
                        database_cursor.execute(file_process_status_insert_sql, (str(file_unique_id), 'Translate And Desk Language Analysis', int(elapsed_seconds)))
                        insert_id_result = database_cursor.fetchone()
                        # check if data inserted or not
                        if ((insert_id_result is None) or (insert_id_result[0] is None)):
                            SERVICE_DESK_TRANSLATE_AND_DESK_LANGUAGE_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '15-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Translate And Desk Language Analysis Process Not Completed')
                        else:
                            SERVICE_DESK_TRANSLATE_AND_DESK_LANGUAGE_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '15-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Translate And Desk Language Analysis Process Completed')
                # elapsed_seconds = int((translate_and_desk_language_analysis_process_end_time - translate_and_desk_language_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((translate_and_desk_language_analysis_process_end_time - translate_and_desk_language_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((translate_and_desk_language_analysis_process_end_time - translate_and_desk_language_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 36 + ' Step : 5 [Translate And Desk Language Analysis] ' + '~' * 36 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Translate And Desk Language Analysis\n• Upcoming Procss : Keywords Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # keywords_analysis_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(servicenow_ticket_create_response['ticket_number']), ticket_sys_id = str(servicenow_ticket_create_response['sys_id']))
                # # check the response
                # if (((keywords_analysis_create_worknotes_backend_response) != None) and (str(keywords_analysis_create_worknotes_backend_response['status']).lower() == 'success')):
                #     SERVICE_DESK_TRANSLATE_AND_DESK_LANGUAGE_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '15-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Translate And Desk Language Analysis Process Completed And Worknotes Updated In ServiceNow')
                # else:
                #     SERVICE_DESK_TRANSLATE_AND_DESK_LANGUAGE_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '15-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Translate And Desk Language Analysis Process Completed But Worknotes Not Updated Into ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '15-D', status = 'ERROR', message = str(error))
                # error_mail(file_name = 'Service-Desk-Data-Process', step = '15-D', message = str(error))
    ######################################################

    ##### starting keywords analysis backend process:S16 #####
    if (SERVICE_DESK_TRANSLATE_AND_DESK_LANGUAGE_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "service_desk_keyword_analysis" function:S16-A
        try:
            from Backend.ServiceDeskDumpHandler.TicketAnalysis.servicedeskkeywordanalysis import service_desk_keyword_analysis
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '16-A', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '16-A', message = str(error))

        # calling "service_desk_keyword_analysis" function:S16-B
        try:
            keyword_analysis_process_start_time = time.time()
            keywords_analysis_backend_response = service_desk_keyword_analysis(account_unique_id = str(account_unique_id))
            if (keywords_analysis_backend_response != None):
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '16-B', status = 'INFO', message = f'For Account: "{account_unique_id}" Keyword Analysis Backend Process Response Generate')
            keyword_analysis_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '16-B', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '16-B', message = str(error))

        # check the result for "ERROR":S16-C
        try:
            if (str(keywords_analysis_backend_response['status']).lower() == 'error'):
                SERVICE_DESK_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(keywords_analysis_backend_response['file_name']), steps = str(keywords_analysis_backend_response['step']), status = 'ERROR', message = str(keywords_analysis_backend_response['message']))
                # sending error mail to developer
                # error_mail(file_name = str(keywords_analysis_backend_response['file_name']), step = str(keywords_analysis_backend_response['step']), message = str(keywords_analysis_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '16-C', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '16-C', message = str(error))

        # check the result for "SUCCESS":S16-D
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
                            SERVICE_DESK_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '16-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Keywords Analysis Process Not Completed')
                        else:
                            SERVICE_DESK_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '16-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Keywords Analysis Process Completed')
                # elapsed_seconds = int((keyword_analysis_process_end_time - keyword_analysis_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((keyword_analysis_process_end_time - keyword_analysis_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((keyword_analysis_process_end_time - keyword_analysis_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 36 + ' Step : 5 [Keywords Analysis] ' + '~' * 36 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Keywords Analysis\n• Upcoming Procss : Automation Mapping' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # keywords_analysis_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(servicenow_ticket_create_response['ticket_number']), ticket_sys_id = str(servicenow_ticket_create_response['sys_id']))
                # # check the response
                # if (((keywords_analysis_create_worknotes_backend_response) != None) and (str(keywords_analysis_create_worknotes_backend_response['status']).lower() == 'success')):
                #     SERVICE_DESK_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '16-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Keywords Analysis Process Completed And Worknotes Updated In ServiceNow')
                # else:
                #     SERVICE_DESK_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '16-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Keyword Analysis Process Completed But Worknotes Not Updated Into ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '16-D', status = 'ERROR', message = str(error))
                # error_mail(file_name = 'Service-Desk-Data-Process', step = '16-D', message = str(error))
    ######################################################

    #### starting automation mapping backend process:S17 #####
    if (SERVICE_DESK_KEYWORD_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # importing "service_desk_automation_mapping" function:S17-A
        try:
            from Backend.ServiceDeskDumpHandler.TicketAnalysis.servicedeskautomationmapping import service_desk_automation_mapping
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '17-A', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '17-A', message = str(error))

        # calling "service_desk_automation_mapping" function:S17-B
        try:
            automation_mapping_process_start_time = time.time()
            automation_mapping_backend_response = service_desk_automation_mapping(account_unique_id = str(account_unique_id))
            if (automation_mapping_backend_response != None):
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '17-B', status = 'INFO', message = f'For Account: "{account_unique_id}" Automation Mapping Backend Process Response Generate')
            automation_mapping_process_end_time = time.time()
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '17-B', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '17-B', message = str(error))

        # check the result for "ERROR":S17-C
        try:
            if (str(automation_mapping_backend_response['status']).lower() == 'error'):
                SERVICE_DESK_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(automation_mapping_backend_response['file_name']), steps = str(automation_mapping_backend_response['step']), status = 'ERROR', message = str(automation_mapping_backend_response['message']))
                # sending error mail to developer
                # error_mail(file_name = str(automation_mapping_backend_response['file_name']), step = str(automation_mapping_backend_response['step']), message = str(automation_mapping_backend_response['message']))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '17-C', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '17-C', message = str(error))

        # check the result for "SUCCESS":S17-D
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
                            SERVICE_DESK_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = False
                            database_connection.rollback()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '17-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Automation Mapping Process Not Completed')
                        else:
                            SERVICE_DESK_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = True
                            database_connection.commit()
                            log_writer(script_name = 'Service-Desk-Data-Process', steps = '17-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Automation Mapping Process Completed')
                # elapsed_seconds = int((automation_mapping_process_end_time - automation_mapping_process_start_time) % 60) #type: ignore
                # elapsed_minutes = int(((automation_mapping_process_end_time - automation_mapping_process_start_time) % 3600) // 60) #type: ignore
                # elapsed_hours = int((automation_mapping_process_end_time - automation_mapping_process_start_time) // 3600) #type: ignore
                # # define servicenow worknotes
                # work_notes = '~' * 36 + ' Step : 6 [Automation Mapping] ' + '~' * 35 + '\n\n• Worknotes Updated By : PRiSM Analytics Tool\n• Completed Process : Automation Mapping\n• Upcoming Procss : Others Analysis' + '\n• Duration of Process Execution :' + f'\n- Hours : {elapsed_hours}' + f'\n- Minutes : {elapsed_minutes}' + f'\n- Seconds : {elapsed_seconds}'
                # # calling "create_worknotes" function
                # automation_mapping_create_worknotes_backend_response = create_worknotes(work_notes = str(work_notes), ticket_number = str(servicenow_ticket_create_response['ticket_number']), ticket_sys_id = str(servicenow_ticket_create_response['sys_id']))
                # # check the response
                # if (((automation_mapping_create_worknotes_backend_response) != None) and (str(automation_mapping_create_worknotes_backend_response['status']).lower() == 'success')):
                #     SERVICE_DESK_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = True
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '17-D', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Automation Mapping Process Completed And Worknotes Updated Into SerivceNow')
                # else:
                #     SERVICE_DESK_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS = False
                #     log_writer(script_name = 'Service-Desk-Data-Process', steps = '17-D', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Automation Mapping Process Completed But Worknotes Not Updated In ServiceNow')
            except Exception as error:
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '17-D', status = 'ERROR', message = str(error))
                # error_mail(file_name = 'Service-Desk-Data-Process', step = '17-D', message = str(error))
    ######################################################

    ##### starting "service_desk_others_analysis" backend process:S18 #####
    if (SERVICE_DESK_AUTOMATION_MAPPING_PROCESS_COMPLETE_STATUS):
        # importing "service_desk_others_analysis" fucntion:S18-A
        try:
            from Backend.ServiceDeskDumpHandler.OthersAnalysis.servicedeskothersanalysis import service_desk_others_analysis
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '18-A', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '18-A', message = str(error))

        # calling "service_desk_others_analysis" function:S18-B
        try:
            # esoar_analysis_function_response = service_desk_others_analysis(account_unique_id = str(account_unique_id), ticket_number = str(servicenow_ticket_create_response['ticket_number']), ticket_sys_id = str(servicenow_ticket_create_response['sys_id']))
            esoar_analysis_function_response = service_desk_others_analysis(account_unique_id = str(account_unique_id), file_unique_id = str(file_unique_id), user_unique_id = str(user_unique_id))
            if (esoar_analysis_function_response != None):
                log_writer(script_name = 'Service-Desk-Data-Process', steps = '18-B', status = 'INFO', message = f'For Account: "{account_unique_id}" ESO Analysis Backend Process Response Generate')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '18-B', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '18-B', message = str(error))

        # check the result for "ERROR":S18-C
        try:
            if (str(esoar_analysis_function_response['status']).lower() == 'error'):
                SERVICE_DESK_ESOAR_ANALYSIS_PROCESS_COMPLETE_STATUS = False
                log_writer(script_name = str(esoar_analysis_function_response['file_name']), steps = str(esoar_analysis_function_response['step']), status = 'ERROR', message = str(esoar_analysis_function_response['message']))
                # sending error mail to developer
                # error_mail(file_name = str(esoar_analysis_function_response['file_name']), step = str(esoar_analysis_function_response['step']), message = str(esoar_analysis_function_response['message']))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '18-C', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '18-C', message = str(error))

        # check the result for "SUCCESS":S18-D
        try:
            if (str(esoar_analysis_function_response['status']).lower() == 'success'):
                SERVICE_DESK_ESOAR_ANALYSIS_PROCESS_COMPLETE_STATUS = True
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '18-D', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '18-D', message = str(error))
    #####################################################

    # updating final "process_name" and "completion_time_seconds" inside "file_process_status":S19
    if (SERVICE_DESK_ESOAR_ANALYSIS_PROCESS_COMPLETE_STATUS):
        # fetching total "completion_time_seconds":S19-A
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
                        log_writer(script_name = 'Service-Desk-Data-Process', steps = '19-A', status = 'SUCCESS', message = f'For Account: "{file_unique_id}" All Process Completion Seconds Fetched')
                    else:
                        log_writer(script_name = 'Service-Desk-Data-Process', steps = '19-A', status = 'ERROR', message = f'For Account: "{file_unique_id}" All Process Completion Seconds Not Fetched')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '19-A', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '19-A', message = str(error))

        # updating "process_name" to "Analysis Complete":S19-B
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
                        log_writer(script_name = 'Service-Desk-Data-Process', steps = '19-B', status = 'ERROR', message = f'For Account: "{str(account_unique_id)}" Whole Analysis Complete')
                    else:
                        database_connection.commit()
                        log_writer(script_name = 'Service-Desk-Data-Process', steps = '19-B', status = 'SUCCESS', message = f'For Account: "{str(account_unique_id)}" Whole Analysis Not Completed')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Data-Process', steps = '19-B', status = 'ERROR', message = str(error))
            # error_mail(file_name = 'Service-Desk-Data-Process', step = '19-B', message = str(error))
    #####################################################