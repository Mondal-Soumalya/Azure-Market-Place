# define "file_process_status_table_create" function
def file_process_status_table_create(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S1
    try:
        import psycopg2
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Process-Status-Table-Create', 'step': '1', 'message': str(error)}

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
        return {'status': 'ERROR', 'file_name': 'Process-Status-Table-Create', 'step': '2', 'message': str(error)}

    # check if "file_process_status" table already present:S3
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
                    return {'status': 'SUCCESS', 'file_name': 'Process-Status-Table-Create', 'step': '3', 'message': '"file_process_status" Table Already Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Process-Status-Table-Create', 'step': '3', 'message': str(error)}

    # execute table create query:S4
    try:
        file_process_status_table_create_sql = f'''
        CREATE TABLE file_process_status (
            id SERIAL PRIMARY KEY,
            file_unique_id VARCHAR(6) NOT NULL CHECK (char_length(file_unique_id) = 6),
            shared_file_name VARCHAR(150) NOT NULL,
            process_name VARCHAR(80) NOT NULL CHECK (
                process_name IN (
                    'Column Mapping', 'File To DB', 'Output Data Fill', 'Data Normalization',
                    'Information Cleaning', 'Translate And Desk Language Analysis',
                    'Keywords Analysis', 'Automation Mapping', 'MTTR Analysis',
                    'Elimination Analysis', 'Standardization Analysis', 'Optimization Analysis',
                    'Final Category Analysis', 'KB Details Analysis', 'Chat Only Ticket',
                    'BuddyBot Analysis', 'CHIP Analysis', 'Analysis Complete'
                )
            ),
            process_description TEXT NOT NULL,
            completion_time_seconds BIGINT NOT NULL DEFAULT 0,
            row_updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            CONSTRAINT fk_file_process FOREIGN KEY (file_unique_id) REFERENCES submitted_file_details(file_unique_id),
            CONSTRAINT unique_file_process UNIQUE (file_unique_id, process_name)
        );
        ALTER TABLE file_process_status OWNER TO {table_owner};'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(file_process_status_table_create_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Process-Status-Table-Create', 'step': '4', 'message': str(error)}

    # verify table created:S5
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
                if (not (database_cursor.fetchone()[0])):
                    return {'status': 'ERROR', 'file_name': 'Process-Status-Table-Create', 'step': '5', 'message': 'Table Not Created'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Process-Status-Table-Create', 'step': '5', 'message': str(error)}

    # define process description mapping:S6
    try:
        process_descriptions = {
            'File To DB': 'Loading submitted file data into the database.',
            'Output Data Fill': 'Populating output tables with input data.',
            'Data Normalization': 'Normalizing data values for uniformity.',
            'Information Cleaning': 'Removing client facing data and cleaning invalid entries.',
            'Translate And Desk Language Analysis': 'Getting the Desk Language of the ticket and translating to English.',
            'Keywords Analysis': 'Extracting and analyzing keywords from the dataset.',
            'Automation Mapping': 'Mapping processes to automation workflows with BoT catalogue.',
            'MTTR Analysis': 'Calculating Mean Time To Resolution.',
            'Elimination Analysis': 'Identifying redundant steps for elimination.',
            'Standardization Analysis': 'Ensuring standard practices across processes.',
            'Optimization Analysis': 'Analyzing optimization opportunities.',
            'Final Category Analysis': 'Classifying data into final categories.',
            'KB Details Analysis': 'Extracting KB articles referenced or attached.',
            'Chat Only Ticket': 'Identifying chat-only tickets.',
            'BuddyBot Analysis': 'Identifying tickets created by BuddyBot.',
            'CHIP Analysis': 'Identifying tickets created by CHIP.',
            'Analysis Complete': 'All parameter analysis completed.'
        }
        case_statements = "\n".join(
            [f"WHEN '{key}' THEN '{value}'" for key, value in process_descriptions.items()]
        )
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Process-Status-Table-Create', 'step': '6', 'message': str(error)}

    # executing trigger function:S7
    try:
        trigger_function_sql = f'''
        CREATE OR REPLACE FUNCTION populate_process_information()
        RETURNS TRIGGER AS $$ 
        BEGIN
            IF NEW.completion_time_seconds IS NULL THEN
                NEW.completion_time_seconds := 0;
            END IF;

            IF NEW.process_name <> 'Column Mapping' THEN
                NEW.process_description := CASE NEW.process_name
                    {case_statements}
                    ELSE 'Process description not available.'
                END;
            END IF;

            IF NEW.file_unique_id IS NOT NULL THEN
                SELECT shared_file_name INTO NEW.shared_file_name
                FROM submitted_file_details
                WHERE file_unique_id = NEW.file_unique_id;

                IF NEW.shared_file_name IS NULL THEN
                    RAISE EXCEPTION 'Invalid file_unique_id: %', NEW.file_unique_id;
                END IF;
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
        return {'status': 'ERROR', 'file_name': 'Process-Status-Table-Create', 'step': '7', 'message': str(error)}

    # executing trigger definition:S8
    try:
        trigger_definition_sql = '''
        DROP TRIGGER IF EXISTS trg_populate_process_information ON file_process_status;
        CREATE TRIGGER trg_populate_process_information
        BEFORE INSERT OR UPDATE ON file_process_status
        FOR EACH ROW
        EXECUTE FUNCTION populate_process_information();'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_definition_sql)
                database_connection.commit()
                return {'status': 'SUCCESS', 'file_name': 'Process-Status-Table-Create', 'step': '8', 'message': '"file_process_status" Table Created With Auto-Trigger Function'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Process-Status-Table-Create', 'step': '8', 'message': str(error)}