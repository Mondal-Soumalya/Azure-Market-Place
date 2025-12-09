# define "service_desk_ticket_file_handler" function
def service_desk_ticket_file_handler(user_email: str, user_unique_id: str, account_unique_id: str, file) -> dict[str, str]: #type: ignore
    # importing module:S01
    try:
        from pathlib import Path
        from dotenv import dotenv_values
        import sys
        from werkzeug.utils import secure_filename
        from datetime import datetime
        from zoneinfo import ZoneInfo
        import shutil
        import pandas
        import psycopg2
        import string
        import random
        from threading import Thread
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '2', 'message' : str(error)}

    # importing user defined function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
        # from Backend.MailSentHandler.mailhandler import mail_handler
        from Backend.ServiceDeskDumpHandler.servicedeskdataprocess import service_desk_data_process
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '3', 'message' : str(error)}

    # define parent folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        submitted_files_folder_path = Path(parent_folder_path) / 'SubmittedFiles'
        service_desk_files_folder_path = Path(submitted_files_folder_path) / 'ServiceDeskFiles'
        temp_files_dump_folder_path = Path(parent_folder_path) / 'TempFilesDump'
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '4', status = 'SUCCESS', message = 'All Folders And Files Path Are Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '4', 'message' : str(error)}

    # check if folders are present:S05
    try:
        folders_to_create = [submitted_files_folder_path, service_desk_files_folder_path, temp_files_dump_folder_path]
        # loop through each folder path and create if not exists
        for folder_path in folders_to_create:
            folder_path.mkdir(parents = True, exist_ok = True)
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '5', 'message' : str(error)}

    # check if ".env" file is present:S06
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '6', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '6', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '6', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '6', 'message' : str(error)}

    # load ".env" file into script:S07
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '7', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '7', 'message' : str(error)}

    # define database connection parameter:S08
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '8', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '8', 'message' : str(error)}

    # check if "submitted_file_details" table present inside database:S09
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
                    log_writer(script_name = 'Service-Desk-File-Handler', steps = '9', status = 'SUCCESS', message = '"submitted_file_details" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-File-Handler', steps = '9', status = 'ERROR', message = '"submitted_file_details" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '9', 'message' : '"submitted_file_details" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '9', 'message' : str(error)}

    # check if "account_details" table present inside database:S10
    try:
        submitted_file_details_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'account_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(submitted_file_details_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Service-Desk-File-Handler', steps = '10', status = 'SUCCESS', message = '"account_details" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-File-Handler', steps = '10', status = 'ERROR', message = '"account_details" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '10', 'message' : '"account_details" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '10', 'message' : str(error)}

    #define file store path:S11
    try:
        # define current UTC time
        utc_current_time = datetime.now(ZoneInfo('UTC')).strftime("%Y-%m-%d_%H-%M-%S")
        # define file name
        new_file_name = secure_filename(f"{account_unique_id}_{utc_current_time}_UTC.xlsx")
        # define file store path
        new_file_archive_store_path = Path(service_desk_files_folder_path) / new_file_name
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '11', status = 'SUCCESS', message = f'"{new_file_name}" File Name Created')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '11', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '11', 'message' : str(error)}

    # if file type is ".xlsx" save the file:S12
    try:
        if (file.filename.endswith('.xlsx')) :
            # shared file name
            shared_file_name = file.filename
            # save the file with new file name
            file.save(new_file_archive_store_path)
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '12', status = 'SUCCESS', message = f'"{new_file_name}" File Saved In "../ServiceDeskFiles" Folder')
        else:
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '12', status = 'ERROR', message = f'"{new_file_name}" Doesn\'t Has Allowed Extension')
            return {'status' : 'INFO', 'file_name' : 'Service-Desk-File-Handler', 'step' : '12', 'message' : 'Submitted File Type Not In ".xlsx" Format'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '12', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '12', 'message' : str(error)}

    # copy stored file into "TempFilesDump" folder for future process:S13
    try:
        # define destination file path
        new_file_temp_stored_path = Path(temp_files_dump_folder_path) / new_file_archive_store_path.name
        shutil.copy2(new_file_archive_store_path, new_file_temp_stored_path)
        # check if file copied sucessfully
        if ((int(new_file_archive_store_path.stat().st_size)) == (int(new_file_temp_stored_path.stat().st_size))):
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '13', status = 'SUCCESS', message = f'"{new_file_name}" File Copied To "../TempFilesDump" Folder For Future Processing')
        else:
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '13', status = 'ERROR', message = f'"{new_file_name}" File Not Copied To "../TempFilesDump" Folder')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '13', 'message' : f'"{new_file_name}" File Not Copied To "../TempFilesDump" Folder'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '13', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '13', 'message' : str(error)}

    # gather submitted files details for data insertion:S14
    try:
        # archive store file name
        saved_file_name = str(new_file_archive_store_path.name)
        # archive store file path
        file_path_in_server = str(new_file_archive_store_path)
        # archive store file size in bytes
        file_size_in_bytes = int(new_file_temp_stored_path.stat().st_size)
        # archive store file rows count
        temp_file_dataframe = pandas.read_excel(str(new_file_temp_stored_path))
        data_rows_count = int(temp_file_dataframe.shape[0])
        del temp_file_dataframe
        # archive store file type
        file_type = str(new_file_temp_stored_path.suffix.lstrip('.').lower())
        # archive store file sheet count
        temp_file_metadata = pandas.ExcelFile(str(new_file_temp_stored_path))
        temp_file_sheet_names = temp_file_metadata.sheet_names
        if (int(len(temp_file_sheet_names)) == 1):
            file_approved_status = 'Approved'
        else:
            file_approved_status = 'Declined'
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '14', status = 'SUCCESS', message = f'For File: "{shared_file_name}" All Metadata Fetched For Data Insertion')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '14', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '14', 'message' : str(error)}

    # define constant
    file_unique_id = ''

    while True:
        # generating "file_uniqe_id" for data insertion:S15
        try:
            file_unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '15', status = 'SUCCESS', message = f'For File: "{shared_file_name}" New "file_unique_id" Generated')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '15', 'message' : str(error)}

        # checking "file_unique_id" already present inside "submitted_file_details" table:S16
        try:
            file_unique_id_check_for_submitted_file_details_sql = '''
            SELECT 1
            FROM submitted_file_details
            WHERE file_unique_id = %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(file_unique_id_check_for_submitted_file_details_sql, (str(file_unique_id), ))
                    # check the result
                    if (database_cursor.fetchone()):
                        log_writer(script_name = 'Service-Desk-File-Handler', steps = '16', status = 'INFO', message = f'For File: "{shared_file_name}" Generated "file_unique_id" Already Present Inside "file_submitted_details" Table, Hence Generating New "file_unique_id"')
                        continue
                    else:
                        log_writer(script_name = 'Service-Desk-File-Handler', steps = '16', status = 'SUCCESS', message = f'For File: "{shared_file_name}" Generated "file_unique_id" Not Present Inside "file_submitted_details" Table')
                        break
        except Exception as error:
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '16', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '16', 'message' : str(error)}

    # insert file metadata into "submitted_file_details" table:S17
    try:
        file_metadata_insert_for_submitted_file_details_sql = '''
        INSERT INTO submitted_file_details (
            file_unique_id,
            account_unique_id,
            file_submitted_by,
            shared_file_name,
            saved_file_name,
            file_path_in_server,
            file_size_in_bytes,
            data_rows_count,
            file_type,
            file_approved_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(file_metadata_insert_for_submitted_file_details_sql, (str(file_unique_id) , str(account_unique_id), str(user_unique_id), str(shared_file_name), str(saved_file_name), str(file_path_in_server), int(file_size_in_bytes), int(data_rows_count), str(file_type), str(file_approved_status)))
                database_connection.commit()
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '17', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '17', 'message' : str(error)}

    # check if file data successfully added into "submitted_file_details" table:S18
    try:
        file_metadata_check_for_submitted_file_details_sql = '''
        SELECT EXISTS (
            SELECT 1 FROM submitted_file_details
            WHERE account_unique_id = %s
            AND file_submitted_by = %s
            AND saved_file_name = %s
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(file_metadata_check_for_submitted_file_details_sql, (str(account_unique_id), str(user_unique_id), str(saved_file_name)))
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Service-Desk-File-Handler', steps = '18', status = 'SUCCESS', message = f'For File: "{saved_file_name}" All Metadata Stored Inside "submitted_file_details" Table')
                else:
                    log_writer(script_name = 'Service-Desk-File-Handler', steps = '18', status = 'ERROR', message = f'For File: "{saved_file_name}" Metadata Not Stored Inside "submitted_file_details" Table')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '18', 'message' : f'For File: "{saved_file_name}" Metadata Not Stored Inside "submitted_file_details" Table'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '18', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '18', 'message' : str(error)}

    # updating "total_rows_count" inside "account_details" table:S19
    try:
        if (int(len(temp_file_sheet_names)) == 1):
            total_rows_count_update_for_account_details_sql = '''
            UPDATE account_details
            SET total_rows_count = total_rows_count + %s
            WHERE account_unique_id = %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(total_rows_count_update_for_account_details_sql, (int(data_rows_count), str(account_unique_id)))
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-File-Handler', steps = '19', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total Rows Count Updated Inside "account_details" Table')
        else:
            log_writer(script_name = 'Service-Desk-File-Handler', steps = '19', status = 'INFO', message = f'For Account: "{account_unique_id}" Skipping "total_rows_count" Update Inside "account_details" Table Due To Not Approved File')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '19', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '19', 'message' : str(error)}

    # # calling "mail_handler" function:S20
    # try:
    #     # define email body template with html tag
    #     email_body = f'''
    #     <html>
    #         <head>
    #             <style>
    #             body {{
    #                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    #                 color: #2c3e50;
    #                 background-color: #f9f9f9;
    #                 padding: 20px;
    #             }}
    #             .container {{
    #                 background-color: #ffffff;
    #                 border: 1px solid #ddd;
    #                 border-radius: 8px;
    #                 padding: 25px;
    #                 max-width: 600px;
    #                 margin: auto;
    #                 box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    #             }}
    #             .highlight {{
    #                 color: #27ae60;
    #                 font-weight: bold;
    #                 font-size: 22px;
    #             }}
    #             .footer-note {{
    #                 font-size: 14px;
    #                 color: #7f8c8d;
    #                 font-style: italic;
    #                 font-weight: bold;
    #                 margin-top: 30px;
    #                 text-align: center;
    #             }}
    #             .greeting, .closing {{
    #                 margin-top: 20px;
    #             }}
    #             </style>
    #         </head>
    #             <body>
    #                 <div class="container">
    #                 <p class="greeting"><strong>Hello Team,</strong></p>
    #                 <p><span style="color: green; font-weight: bold;"><strong>Success!</strong></span> The service-desk dump file has been uploaded <em>without any issues</em>.</p>
    #                 <p><strong>Below are the uploaded file details:</strong></p>
    #                 <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; font-family: Arial, sans-serif;">
    #                     <tr>
    #                         <th style="background-color: #f2f2f2;">Detail</th>
    #                         <th style="background-color: #f2f2f2;">Value</th>
    #                     </tr>
    #                     <tr>
    #                         <td>File Name</td>
    #                         <td>{file.filename}</td>
    #                     </tr>
    #                     <tr>
    #                         <td>File Type</td>
    #                         <td>{file_type}</td>
    #                     </tr>
    #                     <tr>
    #                         <td>Submitted Time(UTC)</td>
    #                         <td>{datetime.now(ZoneInfo('UTC')).strftime('%d-%b-%Y %H:%M:%S')}</td>
    #                     </tr>
    #                     <tr>
    #                         <td>File Size(MB)</td>
    #                         <td>{(int(file_size_in_bytes) / (1024 * 1024)):.2f}</td>
    #                     </tr>
    #                 </table>
    #             <p><strong>A new ticket will be create inside ServiceNow after successfull intial file process.</strong></p>
    #             <p class="closing"> <strong>Thank you</strong> for your attention.<br><br>
    #             Best Regards,<br>
    #             <strong>Automation ASTRA</strong></p>
    #             <p class="footer-note">
    #                 *** This is a system-generated email. Please do not reply. ***
    #             </p>
    #             </div>
    #         </body>
    #     </html>'''
    #     mail_handler(email_subject = 'ASTRA | ESOAR Analysis', email_to = str(user_email).lower(), email_cc = 'soumalya.mondal@capgemini.com;anurag.thakur@capgemini.com', email_body = str(email_body))
    # except Exception as error:
    #     log_writer(script_name = 'Service-Desk-File-Handler', steps = '20', status = 'ERROR', message = str(error))
    #     return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '20', 'message' : str(error)}

    # calling "service_desk_data_process" thread:S21
    try:
        def run_service_desk_process():
            service_desk_data_process(account_unique_id = str(account_unique_id), file_unique_id = str(file_unique_id), user_unique_id = str(user_unique_id), user_email = str(user_email), file_path = str(new_file_temp_stored_path))
        thread = Thread(target = run_service_desk_process)
        thread.start()
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '21', status = 'SUCCESS', message = 'A New Thread Started For Service-Desk Data Processing')
        # return message to frontend
        return {'status' : 'SUCCESS', 'file_name' : 'Service-Desk-File-Handler', 'step' : '21', 'message' : 'File Saved & Data Processing Will Start Shortly'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-File-Handler', steps = '21', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-File-Handler', 'step' : '21', 'message' : str(error)}