# define "submitted_file_details_table_create" function
def submitted_file_details_table_create(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S01
    try:
        import psycopg2
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Submitted-File-Details-Table-Create', 'step': '1', 'message': str(error)}

    # define database connection parameter:S02
    try:
        database_connection_parameter = {
            "dbname": str(db_name),
            "user": str(db_user),
            "password": str(db_password),
            "host": str(db_host),
            "port": str(db_port)
        }
        table_owner = str(db_user)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Submitted-File-Details-Table-Create', 'step': '2', 'message': str(error)}

    # check if "submitted_file_details" table already present:S03
    try:
        submitted_file_details_table_present_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'submitted_file_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(submitted_file_details_table_present_sql)
                if (database_cursor.fetchone()[0]):
                    return {'status': 'SUCCESS', 'file_name': 'Submitted-File-Details-Table-Create', 'step': '3', 'message': '"submitted_file_details" Table Already Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Submitted-File-Details-Table-Create', 'step': '3', 'message': str(error)}

    # execute table create query:S04
    try:
        submitted_file_details_table_create_sql = f'''
        CREATE TABLE submitted_file_details (
            id SERIAL PRIMARY KEY,
            file_unique_id VARCHAR(6) NOT NULL UNIQUE CHECK (char_length(file_unique_id) = 6),
            account_name VARCHAR(150) NOT NULL,
            file_submit_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            shared_file_name VARCHAR(150) NOT NULL,
            saved_file_name VARCHAR(150) NOT NULL,
            file_path_in_server TEXT NOT NULL,
            file_size_in_bytes BIGINT NOT NULL,
            data_rows_count BIGINT NOT NULL,
            file_type VARCHAR(4) NOT NULL CHECK (LOWER(file_type) = 'xlsx'),
            file_approved_status VARCHAR(8) NOT NULL DEFAULT 'Declined' CHECK (file_approved_status IN ('Approved','Declined'))
        );
        ALTER TABLE submitted_file_details OWNER TO {table_owner};'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(submitted_file_details_table_create_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Submitted-File-Details-Table-Create', 'step': '4', 'message': str(error)}

    # verify table created:S05
    try:
        submitted_file_details_table_present_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'submitted_file_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(submitted_file_details_table_present_sql)
                if (not (database_cursor.fetchone()[0])):
                    return {'status': 'ERROR', 'file_name': 'Submitted-File-Details-Table-Create', 'step': '5', 'message': '"submitted_file_details" Table Not Created'}
                else:
                    return {'status': 'SUCCESS', 'file_name': 'Submitted-File-Details-Table-Create', 'step': '5', 'message': '"submitted_file_details" Table Created Successfully'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Submitted-File-Details-Table-Create', 'step': '5', 'message': str(error)}