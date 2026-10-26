from pipeline.fetch_all import fetch_inspections_backfill
from pipeline.clean import clean_all_inspections
from pipeline.database import init_database
from manual_run_pipeline import RESTORE_YEARS_BACK

# Fills export inspections weeks the WA_GR101 reports missed (skipped runs) from FGIS
# certificate data, for every marketing year a full restore covers. Run it by hand when
# weeks are missing. Commit data/raw/fgis afterwards so pipeline runs keep the filled weeks
if __name__ == "__main__":
    print("--------------------")
    fetch_inspections_backfill(years_back=RESTORE_YEARS_BACK)
    clean_all_inspections()
    init_database()
    print("--------------------")
