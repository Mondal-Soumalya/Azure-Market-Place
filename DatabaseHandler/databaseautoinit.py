# define "database_auto_init" function
def database_auto_init() -> dict[str, str]: #type: ignore
    # importing python module:S1
    try:
        from pathlib import Path
        from dotenv import dotenv_values
        import sys
        import psycopg2
        from psycopg2 import sql
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '1', 'message' : str(error)}

    # appending system path:S2
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '2', 'message' : str(error)}

    # define parent folder and file path:S3
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        database_handler_folder_path = Path(parent_folder_path) / 'DatabaseHandler'
        database_table_create_folder_path = Path(database_handler_folder_path) / 'DatabaseTableCreate'
        database_data_entry_folder_path = Path(database_handler_folder_path) / 'DatabaseDataEntry'
        bot_catalogue_data_excel_file_path = Path(database_data_entry_folder_path) / 'BoT_Catalouge_Details.xlsx'
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '3', 'message' : str(error)}

    # check if ".env" file is present:S4
    try:
        if (not ((env_file_path.exists()) and (env_file_path.is_file()))):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '4', 'message' : '".env" File Not Present.'}
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '4', 'message' : str(error)}

    # define all the files name:S5
    try:
        database_table_create_scripts_files = ['applicationlogtablecreate.py', 'botcataloguedetailstablecreate.py', 'submittedfiletablecreate.py', 'fileprocessstatustablecreate.py', 'skiprowdetailstablecreate.py', 'inputincidentdatatablecreate.py', 'processincidentdatatablecreate.py', 'tokencountdetailstablecreate.py']
        database_data_entry_files = ['botcatalougedataentry.py', 'BoT_Catalouge_Details.xlsx']
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '5', 'message' : str(error)}

    # check all the files are present:S6
    try:
        # checking "database_table_create" files
        for file_name in database_table_create_scripts_files:
            if not (Path(database_table_create_folder_path) / file_name).exists():
                return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '6', 'message' : f'File Not Found: {file_name}.'}
        # checking "database_data_entry" files
        for file_name in database_data_entry_files:
            if not (Path(database_data_entry_folder_path) / file_name).exists():
                return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '6', 'message' : f'File Not Found: {file_name}.'}
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '6', 'message' : str(error)}

    # load environment variables and admin credential:S7
    try:
        environment_values = dotenv_values(env_file_path)
        db_name = str(environment_values.get('DATABASE_NAME'))
        db_user = str(environment_values.get('DATABASE_USER'))
        db_password = str(environment_values.get('DATABASE_PASSWORD'))
        db_host = str(environment_values.get('DATABASE_HOST'))
        db_port = str(environment_values.get('DATABASE_PORT'))
        # define postgresql admin credential
        admin_database_connection_parameter = {
            'dbname' : str(environment_values.get('ADMIN_DB_NAME')),
            'user' : str(environment_values.get('ADMIN_DB_USER')),
            'password' : str(environment_values.get('ADMIN_DB_PASSWORD')),
            'host' : str(environment_values.get('ADMIN_DB_HOST')),
            'port' : str(environment_values.get('ADMIN_DB_PORT'))
        }
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '7', 'message' : str(error)}

    # create database "user":S8
    database_cursor = None
    database_connection = None
    try:
        create_user_sql = sql.SQL("CREATE ROLE {} WITH LOGIN NOSUPERUSER CREATEDB NOCREATEROLE INHERIT NOREPLICATION NOBYPASSRLS CONNECTION LIMIT -1 PASSWORD %s").format(sql.Identifier(db_user))
        database_connection = psycopg2.connect(**admin_database_connection_parameter) #type: ignore
        database_connection.autocommit = True  
        database_cursor = database_connection.cursor()
        try:
            database_cursor.execute(create_user_sql, (db_password,))
            print(f'SUCCESS - "{db_user}" User Created Successfully.')
        except psycopg2.Error as pg_error:
            if 'already exists' in str(pg_error):
                print(f'INFO - "{db_user}" User Already Present.')
            else:
                raise pg_error
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '8', 'message' : str(error)}
    finally:
        if database_cursor:
            database_cursor.close()
        if database_connection:
            database_connection.close()

    # check if database is present:S9
    database_cursor = None
    database_connection = None
    try:
        database_existence_check_sql = '''
        SELECT EXISTS (
            SELECT FROM pg_database
            WHERE datname = %s
        );'''
        database_connection = psycopg2.connect(**admin_database_connection_parameter) #type: ignore
        database_connection.autocommit = True  
        database_cursor = database_connection.cursor()
        database_cursor.execute(database_existence_check_sql, (db_name,))
        if (database_cursor.fetchone()[0]):
            print(f'INFO - "{db_name}" Database Already Present.')
        else:
            # create "database" if not present
            create_database_sql = sql.SQL("CREATE DATABASE {} OWNER {}").format(sql.Identifier(db_name), sql.Identifier(db_user))
            database_cursor.execute(create_database_sql)
            print(f'SUCCESS - "{db_name}" Database Created Successfully.')
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '9', 'message' : str(error)}
    finally:
        if database_cursor:
            database_cursor.close()
        if database_connection:
            database_connection.close()

    # creating "application_log" table:S10
    # importing "application_log_table_create" function:S10-A
    try:
        from DatabaseHandler.DatabaseTableCreate.applicationlogtablecreate import application_log_table_create
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '10-A', 'message' : str(error)}

    # calling "application_log_table_create" function:S10-B
    try:
        application_log_table_create_backend_response = application_log_table_create(db_name = str(db_name), db_user = str(db_user), db_password = str(db_password), db_host = str(db_host), db_port = str(db_port))
        if (application_log_table_create_backend_response == None):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '10-B', 'message' : '"application_log_table_create" Function Not Executed Properly.'}
        elif (str(application_log_table_create_backend_response['status']).lower() == 'error'):
            return {'status' : 'ERROR', 'file_name' : str(application_log_table_create_backend_response['file_name']), 'step' : str(application_log_table_create_backend_response['step']), 'message' : str(application_log_table_create_backend_response['message'])}
        elif (str(application_log_table_create_backend_response['status']).lower() == 'info'):
            print(f"INFO - {str(application_log_table_create_backend_response['message'])}.")
        elif (str(application_log_table_create_backend_response['status']).lower() == 'success'):
            print(f"SUCCESS - {str(application_log_table_create_backend_response['message'])}.")
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '10-B', 'message' : str(error)}

    # creating "bot_catalogue_details" table:S11
    # importing "bot_catalogue_details_table_create" function:S11-A
    try:
        from DatabaseHandler.DatabaseTableCreate.botcataloguedetailstablecreate import bot_catalogue_details_table_create
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '11-A', 'message' : str(error)}

    # calling "bot_catalogue_details_table_create" function:S11-B
    try:
        bot_catalogue_details_table_create_backend_response = bot_catalogue_details_table_create(db_name = str(db_name), db_user = str(db_user), db_password = str(db_password), db_host = str(db_host), db_port = str(db_port))
        if (bot_catalogue_details_table_create_backend_response == None):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '11-B', 'message' : '"bot_catalogue_details_table_create" Function Not Executed Properly.'}
        elif (str(bot_catalogue_details_table_create_backend_response['status']).lower() == 'error'):
            return {'status' : 'ERROR', 'file_name' : str(bot_catalogue_details_table_create_backend_response['file_name']), 'step' : str(bot_catalogue_details_table_create_backend_response['step']), 'message' : str(bot_catalogue_details_table_create_backend_response['message'])}
        elif (str(bot_catalogue_details_table_create_backend_response['status']).lower() == 'info'):
            print(f"INFO - {str(bot_catalogue_details_table_create_backend_response['message'])}.")
        elif (str(bot_catalogue_details_table_create_backend_response['status']).lower() == 'success'):
            print(f"SUCCESS - {str(bot_catalogue_details_table_create_backend_response['message'])}.")
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '11-B', 'message' : str(error)}

    # creating "submitted_file_details" table:S12
    # importing "submitted_file_details_table_create" function:S12-A
    try:
        from DatabaseHandler.DatabaseTableCreate.submittedfiletablecreate import submitted_file_details_table_create
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '12-A', 'message' : str(error)}

    # calling "submitted_file_details_table_create" function:S12-B
    try:
        submitted_file_details_table_create_backend_response = submitted_file_details_table_create(db_name = str(db_name), db_user = str(db_user), db_password = str(db_password), db_host = str(db_host), db_port = str(db_port))
        if (submitted_file_details_table_create_backend_response == None):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '12-B', 'message' : '"submitted_file_details_table_create" Function Not Executed Properly.'}
        elif (str(submitted_file_details_table_create_backend_response['status']).lower() == 'error'):
            return {'status' : 'ERROR', 'file_name' : str(submitted_file_details_table_create_backend_response['file_name']), 'step' : str(submitted_file_details_table_create_backend_response['step']), 'message' : str(submitted_file_details_table_create_backend_response['message'])}
        elif (str(submitted_file_details_table_create_backend_response['status']).lower() == 'info'):
            print(f"INFO - {str(submitted_file_details_table_create_backend_response['message'])}.")
        elif (str(submitted_file_details_table_create_backend_response['status']).lower() == 'success'):
            print(f"SUCCESS - {str(submitted_file_details_table_create_backend_response['message'])}.")
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '12-B', 'message' : str(error)}

    # creating "file_process_status" table:S13
    # importing "file_process_status_table_create" function:S13-A
    try:
        from DatabaseHandler.DatabaseTableCreate.fileprocessstatustablecreate import file_process_status_table_create
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '13-A', 'message' : str(error)}

    # calling "file_process_status_table_create" function:S13-B
    try:
        file_process_status_table_create_backend_response = file_process_status_table_create(db_name = str(db_name), db_user = str(db_user), db_password = str(db_password), db_host = str(db_host), db_port = str(db_port))
        if (file_process_status_table_create_backend_response == None):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '13-B', 'message' : '"file_process_status_table_create" Function Not Executed Properly.'}
        elif (str(file_process_status_table_create_backend_response['status']).lower() == 'error'):
            return {'status' : 'ERROR', 'file_name' : str(file_process_status_table_create_backend_response['file_name']), 'step' : str(file_process_status_table_create_backend_response['step']), 'message' : str(file_process_status_table_create_backend_response['message'])}
        elif (str(file_process_status_table_create_backend_response['status']).lower() == 'info'):
            print(f"INFO - {str(file_process_status_table_create_backend_response['message'])}.")
        elif (str(file_process_status_table_create_backend_response['status']).lower() == 'success'):
            print(f"SUCCESS - {str(file_process_status_table_create_backend_response['message'])}.")
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '13-B', 'message' : str(error)}

    # creating "skip_row_details" table:S14
    # importing "skip_row_details_table_create" function:S14-A
    try:
        from DatabaseHandler.DatabaseTableCreate.skiprowdetailstablecreate import skip_row_details_table_create
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '14-A', 'message' : str(error)}

    # calling "skip_row_details_table_create" function:S14-B
    try:
        skip_row_details_table_create_backend_response = skip_row_details_table_create(db_name = str(db_name), db_user = str(db_user), db_password = str(db_password), db_host = str(db_host), db_port = str(db_port))
        if (skip_row_details_table_create_backend_response == None):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '14-B', 'message' : '"skip_row_details_table_create" Function Not Executed Properly.'}
        elif (str(skip_row_details_table_create_backend_response['status']).lower() == 'error'):
            return {'status' : 'ERROR', 'file_name' : str(skip_row_details_table_create_backend_response['file_name']), 'step' : str(skip_row_details_table_create_backend_response['step']), 'message' : str(skip_row_details_table_create_backend_response['message'])}
        elif (str(skip_row_details_table_create_backend_response['status']).lower() == 'info'):
            print(f"INFO - {str(skip_row_details_table_create_backend_response['message'])}.")
        elif (str(skip_row_details_table_create_backend_response['status']).lower() == 'success'):
            print(f"SUCCESS - {str(skip_row_details_table_create_backend_response['message'])}.")
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '14-B', 'message' : str(error)}

    # creating "input_incident_data" table:S15
    # importing "input_incident_data_table_create" function:S15-A
    try:
        from DatabaseHandler.DatabaseTableCreate.inputincidentdatatablecreate import input_incident_data_table_create
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '15-A', 'message' : str(error)}

    # calling "input_incident_data_table_create" function:S15-B
    try:
        input_incident_data_table_create_backend_response = input_incident_data_table_create(db_name = str(db_name), db_user = str(db_user), db_password = str(db_password), db_host = str(db_host), db_port = str(db_port))
        if (input_incident_data_table_create_backend_response == None):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '15-B', 'message' : '"input_incident_data_table_create" Function Not Executed Properly.'}
        elif (str(input_incident_data_table_create_backend_response['status']).lower() == 'error'):
            return {'status' : 'ERROR', 'file_name' : str(input_incident_data_table_create_backend_response['file_name']), 'step' : str(input_incident_data_table_create_backend_response['step']), 'message' : str(input_incident_data_table_create_backend_response['message'])}
        elif (str(input_incident_data_table_create_backend_response['status']).lower() == 'info'):
            print(f"INFO - {str(input_incident_data_table_create_backend_response['message'])}.")
        elif (str(input_incident_data_table_create_backend_response['status']).lower() == 'success'):
            print(f"SUCCESS - {str(input_incident_data_table_create_backend_response['message'])}.")
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '15-B', 'message' : str(error)}

    # creating "processed_incident_data" table:S16
    # importing "processed_incident_data_table_create" function:S16-A
    try:
        from DatabaseHandler.DatabaseTableCreate.processincidentdatatablecreate import processed_incident_data_table_create
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '16-A', 'message' : str(error)}

    # calling "processed_incident_data_table_create" function:S16-B
    try:
        processed_incident_data_table_create_backend_response = processed_incident_data_table_create(db_name = str(db_name), db_user = str(db_user), db_password = str(db_password), db_host = str(db_host), db_port = str(db_port))
        if (processed_incident_data_table_create_backend_response == None):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '16-B', 'message' : '"processed_incident_data_table_create" Function Not Executed Properly.'}
        elif (str(processed_incident_data_table_create_backend_response['status']).lower() == 'error'):
            return {'status' : 'ERROR', 'file_name' : str(processed_incident_data_table_create_backend_response['file_name']), 'step' : str(processed_incident_data_table_create_backend_response['step']), 'message' : str(processed_incident_data_table_create_backend_response['message'])}
        elif (str(processed_incident_data_table_create_backend_response['status']).lower() == 'info'):
            print(f"INFO - {str(processed_incident_data_table_create_backend_response['message'])}.")
        elif (str(processed_incident_data_table_create_backend_response['status']).lower() == 'success'):
            print(f"SUCCESS - {str(processed_incident_data_table_create_backend_response['message'])}.")
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '16-B', 'message' : str(error)}

    # creating "token_count_details" table:S17
    # importing "token_count_details_table_create" function:S17-A
    try:
        from DatabaseHandler.DatabaseTableCreate.tokencountdetailstablecreate import token_count_details_table_create
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '17-A', 'message' : str(error)}

    # calling "token_count_details_table_create" function:S17-B
    try:
        token_count_details_table_create_backend_response = token_count_details_table_create(db_name = str(db_name), db_user = str(db_user), db_password = str(db_password), db_host = str(db_host), db_port = str(db_port))
        if (token_count_details_table_create_backend_response == None):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '17-B', 'message' : '"token_count_details_table_create" Function Not Executed Properly.'}
        elif (str(token_count_details_table_create_backend_response['status']).lower() == 'error'):
            return {'status' : 'ERROR', 'file_name' : str(token_count_details_table_create_backend_response['file_name']), 'step' : str(token_count_details_table_create_backend_response['step']), 'message' : str(token_count_details_table_create_backend_response['message'])}
        elif (str(token_count_details_table_create_backend_response['status']).lower() == 'info'):
            print(f"INFO - {str(token_count_details_table_create_backend_response['message'])}.")
        elif (str(token_count_details_table_create_backend_response['status']).lower() == 'success'):
            print(f"SUCCESS - {str(token_count_details_table_create_backend_response['message'])}.")
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '17-B', 'message' : str(error)}

    # inserting data into "bot_catalogue_details" table:S18
    # importing "bot_catalogue_details_data_entry" function:S18-A
    try:
        from DatabaseHandler.DatabaseDataEntry.botcatalougedataentry import bot_catalogue_details_data_entry
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '18-A', 'message' : str(error)}

    # calling "bot_catalogue_details_data_entry" function:S18-B
    try:
        token_count_details_table_create_backend_response = bot_catalogue_details_data_entry(db_name = str(db_name), db_user = str(db_user), db_password = str(db_password), db_host = str(db_host), db_port = str(db_port), excel_file_path = str(bot_catalogue_data_excel_file_path))
        if (token_count_details_table_create_backend_response == None):
            return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '18-B', 'message' : '"bot_catalogue_details_data_entry" Function Not Executed Properly.'}
        elif (str(token_count_details_table_create_backend_response['status']).lower() == 'error'):
            return {'status' : 'ERROR', 'file_name' : str(token_count_details_table_create_backend_response['file_name']), 'step' : str(token_count_details_table_create_backend_response['step']), 'message' : str(token_count_details_table_create_backend_response['message'])}
        elif (str(token_count_details_table_create_backend_response['status']).lower() == 'info'):
            print(f"INFO - {str(token_count_details_table_create_backend_response['message'])}.")
            return {'status' : 'SUCCESS', 'file_name' : 'Database-Auto-Init', 'step' : '18-B', 'message' : 'All The Initial Setup Completed For PRiSM-Analytics Application.'}
        elif (str(token_count_details_table_create_backend_response['status']).lower() == 'success'):
            print(f"SUCCESS - {str(token_count_details_table_create_backend_response['message'])}.")
            return {'status' : 'SUCCESS', 'file_name' : 'Database-Auto-Init', 'step' : '18-B', 'message' : 'All The Initial Setup Completed For PRiSM-Analytics Application.'}
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Database-Auto-Init', 'step' : '18-B', 'message' : str(error)}