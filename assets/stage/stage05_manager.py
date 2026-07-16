from gear import Gear

def get_stage_data():
    """
    [STAGE 05] 메커니컬 가젯: 동력의 분기
    - 하나의 중앙 동력원을 돌려 상단과 하단의 서로 다른 타겟 톱니를 동시에 가동시킵니다.
    """
    gears = []
    
    # 1. 화면 정중앙의 초대형 동력원 (이빨 36개, 반지름 110)
    center_driver = Gear(x=480, y=360, radius=110, teeth=36, is_driver=True)
    center_driver.target_speed = 0.0
    
    # 2. [상단 분기선] 상단 징검다리 기어 (이빨 12개, 반지름 40) -> 위쪽 방향 배치
    top_bridge = Gear(x=480, y=220, radius=40, teeth=12, is_driver=False)
    
    # 3. [상단 최종 목표] 상단 대형 타겟 기어 (이빨 24개, 반지름 80)
    top_target = Gear(x=480, y=100, radius=80, teeth=24, is_driver=False)
    
    # 4. [하단 분기선] 하단 징검다리 기어 (이빨 18개, 반지름 60) -> 아래쪽 방향 배치
    bottom_bridge = Gear(x=480, y=520, radius=60, teeth=18, is_driver=False)
    
    # 5. [하단 최종 목표] 하단 중형 타겟 기어 (이빨 12개, 반지름 45)
    bottom_target = Gear(x=480, y=625, radius=45, teeth=12, is_driver=False)
    
    # 중앙 동력원에서 양 갈래로 동력 뻗쳐 나가기
    center_driver.connect(top_bridge)
    top_bridge.connect(top_target)
    
    center_driver.connect(bottom_bridge)
    bottom_bridge.connect(bottom_target)
    
    # 리스트 적재 (중앙 -> 상단라인 -> 하단라인 순)
    gears.append(center_driver)  # Index 0
    gears.append(top_bridge)     # Index 1
    gears.append(top_target)     # Index 2 (상단 타겟)
    gears.append(bottom_bridge)  # Index 3
    gears.append(bottom_target)  # Index 4 (하단 타겟)
    
    # 최종 마스터 스테이지 클리어 조건: 상단 최종 목표(Index 2)가 한 바퀴(360도) 이상 회전
    clear_condition = {
        "target_index": 2,
        "required_angle": 360.0
    }
    
    return gears, clear_condition
