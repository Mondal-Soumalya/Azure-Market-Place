# define form_submitted_data_handler function
def form_submitted_data_handler(form_data: dict, account_name: str, deployment_id: str) -> tuple:
    # define constant
    RESOURCE_DUMP_FOLDER_PRESENT_STATUS = False
    SOP_DUMP_FOLDER_PRESENT_STATUS = False

    # importing module:S01
    try:
        import os
        import sys
        import json
        from werkzeug.utils import secure_filename
    except Exception as error:
        print(f'ERROR - [Form-Data-Handler:S01] - {str(error).title()}')

    # appending system path:S02
    try:
        sys.path.append(os.getcwd())
    except Exception as error:
        print(f'ERROR - [Form-Data-Handler:S02] - {str(error).title()}')

    # importing user-define function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        print(f'ERROR - [Form-Data-Handler:S03] - {str(error).title()}')

    # define parent folder path:S04
    try:
        parent_folder_path = os.getcwd()
        resource_dump_folder_path = os.path.join(parent_folder_path, 'ResourceDump')
        sop_dump_folder_path = os.path.join(resource_dump_folder_path, 'SoPDump')
        sop_data_dump_folder_path = os.path.join(sop_dump_folder_path, 'SoPData')
        log_writer(script_name= 'Form-Data-Handler', steps= '4', status= 'SUCCESS', message= 'All Folders Are Defined')
    except Exception as error:
        log_writer(script_name= 'Form-Data-Handler', steps= '4', status= 'ERROR', message= f'{str(error).title()}')
        print(f'ERROR - [Form-Data-Handler:S04] - {str(error).title()}')

    # check "ResourceDump" folder present:S05
    try:
        if (not (os.path.exists(resource_dump_folder_path))):
            # create folder
            os.makedirs(resource_dump_folder_path)
            # check if folder is created
            if (not (os.path.exists(resource_dump_folder_path))):
                RESOURCE_DUMP_FOLDER_PRESENT_STATUS = False
                log_writer(script_name= 'Form-Data-Handler', steps= '5', status= 'ERROR', message= '"ResourceDump" Folder Not Created')
                sys.exit(1)
            else:
                RESOURCE_DUMP_FOLDER_PRESENT_STATUS = True
                log_writer(script_name= 'Form-Data-Handler', steps= '5', status= 'SUCCESS', message= '"ResourceDump" Folder Already Present')
    except Exception as error:
        log_writer(script_name= 'Form-Data-Handler', steps= '5', status= 'ERROR', message= f'{str(error).title()}')
        print(f'ERROR - [Form-Data-Handler:S05] - {str(error).title()}')

    # check "SOPDump" folder present status:S06
    if (RESOURCE_DUMP_FOLDER_PRESENT_STATUS):
        try:
            if (not (os.path.exists(sop_dump_folder_path))):
                # create folder
                os.makedirs(sop_dump_folder_path)
                # check if folder is created
                if (not (os.path.exists(sop_dump_folder_path))):
                    SOP_DUMP_FOLDER_PRESENT_STATUS = False
                    log_writer(script_name= 'Form-Data-Handler', steps= '6', status= 'ERROR', message= '"RecourceDump\SoPDump" Folder Not Created')
                    sys.exit(1)
                else:
                    SOP_DUMP_FOLDER_PRESENT_STATUS = True
                    log_writer(script_name= 'Form-Data-Handler', steps= '6', status= 'SUCCESS', message= '"ResourceDump\SoPDump" Folder Already Present')
        except Exception as error:
            log_writer(script_name= 'Form-Data-Handler', steps= '6', status= 'ERROR', message= f'{str(error).title()}')
            print(f'ERROR - [Form-Data-Handler:S06] - {str(error).title()}')

    # check "SoPData" folder present status:S07
    if (SOP_DUMP_FOLDER_PRESENT_STATUS):
        try:
            if (not (os.path.exists(sop_data_dump_folder_path))):
                # create folder
                os.makedirs(sop_data_dump_folder_path)
                # check if folder is created
                if (not (os.path.exists(sop_data_dump_folder_path))):
                    SOP_DUMP_FOLDER_PRESENT_STATUS = False
                    log_writer(script_name= 'Form-Data-Handler', steps= '7', status= 'ERROR', message= '"ResourceDump\SoPDump\SoPFile" Folder Not Created')
                    sys.exit(1)
                else:
                    SOP_DUMP_FOLDER_PRESENT_STATUS = True
                    log_writer(script_name= 'Form-Data-Handler', steps= '7', status= 'SUCCESS', message= '"ResourceDump\SoPDump\SoPFile" Folder Already Present')
        except Exception as error:
            log_writer(script_name= 'Form-Data-Handler', steps= '7', status= 'ERROR', message= f'{str(error).title()}')
            print(f'ERROR - [Form-Data-Handler:S07] - {str(error).title()}')

    # define file store path:S08
    try:
        # define file name
        unique_sop_file_name = secure_filename(f"{str(account_name.upper())}.json")
        log_writer(script_name= 'Form-Data-Handler', steps= '8', status= 'SUCCESS', message= f'"{unique_sop_file_name}" File Name Created')
        # define file store path
        unique_sop_data_store_path = os.path.join(sop_data_dump_folder_path, unique_sop_file_name)
    except Exception as error:
        log_writer(script_name= 'Form-Data-Handler', steps= '8', status= 'ERROR', message= f'{str(error).title()}')
        print(f'ERROR - [Form-Data-Handler:S08] - {str(error).title()}')

    # save data to JSON file:S09
    try:
        with open(unique_sop_data_store_path, 'w') as json_file:
            json.dump(form_data, json_file, indent=4)
        log_writer(script_name= 'Form-Data-Handler', steps= '9', status= 'SUCCESS', message= f'"{unique_sop_file_name}" File Saved In "..\SoPData" Folder')
    except Exception as error:
        log_writer(script_name= 'Form-Data-Handler', steps= '9', status= 'ERROR', message= f'{str(error).title()}')
        print(f'ERROR - [Form-Data-Handler:S09] - {str(error).title()}')

    # check the file is present or not:S10
    try:
        if (os.path.exists(unique_sop_data_store_path)):
            # return success mesaage
            return {'message': 'Success'}, 200
        else:
            # return failure message
            return {'message': 'File Not Saved'}, 500
    except Exception as error:
        return {'message': f'Final Check Error - {str(error).title()}'}, 500