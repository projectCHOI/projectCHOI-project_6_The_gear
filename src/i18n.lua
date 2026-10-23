-- All player-facing text is stored here. Internal state names stay unchanged.
local I18n={language='en'}
local messages={
 en={
  heading='THE GEAR / STAGE %d OF 5',
  stage1='First connection',stage2='Mix the sizes',stage3='Turn the corner',
  stage4='Climb the chain',stage5='The final workshop',
  shortcuts='R: retry   H: placement hint   M: mute   ESC: quit',
  toolbox='TOOLBOX',drag='Drag a gear into the zone',zone='GAME ZONE',winch='WINCH / WELL',
  small='SMALL',medium='MEDIUM',large='LARGE',well='WELL',clickChest='CLICK CHEST',
  open='OPEN',door='DOOR',lift='LIFT: %d%%',auto='AUTO',goal='GOAL',
  jammed='JAMMED: remove a gear',
  placementHelp='Drag to move. Right-click to return. H: show a possible route.',
  clear='STAGE CLEAR!',allClear='ALL STAGES CLEAR!',bagKey='BAG: KEY',bagEmpty='BAG: empty',
  noStock='No gears of this size left.',
  invalid='Cannot place here. Keep gears inside the zone without overlap.',
  guideRaised='Chest is up! Click the CLOSED CHEST to open it.',
  guideCollect='Click the golden KEY inside the open chest.',
  guideUnlock='Key collected. Click the door at the far right.',
  guideAllClear='All stages cleared! ENTER: play again.',
  guideClear='Room complete! SPACE: next stage.',
  guideJammed='Gears are JAMMED. Remove a gear from the conflicting loop.',
  guideLift='Power connected! The winch is raising the chest.',
  guideBuild='Drag gears from TOOLBOX. Connect the moving green source to the GOLD gear.'
 },
 ko={
  heading='톱니바퀴 / 스테이지 %d / 5',
  stage1='첫 번째 연결',stage2='다양한 크기의 톱니바퀴',stage3='모퉁이를 돌아서',
  stage4='위로 이어지는 동력',stage5='마지막 작업실',
  shortcuts='R: 재시작   H: 배치 힌트   M: 음소거   ESC: 종료',
  toolbox='톱니바퀴 보관함',drag='톱니바퀴를 끌어 배치하세요',zone='게임 구역',winch='도르레 / 우물',
  small='소형',medium='중형',large='대형',well='우물',clickChest='상자 클릭',
  open='열림',door='출구',lift='인양: %d%%',auto='동력원',goal='목표',
  jammed='회전 충돌: 톱니바퀴를 빼세요',
  placementHelp='드래그: 이동 / 오른쪽 클릭: 보관함 반환 / H: 배치 힌트',
  clear='스테이지 완료!',allClear='모든 스테이지 완료!',bagKey='가방: 열쇠',bagEmpty='가방: 비어 있음',
  noStock='이 크기의 톱니바퀴를 모두 사용했습니다.',
  invalid='배치할 수 없습니다. 게임 구역 안에 겹치지 않게 놓으세요.',
  guideRaised='상자가 올라왔습니다! 닫힌 상자를 클릭해 여세요.',
  guideCollect='열린 상자 안의 황금 열쇠를 클릭하세요.',
  guideUnlock='열쇠를 얻었습니다. 맨 오른쪽 출구를 클릭하세요.',
  guideAllClear='모든 스테이지를 완료했습니다! ENTER: 처음부터 다시 시작',
  guideClear='스테이지 완료! SPACE: 다음 스테이지',
  guideJammed='회전 방향이 충돌합니다. 고리를 이루는 톱니바퀴를 빼세요.',
  guideLift='동력이 연결되었습니다! 도르레가 상자를 끌어올립니다.',
  guideBuild='보관함의 톱니바퀴를 배치해 초록 동력원과 황금 톱니바퀴를 연결하세요.'
 }
}
function I18n.set(language)
 assert(messages[language], 'Unsupported language: '..tostring(language))
 I18n.language=language
end
function I18n.t(key,...)
 local value=assert(messages[I18n.language][key], 'Missing translation: '..key)
 if select('#',...)>0 then return string.format(value,...) end
 return value
end
return I18n
