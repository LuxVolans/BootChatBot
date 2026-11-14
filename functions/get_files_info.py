import os



def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    try:

        working_dir_abs = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_directory]) == working_dir_abs



        #Error Cases:
        if not valid_target_dir:
            raise ValueError(f'Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_directory):
            raise ValueError(f'"{directory}" is not a directory')
        if os.path.isdir(target_directory):
            end_message = []
            for item in os.listdir(target_directory):
                item_path = os.path.join(target_directory, item)
                item_string = f"  - {item}: file_size={os.path.getsize(os.path.join(target_directory, item))} bytes, is_dir={os.path.isdir(os.path.join(target_directory, item))} \n"
                end_message.append(item_string)
            return f"Result for current directory: \n{''.join(end_message)}"
    except Exception as e:
        return str(f"Error: {e}") 


   # for item in target_directory:
        


    