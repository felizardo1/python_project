class DataConsistencyError(Exception):
    """
    Custom exception for data consistency errors in the python_project.

    Attributes:
        message (str): Explanation of the error.
        error_code (str): A code identifying the type of consistency error.
    """
    def __init__(self, message, error_code="CONSISTENCY_ERROR"):
        """
        Initialize the DataConsistencyError with a message and optional error code.

        Args:
            message (str): Explanation of the error.
            error_code (str, optional): Code identifying the error type. Defaults to 'CONSISTENCY_ERROR'.
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        """
        Return a string representation of the error.

        Returns:
            str: Formatted error message with error code.
        """
        return f"DataConsistencyError [{self.error_code}]: {self.message}"