# define form_submitted_file_handler function
def form_submitted_file_handler(save_type: str, sop_file, account_name: str) -> dict[str, str]: #type: ignore
    # importing module:S01
    try:
        import os
        from pathlib import Path
        import sys
        from datetime import datetime
        from werkzeug.utils import secure_filename
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S01] - {str(error).title()}', 'file_path' : 'NA'}

    # appending system path:S02
    try:
        sys.path.append(os.getcwd())
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S01] - {str(error).title()}', 'file_path' : 'NA'}

    # importing user-define function:S03
    try:
        from Backend.LogHandler.logwriter import log_writer
    except Exception as error:
        return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S01] - {str(error).title()}', 'file_path' : 'NA'}

    # define parent folder path:S04
    try:
        parent_folder_path = Path.cwd()
        resource_dump_folder_path = Path(parent_folder_path) / 'ResourceDump'
        incident_dump_folder_path = Path(resource_dump_folder_path) / 'IncidentDump'
        sop_dump_folder_path = Path(resource_dump_folder_path) / 'SoPDump'
        sop_file_dump_folder_path = Path(resource_dump_folder_path) / 'SoPFile'
        log_writer(script_name= 'File-Save-Handler', steps= '4', status= 'SUCCESS', message= 'All Folders Are Defined')
    except Exception as error:
        log_writer(script_name= 'File-Save-Handler', steps= '4', status= 'ERROR', message= f'{str(error).title()}')
        return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S04] - {str(error).title()}', 'file_path' : 'NA'}

    # check if "ResourceDump" folder is present:S05
    try:
        if ((resource_dump_folder_path.exists()) and (resource_dump_folder_path.is_dir())):
            log_writer(script_name= 'File-Save-Handler', steps= '5', status= 'SUCCESS', message= '"ResourceDump" Folder Already Present')
        else:
            # create folder
            resource_dump_folder_path.mkdir()
            # check if folder is created
            if ((resource_dump_folder_path.exists()) and (resource_dump_folder_path.is_dir())):
                log_writer(script_name= 'File-Save-Handler', steps= '5', status= 'ERROR', message= '"ResourceDump" Folder Not Created')
                return {'status' : 'ERROR', 'message' : '"ResourceDump" Folder Not Created', 'file_path' : 'NA'}
            else:
                log_writer(script_name= 'File-Save-Handler', steps= '5', status= 'SUCCESS', message= '"ResourceDump" Folder Is Created Successfully')
    except Exception as error:
        log_writer(script_name= 'File-Save-Handler', steps= '5', status= 'ERROR', message= f'{str(error).title()}')
        return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S05] - {str(error).title()}', 'file_path' : 'NA'}

    # check if "SOPDump" folder is present:S06
    try:
        if ((sop_dump_folder_path.exists()) and (sop_dump_folder_path.is_dir())):
            log_writer(script_name= 'File-Save-Handler', steps= '5', status= 'SUCCESS', message= '"ResourceDump\\SoPDump" Folder Already Present')
        else:
            # create folder
            sop_dump_folder_path.mkdir()
            # check if folder is created
            if ((sop_dump_folder_path.exists()) and (sop_dump_folder_path.is_dir())):
                log_writer(script_name= 'File-Save-Handler', steps= '6', status= 'ERROR', message= '"RecourceDump\\SoPDump" Folder Not Created')
                return {'status' : 'ERROR', 'message' : '"RecourceDump\\SoPDump" Folder Not Created', 'file_path' : 'NA'}
            else:
                log_writer(script_name= 'File-Save-Handler', steps= '6', status= 'SUCCESS', message= '"ResourceDump\\SoPDump" Folder Created Successfullt')
    except Exception as error:
        log_writer(script_name= 'File-Save-Handler', steps= '6', status= 'ERROR', message= f'{str(error).title()}')
        return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S06] - {str(error).title()}', 'file_path' : 'NA'}

    # check if "SoPFile" folder is present:S07
    try:
        if ((sop_file_dump_folder_path.exists()) and (sop_file_dump_folder_path.is_dir())):
            # create folder
            os.makedirs(sop_file_dump_folder_path)
            # check if folder is created
            if (not (os.path.exists(sop_file_dump_folder_path))):
                log_writer(script_name= 'File-Save-Handler', steps= '7', status= 'ERROR', message= '"ResourceDump\\SoPDump\\SoPFile" Folder Not Created')
            else:
                log_writer(script_name= 'File-Save-Handler', steps= '7', status= 'SUCCESS', message= '"ResourceDump\\SoPDump\\SoPFile" Folder Already Present')
    except Exception as error:
        log_writer(script_name= 'File-Save-Handler', steps= '7', status= 'ERROR', message= f'{str(error).title()}')
        return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S07] - {str(error).title()}', 'file_path' : 'NA'}

    # define file store path based on "save_type"
    # if "save_type" is "sop":S08-A
    if (str(save_type).lower() == 'sop'):
        # define secure file name and file path
        try:
            cleared_unique_sop_file_name = secure_filename(f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}_{str(account_name.upper())}.docx")
            # define file store path
            unique_sop_file_store_path = Path(sop_file_dump_folder_path) / cleared_unique_sop_file_name
            log_writer(script_name= 'File-Save-Handler', steps= '8-A', status= 'SUCCESS', message= f'New File Name: "{cleared_unique_sop_file_name}" Created To Store "{str(account_name).upper()}" SoP')
        except Exception as error:
            log_writer(script_name= 'File-Save-Handler', steps= '8-A', status= 'ERROR', message= f'{str(error).title()}')
            return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S08-A] - {str(error).title()}', 'file_path' : 'NA'}

        # save the file and sent response:S08-B
        try:
            # check if file type is .docx
            if (sop_file.filename.endswith('.docx')):
                # save the file
                sop_file.save(unique_sop_file_store_path)
                # check the file save status
                if ((unique_sop_file_store_path.exists()) and (unique_sop_file_store_path.is_file())):
                    if (int(unique_sop_file_store_path.stat().st_size) > 0):
                        log_writer(script_name= 'File-Save-Handler', steps= '8-B', status= 'SUCCESS', message= f'"{cleared_unique_sop_file_name}" File Saved Successfully Inside "..\\SoPFile" Folder')
                        # return frontend mesaage
                        return {'status' : 'SUCCESS', 'message' : f'File Save Successfully', 'file_path' : f'{str(unique_sop_file_store_path)}'}
                    else:
                        log_writer(script_name= 'File-Save-Handler', steps= '8-B', status= 'SUCCESS', message= f'"{cleared_unique_sop_file_name}" File Saved Corrupted')
                        # return frontend mesaage
                        return {'status' : 'SUCCESS', 'message' : f'File Saved But Corrupted', 'file_path' : 'NA'}
                else:
                    log_writer(script_name= 'File-Save-Handler', steps= '8-B', status= 'SUCCESS', message= f'"{cleared_unique_sop_file_name}" File Not Saved')
                    # return frontend mesaage
                    return {'status' : 'SUCCESS', 'message' : f'File Not Saved', 'file_path' : 'NA'}
            else:
                log_writer(script_name= 'File-Save-Handler', steps= '8-B', status= 'SUCCESS', message= f'"{cleared_unique_sop_file_name}" File Has Not In Allowed Extension Which Is ".docx"')
                # return frontend mesaage
                return {'status' : 'SUCCESS', 'message' : 'File Type Is Not Allowed', 'file_path' : 'NA'}
        except Exception as error:
            log_writer(script_name= 'File-Save-Handler', steps= '8-B', status= 'ERROR', message= f'{str(error).title()}')
            return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S08-B] - {str(error).title()}', 'file_path' : 'NA'}

    # if "save_type" is "incident":S09-B
    if (str(save_type).lower() == 'incident'):
        # define secure file name and file path
        try:
            cleared_unique_incident_file_name = secure_filename(f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}_{str(account_name.upper())}.{Path(sop_file.filename).suffix}")
            # define file store path
            unique_incident_file_store_path = Path(sop_file_dump_folder_path) / cleared_unique_incident_file_name
            log_writer(script_name= 'File-Save-Handler', steps= '9-A', status= 'SUCCESS', message= f'New File Name: "{cleared_unique_incident_file_name}" Created To Store "{str(account_name).upper()}" SoP')
        except Exception as error:
            log_writer(script_name= 'File-Save-Handler', steps= '9-A', status= 'ERROR', message= f'{str(error).title()}')
            return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S09-A] - {str(error).title()}', 'file_path' : 'NA'}

        # save the file and sent response:S09-B
        try:
            # save the file
            sop_file.save(unique_incident_file_store_path)
            # check the file save status
            if ((unique_incident_file_store_path.exists()) and (unique_incident_file_store_path.is_file())):
                if (int(unique_incident_file_store_path.stat().st_size) > 0):
                    log_writer(script_name= 'File-Save-Handler', steps= '9-B', status= 'SUCCESS', message= f'"{cleared_unique_incident_file_name}" File Saved Successfully Inside "..\\SoPFile" Folder')
                    # return frontend mesaage
                    return {'status' : 'SUCCESS', 'message' : f'File Save Successfully', 'file_path' : f'{str(unique_incident_file_store_path)}'}
                else:
                    log_writer(script_name= 'File-Save-Handler', steps= '9-B', status= 'SUCCESS', message= f'"{cleared_unique_incident_file_name}" File Saved Corrupted')
                    # return frontend mesaage
                    return {'status' : 'SUCCESS', 'message' : f'File Saved But Corrupted', 'file_path' : 'NA'}
            else:
                log_writer(script_name= 'File-Save-Handler', steps= '9-B', status= 'SUCCESS', message= f'"{cleared_unique_incident_file_name}" File Not Saved')
                # return frontend mesaage
                return {'status' : 'SUCCESS', 'message' : f'File Not Saved', 'file_path' : 'NA'}
        except Exception as error:
            log_writer(script_name= 'File-Save-Handler', steps= '9-B', status= 'ERROR', message= f'{str(error).title()}')
            return {'status' : 'ERROR', 'message' : f'[File-Save-Handler:S09-B] - {str(error).title()}', 'file_path' : 'NA'}