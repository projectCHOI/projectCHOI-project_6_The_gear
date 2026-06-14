# 마우스 클릭 및 상호작용
import pygame
from gear import Gear

class PuzzleManager:
    def __init__(self):
        """퍼즐 스테이지와 톱니바퀴 그룹을 총괄 관리하는 클래스"""
        self.gears = []          # 현재 스테이지에 배치된 모든 톱니바퀴 리스트
        self.current_level = 1   # 현재 진행 중인 스테이지 번호
        self.is_cleared = False   # 현재 스테이지 클리어 여부
        
        # 첫 번째 스테이지 초기화
        self.load_level(self.current_level)

    def load_level(self, level_num):
        """지정한 레벨의 톱니바퀴 배치 데이터와 클리어 조건을 불러오는 함수"""
        self.gears.clear()
        self.is_cleared = False
        self.current_level = level_num

        if level_num == 1:
            # [레벨 1: 우물 속의 열쇠 (테스트 배치)]
            # 1. 플레이어가 마우스로 돌릴 메인 동력원 톱니바퀴 (Driver)
            driver_gear = Gear(x=300, y=360, radius=80, teeth=24, is_driver=True)
            # 임시 테스트용 속도 부여 (나중에 마우스 드래그로 제어)
            driver_gear.target_speed = 45.0  # 초당 45도 회전
            
            # 2. 동력을 전달받아 최종 목적지 기믹을 움직일 종속 톱니바퀴 (Follower)
            target_gear = Gear(x=450, y=360, radius=60, teeth=18, is_driver=False)
            
            # 3. 두 톱니바퀴를 물리적으로 맞물림 (연결)
            driver_gear.connect(target_gear)
            
            # 리스트에 등록
            self.gears.append(driver_gear)
            self.gears.append(target_gear)
            
            print(f"Level {level_num} loaded: 우물 속의 열쇠 구조 생성 완료.")
            
        elif level_num == 2:
            # TODO: 레벨 2 복합 톱니바퀴 및 도르래 기믹 배치 예정
            pass

    def update(self, dt):
        """스테이지 내 모든 톱니바퀴의 물리 회전 연산 및 클리어 조건 판정"""
        if not self.gears:
            return

        # 1. 동력원(Driver)을 기점으로 연쇄 회전 연산 실행 (DFS 그래프 탐색)
        # 리스트 내의 동력원 톱니바퀴를 찾아 회전 업데이트를 시작합니다.
        for gear in self.gears:
            if gear.is_driver:
                gear.update_rotation(dt)
                break  # 하나의 동력원 계통 처리 후 탈출

        # 2. 스테이지 클리어 조건 체크
        self.check_clear_condition()

    def check_clear_condition(self):
        """최종 목적지 톱니바퀴가 특정 조건(예: 특정 각도 도달)을 만족했는지 판정"""
        if self.current_level == 1 and len(self.gears) >= 2:
            target_gear = self.gears[1]  # 두 번째 종속 톱니바퀴
            
            # 예시 조건: 종속 톱니바퀴가 한 바퀴(360도) 이상 회전했을 때 클리어
            if abs(target_gear.angle) >= 360.0:
                if not self.is_cleared:
                    self.is_cleared = True
                    print("🎉 Level 1 Cleared! 우물에서 열쇠가 든 상자가 완전히 올라왔습니다.")

    def draw(self, screen):
        """스테이지 내의 모든 톱니바퀴 객체들을 화면에 렌더링"""
        for gear in self.gears:
            gear.draw(screen)
            
        # 스테이지가 클리어되었다면 화면에 임시 안내 텍스트 출력 규칙 마련
        if self.is_cleared:
            # 나중에 서평원 꺾깎체 폰트 렌더링으로 대체될 영역
            pass