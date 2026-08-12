import subprocess
import logging
import os
from datetime import datetime


# Create logs directory
os.makedirs("logs", exist_ok=True)


# Configure logging
logging.basicConfig(
    filename="logs/etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():

    print("=" * 40)
    print("      RIDE ETL PIPELINE")
    print("=" * 40)

    logging.info("ETL pipeline started")

    steps = [
        ("Extract", "src/extract.py"),
        ("Load", "src/load.py"),
        ("Data Quality", "src/data_quality.py"),
        ("Transform", "src/transform.py")
    ]

    for step_name, script in steps:

        print(f"\nRunning {step_name}...")
        logging.info(f"{step_name} started")

        result = subprocess.run(
            ["python", script],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            print(f"✓ {step_name} completed")
            logging.info(f"{step_name} completed successfully")

            if result.stdout:
                logging.info(result.stdout.strip())

        else:

            print(f"✗ {step_name} failed")
            print(result.stderr)

            logging.error(
                f"{step_name} failed: {result.stderr.strip()}"
            )

            logging.error("ETL pipeline stopped")

            return

    logging.info("ETL pipeline completed successfully")

    print("\n" + "=" * 40)
    print("     PIPELINE COMPLETED")
    print("=" * 40)


if __name__ == "__main__":
    run_pipeline()