# MedNorth ETL Pipeline

This project is an ETL (Extract, Transform, Load) pipeline built in Python to consolidate employee data for the MedNorth Health network. It merges records from an EMR system (CSV) and an HRIS system (JSON) into a unified JSON format (JAF Schema).

## Project Structure

```
etl_project/
├── data/
│   ├── raw/                # Source CSV and JSON files
│   └── processed/          # Output JAF records (accepted and rejected)
├── src/
│   ├── extractor.py        # Data extraction logic (CSV & JSON)
│   ├── transformers.py     # Data transformation and merge logic
│   └── models.py           # Pydantic schemas for data validation
├── main.py                 # Main orchestration script
├── requirements.txt        # Python dependencies
└── ANSWERS.md              # Documentation for source mapping and take-home questions
```

## How to Run

1. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place the raw source files (`sample_source_data.csv` and `sample_source_data_2.json`) inside the `data/raw/` directory.

4. Run the ETL pipeline:
   ```bash
   python main.py
   ```

5. Check the outputs in the `data/processed/` directory:
   - `jaf_records_final.json`: Validated and merged records.
   - `jaf_records_rejected.json`: Records that failed validation or lacked required fields (e.g., missing Department).

## Design Decisions

- **Separation of Concerns:** The code is modularized into Extractors, Transformers, and Models.
- **Data Validation:** use `Pydantic` to enforce the Target JAF Schema strict types and rules.
- **Merge Strategy:** Records are deduplicated and merged using the `email` as a primary key, prioritizing the HRIS system as the source of truth.
- **Graceful Rejection:** Records missing required fields are not silently dropped; they are routed to a rejected queue for further analysis.

Please refer to `ANSWERS.md` for a detailed breakdown of the source-to-JAF field mapping and additional assumptions.
