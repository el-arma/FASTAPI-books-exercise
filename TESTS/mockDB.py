import os
import shutil

def create_test_db(source_DB, target_DB):
    if not os.path.exists(source_DB):
        raise FileNotFoundError(f"Source DB not found: {source_DB}")
   
    try:
        # Copy PROD - TEST
        shutil.copy(source_DB, target_DB)
    except Exception as e:
        print(f"An error occured: {e}")
        raise 

    print("Mock DB prepared.")

    return None
