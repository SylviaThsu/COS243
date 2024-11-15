# df2sqlite.py
import sqlite3
import pandas as pd
import logging
from create_course_dataframe import create_course_dataframe, process_xlsx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

CLEAN_COLUMNS = {
        'Course Code': 'course_code',
        'Course Title': 'course_title', 
        'Cr': 'credits',
        'Prereq(s)': 'prerequisites',
        'Instructor ': 'instructor',
        'Major/ GE/ \nElective': 'course_type',
        'Format': 'class_format',
        'Mon': 'monday_start',
        'MonTo': 'monday_end',
        'Tue': 'tuesday_start',
        'TueTo': 'tuesday_end',
        'Wed': 'wednesday_start',
        'WedTo': 'wednesday_end',
        'Thu': 'thursday_start',
        'ThuTo': 'thursday_end',
        'Fri': 'friday_start',
        'FriTo': 'friday_end',
        'Sat': 'saturday_start',
        'SatTo': 'saturday_end',
        'Platform': 'platform',
        'New/ Repeat': 'course_status',
        'Room': 'room_number'
                }

def save_to_sqlite(df, database_name='courses.db', table_name='courses'):
    """
    Save DataFrame to SQLite Database
    """
    try:
        # Rename columns using the mapping
        df = df.rename(columns=CLEAN_COLUMNS)
        
        logging.info(f"Connecting to database: {database_name}")
        conn = sqlite3.connect(database_name)
        
        logging.info(f"Saving DataFrame to table: {table_name}")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        logging.info("Data successfully saved to SQLite database")
        
        # Verify the data
        row_count = pd.read_sql(f"SELECT COUNT(*) FROM {table_name}", conn).iloc[0,0]
        logging.info(f"Verified {row_count} rows in table {table_name}")
        
        conn.close()
        return True
        
    except Exception as e:
        logging.error(f"Error saving to database: {str(e)}")
        return False

if __name__ == "__main__":
    # Load and process XLSX file
    file_path = "FTCM_Course List_Spring2025.xlsx"
    result = process_xlsx(file_path)

    if result:
        column_names, department_program_courses = result
        
        # Use the keys from CLEAN_COLUMNS for cleaned_column_names
        cleaned_column_names = list(CLEAN_COLUMNS.keys())
        
        # Create DataFrame
        df = create_course_dataframe(cleaned_column_names, column_names, department_program_courses)
        
        # Save to SQLite
        if save_to_sqlite(df):
            logging.info("Process completed successfully")
        else:
            logging.error("Failed to save data to SQLite")
    else:
        logging.error("Failed to process XLSX file")
