# define "bot_catalogue_details_data_entry" function
def bot_catalogue_details_data_entry(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str, excel_file_path: str) -> dict[str, str]:
    # importing python modules:S1
    try:
        import psycopg2
        import pandas
        from pathlib import Path
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '1', 'message': str(error)}

    # define database parameters:S2
    try:
        database_connection_parameter = {
            "dbname": str(db_name),
            "user": str(db_user),
            "password": str(db_password),
            "host": str(db_host),
            "port": str(db_port)
        }
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '2', 'message': str(error)}

    # check if "bot_catalogue_details" table exists:S3
    try:
        table_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema='public'
            AND table_name='bot_catalogue_details'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(table_check_sql)
                if (not (database_cursor.fetchone()[0])):
                    return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '3', 'message': '"bot_catalogue_details" Table Not Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '3', 'message': str(error)}

    # define UPSERT SQL:S4
    try:
        bot_catalogue_details_upsert_sql = '''
        INSERT INTO bot_catalogue_details (
            bot_source, bot_id, functionality, short_solution_description, tower,
            technology, primary_developed_language, secondary_developed_language,
            operational_response, developed_platform, demand_category, type_of_automation,
            solution_description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (bot_id) DO UPDATE SET
            bot_source                   = EXCLUDED.bot_source,
            functionality                = EXCLUDED.functionality,
            short_solution_description   = EXCLUDED.short_solution_description,
            tower                        = EXCLUDED.tower,
            technology                   = EXCLUDED.technology,
            primary_developed_language   = EXCLUDED.primary_developed_language,
            secondary_developed_language = EXCLUDED.secondary_developed_language,
            operational_response         = EXCLUDED.operational_response,
            developed_platform           = EXCLUDED.developed_platform,
            demand_category              = EXCLUDED.demand_category,
            type_of_automation           = EXCLUDED.type_of_automation,
            solution_description         = EXCLUDED.solution_description;'''
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '4', 'message': str(error)}

    # verify Excel file:S5
    try:
        excel_path = Path(str(excel_file_path).strip().strip('"'))
        if (not (excel_path.exists() and excel_path.is_file() and excel_path.suffix.lower() == '.xlsx')):
            return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '5', 'message': 'Invalid Excel File Path'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '5', 'message': str(error)}

    # load input Excel:S6
    try:
        dataframe = pandas.read_excel(str(excel_path), keep_default_na = False)
        required_columns = [
            'bot_source', 'bot_id', 'functionality', 'short_solution_description', 'tower',
            'technology', 'primary_developed_language', 'secondary_developed_language',
            'operational_response', 'developed_platform', 'demand_category',
            'type_of_automation', 'solution_description'
        ]
        filtered_df = dataframe[required_columns]
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '6', 'message': str(error)}

    # prepare cleaned rows list:S7
    try:
        def clean_cell(value):
            if value is None:
                return 'N/A'
            value_str = str(value).strip()
            return value_str if value_str else 'N/A'

        # creating empty "insertion_rows" list
        insertion_rows = []
        # loop through all the values
        for row in filtered_df.values:
            insertion_rows.append((
                clean_cell(row[0]),  # bot_source
                clean_cell(row[1]),  # bot_id
                clean_cell(row[2]),  # functionality
                clean_cell(row[3]),  # short_solution_description
                clean_cell(row[4]),  # tower
                clean_cell(row[5]),  # technology
                clean_cell(row[6]),  # primary_developed_language
                clean_cell(row[7]),  # secondary_developed_language
                clean_cell(row[8]),  # operational_response
                clean_cell(row[9]),  # developed_platform
                clean_cell(row[10]), # demand_category
                clean_cell(row[11]), # type_of_automation
                clean_cell(row[12])  # solution_description
            ))
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '7', 'message': str(error)}

    # perform UPSERT into table:S8
    try:
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.executemany(bot_catalogue_details_upsert_sql, insertion_rows)
                database_connection.commit()
        return {'status': 'SUCCESS', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '8', 'message': 'BoT Catalogue Data Inserted Successfully'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'BoT-Catalogue-Data-Entry', 'step': '8', 'message': str(error)}