
import time
import json
import threading
import datetime
import random
import numpy as np

from Kalman.KalmanPredictor import KalmanPredictor
import Const
from GUI import *
from TextColor import *


class HandOverSimulator:
    def __init__(self):
        self.CaseData, self.CaseDataBehind = ReadJsonData()              # 輻射場型資料
        self.Target_Angle_Value = 0
        self.Cur_Angle_Value = 0
        self.Cur_RSRP_Value = self.CaseDataBehind['Case']['0']['Angle']["0"]
        self.Cur_Case_Value = 0
        self.Old_Case_Value = 0
        self.Case_SavePoint_Value = 0

        # 過程參數
        self.increment = Const.STEP_OFFEST_BASE
        self.RSRP_offest = Const.RSRP_OFFEST_BASE
        self.running = False
        self.current_time = ""
        self.cur_err_time = ""
        self.pre_err_time = ""
        self.lock = threading.Lock()

        self.HandoverState = 0             
        self.HandoverCheck = False
        self.HandoverThreshold = Const.HANDOVER_THRESHOLD       # 105~125             
        self.SortPotentialList = []

        self.Check_RSRP_State = 0
        self.Check_RSRP_Sum = 0
        self.Check_RSRP_Avg = 0

        # 暫時使用的變數
        self.Counter = 0
        
    def Start(self):
        self.running = True
        self.AngleKalman = KalmanPredictor(self)
        self.AngleKalman.KalmanFilter(self.Cur_Angle_Value, "Angle")
        self.RSRPKalman = KalmanPredictor(self)
        self.AngleKalmanState = True                     # True 有資料的更新、 False 無資料的更新    
        self.RSRPKalmanState = True                     # True 有資料的更新、 False 無資料的更新    
        self.QueueCnt = 1                               
        
        # 啟動更新數值的執行緒
        update_thread = threading.Thread(target=self.Updata)
        update_thread.start()

        update_state_thread = threading.Thread(target=self.Updata_State)
        update_state_thread.start()

        # GUI
        self.Open_GUI_thread = threading.Thread(target=self.GUI, args=(self.GUI_Close,))
        self.Open_GUI_thread.start()

        # Join Threads
        self.Open_GUI_thread.join()
        update_thread.join()
        update_state_thread.join()
        
    def GUI_Close(self):        # GUI CallBack Function
        print("GUI Winows Close => Process End")
        self.running = False

    def GUI(self, GUI_Close):
        # GUI
        self.app = App(self)
        self.app.mainloop()
        self.app.destroy

        # GUI Close
        GUI_Close()

    def Updata(self):
        while self.running:
            with self.lock:
                self.current_time = datetime.datetime.now().strftime("Time : %H:%M:%S")
                if self.Cur_Angle_Value != self.Target_Angle_Value:
                    if self.Cur_Angle_Value < self.Target_Angle_Value:
                        self.Cur_Angle_Value += self.increment + (random.randint(Const.STEP_OFFEST_MIN, Const.STEP_OFFEST_MAX) if Const.STEP_RANDOM_ACTIVATE == True else 0)
                    else:
                        self.Cur_Angle_Value -= self.increment + (random.randint(Const.STEP_OFFEST_MIN, Const.STEP_OFFEST_MAX) if Const.STEP_RANDOM_ACTIVATE == True else 0)

                    if self.Cur_Angle_Value > Const.ANGLE_MAX: self.Cur_Angle_Value = Const.ANGLE_MAX
                    elif self.Cur_Angle_Value < Const.ANGLE_MIN: self.Cur_Angle_Value = Const.ANGLE_MIN
                    
                
            # updata_interval = [1, 0.75, 0.5, 0.25]
            # time.sleep(random.choice(updata_interval)) 

            time.sleep(random.uniform(0.75, 0.25)) 
            
            # time.sleep(0.1)       # UE 移動速度暫定不變

    def Updata_State(self):
        while self.running:
            with self.lock:
                # Max、 Mix RSRP    
                max_key = float(max(self.CaseData['Case'][str(self.Cur_Case_Value)]['RSRP'], key=float))
                min_key = float(min(self.CaseData['Case'][str(self.Cur_Case_Value)]['RSRP'], key=float))
                
                # 根據當前的 RIS CASE 以及 UE 所在角度，來計算 UE 回傳的 RSRP       # GET RSRP
                self.Cur_RSRP_Value = self.CaseDataBehind['Case'][str(self.Cur_Case_Value)]['Angle'][str(self.Cur_Angle_Value)]       # UE 回傳的 RSRP     
                self.Cur_RSRP_Value = self.Cur_RSRP_Value + self.RSRP_offest + (random.randint(Const.RSRP_OFFEST_MIN, Const.RSRP_OFFEST_MAX) if Const.RSRP_FLUCTUATING_ACTIVATE == True else 0) * random.choice([1, -1])      # RSRP 的偏差
                if (self.Cur_RSRP_Value > max_key): self.Cur_RSRP_Value = max_key
                elif (self.Cur_RSRP_Value < min_key): self.Cur_RSRP_Value = min_key
                # ================================================================================================ #
                # ================================  RIS Case 預測  =============================================== #
                # ================================================================================================ #

                def Angle_Predictor(Cur_Case_Value=None):
                    self.AngleKalman.KalmanFilter(Cur_Case_Value, "Angle")

                # ================================================================================================ #
                # ================================  RSRP 預測  =================================================== #
                # ================================================================================================ #

                def RSRP_Predictor(Cur_RSRP_Value=None):
                    self.RSRPKalman.KalmanFilter(Cur_RSRP_Value, "RSRP")

                # ================================================================================================ #
                # ================================  確認 Handover 結果是否正確  ================================== #
                # ================================================================================================ #

                # 重新切換 Case 後的下一個時刻點，檢查切換的位置是否正確
                if self.HandoverCheck == True:      
                    # 切換正確 (如果是正確的，則理應當 RSRP 要變好)
                    if self.Cur_RSRP_Value >= self.HandoverThreshold:             # 判斷是否大於 threshold 來確定是某切換角度是正確的
                        self.RSRPKalmanState = True
                        self.HandoverCheck = False

                        self.RSRPKalman = KalmanPredictor(self)         # 不論切正確與否，從新初始化    
                        RSRP_Predictor(self.Cur_RSRP_Value)
                        RSRP_Predictor(None)

                        print("(Correct)")
                        print(f"Ori : {self.AngleKalman.PredictResult}")
                        Angle_Predictor(self.Cur_Case_Value)
                        print(f"Update : {self.AngleKalman.PredictResult}")
                        Angle_Predictor(None)
                        print(f"First : {self.AngleKalman.PredictResult}")
                        # Angle_Predictor(None)
                        # print(f"Second : {self.AngleKalman.PredictResult}")

                        if(self.QueueCnt <= Const.TERMINATE_SET):
                            print(f"小於限制次數 : {self.QueueCnt}")
                            for idx, i in enumerate(range(1,self.QueueCnt+1,2)):
                                Angle_Predictor(None)
                                print(f"({idx}) : {self.AngleKalman.PredictResult}")

                            
                        self.QueueCnt = 1
                        print(f"Handover 正確!!!! (目前 RIS 角度 : {self.Cur_Case_Value}) (收到 RSRP : {self.Cur_RSRP_Value}) (真正位置為 : {self.Cur_Angle_Value})")
                        print("初始化 RSRPKalman !!!!")
                        print("=====================================================================")
                        continue

                    # 切換錯誤 (需要嘗試補救)       
                    else:
                        self.RSRPKalmanState = True
                        print(f"Handover 錯了!!!! (目前 RIS 角度 : {self.Cur_Case_Value}) (收到 RSRP : {self.Cur_RSRP_Value}) (真正位置為 : {self.Cur_Angle_Value})")
                        if self.QueueCnt > Const.TERMINATE_SET or self.QueueCnt >= len((self.SortPotentialList if Const.PREDICT_ANGLE_ACTIVATE == False else self.SortPotentialListByPredict)):
                            self.RSRPKalman = KalmanPredictor(self)         # 不論切正確與否，重新初始化
                            RSRP_Predictor(self.Cur_RSRP_Value)
                            RSRP_Predictor(None)

                            if(Const.RECOVERY_ACTIVATE == False):                               # 回頭補救機制
                                print("(Error)")
                                print(f"Ori : {self.AngleKalman.PredictResult}")
                                Angle_Predictor(self.Old_Case_Value - (self.AngleKalman.PredictResult - self.Old_Case_Value))
                                print(f"Update : {self.AngleKalman.PredictResult}")
                                Angle_Predictor(None)
                                print(f"First : {self.AngleKalman.PredictResult}")
                                Angle_Predictor(None)
                                print(f"Second : {self.AngleKalman.PredictResult}")
                                Angle_Predictor(None)
                                print(f"Third : {self.AngleKalman.PredictResult}")
                            else:                                                               # 復原機制
                                self.Cur_Case_Value = self.Old_Case_Value
                                self.AngleKalman = KalmanPredictor(self)   
                                Angle_Predictor(self.Cur_Case_Value)
                                
                                print(f"回復於原始位置 : CASE({self.Old_Case_Value})")
                            
                            self.QueueCnt = 1
                            self.HandoverCheck = False
                            print("跟丟目標")
                            print("=====================================================================")
                            continue
                        else:
                            self.Cur_Case_Value = (self.SortPotentialList[self.QueueCnt] if Const.PREDICT_ANGLE_ACTIVATE == False else self.SortPotentialListByPredict[self.QueueCnt])
                            self.QueueCnt += 1          #嘗試補救
                            print(f"(嘗試補救) 切 : {self.Cur_Case_Value}")
                            print("初始化 RSRPKalman !!!!")
                            print("=====================================================================")
                            time.sleep(Const.INTERVAL_TIME)
                            continue


                # ============================================================================================================ #
                # ================================  更新 kalman filter 、 判斷是否需要 handover  ============================== #
                # ============================================================================================================ #


                # 每次 update 就去做 RSRP kalman filter  
                if self.RSRPKalmanState == True:
                    RSRP_Predictor(self.Cur_RSRP_Value)
                    RSRP_Predictor(None)

                    if self.Check_RSRP_State == 0:
                        if self.Cur_RSRP_Value < self.HandoverThreshold:        # 訊號夠差，發現可能要切換 Case
                            self.Check_RSRP_State += 1
                            self.Check_RSRP_Sum = self.Cur_RSRP_Value

                    else:                                                       # 收集近幾筆資料，確認是否真的是要切換 Case
                        if self.Check_RSRP_State < Const.CHECK_RSRP_AVG_NUM:
                            self.Check_RSRP_State += 1
                            self.Check_RSRP_Sum += self.Cur_RSRP_Value
                        else:
                            self.Check_RSRP_State = 0
                            self.Check_RSRP_Avg = round(self.Check_RSRP_Sum/Const.CHECK_RSRP_AVG_NUM, 1)
                            print(f"RSRP_Avg({Const.CHECK_RSRP_AVG_NUM}s) : {self.Check_RSRP_Avg} / Threshold : {self.HandoverThreshold}")
                            print(f"=====================================================================")

                            if self.Check_RSRP_Avg < self.HandoverThreshold: 
                                self.RSRPKalmanState = False                        

                                # 第一次切換
                                self.Old_Case_Value = self.Cur_Case_Value
                                if self.Cur_Case_Value != 0:
                                    self.Cur_Case_Value = -self.Cur_Case_Value      # 切成反方向
                                else:
                                    self.Cur_Case_Value = 30 

                                if(self.cur_err_time != "") : self.pre_err_time = self.cur_err_time
                                self.cur_err_time = int(datetime.datetime.now().strftime("%S"))
                else:
                    if self.HandoverState == 0:
                        RSRP_Predictor(None)
                        Angle_Predictor(None)

                        # 根據 RSRP 預測值，找出有可能的正確 RIS 角度為何      
                        First_Chg_Case_PotentialList = []
                        First_Chg_Case_PotentialList = set(First_Chg_Case_PotentialList) 
                        for i in np.arange(Const.CASE_CHANGE_SIMPLED_DATA_RANGE_MIN, Const.CASE_CHANGE_SIMPLED_DATA_RANGE_MAX+Const.CASE_CHANGE_SIMPLED_DATA_RANGE_STEP, Const.CASE_CHANGE_SIMPLED_DATA_RANGE_STEP):
                            RSRP_var = self.Cur_RSRP_Value + i
                            if RSRP_var > max_key : RSRP_var = max_key
                            elif RSRP_var < min_key : RSRP_var = min_key
                            if Const.DATA_TYPE == "INT": RSRP_var = int(RSRP_var)
                            First_Chg_Case_PotentialList |= set(self.CaseData['Case'][str(self.Cur_Case_Value)]['RSRP'][str(RSRP_var)])
                        First_Chg_Case_PotentialList = list(First_Chg_Case_PotentialList) 

                        Ori_PotentialList = []           
                        Ori_PotentialList = set(Ori_PotentialList) 
                        for i in np.arange(Const.ORI_SIMPLED_DATA_RANGE_MIN, Const.ORI_SIMPLED_DATA_RANGE_MAX+Const.ORI_SIMPLED_DATA_RANGE_STEP, Const.ORI_SIMPLED_DATA_RANGE_STEP):        # Error Range                           # 手動!!!!!!
                            RSRP_var = round(self.RSRPKalman.PredictResult*2)/2 +i                            
                            if RSRP_var > max_key : RSRP_var = max_key
                            elif RSRP_var < min_key : RSRP_var = min_key
                            if Const.DATA_TYPE == "INT": RSRP_var = int(RSRP_var)
                            Ori_PotentialList |= set(self.CaseData['Case'][str(self.Old_Case_Value)]['RSRP'][str(RSRP_var)])
                        Ori_PotentialList = list(Ori_PotentialList) 

                        # 相同元素處理
                        Common_ElementList = list(set(Ori_PotentialList) & set(First_Chg_Case_PotentialList))
                        self.SortPotentialList = sorted(Common_ElementList, key=lambda x: abs(x - self.Old_Case_Value))  
                        self.SortPotentialListByPredict = sorted(Common_ElementList, key=lambda x: abs(x - self.AngleKalman.PredictResult))  
                        for index in range(len(self.SortPotentialList)):       # range 本來就會少 1
                            if index < len(self.SortPotentialList)-1:
                                if (abs(self.SortPotentialList[index]) == abs(self.SortPotentialList[index+1])) and self.SortPotentialList[index] > 0:
                                    self.SortPotentialList[index], self.SortPotentialList[index+1] = self.SortPotentialList[index+1], self.SortPotentialList[index]

                                if (abs(self.SortPotentialListByPredict[index]) == abs(self.SortPotentialListByPredict[index+1])) and self.SortPotentialListByPredict[index] > 0:
                                    self.SortPotentialListByPredict[index], self.SortPotentialListByPredict[index+1] = self.SortPotentialListByPredict[index+1], self.SortPotentialListByPredict[index]

                        # Log
                        print(f"Current Time : {self.current_time}")
                        print(f"{bcolors.HEADER}Cur UE Angle : {bcolors.ENDC}{self.Cur_Angle_Value}")
                        print(f"{bcolors.HEADER}Kalman_Angle_Value : {bcolors.ENDC}{self.AngleKalman.PredictResult}")
                        print(f"{bcolors.OKCYAN}Cur_Case_Value : {bcolors.ENDC}{self.Cur_Case_Value}")
                        print(f"{bcolors.OKCYAN}Cur_RSRP_Value : {bcolors.ENDC}{self.Cur_RSRP_Value}")
                        print(f"{bcolors.OKCYAN}First_Chg_Case_PotentialList : {bcolors.ENDC}{First_Chg_Case_PotentialList}")
                        print(f"{bcolors.OKBLUE}Old_Case_Value : {bcolors.ENDC}{self.Old_Case_Value}")
                        print(f"{bcolors.OKBLUE}Kalman_RSRP_Value : {bcolors.ENDC}{self.RSRPKalman.PredictResult}")
                        print(f"{bcolors.OKBLUE}Ori_PotentialList : {bcolors.ENDC}{Ori_PotentialList}")
                        print(f"{bcolors.WARNING}Common_ElementList : {bcolors.ENDC}{Common_ElementList}")
                        print(f"{bcolors.WARNING}Choose_Queue : {bcolors.ENDC}{self.SortPotentialList}")
                        print(f"{bcolors.WARNING}Choose_Queue_ByPredict : {bcolors.ENDC}{self.SortPotentialListByPredict}")
                        print(f"=====================================================================")

                        self.HandoverState = 0          #初始化
                        self.HandoverCheck = True
                        if( len(self.SortPotentialList if Const.PREDICT_ANGLE_ACTIVATE == False else self.SortPotentialListByPredict) != 0):
                            self.Cur_Case_Value = (self.SortPotentialList[0] if Const.PREDICT_ANGLE_ACTIVATE == False else self.SortPotentialListByPredict[0])      # 切換 Case

            time.sleep(Const.INTERVAL_TIME)
            

def ReadJsonData():
    Data_Fixed_Json_Path = Const.DATA_FILE
    with open(Data_Fixed_Json_Path, 'r') as f:
        Data_Fixed_Json = json.load(f)

    Data_Fixed_Behind_Json_Path = Const.DATA_BEHIND_FILE
    with open(Data_Fixed_Behind_Json_Path, 'r') as f:
        Data_Fixed_Behind_Json = json.load(f)

    return Data_Fixed_Json, Data_Fixed_Behind_Json
        
if __name__ == "__main__":
    game = HandOverSimulator()
    game.Start()
    print("程式已結束")
