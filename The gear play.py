import pygame
import sys
import os

from assets.stage.puzzle import PuzzleManager
from assets.player.player_manager import PlayerManager
from assets.sounds.sound_manager import SoundManager
from assets.music.music_manager import MusicManager

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Gear : The Puzzler")

clock = pygame.time.Clock()
FPS = 60
COLOR_BG = (30, 30, 35)
COLOR_TEXT = (220, 220, 220)

def main():
    puzzle_manager = PuzzleManager()
    player_manager = PlayerManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    sound_manager = SoundManager()
    music_manager = MusicManager()
    
    sound_manager.play_bgm("main")
    clear_sound_played = False
    font = pygame.font.SysFont("malgungothic", 28)
    sub_font = pygame.font.SysFont("malgungothic", 20)
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0 
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and puzzle_manager.is_cleared:
                    next_level = puzzle_manager.current_level + 1
                    if next_level <= 5:
                        puzzle_manager.load_level(next_level)
                        clear_sound_played = False
                        sound_manager.play_bgm("main") 
                    else:
                        print("전체 캠페인 완수!")
            
            # 마우스 제어 감시 규칙 명형 분기
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # A. 톱니바퀴 연동 조작 시도 (상자가 닫혀있을 때만)
                if not puzzle_manager.is_box_open:
                    player_manager.handle_event(event, puzzle_manager.gears)
                    if player_manager.is_dragging:
                        music_manager.play_install_sound()
                
                # B. 서사 아이템 월드 클릭 스캔 연동
                interaction = puzzle_manager.handle_clicks(event.pos)
                if interaction == "get_key":
                    # 열쇠를 주우면 가방 데이터에 박아 넣고 효과음 믹싱 가능
                    player_manager.gain_gear_to_inventory("key_item", 1)
                    music_manager.play_install_sound() 
                elif interaction == "unlock_door":
                    # 문이 열리는 짜릿한 연출 효과음
                    pass

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                player_manager.handle_event(event, puzzle_manager.gears)

        # 상태 실시간 제어
        player_manager.update(dt)
        puzzle_manager.update(dt)

        screen.fill(COLOR_BG)
        puzzle_manager.draw(screen)
        player_manager.draw(screen)

        # 📜 상황별 동선 안내 자막 UI 갱신 규칙
        level_text = font.render(f"STAGE {puzzle_manager.current_level} : 우물 속의 열쇠", True, COLOR_TEXT)
        screen.blit(level_text, (30, 30))
        
        # 하단 미션 가이드라인 문자열 출력
        if not puzzle_manager.is_box_open:
            guide_str = "🎯 동력원 기어를 돌려 잠긴 보물상자를 개방하세요!"
        elif puzzle_manager.is_box_open and not puzzle_manager.has_key:
            guide_str = "🔍 상자가 열렸습니다! 내부의 황금 열쇠[KEY]를 클릭하여 획득하세요!"
        elif puzzle_manager.has_key and not puzzle_manager.door_unlocked:
            guide_str = "🚪 열쇠를 가방에 챙겼습니다! 우측의 굳게 닫힌 문을 클릭해 잠금을 해제하세요!"
        else:
            guide_str = "🎉 문이 열렸습니다! [SPACE] 키를 눌러 다음 방으로 진입하세요!"
            
        guide_text = sub_font.render(guide_str, True, (255, 255, 150))
        screen.blit(guide_text, (30, SCREEN_HEIGHT - 50))
        
        if puzzle_manager.is_cleared:
            if not clear_sound_played:
                sound_manager.stop_bgm()           
                sound_manager.play_effect("clear") 
                clear_sound_played = True
                
            if puzzle_manager.current_level < 5:
                clear_text = font.render("🎉 STAGE CLEAR!", True, (100, 255, 100))
            else:
                clear_text = font.render("🏆 ALL STAGES CLEARED!", True, (255, 215, 0))
            screen.blit(clear_text, (1280 // 2 - 120, 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
