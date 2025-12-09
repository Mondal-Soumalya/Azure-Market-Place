# define form_submitted_file_handler function
def form_submitted_file_handler(sop_file, account_name: str) -> tuple:
    # define constant
    RESOURCE_DUMP_FOLDER_PRESENT_STATUS = False
    SOP_DUMP_FOLDER_PRESENT_STATUS = False

    # importing module:S01
    try:
        import os
        import sys
        from werkzeug.utils import secure_filename
    except Exception as error:
        print(f'ERROR - [Form-File-Handler:S01] - {str(error).title()}')

    # appending system path:S02
    try:
        sys.path.append(os.getcwd())
    except Exception as error:
        print(f'ERROR - [Form-File-Handler:S02] - {str(error).title()}')

    # importing user-define function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        print(f'ERROR - [Form-File-Handler:S03] - {str(error).title()}')

    # define parent folder path:S04
    try:
        parent_folder_path = os.getcwd()
        resource_dump_folder_path = os.path.join(parent_folder_path, 'ResourceDump')
        sop_dump_folder_path = os.path.join(resource_dump_folder_path, 'SoPDump')
        sop_file_dump_folder_path = os.path.join(sop_dump_folder_path, 'SoPFile')
        log_writer(script_name= 'Form-File-Handler', steps= '4', status= 'SUCCESS', message= 'All Folders Are Defined')
    except Exception as error:
        log_writer(script_name= 'Form-File-Handler', steps= '4', status= 'ERROR', message= f'{str(error).title()}')
        print(f'ERROR - [Form-File-Handler:S04] - {str(error).title()}')

    # check "ResourceDump" folder present:S05
    try:
        if (not (os.path.exists(resource_dump_folder_path))):
            # create folder
            os.makedirs(resource_dump_folder_path)
            # check if folder is created
            if (not (os.path.exists(resource_dump_folder_path))):
                RESOURCE_DUMP_FOLDER_PRESENT_STATUS = False
                log_writer(script_name= 'Form-File-Handler', steps= '5', status= 'ERROR', message= '"ResourceDump" Folder Not Created')
                sys.exit(1)
            else:
                RESOURCE_DUMP_FOLDER_PRESENT_STATUS = True
                log_writer(script_name= 'Form-File-Handler', steps= '5', status= 'SUCCESS', message= '"ResourceDump" Folder Already Present')
    except Exception as error:
        log_writer(script_name= 'Form-File-Handler', steps= '5', status= 'ERROR', message= f'{str(error).title()}')
        print(f'ERROR - [Form-File-Handler:S05] - {str(error).title()}')

    # check "SOPDump" folder present status:S06
    if (RESOURCE_DUMP_FOLDER_PRESENT_STATUS):
        try:
            if (not (os.path.exists(sop_dump_folder_path))):
                # create folder
                os.makedirs(sop_dump_folder_path)
                # check if folder is created
                if (not (os.path.exists(sop_dump_folder_path))):
                    SOP_DUMP_FOLDER_PRESENT_STATUS = False
                    log_writer(script_name= 'Form-File-Handler', steps= '6', status= 'ERROR', message= '"RecourceDump\\SoPDump" Folder Not Created')
                    sys.exit(1)
                else:
                    SOP_DUMP_FOLDER_PRESENT_STATUS = True
                    log_writer(script_name= 'Form-File-Handler', steps= '6', status= 'SUCCESS', message= '"ResourceDump\\SoPDump" Folder Already Present')
        except Exception as error:
            log_writer(script_name= 'Form-File-Handler', steps= '6', status= 'ERROR', message= f'{str(error).title()}')
            print(f'ERROR - [Form-File-Handler:S06] - {str(error).title()}')

    # check "SoPFile" folder present status:S07
    if (SOP_DUMP_FOLDER_PRESENT_STATUS):
        try:
            if (not (os.path.exists(sop_file_dump_folder_path))):
                # create folder
                os.makedirs(sop_file_dump_folder_path)
                # check if folder is created
                if (not (os.path.exists(sop_file_dump_folder_path))):
                    SOP_DUMP_FOLDER_PRESENT_STATUS = False
                    log_writer(script_name= 'Form-File-Handler', steps= '7', status= 'ERROR', message= '"ResourceDump\\SoPDump\\SoPFile" Folder Not Created')
                    sys.exit(1)
                else:
                    SOP_DUMP_FOLDER_PRESENT_STATUS = True
                    log_writer(script_name= 'Form-File-Handler', steps= '7', status= 'SUCCESS', message= '"ResourceDump\\SoPDump\\SoPFile" Folder Already Present')
        except Exception as error:
            log_writer(script_name= 'Form-File-Handler', steps= '7', status= 'ERROR', message= f'{str(error).title()}')
            print(f'ERROR - [Form-File-Handler:S07] - {str(error).title()}')

    # define file store path:S08
    try:
        # define file name
        unique_sop_file_name = secure_filename(f"{str(account_name.upper())}.docx")
        log_writer(script_name= 'Form-File-Handler', steps= '8', status= 'SUCCESS', message= f'"{unique_sop_file_name}" File Name Created')
        # define file store path
        unique_sop_file_store_path = os.path.join(sop_file_dump_folder_path, unique_sop_file_name)
    except Exception as error:
        log_writer(script_name= 'Form-File-Handler', steps= '8', status= 'ERROR', message= f'{str(error).title()}')
        print(f'ERROR - [Form-File-Handler:S08] - {str(error).title()}')

    # save the file:S09
    try:
        # check if file type is .docx
        if (sop_file.filename.endswith('.docx')):
            sop_file.save(unique_sop_file_store_path)
            log_writer(script_name= 'Form-File-Handler', steps= '9', status= 'SUCCESS', message= f'"{unique_sop_file_name}" File Saved In "..\\SoPFile" Folder')
    except Exception as error:
        log_writer(script_name= 'Form-File-Handler', steps= '9', status= 'ERROR', message= f'{str(error).title()}')
        print(f'ERROR - [Form-File-Handler:S09] - {str(error).title()}')
        return {'message': f'File Save Error - {str(error).title()}', 'filename': 'N/A'}, 500

    # check the file is present or not:S10
    try:
        if (os.path.exists(unique_sop_file_store_path)):
            # return success mesaage
            return {'message': 'Success'}, 200, unique_sop_file_store_path
        else:
            # return failure message
            return {'message': 'File Not Saved'}, 500
    except Exception as error:
        return {'message': f'Final Check Error - {str(error).title()}'}, 500