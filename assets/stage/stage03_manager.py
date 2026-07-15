from gear import Gear

def get_stage_data():
    """
    [STAGE 03] 방향성의 역전: 아이들러 기어 (Idler Gear)
    - 4개의 연쇄적인 맞물림을 통해 회전 방향이 어떻게 역전되는지 몸소 체험하는 단계입니다.
    """
    gears = []
    
    # 1. 좌측 대형 동력원 (이빨 24개, 반지름 80)
    driver_gear = Gear(x=320, y=360, radius=80, teeth=24, is_driver=True)
    driver_gear.target_speed = 0.0
    
    # 2. 첫 번째 중간 기어 (이빨 12개, 반지름 45) -> 역회전
    mid_gear_1 = Gear(x=445, y=360, radius=45, teeth=12, is_driver=False)
    
    # 3. 두 번째 중간 기어 (이빨 18개, 반지름 60) -> 정회전
    mid_gear_2 = Gear(x=550, y=360, radius=60, teeth=18, is_driver=False)
    
    # 4. 우측 목표 기어 (이빨 12개, 반지름 45) -> 최종 역회전
    target_gear = Gear(x=655, y=360, radius=45, teeth=12, is_driver=False)
    
    # 연쇄 동력 라인 조립
    driver_gear.connect(mid_gear_1)
    mid_gear_1.connect(mid_gear_2)
    mid_gear_2.connect(target_gear)
    
    # 리스트 적재
    gears.append(driver_gear)  # Index 0
    gears.append(mid_gear_1)  # Index 1
    gears.append(mid_gear_2)  # Index 2
    gears.append(target_gear)  # Index 3
    
    # 클리어 조건: 최종 목표 기어(Index 3)가 역방향/정방향 상관없이 1바퀴 회전
    clear_condition = {
        "target_index": 3,
        "required_angle": 360.0
    }
    
    return gears, clear_condition
