# define "service_desk_automation_mapping" function
def service_desk_automation_mapping(account_unique_id: str) -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
        import nltk
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        import re
        from rapidfuzz import fuzz
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        service_desk_dump_handler_folder_path = Path(backend_folder_path) / 'ServiceDeskDumpHandler'
        ticket_analysis_folder_path = Path(service_desk_dump_handler_folder_path) / 'TicketAnalysis'
        nltk_model_folder_path = Path(ticket_analysis_folder_path) / 'NLTKModel'
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '7', 'message' : str(error)}

    # check if "input_sd_data" table present inside database:S08
    try:
        input_sd_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'input_sd_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(input_sd_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '8', status = 'SUCCESS', message = '"input_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '8', status = 'ERROR', message = '"input_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '8', 'message' : '"input_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '8', 'message' : str(error)}

    # check if "processed_sd_data" table present inside database:S09
    try:
        processed_sd_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'processed_sd_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(processed_sd_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '9', status = 'SUCCESS', message = '"processed_sd_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '9', status = 'ERROR', message = '"processed_sd_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '9', 'message' : '"processed_sd_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '9', 'message' : str(error)}

    # check if "bot_catalogue_details" table present inside database:S10
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
                    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '10', status = 'SUCCESS', message = '"bot_catalogue_details" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '10', status = 'ERROR', message = '"bot_catalogue_details" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '10', 'message' : '"bot_catalogue_details" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '10', 'message' : str(error)}

    # fetch "bot_id", "technology", "tower", "short_solution_description" from "bot_catalogue_details" table:S11
    try:
        fetch_details_from_bot_catalouge_table_sql = '''
        SELECT bot_id, technology, tower, short_solution_description
        FROM bot_catalogue_details;'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(fetch_details_from_bot_catalouge_table_sql)
                reference_details = database_cursor.fetchall()
                log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '11', status = 'SUCCESS', message = f'Total: "{len(reference_details)}" BoT Reference Loaded From "bot_catalogue_details" Into Script')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '11', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '11', 'message' : str(error)}

    # configured "NLTK" model for data cleaning:S12
    try:
        nltk.data.path.append(nltk_model_folder_path)
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '12', status = 'SUCCESS', message = 'NLTK Lemmatizer And Stop Words Model Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '12', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '12', 'message' : str(error)}

    # process "bot_reference_data" for better searching:S13
    try:
        # define "bot_reference_data" empty list
        bot_reference_data = []
        for data_row in reference_details:
            # Create dictionary for the row
            row_dict = {
                'bot_id': data_row[0],
                'technology': data_row[1],
                'tower': data_row[2],
                'short_solution_description': data_row[3]
            }

            # clean and tokenize each text column
            for column_name in ['technology', 'tower', 'short_solution_description']:
                column_values = row_dict.get(column_name, '')
                if column_values is None:
                    column_values = ''
                column_values = column_values.lower()
                column_values = re.sub(r'[^a-z0-9\s]', '', column_values)
                word_tokens = [lemmatizer.lemmatize(word) for word in column_values.split() if word and word not in stop_words]
                row_dict[column_name] = ' '.join(word_tokens)
            bot_reference_data.append(row_dict)
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '13', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '13', 'message' : str(error)}

    # define "processed_text" function:S14
    try:
        def clean_text(text, lemmatizer, stop_words):
            if ((not isinstance(text, str)) or (not text)):
                return ''
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', '', text)
            word_tokens = [lemmatizer.lemmatize(word) for word in text.split() if word and word not in stop_words]
            return ' '.join(word_tokens)
    except Exception as error:
        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '14', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '14', 'message' : str(error)}

    # define constant
    total_count = 0
    skipped_rows = 0
    automation_mapping_rows_limiter = int(str(environment_values.get('SERVICE_DESK_AUTOMATION_MAPPING_BATCH')))
    fuzzy_search_confidence_score = int(str(environment_values.get('SERVICE_DESK_AUTOMATION_MAPPING_CONFIDENCE_SCORE')))
    automation_mapping_top_score_count = int(str(environment_values.get('SERVICE_DESK_AUTOMATION_MAPPING_TOP_MATCH_COUNT')))

    # loop through all the available data
    while True:
        # define empty list
        processed_data_insert_rows = []
        input_data_update_rows = []

        # fetching "account_unique_id", "ticket_number", "keywords_1", "keywords_2", "automation_probability", "bot_availability", "bid" from "processed_sd_data" table:S15
        try:
            fetch_to_be_process_data_sql = '''
            SELECT
                isdd.account_unique_id,
                isdd.ticket_number,
                psdd.keywords_1,
                psdd.keywords_2,
                psdd.automation_probability,
                psdd.bot_availability,
                psdd.bid
            FROM
                input_sd_data isdd
            JOIN
                processed_sd_data psdd
                ON isdd.account_unique_id = psdd.account_unique_id
                AND isdd.ticket_number = psdd.ticket_number
            WHERE
                isdd.account_unique_id = %s
                AND isdd.row_status = 6
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: # type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (str(account_unique_id), automation_mapping_rows_limiter))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) > 0):
                        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '15', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Fetched For Service-Desk-Automation-Mapping Process')
                    else:
                        log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '15', status = 'INFO', message = f'For Account: "{account_unique_id}" No New Rows Present For Service-Desk-Automation-Mapping Process')
                        break
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '15', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '15', 'message' : str(error)}

        # process every rows for bot mapping:S16
        try:
            for i, data_row in enumerate(to_be_processed_data):
                row_list = list(data_row)
                # check if "keywords_1" and "keywords_2"
                if ((row_list[2] is None or str(row_list[2]).strip().lower() in ["unspecified", "n/a"]) and (row_list[3] is None or str(row_list[3]).strip().lower() in ["unspecified", "n/a"])):
                    row_list[4] = 'No'  # automation_probability
                    row_list[5] = 'No'  # bot_availability
                    row_list[6] = 'N/A'  # bid
                    to_be_processed_data[i] = tuple(row_list)
                    skipped_rows += 1
                    continue
                else:
                    # process "keywords_1" for better search result
                    k1_processed = clean_text(row_list[2], lemmatizer, stop_words)
                    # process both "keywords_1" and "keywords_2" for better search result
                    k1_k2_processed = clean_text(f"{row_list[2]} {row_list[3]}", lemmatizer, stop_words)
                    # define "reference_candidate" empty list for top "bot_id" matching
                    reference_candidate = []

                    # high confidence match
                    for reference_data in bot_reference_data:
                        for column_name in ['technology', 'tower']:
                            ref_text = reference_data.get(column_name, '')
                            # Use regex for word-boundary exact matching like old script
                            if k1_processed and re.search(rf'\b{k1_processed}\b', ref_text, flags = re.IGNORECASE):
                                reference_candidate.append(reference_data)
                                break

                    # broad match if no high confidence match
                    if not reference_candidate:
                        if k1_k2_processed:
                            k1_k2_words = k1_k2_processed.split()
                            for reference_data in bot_reference_data:
                                for column_name in ['technology', 'tower', 'short_solution_description']:
                                    ref_text = reference_data.get(column_name, '')
                                    # check if any preprocessed keyword word appears (word-boundary)
                                    if any(re.search(rf'\b{word}\b', ref_text, flags = re.IGNORECASE) for word in k1_k2_words if word):
                                        reference_candidate.append(reference_data)
                                        break

                    # fuzzy matching & ranking
                    if reference_candidate:
                        all_scores = {}
                        for reference_data in reference_candidate:
                            comparison_text = ' '.join([reference_data.get(col, '') for col in ['technology', 'tower', 'short_solution_description']])
                            fuzzy_match_score = fuzz.token_set_ratio(k1_k2_processed, comparison_text)
                            if int(fuzzy_match_score) > int(fuzzy_search_confidence_score):
                                all_scores[reference_data['bot_id']] = fuzzy_match_score

                        # rank top 3 like old script
                        if all_scores:
                            sorted_scores = sorted(all_scores.items(), key = lambda x: x[1], reverse = True)
                            top_botids = [bot_id for bot_id, score in sorted_scores[:automation_mapping_top_score_count]]
                            top_botid = ', '.join(top_botids)
                        else:
                            top_botid = 'N/A'
                    else:
                        top_botid = 'N/A'

                    # update fields
                    row_list[4] = 'Yes' if top_botid != 'N/A' else 'No'  # automation_probability
                    row_list[5] = 'Yes' if top_botid != 'N/A' else 'No'  # bot_availability
                    row_list[6] = top_botid                              # bid

                # replace updated row
                to_be_processed_data[i] = tuple(row_list)
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '16', status = 'ERROR', message = str(error))
            return {'status': 'ERROR', 'file_name': 'Service-Desk-Automation-Mapping', 'step': '16', 'message': str(error)}

        # re-order column for data insertion:S17
        try:
            for data_row in to_be_processed_data:
                total_count += 1
                # appending data into "processed_data_insert_rows" empty list
                processed_data_insert_rows.append((
                    data_row[0], # account_unique_id
                    data_row[1], # ticket_number
                    str(data_row[4]), # automation_probability
                    str(data_row[5]), # bot_availability
                    str(data_row[6]) # bid
                ))
                # appending data into "input_data_update_rows" empty list
                input_data_update_rows.append((
                    data_row[0], # account_unique_id
                    data_row[1] # ticket_number
                ))
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '17', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '17', 'message' : str(error)}

        # inserting bot mapping data into "processed_sd_data":S18
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_sd_data (
                account_unique_id,
                ticket_number,
                automation_probability,
                bot_availability,
                bid
            )
            VALUES %s
            ON CONFLICT (ticket_number, account_unique_id)
            DO UPDATE SET
                automation_probability= EXCLUDED.automation_probability,
                bot_availability      = EXCLUDED.bot_availability,
                bid                   = EXCLUDED.bid;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '18', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Upserted Into "processed_sd_data" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '18', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '18', 'message' : str(error)}

        # updating "row_status" of "input_sd_data" to "7" after bot mapping:S19
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_sd_data AS t
            SET row_status = 7,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(account_unique_id, ticket_number)
            WHERE t.account_unique_id = v.account_unique_id
            AND t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '19', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {int(len(to_be_processed_data))}-Rows Updated "row_status" To "6" Inside "input_sd_data" Table')
        except Exception as error:
            log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '19', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '19', 'message' : str(error)}

    # sending return message to main script:S20
    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '20', status = 'INFO', message = f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data Service-Desk-Automation-Mapping Completed And Updated Into "input_sd_data" Table')
    log_writer(script_name = 'Service-Desk-Automation-Mapping', steps = '20', status = 'INFO', message = f'For Account: "{account_unique_id}" Total {skipped_rows}-Rows Skipped Due To "keywords_1" And "keywords_2" Both Data Unavailability')
    return {'status' : 'SUCCESS', 'file_name' : 'Service-Desk-Automation-Mapping', 'step' : '20', 'message' : f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data Service-Desk-Automation-Mapping Completed And Updated Into "input_sd_data" Table'}