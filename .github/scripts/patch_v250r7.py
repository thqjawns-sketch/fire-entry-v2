from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

if "V2.50-R6" not in s:
    raise SystemExit("Expected V2.50-R6 not found")
s = s.replace("V2.50-R6", "V2.50-R7")

location_block = '''<div class="v29BoardCard">
    <div class="v250BoardVisualTitle">🗺️ 위치 관제</div>
    <div class="v33BoardCardScroll">
      <div class="v33BoardLayout">
        <div id="v33FloorPanel" class="v33SidePanel v33FloorPanel"></div>
        <div id="v29LocationBoard" class="v33PlanWrap"></div>
        <div id="v33SummaryPanel" class="v33SidePanel"></div>
      </div>
    </div>

  </div>'''

location_with_roster = '''<div class="v29BoardCard">
    <div class="v250BoardVisualTitle">🗺️ 위치 관제</div>
    <div class="v33BoardCardScroll">
      <div class="v33BoardLayout">
        <div id="v33FloorPanel" class="v33SidePanel v33FloorPanel"></div>
        <div id="v29LocationBoard" class="v33PlanWrap"></div>
        <div id="v33SummaryPanel" class="v33SidePanel"></div>
      </div>
    </div>

    <div id="v34FloorMembers" class="v34FloorMembers">
      <div class="v34FloorMembersHead">선택 층 활동대원</div>
      <div class="v34FloorMemberEmpty">층을 선택하면 해당 층의 활동대원이 표시됩니다.</div>
    </div>
  </div>'''

if location_block not in s:
    raise SystemExit("Location board block missing")
s = s.replace(location_block, location_with_roster, 1)

css_anchor = '.v250BoardVisualTitle{margin:0 0 10px;font-size:19px;font-weight:950;color:#173d67}'
css_extra = '''\n/* ===== V2.50-R7 선택층 활동대원 복원 ===== */\n#teamBoardPageV29 #v34FloorMembers{margin-top:12px}\n#teamBoardPageV29 #v34FloorMembers .memberRow{cursor:default!important}\n'''
if css_anchor not in s:
    raise SystemExit("CSS anchor missing")
s = s.replace(css_anchor, css_anchor + css_extra, 1)

p.write_text(s, encoding="utf-8")
