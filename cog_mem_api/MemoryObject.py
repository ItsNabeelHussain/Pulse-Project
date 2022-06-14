from datetime import datetime


class MemoryObject:
    """
     class for memory objects
    """
    def __init__(self):
        self.MOID = "" #time.now() + ctr
        self.TimeStamp = datetime.now()
        self.PerceptKeys = []
        self.Content =dict()
