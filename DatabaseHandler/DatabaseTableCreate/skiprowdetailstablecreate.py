# define "skip_row_details_table_create" function
def skip_row_details_table_create(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S1
    try:
        import psycopg2
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '1', 'message': str(error)}

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
        return {'status': 'ERROR', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '2', 'message': str(error)}

    # check if "skip_row_details" table already exists:S3
    try:
        skip_row_details_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'skip_row_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(skip_row_details_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    return {'status': 'INFO', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '3', 'message': '"skip_row_details" Table Already Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '3', 'message': str(error)}

    # execute table create query:S4
    try:
        skip_row_details_table_create_sql = f'''
        CREATE TABLE skip_row_details (
            id SERIAL PRIMARY KEY,
            ticket_number VARCHAR(20) NOT NULL,
            file_unique_id VARCHAR(6) NOT NULL CHECK (char_length(file_unique_id) = 6),
            row_inserted_at TIMESTAMP NOT NULL DEFAULT NOW(),
            skip_reason VARCHAR(50),
            CONSTRAINT fk_file_unique FOREIGN KEY (file_unique_id) REFERENCES submitted_file_details(file_unique_id)
        );
        ALTER TABLE skip_row_details OWNER TO {table_owner};'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(skip_row_details_table_create_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '4', 'message': str(error)}

    # verify table creation:S5
    try:
        skip_row_details_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'skip_row_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(skip_row_details_table_present_check_sql)
                if (not (database_cursor.fetchone()[0])):
                    return {'status': 'ERROR', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '5', 'message': 'Table Not Created'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '5', 'message': str(error)}

    # trigger function creation:S6
    try:
        trigger_function_sql = '''
        CREATE OR REPLACE FUNCTION check_file_exists()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Skip insert if file_unique_id not found
            IF NOT EXISTS (
                SELECT 1 FROM submitted_file_details sfd
                WHERE sfd.file_unique_id = NEW.file_unique_id
            ) THEN
                RETURN NULL;
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_function_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '6', 'message': str(error)}

    # trigger definition:S7
    try:
        trigger_definition_sql = '''
        DROP TRIGGER IF EXISTS trg_check_account_file ON skip_row_details;
        CREATE TRIGGER trg_check_account_file
        BEFORE INSERT ON skip_row_details
        FOR EACH ROW
        EXECUTE FUNCTION check_file_exists();'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_definition_sql)
                database_connection.commit()
                return {'status': 'SUCCESS', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '7', 'message': '"skip_row_details" Table Created With Auto-Trigger Function'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Skip-Row-Details-Table-Create', 'step': '7', 'message': str(error)}