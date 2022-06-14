import json

from cog_mem_api.MemoryContent import MemoryContent
from sqlalchemy import create_engine
import pandas as pd


class PhysicalCognitiveMemory:
    """
     class for physicalCognitiveMemory
    """

    def __init__(self):
        self.Host = "127.0.0.1"
        # self.Host = "66.45.36.17"
        self.User = "usman151mrd"
        self.DBName = "Pulse_data_T"
        # self.DBName = "pulse_data"
        self.Password = "AAbb1234"
        self.Port = "5432"

    def Save(self):
        pass

    def Load(self):
        pass

    def AddMemory(self, memory_content: pd.DataFrame, source) -> bool:
        print("Data added successfully")
        if source in ["YOUTUBE", "REDDIT", "NEWS", "TWITTER"]:
            memory = memory_content
            try:
                engine = create_engine(
                    f'postgresql://{self.User}:{self.Password}@{self.Host}:{self.Port}/{self.DBName}')
                memory.to_sql(source, con=engine, if_exists='append', index=False)
                return True
            except:
                return False
        else:
            return False

    def RemoveMemory(self, cue):
        pass

    def RetrieveMemory(self, source):

        engine = create_engine(f'postgresql://{self.User}:{self.Password}@{self.Host}:{self.Port}/{self.DBName}')
        # engine = create_engine(f'postgresql://usman:Fa@12345@127.0.0.1:5432/pulse_data')
        if source in ["YOUTUBE", "REDDIT", "NEWS", "TWITTER"]:
            table_df = pd.read_sql_table(source, con=engine)
            response = (table_df.to_dict(orient='records'))
            return json.dumps(response)

        else:
            raise Exception(f"NO Such table ({source}) exist")


