import json

class JSONLoader:
    """Class to load data into JSON files."""
    
    def __init__(self, final_filepath: str, rejected_filepath: str):
        self.final_filepath = final_filepath
        self.rejected_filepath = rejected_filepath

    def _default_serializer(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return str(obj)

    def load(self, jaf_records: list, rejected_records: list):
        # Convert JAF Pydantic models to dicts
        lista_json = [record.model_dump(mode='json') for record in jaf_records]
        
        # Save valid records
        with open(self.final_filepath, 'w') as f:
            json.dump(lista_json, f, indent=4)
            
        # Save rejected records
        with open(self.rejected_filepath, 'w') as f:
            json.dump(rejected_records, f, indent=4, default=self._default_serializer)
