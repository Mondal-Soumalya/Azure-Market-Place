# define "incident_keyword_analysis" function
def incident_keyword_analysis(account_unique_id: str) -> dict[str, str]: #type: ignore
    # importing python module:S01
    try:
        from pathlib import Path
        import sys
        from dotenv import dotenv_values
        import psycopg2
        from psycopg2.extras import execute_values
        import json
        from openai import AsyncAzureOpenAI
        import nltk
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        from nltk.tokenize import word_tokenize
        import re
        from tenacity import retry, stop_after_attempt, wait_exponential
        import tiktoken
        import asyncio
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '1', 'message' : str(error)}

    # appending system path:S02
    try:
        sys.path.append(str(Path.cwd()))
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '2', 'message' : str(error)}

    # importing "log_writer" function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '3', 'message' : str(error)}

    # define folder and file path:S04
    try:
        parent_folder_path = Path.cwd()
        env_file_path = Path(parent_folder_path) / '.env'
        backend_folder_path = Path(parent_folder_path) / 'Backend'
        incident_dump_handler_folder_path = Path(backend_folder_path) / 'IncidentDumpHandler'
        ticket_analysis_folder_path = Path(incident_dump_handler_folder_path) / 'TicketAnalysis'
        nltk_model_folder_path = Path(ticket_analysis_folder_path) / 'NLTKModel'
        reference_data_folder_path = Path(ticket_analysis_folder_path) / 'ReferenceData'
        incident_keyword_analysis_system_prompt_file_path = Path(reference_data_folder_path) / 'IncidentKeywordAnalysisSystemPrompt.txt'
        incident_keyword_mapping_json_file_path = Path(reference_data_folder_path) / 'IncidentKeywordMapping.json'
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '4', status = 'SUCCESS', message = 'All Folder And File Path Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '4', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '4', 'message' : str(error)}

    # check if ".env" file is present:S05
    try:
        if ((env_file_path.exists()) and (env_file_path.is_file())):
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '5', status = 'SUCCESS', message = '".env" File Is Present')
        else:
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '5', status = 'ERROR', message = '".env" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '5', 'message' : '".env" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '5', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '5', 'message' : str(error)}

    # load ".env" file into script:S06
    try:
        environment_values = dotenv_values(env_file_path)
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '6', status = 'SUCCESS', message = '".env" File Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '6', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '6', 'message' : str(error)}

    # define database connection parameter:S07
    try:
        database_connection_parameter = {
            "dbname" : str(environment_values.get('DATABASE_NAME')),
            "user" : str(environment_values.get('DATABASE_USER')),
            "password" : str(environment_values.get('DATABASE_PASSWORD')),
            "host" : str(environment_values.get('DATABASE_HOST')),
            "port" : str(environment_values.get('DATABASE_PORT'))
        }
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '7', status = 'SUCCESS', message = 'Database Connection Parameter Defined')
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '7', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '7', 'message' : str(error)}

    # check if "input_incident_data" table present inside database:S08
    try:
        input_incident_data_table_present_check_sql = '''
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'input_incident_data'
        );'''
        with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
            with database_connection.cursor() as database_cursor:
                database_cursor.execute(input_incident_data_table_present_check_sql)
                if (database_cursor.fetchone()[0]):
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '8', status = 'SUCCESS', message = '"input_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '8', status = 'ERROR', message = '"input_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '8', 'message' : '"input_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '8', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '8', 'message' : str(error)}

    # check if "token_count_details" table present inside database:S09
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
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '9', status = 'SUCCESS', message = '"token_count_details" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '9', status = 'ERROR', message = '"token_count_details" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '9', 'message' : '"token_count_details" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '9', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '9', 'message' : str(error)}

    # check if "processed_incident_data" table present inside database:S10
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
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '10', status = 'SUCCESS', message = '"processed_incident_data" Table Present Inside Database')
                else:
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '10', status = 'ERROR', message = '"processed_incident_data" Table Not Present')
                    return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '10', 'message' : '"processed_incident_data" Table Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '10', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '10', 'message' : str(error)}

    # define azure openai configuration:S11
    try:
        api_endpoint = str(environment_values.get('OPENAI_API_ENDPOINT'))
        api_deployment_name = str(environment_values.get('OPENAI_DEPLOYMENT_NAME'))
        api_version = str(environment_values.get('OPENAI_API_VERSION'))
        api_key = str(environment_values.get('OPENAI_API_KEY'))
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '11', status = 'SUCCESS', message = 'Azure OpenAI Configured With "gpt-4o" Tokenizer')
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '11', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '11', 'message' : str(error)}

    # check if "IncidentKeywordAnalysisSystemPrompt.txt" file is present:S12
    try:
        if ((incident_keyword_analysis_system_prompt_file_path.exists()) and (incident_keyword_analysis_system_prompt_file_path.is_file()) and (incident_keyword_analysis_system_prompt_file_path.suffix.lower() == '.txt')):
            with open(incident_keyword_analysis_system_prompt_file_path, 'r', encoding = 'utf-8') as system_prompt_file:
                incident_keyword_analysis_system_prompt = system_prompt_file.read()
                log_writer(script_name = 'Incident-Keyword-Analysis', steps = '12', status = 'SUCCESS', message = 'System Prompt Loaded Into Script')
        else:
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '12', status = 'ERROR', message = '"IncidentKeywordAnalysisSystemPrompt.txt" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '12', 'message' : '"IncidentKeywordAnalysisSystemPrompt.txt" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '12', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '12', 'message' : str(error)}

    # check if "IncidentKeywordMapping.json"" file is present:S13
    try:
        if ((incident_keyword_mapping_json_file_path.exists()) and (incident_keyword_mapping_json_file_path.is_file()) and (incident_keyword_mapping_json_file_path.suffix.lower() == '.json')):
            with open(incident_keyword_mapping_json_file_path, 'r', encoding = 'utf-8') as keyword_mapping_file:
                incident_keyword_alias_map = json.load(keyword_mapping_file)
                log_writer(script_name = 'Incident-Keyword-Analysis', steps = '13', status = 'SUCCESS', message = 'Keyword Alias Mapping Loaded Into Script')
        else:
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '13', status = 'ERROR', message = '"IncidentKeywordMapping.json" File Not Present')
            return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '13', 'message' : '"IncidentKeywordMapping.json" File Not Present'}
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '13', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '13', 'message' : str(error)}

    # configured "NLTK" model for data cleaning:S14
    try:
        nltk.data.path.append(nltk_model_folder_path)
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '14', status = 'SUCCESS', message = 'NLTK Lemmatizer And Stop Words Model Loaded Into Script')
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '14', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '14', 'message' : str(error)}

    # define "clean_text" function:S15
    try:
        def clean_text(text: str) -> str:
            if (not text):
                return ''
            # normalize and clean unwanted characters
            text = text.lower()
            text = re.sub(r'[^a-zA-Z\s]', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            # tokenize input words
            tokens = word_tokenize(text)
            # remove stopwords and lemmatize
            cleaned_tokens = [
                lemmatizer.lemmatize(tok)
                for tok in tokens
                if tok not in stop_words
            ]
            return ' '.join(cleaned_tokens)
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '15', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '15', 'message' : str(error)}

    # define async "get_k1_k2" function:S16
    try:
        @retry(wait = wait_exponential(min = 2, max = 10), stop = stop_after_attempt(3))
        async def get_k1_k2(session, ticket_input_text):
            # requesting openai-api with "incident_keyword_analysis_system_prompt" and "ticket_input_text"
            try:
                api_response = await session.chat.completions.create(
                    model = api_deployment_name,
                    messages = [
                        {'role': 'system', 'content': incident_keyword_analysis_system_prompt},
                        {'role': 'user', 'content': ticket_input_text}
                    ],
                    temperature = 0.3,
                    max_tokens = 8192
                )
                # fetch response content
                api_response_result_content = api_response.choices[0].message.content

                # fetching "prompt_tokens" and "completion_tokens" from the api response
                prompt_tokens = getattr(api_response.usage, 'prompt_tokens', 0)
                completion_tokens = getattr(api_response.usage, 'completion_tokens', 0)

                # parse raw response into JSON
                try:
                    raw_api_json = json.loads(api_response_result_content)
                except json.JSONDecodeError:
                    return None, None, 'Unspecified', 'Unspecified', prompt_tokens, completion_tokens

                # check if JSON is not empty
                if (not raw_api_json):
                    return None, None, 'Unspecified', 'Unspecified', prompt_tokens, completion_tokens

                # return final output
                return (raw_api_json.get('account_unique_id'),
                        raw_api_json.get('ticket_number'),
                        raw_api_json.get('K1', 'Unspecified'),
                        raw_api_json.get('K2', 'Unspecified'),
                        prompt_tokens,
                        completion_tokens
                )
            except Exception:
                return None, None, 'Unspecified', 'Unspecified', 0, 0
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '16', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '16', 'message' : str(error)}

    # define async "process_incident_tickets" function for concurrency:S17
    try:
        async def process_incident_tickets(rows):
            # creating azure openai client for async request
            async with AsyncAzureOpenAI(api_key = api_key, api_version = api_version, azure_endpoint = api_endpoint) as openai_async_client:
                # define tokenizer
                tokenizer = tiktoken.encoding_for_model('gpt-4o')
                max_input_token = int(str(environment_values.get('INCIDENT_KEYWORD_ANALYSIS_INPUT_TOKEN')))

                # define "process_single_row" helper function for concurrent request
                async def process_single_row(row):
                    input_text = (
                        f"account_unique_id: {row[0]}\n"
                        f"ticket_number: {row[1]}\n"
                        f"short_description: {clean_text(str(row[2] or ''))}\n"
                        f"description: {clean_text(str(row[3] or ''))}\n"
                        f"work_notes: {clean_text(str(row[4] or ''))}\n"
                        f"resolution_notes: {clean_text(str(row[5] or ''))}"
                    )
                    # creating "input_text" tokenizer
                    if tokenizer:
                        tokenized = tokenizer.encode(input_text)
                        if (len(tokenized) > int(max_input_token)):
                            tokenized = tokenized[:int(max_input_token)]
                        input_text = tokenizer.decode(tokenized)
                    return await get_k1_k2(openai_async_client, input_text)

                # calling async function for row processing
                async_results = await asyncio.gather(*(process_single_row(row) for row in rows))

                # skip the row if either "account_unique_id" or "ticket_number" is missing
                filtered_results = []
                # loop through all the async_results
                for async_row in async_results:
                    account_unique_id, ticket_number, k1, k2, prompt_token, output_token = async_row
                    if ((account_unique_id is None) or (ticket_number is None)):
                        continue
                    else:
                        filter_async_dict = {
                            'account_unique_id' : account_unique_id,
                            'ticket_number' : ticket_number,
                            'K1' : k1,
                            'K2' : k2,
                            'prompt_tokens' : prompt_token,
                            'completion_tokens' : output_token
                        }
                        filtered_results.append(filter_async_dict)
                # return filtered result
                return filtered_results
    except Exception as error:
        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '17', status = 'ERROR', message = str(error))
        return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '17', 'message' : str(error)}

    # define constant
    total_count = 0
    keyword_analysis_rows_limiter = int(str(environment_values.get('INCIDENT_KEYWORD_ANALYSIS_BATCH')))
    same_batch_retry_count_limiter = int(str(environment_values.get('INCIDENT_KEYWORD_ANALYSIS_SAME_BATCH_RETRY_COUNT')))
    same_batch_counter = 0
    previous_batch_ids = set()

    # loop through all the available data
    while True:
        # define empty list
        processed_data_insert_rows = []
        token_details_insert_rows = []
        input_data_update_rows = []

        # fetching rows for keyword analysis:S18
        try:
            fetch_to_be_process_data_sql = '''
            SELECT
                iid.account_unique_id,
                iid.ticket_number,
                pid.short_description,
                pid.description,
                pid.work_notes,
                pid.resolution_notes
            FROM
                input_incident_data iid
            JOIN
                processed_incident_data pid
                ON iid.account_unique_id = pid.account_unique_id
                AND iid.ticket_number = pid.ticket_number
            WHERE
                iid.account_unique_id = %s
                AND iid.row_status = 4
            LIMIT %s;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    database_cursor.execute(fetch_to_be_process_data_sql, (account_unique_id, keyword_analysis_rows_limiter))
                    to_be_processed_data = database_cursor.fetchall()
                    # check if new data present inside table
                    if (int(len(to_be_processed_data)) == 0):
                        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '18', status = 'INFO', message = f'For Account: "{account_unique_id}" No New Rows Present For Keyword Analysis')
                        break
                    # check if batch is same as previous
                    current_batch_ids = {(row[0], row[1]) for row in to_be_processed_data}
                    if (current_batch_ids == previous_batch_ids):
                        same_batch_counter += 1
                        log_writer(script_name = 'Incident-Keyword-Analysis', steps = '18', status = 'INFO', message = f'Same Batch Fetched {same_batch_counter} Times For Keyword Analysis')
                        if (int(same_batch_counter) >= int(same_batch_retry_count_limiter)):
                            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '18', status = 'INFO', message = f'Same Batch Reached {same_batch_retry_count_limiter} Times For Keyword Analysis, Breaking Loop')
                            break
                    else:
                        same_batch_counter = 0
                        previous_batch_ids = current_batch_ids
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '18', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {len(to_be_processed_data)}-Rows Fetched For Keyword Analysis Process')
        except Exception as error:
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '18', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '18', 'message' : str(error)}

        # call async function for keyword analysis:S19
        try:
            final_result = asyncio.run(process_incident_tickets(to_be_processed_data))
            total_count += int(len(final_result))
        except Exception as error:
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '19', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '19', 'message' : str(error)}

        # reorder column for data insertion:S20
        try:
            for data_row in final_result:
                # creating tuple for keyword insertion
                processed_data_insert_rows.append((
                    data_row['account_unique_id'],
                    data_row['ticket_number'],
                    str((incident_keyword_alias_map.get((data_row.get('K1') or '').lower().strip(), data_row.get('K1') or '')).title()),
                    str((incident_keyword_alias_map.get((data_row.get('K2') or '').lower().strip(), data_row.get('K2') or '')).title())
                ))

                # creating tuple for token insertion
                token_details_insert_rows.append((
                    data_row['account_unique_id'],
                    data_row['ticket_number'],
                    int(data_row['prompt_tokens']),
                    int(data_row['completion_tokens']),
                    str(api_deployment_name),
                    str(api_version)
                ))

                # creating tuple for input table update
                input_data_update_rows.append((
                    data_row['account_unique_id'],
                    data_row['ticket_number']
                ))
        except Exception as error:
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '20', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '20', 'message' : str(error)}

        # inserting keywords into "processed_incident_data":S21
        try:
            data_upsert_sql_for_processed_incident_data_table = '''
            INSERT INTO processed_incident_data (
                account_unique_id,
                ticket_number,
                keywords_1,
                keywords_2
            )
            VALUES %s
            ON CONFLICT (account_unique_id, ticket_number)
            DO UPDATE SET
                keywords_1  = EXCLUDED.keywords_1,
                keywords_2  = EXCLUDED.keywords_2;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, data_upsert_sql_for_processed_incident_data_table, processed_data_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '21', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {len(to_be_processed_data)}-Rows Upserted Into "processed_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '21', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '21', 'message' : str(error)}

        # inserting token details into "token_count_details" table:S22
        try:
            token_upsert_sql = '''
            INSERT INTO token_count_details (
                account_unique_id,
                ticket_number,
                prompt_token,
                output_token,
                model_name,
                model_version
            )
            VALUES %s
            ON CONFLICT (account_unique_id, ticket_number)
            DO UPDATE SET
                prompt_token    = token_count_details.prompt_token + EXCLUDED.prompt_token,
                output_token    = token_count_details.output_token + EXCLUDED.output_token,
                model_name      = EXCLUDED.model_name,
                model_version   = EXCLUDED.model_version;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, token_upsert_sql, token_details_insert_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '22', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {len(to_be_processed_data)}-Rows Upserted Into "token_count_details" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '22', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '22', 'message' : str(error)}

        # updating "row_status" of "input_incident_data" to "5" after normalized data:S23
        try:
            update_row_status_sql_for_input_incident_data_table = '''
            UPDATE input_incident_data AS t
            SET row_status = 5,
                row_updated_at = NOW()
            FROM (VALUES %s) AS v(account_unique_id, ticket_number)
            WHERE t.account_unique_id = v.account_unique_id
            AND t.ticket_number = v.ticket_number;'''
            with psycopg2.connect(**database_connection_parameter) as database_connection: #type: ignore
                with database_connection.cursor() as database_cursor:
                    execute_values(database_cursor, update_row_status_sql_for_input_incident_data_table, input_data_update_rows)
                    database_connection.commit()
                    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '23', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {len(to_be_processed_data)}-Rows Updated "row_status" To "5" Inside "input_incident_data" Table')
        except Exception as error:
            log_writer(script_name = 'Incident-Keyword-Analysis', steps = '23', status = 'ERROR', message = str(error))
            return {'status' : 'ERROR', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '23', 'message' : str(error)}

    # sending return message to main script:S24
    log_writer(script_name = 'Incident-Keyword-Analysis', steps = '24', status = 'SUCCESS', message = f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data Keyword Analysis Completed And Updated Into "input_incident_data" Table')
    return {'status' : 'SUCCESS', 'file_name' : 'Incident-Keyword-Analysis', 'step' : '24', 'message' : f'For Account: "{account_unique_id}" Total {total_count}-Rows Of Data Keyword Analysis Completed And Updated Into "input_incident_data" Table'}