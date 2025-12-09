# define "bot_catalogue_details_table_create" function
def bot_catalogue_details_table_create(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S01
    try:
        import psycopg2
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '1', 'message': str(error)}

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
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '2', 'message': str(error)}

    # check if "bot_catalogue_details" table already present:S03
    try:
        bot_catalogue_details_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'bot_catalogue_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(bot_catalogue_details_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '3', 'message': '"bot_catalogue_details" Table Already Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '3', 'message': str(error)}

    # execute table create query:S04
    try:
        bot_catalogue_details_table_create_sql = f'''
        CREATE TABLE bot_catalogue_details (
            id SERIAL PRIMARY KEY,
            bot_source VARCHAR(50),
            bot_id VARCHAR(20) NOT NULL UNIQUE,
            functionality VARCHAR(255),
            short_solution_description TEXT,
            tower VARCHAR(100),
            technology VARCHAR(100),
            primary_developed_language VARCHAR(50),
            secondary_developed_language VARCHAR(50),
            operational_response VARCHAR(20) CHECK (operational_response IN ('Remediate', 'Diagnostic')),
            developed_platform VARCHAR(50),
            demand_category VARCHAR(50),
            type_of_automation VARCHAR(100),
            solution_description TEXT,
            row_created_at TIMESTAMPTZ DEFAULT NOW(),
            row_updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        ALTER TABLE bot_catalogue_details OWNER TO {table_owner};'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(bot_catalogue_details_table_create_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '4', 'message': str(error)}

    # verify table created:S05
    try:
        bot_catalogue_details_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'bot_catalogue_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(bot_catalogue_details_table_present_check_sql)
                if (not (database_cursor.fetchone()[0])):
                    return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '5', 'message': 'Table Not Created'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '5', 'message': str(error)}

    # executing trigger function:S06
    try:
        trigger_function_sql = '''
        DROP FUNCTION IF EXISTS normalize_bot_fields();
        CREATE FUNCTION normalize_bot_fields()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Normalize bot_id: trim + uppercase
            IF NEW.bot_id IS NOT NULL THEN
                NEW.bot_id := UPPER(TRIM(NEW.bot_id));
            END IF;

            -- Update timestamp
            NEW.row_updated_at := NOW();

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_function_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '6', 'message': str(error)}

    # executing trigger definition:S07
    try:
        trigger_definition_sql = '''
        DROP TRIGGER IF EXISTS trg_normalize_bot_fields ON bot_catalogue_details;
        CREATE TRIGGER trg_normalize_bot_fields
        BEFORE INSERT OR UPDATE ON bot_catalogue_details
        FOR EACH ROW
        EXECUTE FUNCTION normalize_bot_fields();'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_definition_sql)
                database_connection.commit()
                return {'status': 'SUCCESS', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '7', 'message': '"bot_catalogue_details" Table Created With Auto-Trigger Function'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Details-Table-Create', 'step': '7', 'message': str(error)}