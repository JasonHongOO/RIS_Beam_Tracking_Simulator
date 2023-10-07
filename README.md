# RIS_Beam_Tracking_Simulator

根據專題目標實作了一個簡易的模擬器，並提供GUI，以在沒有整個基站架構及RIS的狀況下，展示專題的成果。

# GUI

![image](https://github.com/JasonHongOO/RIS_Beam_Tracking_Simulator/blob/main/Image/1.PNG)

參數說明

- **Target Angle :** 指定 UE 移動到相對於 RIS 的目標角度，可在上方輸入欄中輸入數值，並按下右邊的 Input Angle 按鈕，以改變 Target Angle 的數值

- **Current Angle :**  模擬 UE 當前相對於 RIS 的角度，此數值會逐漸向 Target Angle 移動

- **Current Case :** 模擬當前 RIS 的反射角度

- **Current RSRP :** 模擬基站接收到 UE 回傳的 RSRP，該數值會由 Current Case 所對應到的輻射場型上找到理論上此時UE應該要接收到的RSRP，接著再加上一個隨機數，模擬接收到的 RSRP 數值會浮動這件事

- **Cur Angle Prediction :** 當前 Kalman Filter 預測 UE 相對於 RIS 的角度位置

- **Pre Angle Prediction :** 前一筆 Cur Angle Prediction 的數值

- **Cur RSRP Prediction :** 當前 Kalman Filter 預測 RSRP 的數值

- **Pre RSRP Prediction :** 前一筆 Cur RSRP Prediction 的數值



# 執行說明

為了維持UE的訊號品質，所以目標會是希望讓 RIS 的反射角度能夠追著 UE 移動，而對應到程式中的參數就會是希望 Current Case 的數值要能在 Current Angle 的附近，以使基站接收到 UE 回傳的訊號報告中的 RSRP 能夠維持相對較高的數值。
