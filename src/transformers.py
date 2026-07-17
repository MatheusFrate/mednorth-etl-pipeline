import pandas as pd
from src.models import Jaf
from datetime import datetime
import re
import numpy as np
from dateutil import parser
from src import models

class DataTransformer:
    """Class to transform data into the desired format."""

    def __init__(self, df_csv: pd.DataFrame, df_json: pd.DataFrame):
        self.df_csv = df_csv
        self.df_json = df_json

    def _clean_name(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'Full_Name' in df.columns:
            def split_name(full_name):
                    if pd.isna(full_name):
                        return pd.Series([None, None])
                    if ',' in full_name:
                        partes = full_name.split(',', 1)
                        return pd.Series([partes[1].strip(), partes[0].strip()])
                    else:
                        partes = full_name.split(' ', 1)
                        if len(partes) == 2:
                            return pd.Series([partes[0].strip(), partes[1].strip()])
                        else:
                            return pd.Series([partes[0].strip(), None])

            df[['First_Name', 'Last_Name']] = df['Full_Name'].apply(split_name)
        return df
    
    def _clean_phone(self, phone: str) -> str:
        
        if pd.isna(phone):
            return None
        phone_str = re.sub(r'\D', '', str(phone))  
        if len(phone_str) == 11 and phone_str.startswith('1'):
            return f"+{phone_str}"
        elif len(phone_str) == 10:
            return f"+1{phone_str}"
        else:
            return None 
        
    def _clean_date(self, date_str: str) -> datetime.date:
        if pd.isna(date_str):
            return None
        try:
            date = parser.parse(str(date_str))
            return date.date()
        except ValueError:
            return None
    
    def _clean_department(self, department: str) -> str:
        if pd.isna(department):
            return None
        if department.lower() in ['er', 'emerg.']:
            return 'Emergency Medicine'
        elif department.lower() in ['card', 'cardiology']:
            return 'Cardiology'
        elif department.lower() in ['ped', 'peds']:
            return 'Pediatrics'
        elif department.lower() in ['adm', 'admin']:
            return 'Administration'
        return None
    
    def _clean_city_state(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'City_State' in df.columns:
            def split_city_state(city_state):
                parts = re.split(r'[,-]', str(city_state))
                if len(parts) == 2:
                    return pd.Series([parts[0].strip(), parts[1].strip()])
                else:
                    return pd.Series([None, None])

            df[['City', 'State']] = df['City_State'].apply(split_city_state)
        return df

    def _clean_status(self, status: str) -> str:
        if pd.isna(status):
            return None
        if status.lower() in ['active', 'y', '1', 'employed', 'leave of absence']:
            return models.StatusEnum.ACTIVE
        elif status.lower() in ['terminated', 'n', '0', 't']:
            return models.StatusEnum.INACTIVE
        return None

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._clean_name(df)
        df['Phone'] = df['Phone'].apply(self._clean_phone)
        df['date_of_birth'] = df['date_of_birth'].apply(self._clean_date)
        df['hire_date'] = df['Hire_Date'].apply(self._clean_date)
        df['Department'] = df['Department'].apply(self._clean_department)
        df = self._clean_city_state(df)
        df['Status'] = df['Status'].apply(self._clean_status)
        df['Email'] = df['Email'].str.lower()
        return df


    def transform(self) -> tuple[list[Jaf], list[dict]]:
        
        df_json = self._clean_data(self.df_json)
        df_csv = self._clean_data(self.df_csv)

        df_csv_without_email = df_csv[df_csv['Email'].isnull()]
        df_json_without_email = df_json[df_json['Email'].isnull()]

        df_csv_vip = df_csv.dropna(subset=['Email']).drop_duplicates(subset=['Email'], keep='first').set_index('Email')
        df_json_vip = df_json.dropna(subset=['Email']).drop_duplicates(subset=['Email'], keep='first').set_index('Email')

        df_final = df_json_vip.combine_first(df_csv_vip)
        
        df_final = df_final.reset_index()

        df_final = pd.concat([df_final, df_csv_without_email, df_json_without_email], ignore_index=True)

        df_final = df_final.astype(object).where(pd.notna(df_final), None)
        records_dict = df_final.to_dict(orient='records')

        jaf_records = []
        rejected_records = []

        for row in records_dict:
            try:
                jaf_record = Jaf(
                    source_system=row.get('source_system'),
                    external_id=row.get('external_id'),
                    first_name=row.get('First_Name'),
                    last_name=row.get('Last_Name'),
                    date_of_birth= row.get('date_of_birth'),
                    email=row.get('Email'),
                    phone=row.get('Phone') if pd.notna(row.get('Phone')) else None,
                    hire_date=row.get('hire_date'),
                    department=row.get('Department'),
                    city=row.get('City'),
                    state=row.get('State'),
                    status=row.get('Status')
                )
                jaf_records.append(jaf_record)
            except Exception as e:
                # If failed in validation of Pydantic (e.g., missing required field), reject
                row['rejection_reason'] = f"Validation Error: {str(e)}"
                rejected_records.append(row)
                
        return jaf_records, rejected_records