import json
import pandas as pd

class DataExtractor:
    """Class to extract data from different file formats."""

    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def extract(self) -> pd.DataFrame:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
class CSVExtractor(DataExtractor):
    """Class to extract data from CSV files."""

    def extract(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path)
        df['source_system'] = 'MedNorth_EMR'
        df = df.rename(columns={
            'Record_ID': 'external_id',
            'Full_Name': 'Full_Name',
            'DOB': 'date_of_birth',
            'Email': 'Email',
            'Phone': 'Phone',
            'Hire_Date': 'Hire_Date',
            'Dept_Code': 'Department',
            'City_State': 'City_State',
            'Active_Flag': 'Status',
        })

        return df

class JSONExtractor(DataExtractor):
    """Class to extract data from JSON files."""

    def extract(self) -> pd.DataFrame:
        with open(self.file_path, 'r') as f:
            dados = json.load(f)
        
        df = pd.json_normalize(dados)
        df['source_system'] = 'PeopleFlow_HRIS'
        df = df.rename(columns={
            'employee_number': 'external_id',
            'name.first': 'First_Name',
            'name.last': 'Last_Name',
            'birth_date': 'date_of_birth',
            'contact.email': 'Email',
            'contact.mobile': 'Phone',
            'start_date': 'Hire_Date',
            'department': 'Department',
            'address.city': 'City',
            'address.state': 'State',
            'address.zip': 'Zip_Code',
            'employment_status': 'Status'
        })
        return df