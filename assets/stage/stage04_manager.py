from gear import Gear

def get_stage_data():
    """
    [STAGE 04] 다중 연쇄 조립: 공간 축의 연결
    - 일렬 배치가 아닌 어긋난 Y축 방향(대각선 구도)으로 배치된 톱니를 연쇄 조립합니다.
    """
    gears = []
    
    # 1. 좌측 하단 구석의 동력원 (이빨 18개, 반지름 60)
    driver_gear = Gear(x=320, y=460, radius=60, teeth=18, is_driver=True)
    driver_gear.target_speed = 0.0
    
    # 2. 중심 지지 중형 기어 (이빨 24개, 반지름 80) -> 대각선 우측 위 방향
    center_gear = Gear(x=440, y=360, radius=80, teeth=24, is_driver=False)
    
    # 3. 우측 상단 목표 기어 (이빨 16개, 반지름 55) -> 우측 위 방향
    target_gear = Gear(x=555, y=260, radius=55, teeth=16, is_driver=False)
    
    # 연쇄 동력 라인 조립 (대각선 연쇄 연결)
    driver_gear.connect(center_gear)
    center_gear.connect(target_gear)
    
    # 리스트 적재
    gears.append(driver_gear)  # Index 0
    gears.append(center_gear)  # Index 1
    gears.append(target_gear)  # Index 2
    
    # 클리어 조건: 최종 목표 기어(Index 2) 360도 회전
    clear_condition = {
        "target_index": 2,
        "required_angle": 360.0
    }
    
    return gears, clear_condition
