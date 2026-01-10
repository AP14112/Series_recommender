import sys
import traceback

class RecommenderException(Exception):
    def __init__(self, message: str, error: Exception = None):
        super().__init__(message)
        self.message = message
        self.error = error
    def __str__(self):
        if self.error:
            return f"{self.message} | Original error: {self.error}"
        return self.message


def raise_recommender_exception(message: str, error: Exception):
   
    _, _, tb = sys.exc_info()
    trace = traceback.format_tb(tb)

    full_message = f"{message}\nTraceback:\n{''.join(trace)}"
    raise RecommenderException(full_message, error)
