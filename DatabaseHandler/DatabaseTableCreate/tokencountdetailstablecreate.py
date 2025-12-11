# define "token_count_details_table_create" function
def token_count_details_table_create(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S1
    try:
        import psycopg2
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Token-Count-Details-Table-Create', 'step': '1', 'message': str(error)}

    # define database connection parameter:S2
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
        return {'status': 'ERROR', 'file_name': 'Token-Count-Details-Table-Create', 'step': '2', 'message': str(error)}

    # check if table exists:S3
    try:
        token_count_details_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'token_count_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(token_count_details_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    return {'status': 'INFO', 'file_name': 'Token-Count-Details-Table-Create', 'step': '3','message': '"token_count_details" Table Already Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Token-Count-Details-Table-Create', 'step': '3', 'message': str(error)}

    # create table:S4
    try:
        token_count_details_table_create_sql = f'''
        CREATE TABLE token_count_details (
            id SERIAL PRIMARY KEY,
            ticket_number VARCHAR(20) NOT NULL,
            row_updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            model_name VARCHAR(100),
            model_version VARCHAR(100),
            prompt_token INTEGER NOT NULL DEFAULT 0,
            output_token INTEGER NOT NULL DEFAULT 0,
            total_tokens INTEGER GENERATED ALWAYS AS (prompt_token + output_token) STORED,
            CONSTRAINT unique_ticket_token UNIQUE (ticket_number)
        );
        ALTER TABLE token_count_details OWNER TO {table_owner};'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(token_count_details_table_create_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Token-Count-Details-Table-Create', 'step': '4', 'message': str(error)}

    # verify table creation:S5
    try:
        verify_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'token_count_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(verify_sql)
                if (not (database_cursor.fetchone()[0])):
                    return {'status': 'ERROR', 'file_name': 'Token-Count-Details-Table-Create', 'step': '5', 'message': 'Table Not Created'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Token-Count-Details-Table-Create', 'step': '5', 'message': str(error)}

    # trigger function:S6
    try:
        trigger_function_sql = '''
        CREATE OR REPLACE FUNCTION sum_token_values()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Normalize ticket_number
            IF NEW.ticket_number IS NOT NULL THEN
                NEW.ticket_number := UPPER(TRIM(NEW.ticket_number));
            END IF;

            -- Allow rows only if ticket exists in input_incident_data
            IF NOT EXISTS (SELECT 1 FROM input_incident_data WHERE ticket_number = NEW.ticket_number)
            THEN
                RETURN NULL; -- Skip insertion
            END IF;

            -- If record exists, update instead of insert
            IF EXISTS (
                SELECT 1 FROM token_count_details
                WHERE ticket_number = NEW.ticket_number
                AND id <> NEW.id
            ) THEN
                UPDATE token_count_details
                SET 
                    prompt_token   = prompt_token + NEW.prompt_token,
                    output_token   = output_token + NEW.output_token,
                    model_name     = COALESCE(NEW.model_name, model_name),
                    model_version  = COALESCE(NEW.model_version, model_version),
                    row_updated_at = NOW()
                WHERE ticket_number = NEW.ticket_number;

                RETURN NULL;
            END IF;

            NEW.row_updated_at := NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_function_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Token-Count-Details-Table-Create', 'step': '6', 'message': str(error)}

    # trigger definition:S7
    try:
        trigger_definition_sql = '''
        DROP TRIGGER IF EXISTS trg_sum_token_values ON token_count_details;
        CREATE TRIGGER trg_sum_token_values
        BEFORE INSERT OR UPDATE ON token_count_details
        FOR EACH ROW
        EXECUTE FUNCTION sum_token_values();'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_definition_sql)
                database_connection.commit()
                return {'status': 'SUCCESS', 'file_name': 'Token-Count-Details-Table-Create', 'step': '7', 'message': '"token_count_details" Table Created With Auto-Trigger Function'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Token-Count-Details-Table-Create', 'step': '7', 'message': str(error)}