import os
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from PIL import Image
import customtkinter

import Const

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
class App(customtkinter.CTk):
    def __init__(self, InteractiveComponent):
        super().__init__()
        self.ParentComponent = InteractiveComponent

        # ===============  Variable  ===============
        self.resizable_frame_visible = False
        self.UpdataState = 0    # 0 update, 1 arrival 

        # ===============  Image  ===============
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Image")
        self.Menu_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "White/menu.png")),
                                                dark_image=Image.open(os.path.join(image_path, "White/menu.png")), size=(20, 20))

        # ===============  Main Frame  ===============
        self.title("Jason Hong Simulator")
        self.geometry(f"{800}x{580}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.MainFrame = customtkinter.CTkFrame(self, corner_radius=0)
        self.MainFrame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.MainFrame.grid_columnconfigure(0, weight=1)
        self.MainFrame.grid_rowconfigure((1), weight=1)

        # Input Entry
        self.InputFrame = customtkinter.CTkFrame(self.MainFrame)
        self.InputFrame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.InputFrame.grid_columnconfigure((0,1), weight=1)
        self.InputFrame.grid_columnconfigure((2), weight=0)
        self.InputFrame.grid_rowconfigure((0), weight=1)

        self.InputEntry = customtkinter.CTkEntry(self.InputFrame, placeholder_text="Input Degree")
        self.InputEntry.grid(row=0, column=0, columnspan=2, padx=10, pady=15, sticky="nsew")

        self.InputConfrimBtn = customtkinter.CTkButton(master=self.InputFrame, border_width=2, text="Input Angle", command=lambda: self.Confirm_event("Input Angle"))
        self.InputConfrimBtn.grid(row=0, column=2, padx=10, pady=15, sticky="nsew")

        self.LogBtn = customtkinter.CTkButton(master=self.InputFrame, border_width=2, text="Log", image=self.Menu_image, compound="left",  command=lambda: self.Log_Frame_event("Log Frame"))
        self.LogBtn.grid(row=0, column=3, padx=10, pady=15, sticky="nsew")

        # ===============  Body Frame  ===============
        self.BodyFrame = customtkinter.CTkFrame(self.MainFrame, corner_radius=0)
        self.BodyFrame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.BodyFrame.grid_columnconfigure((0,1), weight=1)
        self.BodyFrame.grid_rowconfigure((0), weight=1)

        # ===============  Left Frame  ===============
        self.LeftFrame = customtkinter.CTkFrame(self.BodyFrame, corner_radius=0)
        self.LeftFrame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.LeftFrame.grid_columnconfigure(0, weight=1)
        self.LeftFrame.grid_rowconfigure((1,2,3,4), weight=1)

        # Target Angle
        self.TargetAngleFrame = customtkinter.CTkFrame(self.LeftFrame, corner_radius=0)
        self.TargetAngleFrame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.TargetAngleFrame.grid_columnconfigure(0, weight=1)
        self.TargetAngleFrame.grid_rowconfigure(0, weight=1)

        self.TargetAngleLabel = customtkinter.CTkLabel(self.TargetAngleFrame, text="Target Angle : None", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.TargetAngleLabel.grid(row=0, column=0, padx=(0,0), pady=10, sticky="nsew")

        # Currnt Angle
        self.CurAngleFrame = customtkinter.CTkFrame(self.LeftFrame, corner_radius=0)
        self.CurAngleFrame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.CurAngleFrame.grid_columnconfigure(0, weight=1)
        self.CurAngleFrame.grid_rowconfigure(0, weight=1)

        self.CurAngleLabel = customtkinter.CTkLabel(self.CurAngleFrame, text="Current Angle : None", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.CurAngleLabel.grid(row=0, column=0, padx=(0,0), pady=10, sticky="nsew")

        # Currnt Case
        self.CurCaseFrame = customtkinter.CTkFrame(self.LeftFrame, corner_radius=0)
        self.CurCaseFrame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.CurCaseFrame.grid_columnconfigure(0, weight=1)
        self.CurCaseFrame.grid_rowconfigure(0, weight=1)

        self.CurCaseLabel = customtkinter.CTkLabel(self.CurCaseFrame, text="Current Case : None", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.CurCaseLabel.grid(row=0, column=0, padx=(0,0), pady=10, sticky="nsew")

        # Currnt RSRP
        self.RSRPFrame = customtkinter.CTkFrame(self.LeftFrame, corner_radius=0)
        self.RSRPFrame.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.RSRPFrame.grid_columnconfigure(0, weight=1)
        self.RSRPFrame.grid_rowconfigure(0, weight=1)

        self.RSRPLabel = customtkinter.CTkLabel(self.RSRPFrame, text="Cur RSRP (case 0) : None", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.RSRPLabel.grid(row=0, column=0, padx=(0,0), pady=10, sticky="nsew")

        # ===============  Right Frame  ===============
        self.RightFrame = customtkinter.CTkFrame(self.BodyFrame, corner_radius=0)
        self.RightFrame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.RightFrame.grid_columnconfigure(0, weight=1)
        self.RightFrame.grid_rowconfigure((1,2,4,5), weight=1)

        # Predict Angle Label
        self.PredictRSRPLabel = customtkinter.CTkLabel(self.RightFrame, text="Predict Angle : ", font=customtkinter.CTkFont(size=10, weight="bold"))
        self.PredictRSRPLabel.grid(row=0, column=0, padx=(0,0), pady=(2,0), sticky="ew")

        # Predict Angle (Cur)
        self.PredictCurAngleFrame = customtkinter.CTkFrame(self.RightFrame, corner_radius=0)
        self.PredictCurAngleFrame.grid(row=1, column=0, padx=5, pady=(0,5), sticky="nsew")
        self.PredictCurAngleFrame.grid_columnconfigure(0, weight=1)
        self.PredictCurAngleFrame.grid_rowconfigure(0, weight=1)

        self.PredictCurAngleLabel = customtkinter.CTkLabel(self.PredictCurAngleFrame, text="Predict Cur Angle : None", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.PredictCurAngleLabel.grid(row=0, column=0, padx=(0,0), pady=10, sticky="nsew")

        # Predict Angle (Recent)
        self.PredictPreAngleFrame = customtkinter.CTkFrame(self.RightFrame, corner_radius=0)
        self.PredictPreAngleFrame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.PredictPreAngleFrame.grid_columnconfigure(0, weight=1)
        self.PredictPreAngleFrame.grid_rowconfigure(0, weight=1)

        self.PredictPreAngleLabel = customtkinter.CTkLabel(self.PredictPreAngleFrame, text="Predict Pre Angle : None", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.PredictPreAngleLabel.grid(row=0, column=0, padx=(0,0), pady=10, sticky="nsew")

        # Predict RSRP Label
        self.PredictRSRPLabel = customtkinter.CTkLabel(self.RightFrame, text="Predict RSRP : ", font=customtkinter.CTkFont(size=10, weight="bold"))
        self.PredictRSRPLabel.grid(row=3, column=0, padx=(0,0), pady=(2,0), sticky="ew")

        # Predict RSRP (Cur)
        self.PredictCurRSRPFrame = customtkinter.CTkFrame(self.RightFrame, corner_radius=0)
        self.PredictCurRSRPFrame.grid(row=4, column=0, padx=5, pady=(0,5), sticky="nsew")
        self.PredictCurRSRPFrame.grid_columnconfigure(0, weight=1)
        self.PredictCurRSRPFrame.grid_rowconfigure(0, weight=1)

        self.PredictCurRSRPLabel = customtkinter.CTkLabel(self.PredictCurRSRPFrame, text="Predict Cur RSRP : None", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.PredictCurRSRPLabel.grid(row=0, column=0, padx=(0,0), pady=10, sticky="nsew")

        # Predict RSRP (Recent)
        self.PredictPreRSRPFrame = customtkinter.CTkFrame(self.RightFrame, corner_radius=0)
        self.PredictPreRSRPFrame.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        self.PredictPreRSRPFrame.grid_columnconfigure(0, weight=1)
        self.PredictPreRSRPFrame.grid_rowconfigure(0, weight=1)

        self.PredictPreRSRPLabel = customtkinter.CTkLabel(self.PredictPreRSRPFrame, text="Predict Pre RSRP : None", font=customtkinter.CTkFont(size=25, weight="bold"))
        self.PredictPreRSRPLabel.grid(row=0, column=0, padx=(0,0), pady=10, sticky="nsew")


        # ===============  Resize Component  ===============
        self.resizable_frame = customtkinter.CTkFrame(self, corner_radius=0, width=300)
        # self.resizable_frame.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="nswe")
        self.resizable_frame.grid_columnconfigure(0, weight=1)
        self.resizable_frame.grid_rowconfigure(0, weight=1)

        # Tab
        self.tabview = customtkinter.CTkTabview(self.resizable_frame) #,height=10
        self.tabview.grid(row=0, column=0, sticky="nsew")
        self.tabview.add("Charts")
        self.tabview.add("Charts(BG)")
        self.tabview.add("Angle")
        self.tabview.add("Handover")
        self.tabview.add("Predict(A)")
        self.tabview.add("Predict(R)")

        self.tabview.tab("Charts").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Charts(BG)").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Angle").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Handover").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Predict(A)").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Predict(R)").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Charts").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Charts(BG)").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Angle").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Handover").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Predict(A)").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Predict(R)").grid_rowconfigure(0, weight=1)


        
        # Charts
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tabview.tab("Charts"))  
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tabview.tab("Charts"), pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        x_data = []
        y_data = [] 
        case = self.ParentComponent.Cur_Case_Value
        for ele in self.ParentComponent.CaseData['Case'][str(case)]['Angle']:
            x_data.append(int(ele))
            y_data.append(self.ParentComponent.CaseData['Case'][str(case)]['Angle'][ele])
        RSRP_var = self.ParentComponent.CaseData["Case"][str(case)]["Angle"]["0"]
        x_array = np.array(self.ParentComponent.CaseData["Case"][str(case)]["RSRP"][str(RSRP_var)])
        y_array = np.ones((len(x_array))) * float(RSRP_var)
        self.ax.plot(x_data, y_data, color='#87cefa', label='Sampled Data')
        self.ax.plot(x_data, y_data, color='#ff8c00', marker='o', label='Sampled Data', linestyle='', markersize=6)
        self.ax.plot(x_array, y_array, color='#ff00ff', marker='o', label='Sampled Data', linestyle='', markersize=6)
        self.canvas.draw()

        # Charts
        self.fig_BG, self.ax_BG = plt.subplots()
        self.canvas_BG = FigureCanvasTkAgg(self.fig_BG, master=self.tabview.tab("Charts(BG)"))  
        self.canvas_BG.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.toolbar_BG = NavigationToolbar2Tk(self.canvas_BG, self.tabview.tab("Charts(BG)"), pack_toolbar=False)
        self.toolbar_BG.update()
        self.toolbar_BG.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        x_data = []
        y_data = [] 
        case = self.ParentComponent.Cur_Case_Value
        for ele in self.ParentComponent.CaseDataBehind['Case'][str(case)]['Angle']:
            x_data.append(int(ele))
            y_data.append(self.ParentComponent.CaseDataBehind['Case'][str(case)]['Angle'][ele])
        RSRP_var = self.ParentComponent.CaseDataBehind["Case"][str(case)]["Angle"]["0"]
        x_array = np.array(self.ParentComponent.CaseDataBehind["Case"][str(case)]["RSRP"][str(RSRP_var)])
        y_array = np.ones((len(x_array))) * float(RSRP_var)
        self.ax_BG.plot(x_data, y_data, color='#87cefa', label='Sampled Data')
        self.ax_BG.plot(x_data, y_data, color='#ff8c00', marker='o', label='Sampled Data', linestyle='', markersize=6)
        self.ax_BG.plot(x_array, y_array, color='#ff00ff', marker='o', label='Sampled Data', linestyle='', markersize=6)
        self.canvas_BG.draw()

        # AngleLogFrame
        self.AngleLogFrame = customtkinter.CTkTextbox(self.tabview.tab("Angle"), font=customtkinter.CTkFont(size=18, weight="bold"), width=400, height=300)   
        self.AngleLogFrame.grid(row=0, column=0, sticky="nswe")
        # HandoverLogFrame
        self.HandoverLogFrame = customtkinter.CTkTextbox(self.tabview.tab("Handover"), font=customtkinter.CTkFont(size=18, weight="bold"), width=400, height=300)   
        self.HandoverLogFrame.grid(row=0, column=0, sticky="nswe")
        # PredictAngleLogFrame
        self.PredictAngleLogFrame = customtkinter.CTkTextbox(self.tabview.tab("Predict(A)"), font=customtkinter.CTkFont(size=18, weight="bold"), width=400, height=300)   
        self.PredictAngleLogFrame.grid(row=0, column=0, sticky="nswe")
        # PredictRSRPLogFrame
        self.PredictRSRPLogFrame = customtkinter.CTkTextbox(self.tabview.tab("Predict(R)"), font=customtkinter.CTkFont(size=18, weight="bold"), width=400, height=300)   
        self.PredictRSRPLogFrame.grid(row=0, column=0, sticky="nswe")

        # ===============  Update Event  ===============
        self.Updata()

    def Log_Frame_event(self, Event):
        def create_resizable_frame(self):
            # Main(Root) Frame Layout
            self.grid_columnconfigure((0,1), weight=1)
            self.geometry(f"{1400}x{580}")

            # Visable
            self.resizable_frame.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="nswe")

            # Variable Setting
            self.resizable_frame_visible = True

        def remove_resizable_frame(self):
            #Unvisable
            self.resizable_frame.grid_forget()
            
            # Main(Root) Frame Layout
            self.grid_columnconfigure(1, weight=0)
            self.geometry(f"{1000}x{580}")

            # Variable Setting
            self.resizable_frame_visible = False

        print(f"Log Bnt Clicked : {Event}")
        if not self.resizable_frame_visible:
            create_resizable_frame(self)
            self.resizable_frame_visible = True
        else:
            remove_resizable_frame(self)
            self.resizable_frame_visible = False

    def Confirm_event(self, Event):
        print(f"Confirm Input Bnt Clicked : {Event}")
        
        try:
            #檢查程式是否退出
            input_value = self.InputEntry.get()
            if(input_value == "exit"):
                self.running = False
                self.CurAngleLabel.configure(text=f"Process Exit")
                self.TargetAngleLabel.configure(text=f"Process Exit")

            # is number check
            int(self.InputEntry.get())

            # main process
            with self.ParentComponent.lock:
                self.ParentComponent.Target_Angle_Value = int(self.InputEntry.get())
        except Exception as e:
            print(f"Input Error : Is Not Number ({e})")
        
        self.TargetAngleLabel.configure(text=f"Target Angle : {self.ParentComponent.Target_Angle_Value}")

    def Updata(self):       # timer ?
        def Basic_GUI_Setting():
            self.CurAngleLabel.configure(text=f"Current Angle : {self.ParentComponent.Cur_Angle_Value}")
            self.PredictCurAngleLabel.configure(text=f"Predict Cur Angle : {self.ParentComponent.AngleKalman.PredictResult}")
            self.PredictPreAngleLabel.configure(text=f"Predict Pre Angle : {self.ParentComponent.AngleKalman.PrePredictResult}")
            self.RSRPLabel.configure(text=f"Cur RSRP : {self.ParentComponent.Cur_RSRP_Value}")
            self.PredictCurRSRPLabel.configure(text=f"Predict Cur RSRP : {self.ParentComponent.RSRPKalman.PredictResult:<10}")
            self.PredictPreRSRPLabel.configure(text=f"Predict Pre RSRP : {self.ParentComponent.RSRPKalman.PrePredictResult:<10}")
            self.CurCaseLabel.configure(text=f"Current Case : {self.ParentComponent.Cur_Case_Value}")

        def Angle_TextBox():    
            if(self.ParentComponent.Cur_Angle_Value == self.ParentComponent.Target_Angle_Value and self.UpdataState == 0):
                self.AngleLogFrame.insert('end', f"{self.ParentComponent.current_time},    (Arrival) Current Angle : {self.ParentComponent.Cur_Angle_Value}\n")
                self.UpdataState = 1    # At the moment of reaching the target Angle (on)
            else:    # Whenever the Angle value is updated
                self.AngleLogFrame.insert('end', f"{self.ParentComponent.current_time},    (Update) Current Angle : {self.ParentComponent.Cur_Angle_Value}\n")
                if(self.ParentComponent.Cur_Angle_Value != self.ParentComponent.Target_Angle_Value): self.UpdataState = 0    
            self.AngleLogFrame.see('end')      # 頁面滑到底 (滑鼠滾輪滑到底)

        def Handover_TextBox():    
            # Handover TextBox
            self.HandoverLogFrame.insert('end', f"{self.ParentComponent.current_time}\n")
            if(self.ParentComponent.Cur_RSRP_Value < self.ParentComponent.HandoverThreshold):
                PotentialList = self.ParentComponent.CaseData['Case'][str(self.ParentComponent.Cur_Case_Value)]['RSRP'][str(self.ParentComponent.Cur_RSRP_Value)]
                SortPotentialList = sorted(PotentialList, key=lambda x: abs(x - self.ParentComponent.Cur_Case_Value))                   # 收到 RSRP 去找出可能的 CASE

                for ele in SortPotentialList:                  # 如何判別角度是否正確
                    if(self.ParentComponent.CaseDataBehind['Case'][str(ele)]['Angle'][str(self.ParentComponent.Cur_Angle_Value)] > self.ParentComponent.HandoverThreshold):           # RIS Case 調整後，對於當前 UE 所在角度所回傳的 RSRP 有沒有變好
                        if(ele == self.ParentComponent.Cur_Angle_Value):
                            self.HandoverLogFrame.insert('end', f"需切換到 {ele} ，且是正確的角度\n")
                            # self.ParentComponent.Cur_Case_Value = ele                   # 切換 Case
                            break
                        else: self.HandoverLogFrame.insert('end', f"需切換到 {ele} ，但並非是 UE 所在的角度\n")

                #實際上在切換角度時，UE 也在移動，也就是第一次切換時

            else: self.HandoverLogFrame.insert('end', f"現在訊號足夠好不用切換 : {self.ParentComponent.Cur_Case_Value}\n")
            self.HandoverLogFrame.insert('end', f"=====================================\n")
            # self.HandoverLogFrame.see('end')      # 頁面滑到底 (滑鼠滾輪滑到底)


        def Predict_TextBox():   
            # Predict TextBox(Angle)
            self.PredictAngleLogFrame.insert('end', f"{self.ParentComponent.current_time}\n")
            self.PredictAngleLogFrame.insert('end', f"Cur Angle : {self.ParentComponent.Cur_Angle_Value}\n")
            self.PredictAngleLogFrame.insert('end', f"Predict Cur Angle : {self.ParentComponent.AngleKalman.PredictResult}\n")
            self.PredictAngleLogFrame.insert('end', f"Predict Pre Angle : {self.ParentComponent.AngleKalman.PrePredictResult}\n")
            self.PredictAngleLogFrame.insert('end', f"=====================================\n")
            # self.PredictAngleLogFrame.see('end')      # 頁面滑到底 (滑鼠滾輪滑到底)

            # Predict TextBox(RSRP)
            self.PredictRSRPLogFrame.insert('end', f"{self.ParentComponent.current_time}\n")
            self.PredictRSRPLogFrame.insert('end', f"Cur RSRP : {self.ParentComponent.Cur_RSRP_Value}\n")
            self.PredictRSRPLogFrame.insert('end', f"Predict Cur RSRP : {self.ParentComponent.RSRPKalman.PredictResult}\n")
            self.PredictRSRPLogFrame.insert('end', f"Predict Pre RSRP : {self.ParentComponent.RSRPKalman.PrePredictResult}\n")
            self.PredictRSRPLogFrame.insert('end', f"=====================================\n")
            # self.PredictRSRPLogFrame.see('end')      # 頁面滑到底 (滑鼠滾輪滑到底)
        
        def Chart():
            self.ax.clear()
            x_data = []
            y_data = [] 
            case = self.ParentComponent.Cur_Case_Value
            for ele in self.ParentComponent.CaseData['Case'][str(case)]['Angle']:
                x_data.append(int(ele))
                y_data.append(self.ParentComponent.CaseData['Case'][str(case)]['Angle'][ele])
            RSRP_var = self.ParentComponent.CaseData["Case"][str(case)]["Angle"][str(case)]
            x_array = np.array(self.ParentComponent.CaseData["Case"][str(case)]["RSRP"][str(RSRP_var)])
            y_array = np.ones((len(x_array))) * float(RSRP_var)
            self.ax.plot(x_data, y_data, color='#87cefa', label='Sampled Data')
            self.ax.plot(x_data, y_data, color='#ff8c00', marker='o', label='Sampled Data', linestyle='', markersize=6)
            self.ax.plot(x_array, y_array, color='#ff00ff', marker='o', label='Sampled Data', linestyle='', markersize=6)
            self.canvas.draw()

        # function
        Basic_GUI_Setting()
        Angle_TextBox()
        Handover_TextBox()
        Predict_TextBox()
        Chart()
        self.after(int(Const.INTERVAL_TIME*1000), self.Updata) 

