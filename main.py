from src.extractor import CSVExtractor, JSONExtractor
from src.transformers import DataTransformer
from src.loaders import JSONLoader

def run_pipeline():
    csv_extractor = CSVExtractor('data/raw/sample_source_data.csv')
    json_extractor = JSONExtractor('data/raw/sample_source_data_2.json')
    loader = JSONLoader('data/processed/jaf_records_final.json', 'data/processed/jaf_records_rejected.json')

    df_csv = csv_extractor.extract()
    df_json = json_extractor.extract()
  
    transformer = DataTransformer(df_csv, df_json)
    jaf_records, rejected_records = transformer.transform()

    loader.load(jaf_records, rejected_records)

if __name__ == "__main__":
    run_pipeline()