# importing module:S01
try:
    from pathlib import Path
    import sys
    import subprocess
    import atexit
    import time
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
    react_app_folder_path = Path(parent_folder_path) / 'Frontend'
    templates_folder_path = Path(react_app_folder_path) / 'dist'  # For production build
    static_folder_path = Path(react_app_folder_path) / 'dist'
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
        # return render_template('index.html')
        return jsonify({
            'status': 'success',
            'message': 'Flask API is running',
            'api_url': 'http://127.0.0.1:5000',
            'react_app': 'Running on separate Vite dev server (check console for port)'
        }), 200
    except Exception as error:
        log_writer(script_name = 'App', steps = '8', status = 'ERROR', message = str(error))
        return jsonify({'error': 'An error occurred'}), 500

# API health check route:S09
@app.route('/api/health') #type: ignore
def health_check():
    try:
        log_writer(script_name = 'App', steps = '9', status = 'SUCCESS', message = 'API Health Check Successful')
        return jsonify({
            'status': 'healthy',
            'message': 'Flask API server is running',
            'version': '1.0.0'
        }), 200
    except Exception as error:
        log_writer(script_name = 'App', steps = '9', status = 'ERROR', message = str(error))
        return jsonify({'error': 'Health check failed'}), 500

# define "incidentanalysis" route:S10
@app.route('/api/incidentanalysis', methods=['GET', 'POST']) #type: ignore
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
            incident_analysis_ticket_file = request.files.get('incident_dump_file') or request.files.get('incident_file')
            #Debug logging
            print(f'DEBUG - Received file fields: {list(request.files.keys())}')
            print(f'DEBUG - File received: {incident_analysis_ticket_file is not None}')
            if incident_analysis_ticket_file:
                print(f'DEBUG - File name: {incident_analysis_ticket_file.filename}')

        except Exception as error:
            log_writer(script_name = 'App', steps = '10-B', status = 'ERROR', message = str(error))
            return jsonify({'error': f'An error occurred while processing the form: {str(error)}'}), 500

        # calling "incident_ticket_file_handler" function to process file:S10-C
        if (incident_analysis_ticket_file):
            try:
                # pass the file to incident_ticket_file_handler function
                incident_file_analysis_backend_process = incident_ticket_file_handler(file = incident_analysis_ticket_file)
                print(f'DEBUG - Handler response: {incident_file_analysis_backend_process}')

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
                import traceback
                error_details = traceback.format_exc()
                print(f'ERROR - Exception in incident analysis: {error_details}')
                log_writer(script_name = 'App', steps = '10-C', status = 'ERROR', message = f'{str(error)} - {error_details}')
                return jsonify({'error': 'An Error Occurred While Processing The Form'}), 500
        else:
            # Return error response if no file is uploaded
            log_writer(script_name = 'App', steps = '10-C', status = 'ERROR', message = 'No File Uploaded')
            return jsonify({'error': 'No File Uploaded'}), 400

    # if it is a "GET" request
    if (request.method == 'GET'):
        # re-directing "/api/incidentanalysis" page with all account data:S18-D
        try:
            log_writer(script_name = 'App', steps = '10-D', status = 'SUCCESS', message = '"/api/incidentanalysis"  API endpoint accessed successfully')
            # return render_template('incidentanalysis.html')
            return jsonify({
                'endpoint': '/api/incidentanalysis',
                'method': 'POST',
                'description': 'Upload and analyze incident dump files',
                'required_fields': ['incident_dump_file']
            }), 200
        except Exception as error:
            log_writer(script_name = 'App', steps = '10-D', status = 'ERROR', message = str(error))
            return jsonify({'error': 'An error occurred while accessing the endpoint'}), 500
react_process = None


