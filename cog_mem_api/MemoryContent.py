import pandas as pd


class MemoryContent:
    """
      class for memory content
    """
    def __init__(self):
        self.MemoryObjects = list()  # contain list of memory objects
        self.Capacity = -1  # maintain the length of memory objects

    def ToDataFrame(self) -> pd.DataFrame:

        return pd.DataFrame(eval(self.MemoryObjects))  # convert memory objects into dataframe

    def Append(self, record: dict):
        """
        function which appends memoryobjects into record
        """

        self.MemoryObjects.append(record)
