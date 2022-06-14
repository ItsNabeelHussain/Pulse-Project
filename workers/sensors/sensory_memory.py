from cog_mem_api.PhysicalCogMemory import *


class Sensor:
    def __init__(self, name, internal_id, interval=86400, attention_limit=1000, source=""):
        self.Name = name
        self.InternalID = internal_id
        self.Attention = []
        self.AttentionLimit = attention_limit
        self.Source = source
        self.Interval = interval
        self.TerminateLoop = False
        self.ErrorCode = ""
        self.PhysicalCMemory = PhysicalCognitiveMemory()

    def AttendTo(self, attention_key) -> bool:
        if attention_key in self.Attention:
            print("Process failed for ", attention_key)
            return False

        if self.CanHaveMoreAttention():
            self.Attention.append(attention_key)
            self.DoWork(attention_key)
            return True

        return False

    def CanHaveMoreAttention(self):
        if len(self.Attention) < self.AttentionLimit:
            return True
        return False

    def Start(self, instances):
        pass

    def live_data_response(self, keyword, source) -> bool:
        content = self.FetchSensorData(keyword)
        if content.shape[0] == 0:
            return False
        senti_content = self.DoLowLevelPerception(content)
        response = self.AddMemory(senti_content, source=source)
        return response

    def DoWork(self, attention_key):
        memoryContent = self.FetchSensorData(attention_key)
        memoryContent_percept = self.DoLowLevelPerception(memoryContent)
        if memoryContent_percept.shape[0] == 0:
            print("Nothing found against ", attention_key)
            return
        self.AddMemory(memoryContent_percept)

    def Stop(self):
        self.TerminateLoop = True

    def SaveCalibration(self):
        pass

    #

    def LoadCalibration(self):
        pass

    def FetchSensorData(self, keyword) -> pd.DataFrame:
        print("Fetch Sensor data called in sensory memory : ", keyword)
        """Abstract"""
        return pd.DataFrame()

    def AddMemory(self, memory_content: pd.DataFrame, source):
        """Abstract"""
        return self.PhysicalCMemory.AddMemory(memory_content, source)

    def RemoveMemory(self, cue):
        """Abstract"""
        pass

    def DoLowLevelPerception(self, memorycontent: pd.DataFrame) -> pd.DataFrame:
        """return percept"""
        pass
