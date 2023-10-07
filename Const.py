# =====================================================
# CASE 1
# DATA_FILE = "./Data/CurveData.json"                    
# DATA_BEHIND_FILE = "./Data/CurveData.json"

# CASE 2
DATA_FILE = "./Data/CurveData_F1.json"                     # "./Data/CurveData_F10.json"
DATA_BEHIND_FILE = "./Data/CurveData_F1.json"

# CASE 3
# DATA_FILE = "./Data/CurveData_F10.json"                     # "./Data/CurveData_F10.json"
# DATA_BEHIND_FILE = "./Data/CurveData_F1.json"

# TEST
# DATA_FILE = "./Data/Data.json"                     # "./Data/CurveData_F10.json"
# DATA_BEHIND_FILE = "./Data/Data.json"

# =====================================================
# HANDOVER PARAMETERS
INTERVAL_TIME=0.25

# HANDOVER_THRESHOLD=-108             # -105~-125
# HANDOVER_THRESHOLD=-110             # -105~-125
# HANDOVER_THRESHOLD=-115             # -105~-125

HANDOVER_THRESHOLD=-112             # -105~-125
THRESHOLD_OFFEST = -6

# Data Info
ANGLE_MIN=-60
ANGLE_MAX=60

# RSRP Data Range (every time handover)
DATA_TYPE = "FLOAT"

ORI_SIMPLED_DATA_RANGE_MIN=-8
ORI_SIMPLED_DATA_RANGE_MAX=8
ORI_SIMPLED_DATA_RANGE_STEP=1

CASE_CHANGE_SIMPLED_DATA_RANGE_MIN=-4                           # 當  CASE 數量少時，給的範圍就要大，需要涵蓋較大範圍，才能彌補 CASE 之間的空缺
CASE_CHANGE_SIMPLED_DATA_RANGE_MAX=4
CASE_CHANGE_SIMPLED_DATA_RANGE_STEP=1

# misassessment
MISASSESSMENT_RANGE_MIN = -0
MISASSESSMENT_RANGE_MAX = 0


# =====================================================
# 補救次數
TERMINATE_SET = 6       # 2 6


# =====================================================
# 使用 ANGLE predictor 的資料來做 "優先順序判斷條件"            # 預設使用 "最後所在 ANGLE" 做 "優先順序判斷條件"
PREDICT_ANGLE_ACTIVATE = True   # True    False


# =====================================================
# RSRP "偏移" 浮動
RSRP_FLUCTUATING_ACTIVATE = True        # True    False

# RSPR OFFEST PARAMETERS
RSRP_OFFEST_BASE=0
RSRP_OFFEST_MIN=0
RSRP_OFFEST_MAX=4


# =====================================================
# UE 移動 "速度"、距離" 浮動
STEP_RANDOM_ACTIVATE = False     # True    False

# UE MOVE OFFEST PARAMETERS
STEP_OFFEST_BASE=1
STEP_OFFEST_MIN=6
STEP_OFFEST_MAX=8


# =====================================================
# 當 kalman filter 預測失敗的補救措施
RECOVERY_ACTIVATE = False     # True    False

# =====================================================
# 當 RSRP 訊號變差，再多收集 n 筆資料
CHECK_RSRP_AVG_NUM = 5



