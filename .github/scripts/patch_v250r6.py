from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

if "V2.50-R5" not in s:
    raise SystemExit("Expected V2.50-R5 not found")
s = s.replace("V2.50-R5", "V2.50-R6")

css_anchor = '@media(max-width:620px){.v250CommanderTeamsGrid{grid-template-columns:1fr}}'
css_extra = """
/* ===== V2.50-R6 지휘관 관제판 정리 ===== */
.v250CommanderSectionTitle{margin:6px 0 10px;font-size:20px;font-weight:950;color:#173d67;letter-spacing:-.3px}
.v250CommanderTeamsHead>span:first-child{font-size:20px!important;font-weight:950!important;color:#173d67}
.v250CommanderTeamsSub{font-size:17px!important;font-weight:950!important;color:#173d67!important}
.v250CommanderTeamsGrid{display:flex!important;flex-direction:column!important;gap:9px!important}
.v250CommanderTeamCard{width:100%;box-sizing:border-box;display:grid!important;grid-template-columns:155px minmax(260px,1.15fr) 235px minmax(390px,1.7fr);align-items:center;gap:12px;padding:11px 14px!important}
.v250CommanderTeamTop{margin:0!important}
.v250CommanderTeamLoc,.v250CommanderTeamMeta,.v250CommanderMembers{margin:0!important}
.v250CommanderMembers{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.v250CommanderMember{font-size:12px;padding:6px 8px}
.v250CommanderTeamMeta{display:flex;flex-wrap:wrap;gap:6px}
.v250CommanderTeamCard .v250CommanderTeamName{font-size:18px}
.v250CommanderTeamCard .v250CommanderTeamCount{font-size:14px}
.v250BoardVisualTitle{margin:0 0 10px;font-size:19px;font-weight:950;color:#173d67}
@media(max-width:1100px){.v250CommanderTeamCard{grid-template-columns:140px 1fr 200px}.v250CommanderMembers{grid-column:1/-1}}
@media(max-width:760px){.v250CommanderTeamCard{grid-template-columns:1fr}.v250CommanderTeamLoc,.v250CommanderTeamMeta,.v250CommanderMembers{grid-column:1}}
"""
if css_anchor not in s:
    raise SystemExit("CSS anchor missing")
s = s.replace(css_anchor, css_anchor + css_extra, 1)

html_anchor = '''<div class="v250CommanderPanel">
  <div id="v29BoardSite" class="v250CommanderSite">현장 : -</div>
  <div id="v250BoardLiveSummary" class="v250CommanderMetrics"></div>'''
html_new = '''<div class="v250CommanderPanel">
  <div id="v29BoardSite" class="v250CommanderSite">현장 : -</div>
  <div class="v250CommanderSectionTitle">👥 인원현황</div>
  <div id="v250BoardLiveSummary" class="v250CommanderMetrics"></div>'''
if html_anchor not in s:
    raise SystemExit("Commander HTML anchor missing")
s = s.replace(html_anchor, html_new, 1)

card_anchor = '''<div class="v29BoardCard">
    <div class="v33BoardCardScroll">'''
card_new = '''<div class="v29BoardCard">
    <div class="v250BoardVisualTitle">🗺️ 위치 관제</div>
    <div class="v33BoardCardScroll">'''
if card_anchor not in s:
    raise SystemExit("Board card anchor missing")
s = s.replace(card_anchor, card_new, 1)

duplicate_block = '''
    <div id="v29BoardDetail" class="v29BoardDetail">
      <div class="v29DetailEmpty">조를 누르면 현재 위치 상세정보가 표시됩니다.</div>
    </div>

    <div id="v34FloorMembers" class="v34FloorMembers">
      <div class="v34FloorMembersHead">선택 층 활동대원</div>
      <div class="v34FloorMemberEmpty">층을 선택하면 해당 층의 활동대원이 표시됩니다.</div>
    </div>

    <div id="v33BoardStats" class="v33BoardStats"></div>

    <div class="v29BoardFoot">
      ※ 층을 선택하면 해당 층의 현재 활동 조와 대원을 확인할 수 있습니다. 방면은 아래쪽 A방면을 기준으로 시계방향 B → C → D 순서입니다.
    </div>
'''
if duplicate_block not in s:
    raise SystemExit("Duplicate board block missing")
s = s.replace(duplicate_block, "\n", 1)

old_init = 'if(!gm.has(key))gm.set(key,{team,activityNo,direction:m.direction||"미지정",floor:m.floor||"미지정",detail:m.detail||"세부장소 미지정",members:[],maxMinutes:0,isolated:false});'
new_init = 'if(!gm.has(key))gm.set(key,{team,activityNo,direction:m.direction||"미지정",floor:m.floor||"미지정",detail:m.detail||"세부장소 미지정",entryTime:m.entryTime||"",members:[],maxMinutes:0,isolated:false});'
if old_init not in s:
    raise SystemExit("Group init missing")
s = s.replace(old_init, new_init, 1)

old_member = '''      g.members.push({id:m.memberId,name:m.memberName||m.name||"",mins,isolated:!!m.isolated});
      if((!g.detail || g.detail==="세부장소 미지정") && m.detail)g.detail=m.detail;'''
new_member = '''      g.members.push({id:m.memberId,name:m.memberName||m.name||"",mins,isolated:!!m.isolated});
      if(m.entryTime && (!g.entryTime || String(m.entryTime)<String(g.entryTime)))g.entryTime=m.entryTime;
      if((!g.detail || g.detail==="세부장소 미지정") && m.detail)g.detail=m.detail;'''
if old_member not in s:
    raise SystemExit("Member grouping block missing")
s = s.replace(old_member, new_member, 1)

old_sort = '''    const groups=[...gm.values()].sort((a,b)=>{
      const na=parseInt(String(a.team).match(/\\d+/)?.[0]||"999",10), nb=parseInt(String(b.team).match(/\\d+/)?.[0]||"999",10);
      return na-nb || a.activityNo-b.activityNo || String(a.team).localeCompare(String(b.team),"ko");
    });'''
new_sort = '''    const groups=[...gm.values()].sort((a,b)=>{
      const ta=String(a.entryTime||"9999-99-99 99:99:99"), tb=String(b.entryTime||"9999-99-99 99:99:99");
      const byEntry=ta.localeCompare(tb);
      if(byEntry!==0)return byEntry;
      const na=parseInt(String(a.team).match(/\\d+/)?.[0]||"999",10), nb=parseInt(String(b.team).match(/\\d+/)?.[0]||"999",10);
      return na-nb || a.activityNo-b.activityNo || String(a.team).localeCompare(String(b.team),"ko");
    });'''
if old_sort not in s:
    raise SystemExit("Team sort block missing")
s = s.replace(old_sort, new_sort, 1)

toggle_anchor = '''async function v250ToggleIsolation(memberId,memberName){
  const m=(window.__dashboardInsideMembers||[]).find(x=>String(x.memberId)===String(memberId)); if(!m)return;'''
toggle_new = '''async function v250ToggleIsolation(memberId,memberName){
  const boardPage=document.getElementById("teamBoardPageV29");
  if(boardPage && getComputedStyle(boardPage).display!=="none")return;
  const m=(window.__dashboardInsideMembers||[]).find(x=>String(x.memberId)===String(memberId)); if(!m)return;'''
if toggle_anchor not in s:
    raise SystemExit("Isolation guard anchor missing")
s = s.replace(toggle_anchor, toggle_new, 1)

p.write_text(s, encoding="utf-8")
