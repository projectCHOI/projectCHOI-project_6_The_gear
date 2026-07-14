from gear import Gear

def get_stage_data():
    """
    [STAGE 02] 응용 기어비: 크기와 회전비
    - 큰 동력원의 회전력이 작은 징검다리 톱니를 거쳐 목표물로 전달되며 회전 속도가 증폭됩니다.
    """
    gears = []
    
    # 1. 대형 동력원 (이빨 32개, 반지름 100)
    driver_gear = Gear(x=350, y=360, radius=100, teeth=32, is_driver=True)
    driver_gear.target_speed = 0.0
    
    # 2. 초소형 징검다리 톱니바퀴 (이빨 8개, 반지름 30) - 회전력을 급격히 변환
    bridge_gear = Gear(x=480, y=360, radius=30, teeth=8, is_driver=False)
    
    # 3. 중형 목표 톱니바퀴 (이빨 16개, 반지름 55)
    target_gear = Gear(x=565, y=360, radius=55, teeth=16, is_driver=False)
    
    # 4. 연쇄 동력 전달선 구축 (동력원 -> 징검다리 -> 목표물)
    driver_gear.connect(bridge_gear)
    bridge_gear.connect(target_gear)
    
    # 5. 리스트 적재 (순서대로 인덱싱됨)
    gears.append(driver_gear) # Index 0
    gears.append(bridge_gear) # Index 1
    gears.append(target_gear) # Index 2
    
    # 클리어 조건: 인덱스 2번(최종 목표 톱니)이 한 바퀴(360도) 이상 회전
    clear_condition = {
        "target_index": 2,
        "required_angle": 360.0
    }
    
    return gears, clear_condition