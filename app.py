# importing module:S01
try:
    from pathlib import Path
    import sys
    from dotenv import dotenv_values
    from flask_cors import CORS
    from flask import Flask, request, render_template, jsonify, session
except Exception as error:
    print(f'ERROR - [App:S01] - {str(error)}')

# appending system path:S02
try:
    sys.path.append(str(Path.cwd()))
except Exception as error:
    print(f'ERROR - [App:S02] - {str(error)}')

# importing user-define module:S03
try:
    from DatabaseHandler.databaseautoinit import database_auto_init
    from Backend.LogHandler.logwriter import log_writer
except Exception as error:
    print(f'ERROR - [App:S03] - {str(error)}')

# creating all the database table:S04
try:
    database_auto_init_backend_response = database_auto_init()
    # check the result
    if (database_auto_init_backend_response == None):
        print('ERROR - [App:S04] - "database_auto_init" Function Not Executed Properly')
    elif (str(database_auto_init_backend_response['status']).lower() == 'error'):
        print(f"ERROR - [{str(database_auto_init_backend_response['file_name'])}:{str(database_auto_init_backend_response['step'])}] - {str(database_auto_init_backend_response['message'])}")
        exit(1)
except Exception as error:
    print(f'ERROR - [App:S04] - {str(error)}')

# define file and folder path:S05
try:
    parent_folder_path = Path.cwd()
    frontend_folder_path = Path(parent_folder_path) / 'Frontend'
    templates_folder_path = Path(frontend_folder_path) / 'templates'
    static_folder_path = Path(frontend_folder_path) / 'static'
    resource_folder_path = Path(static_folder_path) / 'resource'
    image_folder_path = Path(resource_folder_path) / 'image'
    env_file_path = Path(parent_folder_path) / '.env'
    log_writer(script_name = 'App', steps = '5', status = 'SUCCESS', message = 'All Folders Are Defined')
except Exception as error:
    log_writer(script_name = 'App', steps = '5', status = 'ERROR', message = str(error))

# check if ".env" file is present:S06
try:
    if ((env_file_path.exists()) and (env_file_path.is_file())):
        log_writer(script_name = 'App', steps = '6', status = 'SUCCESS', message = '".env" File Is Present')
    else:
        log_writer(script_name = 'App', steps = '6', status = 'ERROR', message = '".env" File Not Present')
        exit(1)
except Exception as error:
    log_writer(script_name = 'App', steps = '6', status = 'ERROR', message = str(error))

# define flask object:S07
try:
    environment_values = dotenv_values(env_file_path)
    flask_secret_key = environment_values.get('FLASK_APPLICATION_SECRET_KEY')
    app = Flask(__name__, template_folder= templates_folder_path, static_folder= static_folder_path)
    CORS(app)
    app.secret_key = flask_secret_key
    log_writer(script_name = 'App', steps = '7', status = 'SUCCESS', message = 'Flask Web-Application Defined With Application Secret-Key')
except Exception as error:
    log_writer(script_name = 'App', steps = '7', status = 'ERROR', message = str(error))

# define "/" route:S08
@app.route('/') # type: ignore
def index():
    try:
        log_writer(script_name = 'App', steps = '8', status = 'SUCCESS', message = '"/" Page Routed Successfully')
        return render_template('index.html')
    except Exception as error:
        log_writer(script_name = 'App', steps = '8', status = 'ERROR', message = str(error))

# define "/analysisenginepage" route:S09
@app.route('/analysisenginepage') #type: ignore
def analysisenginepage():
    try:
        log_writer(script_name = 'App', steps = '9', status = 'SUCCESS', message = '"/analysisenginepage" Page Routed Successfully')
        return render_template('analysisenginepage.html')
    except Exception as error:
        log_writer(script_name = 'App', steps = '9', status = 'ERROR', message = str(error))

# define "incidentanalysis" route:S10
@app.route('/incidentanalysis', methods=['GET', 'POST']) #type: ignore
def incidentanalysis():
    # if it is "POST" request
    if (request.method == 'POST'):
        # importing "incident_ticket_file_handler" function to process incident file:S18-A
        try:
            from Backend.IncidentDumpHandler.incidentfilehandler import incident_ticket_file_handler
        except Exception as error:
            log_writer(script_name = 'App', steps = '10-A', status = 'ERROR', message = str(error))
            return jsonify({'error': 'An error occurred while processing the form'}), 500

        # fetching details from frontend:S10-B
        try:
            # get ticket dump file
            incident_analysis_ticket_file = request.files.get('incident_dump_file')
        except Exception as error:
            log_writer(script_name = 'App', steps = '10-B', status = 'ERROR', message = str(error))
            return jsonify({'error': 'An error occurred while processing the form'}), 500

        # calling "incident_ticket_file_handler" function to process file:S10-C
        if (incident_analysis_ticket_file):
            try:
                # pass the file to incident_ticket_file_handler function
                incident_file_analysis_backend_process = incident_ticket_file_handler(file = incident_analysis_ticket_file)
                # check response
                if (str(incident_file_analysis_backend_process['status']).lower() == 'success'):
                    log_writer(script_name = 'App', steps = '10-C', status = 'SUCCESS', message = str(incident_file_analysis_backend_process['message']))
                    return jsonify({'message': incident_file_analysis_backend_process['message']}), 200
                if (str(incident_file_analysis_backend_process['status']).lower() == 'info'):
                    log_writer(script_name = incident_file_analysis_backend_process['file_name'], steps = incident_file_analysis_backend_process['step'], status = 'INFO', message = str(incident_file_analysis_backend_process['message']))
                    return jsonify({'message': incident_file_analysis_backend_process['message']}), 500
                if (str(incident_file_analysis_backend_process['status']).lower() == 'error'):
                    log_writer(script_name = incident_file_analysis_backend_process['file_name'], steps = incident_file_analysis_backend_process['step'], status = 'ERROR', message = str(incident_file_analysis_backend_process['message']))
                    return jsonify({'message': incident_file_analysis_backend_process['message']}), 500
            except Exception as error:
                log_writer(script_name = 'App', steps = '10-C', status = 'ERROR', message = str(error))
                return jsonify({'error': 'An Error Occurred While Processing The Form'}), 500
        else:
            # Return error response if no file is uploaded
            log_writer(script_name = 'App', steps = '10-C', status = 'ERROR', message = 'No File Uploaded')
            return jsonify({'error': 'No File Uploaded'}), 400

    # if it is a "GET" request
    if (request.method == 'GET'):
        # re-directing "/incidentanalysis" page with all account data:S18-D
        try:
            log_writer(script_name = 'App', steps = '10-D', status = 'SUCCESS', message = '"/incidentanalysis" Page Routed Successfully')
            return render_template('incidentanalysis.html')
        except Exception as error:
            log_writer(script_name = 'App', steps = '10-D', status = 'ERROR', message = str(error))

# define main function
if __name__ == '__main__':
    # calling flask application
    try:
        app.run(host = '127.0.0.1', debug = True, port = 5000, use_reloader = False)
    except Exception as error:
        print(f'ERROR - {str(error)}')