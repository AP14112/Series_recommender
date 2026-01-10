import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_loader import DataLoader
from src.vector_score import VectorScore
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import RecommenderException

load_dotenv()

logger = get_logger(__name__)


def main():
    try:
        logger.info("Starting build pipeline...")
        series_loader = DataLoader(
            original_csv="data/series_metadata.csv",
            processed_csv="data/processed_series_metadata.csv",
        )
        processed_series_csv = series_loader.process()

        logger.info("Series metadata processed successfully")
        user_loader = DataLoader(
            original_csv="data/user_interactions.csv",
            processed_csv="data/processed_user_interactions.csv",
        )
        processed_user_csv = user_loader.user_process()

        logger.info("User interactions processed successfully")
        vector_builder = VectorScore(
            csv_path=processed_series_csv,
            persist_directory="faiss_db",
        )
        vector_builder.build_and_save_vector_store()

        logger.info("Vector store built successfully")
        logger.info("Build pipeline completed successfully")

    except Exception as e:
        logger.error(f"Failed to execute build pipeline: {str(e)}")
        raise RecommenderException("Error during build pipeline", e)



if __name__ == "__main__":
    main()
