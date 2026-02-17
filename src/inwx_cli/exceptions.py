# inwx_cli/exceptions.py

class INWXAPIError(RuntimeError):
    """
    Raised when INWX API returns an error code.
    """

    def __init__(self, result: dict):
        self.result = result

        super().__init__(str(self.result))
