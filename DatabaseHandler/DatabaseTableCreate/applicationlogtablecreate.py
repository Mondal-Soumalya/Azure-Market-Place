# define "application_log_table_create" function
def application_log_table_create(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S1
    try:
        import psycopg2
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Application-Log-Table-Create', 'step': '1', 'message': str(error)}

    # define database connection parameter:S2
    try:
        database_connection_parameter = {
            'dbname': str(db_name),
            'user': str(db_user),
            'password': str(db_password),
            'host': str(db_host),
            'port': str(db_port)
        }
        table_owner = str(db_user)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Application-Log-Table-Create', 'step': '2', 'message': str(error)}

    # check if "application_log" table already present:S3
    try:
        application_log_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'application_log'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(application_log_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    return {'status': 'INFO', 'file_name': 'Application-Log-Table-Create', 'step': '3', 'message': '"application_log" Table Already Present.'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Application-Log-Table-Create', 'step': '3', 'message': str(error)}

    # execute table create query:S4
    try:
        application_log_table_create_sql = f'''
        CREATE TABLE application_log (
            id SERIAL PRIMARY KEY,
            logtime TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            service_name VARCHAR(100) NOT NULL,
            service_step VARCHAR(10) NOT NULL,
            service_status VARCHAR(10) NOT NULL CHECK (service_status IN ('SUCCESS','INFO','ERROR')),
            message TEXT
        );
        ALTER TABLE application_log OWNER TO {table_owner};'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(application_log_table_create_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Application-Log-Table-Create', 'step': '4', 'message': str(error)}

    # verify table created:S5
    try:
        application_log_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'application_log'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(application_log_table_present_check_sql)
                if (not (database_cursor.fetchone()[0])):
                    return {'status': 'ERROR', 'file_name': 'Application-Log-Table-Create', 'step': '5', 'message': 'Table Not Created.'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Application-Log-Table-Create', 'step': '5', 'message': str(error)}

    # executing trigger functions:S6
    try:
        trigger_function_sql = '''
        DROP FUNCTION IF EXISTS normalize_application_log_fields();
        CREATE FUNCTION normalize_application_log_fields()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.service_name IS NOT NULL THEN
                NEW.service_name := UPPER(TRIM(NEW.service_name));
            END IF;

            IF NEW.service_status IS NOT NULL THEN
                NEW.service_status := UPPER(TRIM(NEW.service_status));
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_function_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Application-Log-Table-Create', 'step': '6', 'message': str(error)}

    # executing trigger definition:S7
    try:
        trigger_definition_sql = '''
        DROP TRIGGER IF EXISTS trg_normalize_application_log_fields ON application_log;
        CREATE TRIGGER trg_normalize_application_log_fields
        BEFORE INSERT OR UPDATE ON application_log
        FOR EACH ROW
        EXECUTE FUNCTION normalize_application_log_fields();'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_definition_sql)
                database_connection.commit()
                return {'status': 'SUCCESS', 'file_name': 'Application-Log-Table-Create', 'step': '7', 'message': '"application_log" Table Created With Auto-Trigger Function.'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Application-Log-Table-Create', 'step': '7', 'message': str(error)}