# define log_writer function
def log_writer(script_name: str, steps: str, status: str, message: str):
    # importing python module:S1
    try:
        from pathlib import Path
        from dotenv import dotenv_values
        import psycopg2
    except Exception as error:
        print(f'ERROR - [Log-Writer:S1] - {str(error).title()}')

    # define folder and file path:S2
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
    except Exception as error:
        print(f'ERROR - [Log-Writer:S2] - {str(error)}')

    # check if ".env" file is present:S3
    try:
        if (not ((env_file_path.exists()) and (env_file_path.is_file()))):
            print('ERROR - ".env" File Not Present, Hence Stop Executing Script')
            exit(1)
    except Exception as error:
        print(f'ERROR - [Log-Writer:S3] - {str(error)}')

    # load ".env" file into script:S4
    try:
        environment_values = dotenv_values(env_file_path)
    except Exception as error:
        print(f'ERROR - [Log-Writer:S4] - {str(error)}')

    # define "PostgreSQL" connection parameter:S5
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
    except Exception as error:
        print(f'ERROR - [Log-Writer:S5] - {str(error)}')

    # insert data into PostgreSQL table:S6
    try:
        log_insert_sql = '''
            INSERT INTO application_log (logtime, service_name, service_step, service_status, message)
            VALUES (NOW(), %s, %s, %s, %s)
        '''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            database_connection.autocommit = True
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(log_insert_sql, (str(script_name), str(steps), str(status), str(message)))
    except Exception as error:
        print(f'ERROR - (Log-Writer:S6) - {str(error).title()}')