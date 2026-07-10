from gear import Gear

def get_stage_data():
    """1스테이지의 톱니바퀴 배치 데이터와 클리어 목표 각도를 반환하는 함수"""
    gears = []
    
    # 톱니바퀴 생성 및 연결
    driver_gear = Gear(x=300, y=360, radius=80, teeth=24, is_driver=True)
    driver_gear.target_speed = 45.0  
    
    target_gear = Gear(x=450, y=360, radius=60, teeth=18, is_driver=False)
    driver_gear.connect(target_gear)
    
    gears.append(driver_gear)
    gears.append(target_gear)
    
    # 클리어 조건 데이터 설정 (목표 톱니바퀴 인덱스, 목표 회전 각도)
    clear_condition = {
        "target_index": 1,
        "required_angle": 360.0
    }
    
    return gears, clear_condition
