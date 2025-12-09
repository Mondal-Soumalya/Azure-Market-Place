# define "input_incident_data_table_create" function
def input_incident_data_table_create(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S01
    try:
        import psycopg2
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '1', 'message': str(error)}

    # define connection params:S02
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
        return {'status': 'ERROR', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '2', 'message': str(error)}

    # check if table exists:S03
    try:
        input_incident_data_table_present_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'input_incident_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(input_incident_data_table_present_sql)
                if (database_cursor.fetchone()[0]):
                    # check if table is empty
                    database_cursor.execute("SELECT COUNT(*) FROM input_incident_data;")
                    if int(database_cursor.fetchone()[0]) == 0:
                        database_cursor.execute("DROP TABLE input_incident_data;")
                        database_connection.commit()
                    else:
                        return {'status': 'SUCCESS', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '3', 'message': '"input_incident_data" Table Already Present With Data'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '3', 'message': str(error)}

    # create table:S04
    try:
        input_incident_data_table_create_sql = f'''
        CREATE TABLE input_incident_data (
            id SERIAL PRIMARY KEY,
            ticket_number VARCHAR(20) NOT NULL,
            ticket_type VARCHAR(50) NOT NULL DEFAULT 'Incident',
            row_inserted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            row_updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            ticket_opened_month VARCHAR(3) CHECK (ticket_opened_month IN ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')),
            ticket_opened_year INTEGER CHECK (ticket_opened_year >= 1900 AND ticket_opened_year <= 2200),
            opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            cmdb_ci VARCHAR(100),
            state VARCHAR(50),
            priority VARCHAR(20),
            category VARCHAR(100),
            channel VARCHAR(50),
            assignment_group VARCHAR(100),
            parent_ticket VARCHAR(50),
            assigned_to VARCHAR(100),
            resolved_by VARCHAR(100),
            ticket_resolved_month VARCHAR(3) CHECK (ticket_resolved_month IN ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')),
            ticket_resolved_year INTEGER CHECK (ticket_resolved_year >= 1900 AND ticket_resolved_year <= 2200),
            resolved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            short_description TEXT,
            description TEXT,
            work_notes TEXT,
            resolution_notes TEXT,
            row_status INTEGER NOT NULL DEFAULT 1 CHECK (row_status IN (1,2,3,4,5,6,7,8,9,10,11)),
            CONSTRAINT unique_ticket_number UNIQUE (ticket_number)
        );
        ALTER TABLE input_incident_data OWNER TO {table_owner};'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(input_incident_data_table_create_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '4', 'message': str(error)}

    # verify table creation:S05
    try:
        verify_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'input_incident_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(verify_sql)
                if (not (database_cursor.fetchone()[0])):
                    return {'status': 'ERROR', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '5', 'message': 'Table Not Created'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '5', 'message': str(error)}

    # trigger function:S06
    try:
        trigger_function_sql = '''
        CREATE OR REPLACE FUNCTION input_incident_full_trigger_function()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.ticket_number IS NOT NULL THEN
                NEW.ticket_number := UPPER(TRIM(NEW.ticket_number));
            END IF;

            IF NEW.opened_at IS NOT NULL THEN
                NEW.ticket_opened_month := TO_CHAR(NEW.opened_at, 'Mon');
                NEW.ticket_opened_year := EXTRACT(YEAR FROM NEW.opened_at)::INTEGER;
            END IF;

            IF NEW.resolved_at IS NOT NULL THEN
                NEW.ticket_resolved_month := TO_CHAR(NEW.resolved_at, 'Mon');
                NEW.ticket_resolved_year := EXTRACT(YEAR FROM NEW.resolved_at)::INTEGER;
            END IF;

            IF NEW.cmdb_ci IS NOT NULL THEN
                NEW.cmdb_ci := UPPER(NEW.cmdb_ci);
            END IF;

            IF TG_OP = 'INSERT' THEN
                NEW.row_inserted_at := NOW();
                NEW.row_updated_at := NOW();
            ELSIF TG_OP = 'UPDATE' THEN
                NEW.row_updated_at := NOW();
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_function_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '6', 'message': str(error)}

    # trigger definition:S07
    try:
        trigger_definition_sql = '''
        DROP TRIGGER IF EXISTS trg_input_incident_data_before_ins_upd ON input_incident_data;
        CREATE TRIGGER trg_input_incident_data_before_ins_upd
        BEFORE INSERT OR UPDATE
        ON input_incident_data
        FOR EACH ROW
        EXECUTE FUNCTION input_incident_full_trigger_function();'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_definition_sql)
                database_connection.commit()
                return {'status': 'SUCCESS', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '7', 'message': '"input_incident_data" Table Created With Auto-Trigger Function'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Input-Incident-Data-Table-Create', 'step': '7', 'message': str(error)}