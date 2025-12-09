# define "processed_incident_data_table_create" function
def processed_incident_data_table_create(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> dict[str, str]:
    # importing python module:S01
    try:
        import psycopg2
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '1', 'message': str(error)}

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
        return {'status': 'ERROR', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '2', 'message': str(error)}

    # check if table exists:S03
    try:
        processed_incident_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'processed_incident_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(processed_incident_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    return {'status': 'SUCCESS', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '3', 'message': '"processed_incident_data" Table Already Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '3', 'message': str(error)}

    # create table:S04
    try:
        processed_incident_data_table_create_sql = f'''
        CREATE TABLE processed_incident_data (
            id SERIAL PRIMARY KEY,
            ticket_number VARCHAR(20) NOT NULL,
            account_name VARCHAR(50) NOT NULL,
            ticket_type VARCHAR(50) NOT NULL DEFAULT 'Incident',
            row_updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            ticket_opened_day INTEGER NOT NULL DEFAULT 1,
            ticket_opened_month VARCHAR(3) CHECK (ticket_opened_month IN ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')),
            ticket_opened_year INTEGER CHECK (ticket_opened_year >= 1900 AND ticket_opened_year <= 2400),
            ticket_opened_week INTEGER NOT NULL DEFAULT 1,
            ticket_opened_hours INTEGER NOT NULL DEFAULT 0,
            ticket_opened_minutes INTEGER NOT NULL DEFAULT 0,
            ticket_opened_seconds INTEGER NOT NULL DEFAULT 0,
            opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            cmdb_ci VARCHAR(100),
            state VARCHAR(50),
            priority VARCHAR(20),
            category VARCHAR(100),
            channel VARCHAR(50),
            assignment_group VARCHAR(100),
            assignment_group_category VARCHAR(7) NOT NULL DEFAULT 'Others' CHECK (assignment_group_category in ('L1','L2','L3','Others')),
            parent_ticket VARCHAR(50),
            assigned_to VARCHAR(100),
            resolved_by VARCHAR(100),
            resolved_type VARCHAR(7) NOT NULL DEFAULT 'Others' CHECK (resolved_type IN ('User','Auto','Others')),
            ticket_resolved_day INTEGER NOT NULL DEFAULT 1,
            ticket_resolved_month VARCHAR(3) CHECK (ticket_resolved_month IN ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')),
            ticket_resolved_year INTEGER CHECK (ticket_resolved_year >= 1900 AND ticket_resolved_year <= 2400),
            ticket_resolved_week INTEGER NOT NULL DEFAULT 1,
            ticket_resolved_hours INTEGER NOT NULL DEFAULT 0,
            ticket_resolved_minutes INTEGER NOT NULL DEFAULT 0,
            ticket_resolved_seconds INTEGER NOT NULL DEFAULT 0,
            resolved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            short_description TEXT,
            description TEXT,
            work_notes TEXT,
            resolution_notes TEXT,
            keywords_1 VARCHAR(100) NOT NULL DEFAULT 'Unspecified',
            keywords_2 VARCHAR(100) NOT NULL DEFAULT 'Unspecified',
            automation_probability VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (automation_probability IN ('Yes','No')),
            bot_availability VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (bot_availability IN ('Yes','No')),
            bid VARCHAR(150) NOT NULL DEFAULT 'N/A',
            ticket_mttr_days INTEGER NOT NULL DEFAULT 0,
            ticket_mttr_hours INTEGER NOT NULL DEFAULT 0,
            ticket_mttr_minutes INTEGER NOT NULL DEFAULT 0,
            ticket_mttr_seconds INTEGER NOT NULL DEFAULT 0,
            ticket_mttr_minutes_bucket VARCHAR(10) NOT NULL DEFAULT '0-5' CHECK (ticket_mttr_minutes_bucket IN ('0-5','5-10','10-20','20-30','>30')),
            ticket_aging_days INTEGER NOT NULL DEFAULT 0,
            ticket_aging_hours INTEGER NOT NULL DEFAULT 0,
            ticket_aging_minutes INTEGER NOT NULL DEFAULT 0,
            ticket_aging_seconds INTEGER NOT NULL DEFAULT 0,
            ticket_aging_minutes_bucket VARCHAR(10) NOT NULL DEFAULT '0-5' CHECK (ticket_aging_minutes_bucket IN ('0-5','5-10','10-20','20-30','>30')),
            cancelled_ticket VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (cancelled_ticket IN ('Yes','No')),
            connector_down VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (connector_down IN ('Yes','No')),
            flapping_event VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (flapping_event IN ('Yes','No')),
            short_duration_ticket VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (short_duration_ticket IN ('Yes','No')),
            sequence_event VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (sequence_event IN ('Yes','No')),
            periodic_event VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (periodic_event IN ('Yes','No')),
            blank_ci VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (blank_ci IN ('Yes','No')),
            parent_child_event VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (parent_child_event IN ('Yes','No')),
            duplicate_event VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (duplicate_event IN ('Yes','No')),
            deduplicate_event VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (deduplicate_event IN ('Yes','No')),
            correlated_event VARCHAR(3) NOT NULL DEFAULT 'No' CHECK (correlated_event IN ('Yes','No')),
            autoheal_category VARCHAR(15) NOT NULL DEFAULT 'Non_AutoHeal' CHECK (autoheal_category IN ('Non_AutoHeal','AutoHeal')),
            eso_analysis TEXT NOT NULL DEFAULT 'N/A',
            final_category VARCHAR(20) NOT NULL DEFAULT 'N/A' CHECK (final_category IN ('Elimination','Standardization','Automation','Exploratory','N/A')),
            CONSTRAINT unique_account_incident_processed UNIQUE (account_name, ticket_number)
        );
        ALTER TABLE processed_incident_data OWNER TO {table_owner};'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(processed_incident_data_table_create_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '4', 'message': str(error)}

    # verify table creation:S05
    try:
        verify_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'processed_incident_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(verify_sql)
                if (not (database_cursor.fetchone()[0])):
                    return {'status': 'ERROR', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '5', 'message': 'Table Not Created'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '5', 'message': str(error)}

    # trigger function:S06
    try:
        trigger_function_sql = '''
        CREATE OR REPLACE FUNCTION processed_incident_trigger_function()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.ticket_number IS NOT NULL THEN
                NEW.ticket_number := UPPER(TRIM(NEW.ticket_number));
            END IF;

            IF NEW.account_name IS NOT NULL THEN
                NEW.account_name := TRIM(NEW.account_name);
            END IF;

            IF NEW.opened_at IS NOT NULL THEN
                NEW.ticket_opened_day := EXTRACT(DAY FROM NEW.opened_at)::INTEGER;
                NEW.ticket_opened_week := EXTRACT(WEEK FROM NEW.opened_at)::INTEGER;
                NEW.ticket_opened_month := TO_CHAR(NEW.opened_at, 'Mon');
                NEW.ticket_opened_year := EXTRACT(YEAR FROM NEW.opened_at)::INTEGER;
                NEW.ticket_opened_hours := EXTRACT(HOUR FROM NEW.opened_at)::INTEGER;
                NEW.ticket_opened_minutes := EXTRACT(MINUTE FROM NEW.opened_at)::INTEGER;
                NEW.ticket_opened_seconds := EXTRACT(SECOND FROM NEW.opened_at)::INTEGER;
            END IF;

            IF NEW.resolved_at IS NOT NULL THEN
                NEW.ticket_resolved_day := EXTRACT(DAY FROM NEW.resolved_at)::INTEGER;
                NEW.ticket_resolved_week := EXTRACT(WEEK FROM NEW.resolved_at)::INTEGER;
                NEW.ticket_resolved_month := TO_CHAR(NEW.resolved_at, 'Mon');
                NEW.ticket_resolved_year := EXTRACT(YEAR FROM NEW.resolved_at)::INTEGER;
                NEW.ticket_resolved_hours := EXTRACT(HOUR FROM NEW.resolved_at)::INTEGER;
                NEW.ticket_resolved_minutes := EXTRACT(MINUTE FROM NEW.resolved_at)::INTEGER;
                NEW.ticket_resolved_seconds := EXTRACT(SECOND FROM NEW.resolved_at)::INTEGER;
            END IF;

            IF NEW.account_name IS NULL OR LENGTH(TRIM(NEW.account_name)) = 0 THEN
                RETURN NULL;
            END IF;

            NEW.row_updated_at := NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;'''
        with psycopg2.connect(**database_connection_parameter) as database_connection:   #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_function_sql)
                database_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '6', 'message': str(error)}

    # trigger definition:S07
    try:
        trigger_definition_sql = '''
        DROP TRIGGER IF EXISTS processed_incident_trigger ON processed_incident_data;
        CREATE TRIGGER processed_incident_trigger
        BEFORE INSERT OR UPDATE
        ON processed_incident_data
        FOR EACH ROW
        EXECUTE FUNCTION processed_incident_trigger_function();'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(trigger_definition_sql)
                database_connection.commit()
                return {'status': 'SUCCESS', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '7', 'message': '"processed_incident_data" Table Created With Auto-Trigger Function'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Processed-Incident-Data-Table-Create', 'step': '7', 'message': str(error)}