# define main function
if __name__ == '__main__':
    # calling flask application
    try:
        react_app_path = Path(parent_folder_path) / 'Frontend'

        # check if node_modules exists, if not run npm install
        node_modules_path = Path(react_app_path) / 'node_modules'
        if not node_modules_path.exists():
            print('INFO - [App:S12] Installing packages...')
            log_writer(script_name = 'App', steps = '12', status = 'INFO', message = 'Installing packages')
            npm_install_process = subprocess.Popen(
                ['npm', 'install'],
                cwd=str(react_app_path),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            npm_install_process.wait()
            print('INFO - [App:S12] packages installed successfully')

        # build the React application for production
        print('INFO - [App:S12] Building application...')
        log_writer(script_name = 'App', steps = '12', status = 'INFO', message = 'Building React application')
        npm_build_process = subprocess.Popen(
            ['npm', 'run', 'build'],
            cwd=str(react_app_path),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        npm_build_process.wait()

        if npm_build_process.returncode == 0:
            print('INFO - [App:S12] Application built successfully')
            log_writer(script_name = 'App', steps = '12', status = 'SUCCESS', message = 'React application built successfully')
        else:
            print('INFO - [App:S12] Build completed with warnings or errors')
            log_writer(script_name = 'App', steps = '12', status = 'INFO', message = 'React build completed with warnings')

        # start the React development server on port 3000
        print('INFO - [App:S12] Starting web server on http://localhost:3000...')
        react_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd=str(react_app_path),
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )

        # register cleanup function to terminate React server when Flask stops
        def cleanup_react_server():
            global react_process
            if react_process:
                print('INFO - [App:S12] Stopping web server...')
                try:
                    if sys.platform == 'win32':
                        # On Windows, use taskkill to terminate the process tree
                        subprocess.call(['taskkill', '/F', '/T', '/PID', str(react_process.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        react_process.terminate()
                        react_process.wait(timeout=5)
                except Exception as e:
                    print(f'INFO - [App:S12] Error stopping web server: {str(e)}')

        atexit.register(cleanup_react_server)

        # wait for React server to start by checking if port 3000 is open
        import socket
        def wait_for_port(port, host = '127.0.0.1', timeout = 30):
            start_time = time.time()
            while time.time() - start_time < timeout:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    try:
                        sock.connect((host, port))
                        return port
                    except Exception:
                        time.sleep(1)
            # try next ports (Vite uses next available port if 3000 is busy)
            for next_port in range(port + 1, port + 10):
                start_time = time.time()
                while time.time() - start_time < timeout:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(1)
                        try:
                            sock.connect((host, next_port))
                            print(f'INFO - [App:S12] web server started on port {next_port}')
                            return next_port
                        except Exception:
                            time.sleep(1)
            print(f'ERROR - [App:S12] web server did not start within {timeout} seconds on ports {port}-{port+9}.')
            return None

        selected_port = wait_for_port(3000)
        if selected_port is None:
            print('INFO - [App:S12] No available port found for React server (ports 3000-3009).')
        else:
            print(f'INFO - [App:S12] React server running on port {selected_port}')

        log_writer(script_name = 'App', steps = '12', status = 'SUCCESS', message = 'web Server Started')
    except Exception as error:
        print(f'ERROR - [App:S12] Failed to start web server: {str(error)}')
        log_writer(script_name = 'App', steps = '12', status = 'ERROR', message = f'web Server Failed: {str(error)}')

    try:
        print('INFO - [App:S13] Starting Flask API server on http://127.0.0.1:5000')
        print('=' * 80)
        print('SERVERS RUNNING:')
        print('  - Check your browser (Website will auto-open)')
        print('  - Flask Backend:  http://127.0.0.1:5000 (API server)')
        print('')
        print('NOTE: Website will use port 3000, or the next available port if 3000 is busy')
        print('      All API requests from Website are proxied to Flask backend')
        print('=' * 80)
        log_writer(script_name = 'App', steps = '13', status = 'SUCCESS', message = 'Flask Application Started on port 5000')
        app.run(host = '127.0.0.1', debug = True, port = 5000, use_reloader = False)
    except Exception as error:
        print(f'ERROR - {str(error)}')