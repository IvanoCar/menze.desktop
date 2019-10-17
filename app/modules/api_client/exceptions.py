class APIError(Exception):
    def __init__(self):
        super().__init__("Can't connect to Menze API.")

class UpdateFailed(Exception):
    def __init__(self):
        super().__init__("Update operation has failed.")

class GetFailed(Exception):
    def __init__(self):
        super().__init__("Get operation has failed.")
