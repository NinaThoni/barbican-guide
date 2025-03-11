import sys
sys.path.append("../")

import logging
import azure.functions as func
from etl_pipeline import run_pipeline  # Import your ETL script

app = func.FunctionApp()  # This is required for Azure Functions v4

@app.function_name(name="barbican_etl_pipeline")  # Define function name
@app.schedule(schedule="0 6 * * * *", arg_name="mytimer", run_on_startup=True,
              use_monitor=False)  # Runs daily at midnight
def barbican_etl_pipeline(mytimer: func.TimerRequest) -> None:
    logging.info("🔄 Starting Barbican ETL pipeline...")

    try:
        run_pipeline()  # Call your ETL function
        logging.info("✅ ETL pipeline completed successfully!")
    except Exception as e:
        logging.error(f"❌ ETL pipeline failed: {e}")
