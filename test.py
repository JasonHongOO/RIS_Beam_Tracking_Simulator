import random
import json
import threading
import datetime
import time

import Const
from Lab_v1 import HandOverSimulator

running_global = True

class MoveSimulator:
    def __init__(self):
        self.CaseData, self.CaseDataBehind = ReadJsonData()
        self.Cur_Case_Value = 0
        self.Cur_Angle_Value = 0
        self.Target_Angle_Value = 0

    def Start(self):
        self.increment = Const.STEP_OFFEST_BASE
        self.update_thread = threading.Thread(target=self.Updata)
        self.update_thread.start()
        
    def Thread_Join(self):
        # Join Threads
        self.update_thread.join()

    def Updata(self):
        while running_global:
            self.current_time = datetime.datetime.now().strftime("Time : %H:%M:%S")
            if self.Cur_Angle_Value != self.Target_Angle_Value:
                if self.Cur_Angle_Value < self.Target_Angle_Value:
                    self.Cur_Angle_Value += self.increment + (random.randint(Const.STEP_OFFEST_MIN, Const.STEP_OFFEST_MAX) if Const.STEP_RANDOM_ACTIVATE == True else 0)
                else:
                    self.Cur_Angle_Value -= self.increment + (random.randint(Const.STEP_OFFEST_MIN, Const.STEP_OFFEST_MAX) if Const.STEP_RANDOM_ACTIVATE == True else 0)

                if self.Cur_Angle_Value > Const.ANGLE_MAX: self.Cur_Angle_Value = Const.ANGLE_MAX
                elif self.Cur_Angle_Value < Const.ANGLE_MIN: self.Cur_Angle_Value = Const.ANGLE_MIN

            updata_interval = [1, 0.75, 0.5, 0.25]
            time.sleep(random.choice(updata_interval)) 

            # time.sleep(random.uniform(1, 0.1)) 
            
            # time.sleep(0.1)       # UE 移動速度暫定不變

    def Input(self, Cur_Case_Value, Target_Angle_Value):
        self.Cur_Case_Value = Cur_Case_Value
        self.Target_Angle_Value = Target_Angle_Value

    def Output(self):
        RSRP_Value = self.CaseDataBehind['Case'][str(self.Cur_Case_Value)]['Angle'][str(self.Cur_Angle_Value)]
        RSRP_Value = RSRP_Value + (random.randint(Const.RSRP_OFFEST_MIN, Const.RSRP_OFFEST_MAX) if Const.RSRP_FLUCTUATING_ACTIVATE == True else 0) * random.choice([1, -1])
        return RSRP_Value, self.Cur_Angle_Value
            
   
def ReadJsonData():
    Data_Fixed_Json_Path = Const.DATA_FILE
    with open(Data_Fixed_Json_Path, 'r') as f:
        Data_Fixed_Json = json.load(f)

    Data_Fixed_Behind_Json_Path = Const.DATA_BEHIND_FILE
    with open(Data_Fixed_Behind_Json_Path, 'r') as f:
        Data_Fixed_Behind_Json = json.load(f)

    return Data_Fixed_Json, Data_Fixed_Behind_Json
           
if __name__ == "__main__":
    CaseData, CaseDataBehind = ReadJsonData()
    # ===============  參數  ===============
    Target_Angle_Value = 0
    Cur_Angle_Value = 0
    Cur_Case_Value = 0
    Cur_RSRP_Value = CaseDataBehind['Case']['0']['Angle']["0"]

    # ===============  Simulator  ===============
    Simulator = HandOverSimulator()
    Simulator.Start()
    Move = MoveSimulator()
    Move.Start()

    # ===============  Start  ===============
    while running_global:
        Simulator.Input(Cur_RSRP_Value, Cur_Angle_Value)
        Cur_Case_Value, Target_Angle_Value = Simulator.Output()

        # print(f"Cur_Case_Value = {Cur_Case_Value}")
        # print(f"Target_Angle_Value = {Target_Angle_Value}")

        Move.Input(Cur_Case_Value, Target_Angle_Value)
        Cur_RSRP_Value, Cur_Angle_Value = Move.Output()

        # print(f"Cur_RSRP_Value = {Cur_RSRP_Value}")
        # print(f"Cur_Angle_Value = {Cur_Angle_Value}")

        time.sleep(0.1)

    #  ===============  Over  ===============
    Simulator.Thread_Join()
    Move.Thread_Join()

    print("程式已結束")


