from gear import Gear
"""
    [STAGE 01] 기초 습득: 동력의 전파
    - 마우스로 왼쪽 큰 동력원을 붙잡고 돌려 오른쪽 목표 톱니를 360도 회전시킵니다.
"""
def get_stage_data():
    gears = []

    # 1. 동력원 (마우스 드래그 가능, 이빨 24개, 반지름 80)
    driver_gear = Gear(x=400, y=360, radius=80, teeth=24, is_driver=True)
    driver_gear.target_speed = 0.0  # 마우스 수동 조작을 위해 초기 자동 속도는 0
    
    # 2. 목표 톱니바퀴 (이빨 18개, 반지름 60)
    target_gear = Gear(x=540, y=360, radius=60, teeth=18, is_driver=False)
    
    # 3. 물리 연결 체결
    driver_gear.connect(target_gear)
    
    # 4. 리스트에 적재
    gears.append(driver_gear) # Index 0
    gears.append(target_gear) # Index 1
    
    # 클리어 조건: 인덱스 1번(목표 톱니)이 한 바퀴(360도) 이상 회전
    clear_condition = {
        "target_index": 1,
        "required_angle": 360.0
    }
    
    return gears, clear_condition
