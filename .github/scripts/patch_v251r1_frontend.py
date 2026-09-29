from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

if 'V2.50-R7' not in s:
    raise SystemExit('Expected V2.50-R7 not found')
s=s.replace('V2.50-R7','V2.51-R1')

old_title='<div class="v29TeamHeaderTitle">👥 2. 조별현황</div>'
new_title='<div class="v29TeamHeaderTitle">🛡️ 2. 조·대원 안전관리</div>'
if old_title not in s:
    raise SystemExit('team section title anchor missing')
s=s.replace(old_title,new_title,1)

team_anchor='<div id="teamStatusV28"></div>'
team_insert='''<div class="v251OfficerBox">
  <div class="v251OfficerLabel">현황 확인자</div>
  <input type="text" id="v251StatusOfficer" class="v251OfficerInput" placeholder="대응단 현황 확인자 성명" autocomplete="name">
  <div class="v251OfficerHint">위치변경 · 안전확인 · 고립지정/해제 기록에 공통 적용됩니다.</div>
</div>
<div id="v251SafetyTargets" class="v251SafetyTargets"></div>

<div id="teamStatusV28"></div>'''
if team_anchor not in s:
    raise SystemExit('team status anchor missing')
s=s.replace(team_anchor,team_insert,1)

s=s.replace('📍 조 위치변경','🛡️ 조 안전관리',1)

css=r'''
/* ===== V2.51-R1 현황 확인자 / 안전확인 / 고립관리 ===== */
.v251OfficerBox{margin:2px 0 12px;padding:12px 13px;border:1px solid #bfd2e5;border-radius:11px;background:#f6faff}
.v251OfficerLabel{font-size:16px;font-weight:950;color:#173d67;margin-bottom:7px}
.v251OfficerInput{margin:0!important;background:#fff!important;font-weight:900!important}
.v251OfficerHint{margin-top:6px;font-size:11px;font-weight:750;color:#607387;line-height:1.45}
.v251SafetyTargets{margin:0 0 12px}
.v251SafetyBox{border:1px solid #e4c36a;border-radius:11px;background:#fffaf0;overflow:hidden}
.v251SafetyHead{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:10px 12px;background:#fff3d6;color:#6b4d00;font-weight:950}
.v251SafetyHead strong{font-size:15px}
.v251SafetySelectAll{width:auto!important;margin:0!important;padding:7px 10px!important;font-size:12px!important;background:#fff!important;color:#6b4d00!important;border:1px solid #d7b85f!important}
.v251SafetyList{padding:6px 10px}
.v251SafetyItem{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:9px;padding:9px 4px;border-bottom:1px solid #f1e2b9}
.v251SafetyItem:last-child{border-bottom:0}
.v251SafetyItem input{width:20px;height:20px}
.v251SafetyName{font-size:14px;font-weight:950;color:#263b50}
.v251SafetyMeta{margin-top:3px;font-size:11px;font-weight:800;color:#66788a}
.v251SafetyState{font-size:12px;font-weight:950;text-align:right;color:#b3261e;white-space:nowrap}
.v251SafetyState.confirmed{color:#9a5b00}
.v251SafetyActions{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 10px 10px}
.v251SafetyActions button{margin:0!important;padding:11px 8px!important;font-size:13px!important}
.v251BatchConfirm{background:#b42318!important;color:#fff!important}
.v251NoTargets{padding:10px 12px;border:1px solid #dce5ee;border-radius:10px;background:#f8fafc;color:#607387;font-size:12px;font-weight:850}
.v251ManageActions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}
.v251ManageActions button{margin:0!important;padding:12px 8px!important;font-size:13px!important;min-height:46px}
.v251SafetyBtn{background:#fff7e6!important;color:#8a5a00!important;border:1px solid #e5b94e!important}
.v251IsolationBtn{background:#fff0f0!important;color:#b42318!important;border:1px solid #d93025!important}
.v251IsolationReleaseBtn{background:#eef7f0!important;color:#137333!important;border:1px solid #188038!important}
.v251NeedsCheck{animation:dangerBlink 1s infinite!important}
.v251IsolationBlink{animation:dangerBlink .8s infinite!important;outline:4px solid #8b0000!important}
.memberRow.v251SafetyConfirmed,.insideStatus.v251SafetyConfirmed{animation:none!important;background:#fce8e6!important;color:#b3261e!important;border-left-color:#d93025!important}
.v250CommanderTeamCard.v251SafetyConfirmed{animation:none!important;border-left-color:#d93025!important;background:#fff8f7!important}
.v250CommanderTeamCard.v251NeedsCheck,.v250CommanderTeamCard.v251IsolationBlink{animation:dangerBlink 1s infinite!important}
.v33FaceChip.v251NeedsCheck,.v33FaceChip.v251IsolationBlink{animation:dangerBlink 1s infinite!important}
.criticalSummary.v251StableCritical{animation:none!important;background:#fce8e6!important;color:#b3261e!important;border-color:#d93025!important}
@media(max-width:560px){.v251SafetyItem{grid-template-columns:auto 1fr}.v251SafetyState{grid-column:2;text-align:left}.v251ManageActions{grid-template-columns:1fr}}
'''
style_pos=s.find('</style>')
if style_pos<0: raise SystemExit('style close missing')
s=s[:style_pos]+css+s[style_pos:]

js=r'''
<script>
/* ===== V2.51-R1 현황 안전관리 ===== */
const V251_STATUS_OFFICER_KEY='fire_app_status_officer_v251';
const V251_RECHECK_MINUTES=10;

function v251StatusOfficerValue(required){
  const el=document.getElementById('v251StatusOfficer');
  const value=((el&&el.value)||localStorage.getItem(V251_STATUS_OFFICER_KEY)||'').trim();
  if(required&&!value)alert('현황 확인자 성명을 먼저 입력하세요.');
  return value;
}
function v251RememberStatusOfficer(){
  const el=document.getElementById('v251StatusOfficer');
  if(!el)return;
  const value=(el.value||'').trim();
  if(value)localStorage.setItem(V251_STATUS_OFFICER_KEY,value);
  else localStorage.removeItem(V251_STATUS_OFFICER_KEY);
}
function v251CurrentSiteId(){
  const raw=((document.getElementById('site')||{}).value||'');
  return typeof v2SiteId==='function'?v2SiteId(raw):raw;
}
function v251ParseTime(v){
  if(!v)return NaN;
  if(v instanceof Date)return v.getTime();
  const s=String(v).trim();
  if(!s)return NaN;
  const t=Date.parse(s.includes('T')?s:s.replace(' ','T'));
  return t;
}
function v251TimeHM(v){
  const t=v251ParseTime(v); if(!Number.isFinite(t))return '';
  return new Date(t).toLocaleTimeString('ko-KR',{hour:'2-digit',minute:'2-digit',hour12:false});
}
function v251MemberSafetyState(m){
  const mins=Number(m&&m.currentMinutes)||0;
  if(m&&m.isolated)return {className:'stayCritical',icon:'🚨',text:'고립대원',isolated:true,due:true,confirmed:false};
  if(mins<=20)return {className:'stayNormal',icon:'🟢',text:'정상',due:false,confirmed:false};
  if(mins<=25)return {className:'stayCaution',icon:'🟠',text:'주의',due:false,confirmed:false};
  if(mins<=30)return {className:'stayWarning',icon:'🔴',text:'경고',due:false,confirmed:false};
  const checked=v251ParseTime(m&&m.safetyCheckedAt);
  if(Number.isFinite(checked)){
    const elapsed=Math.max(0,(Date.now()-checked)/60000);
    if(elapsed<V251_RECHECK_MINUTES){
      const remain=Math.max(1,Math.ceil(V251_RECHECK_MINUTES-elapsed));
      return {className:'stayCritical',icon:'🔴',text:'안전확인 완료 '+v251TimeHM(m.safetyCheckedAt)+' · 재확인 '+remain+'분 후',due:false,confirmed:true};
    }
    return {className:'stayCritical',icon:'🚨',text:'재확인 필요',due:true,recheck:true,confirmed:false};
  }
  return {className:'stayCritical',icon:'🚨',text:'즉시확인',due:true,confirmed:false};
}
function v251FindMember(id){return (window.__dashboardInsideMembers||[]).find(m=>String(m.memberId)===String(id));}
function v251TeamName(m){
  try{return v19TeamInfo(m).team||m.team||'미지정';}catch(e){return (m&&m.team)||'미지정';}
}
function v251NeedOfficer(){const o=v251StatusOfficerValue(true);if(o)v251RememberStatusOfficer();return o;}

const v251BaseCall=(typeof v2CallPost==='function')?v2CallPost:null;
if(v251BaseCall){
  window.v2CallPost=async function(form){
    const action=form&&form.get?String(form.get('action')||''):'';
    if(['updateLocation','batchUpdateLocation','updateTeam'].includes(action)){
      const officer=v251NeedOfficer();
      if(!officer)throw new Error('현황 확인자를 입력하세요.');
      if(!form.get('officer'))form.set('officer',officer);
    }
    return v251BaseCall(form);
  };
}

async function v251Post(action,ids,extra){
  const officer=v251NeedOfficer(); if(!officer)return null;
  const siteId=v251CurrentSiteId(); if(!siteId){alert('화재현장을 선택하세요.');return null;}
  const form=new URLSearchParams();
  form.set('action',action); form.set('siteId',siteId); form.set('officer',officer);
  form.set('members',JSON.stringify((ids||[]).map(id=>({id:String(id)}))));
  Object.keys(extra||{}).forEach(k=>form.set(k,extra[k]));
  try{
    const d=await (v251BaseCall?v251BaseCall(form):v2CallPost(form));
    if(!d||(!d.ok&&!d.success))throw new Error((d&&d.error)||(d&&d.message)||'처리 실패');
    if(typeof closeDashboardMemberDetail==='function')closeDashboardMemberDetail();
    await loadDashboard(false);
    v251RefreshEnhancements();
    return d;
  }catch(e){alert((e&&e.message)||'처리에 실패했습니다.');return null;}
}
async function v251SafetyCheckIds(ids){
  if(!ids||!ids.length){alert('안전확인할 대원을 선택하세요.');return;}
  if(!confirm(ids.length+'명을 안전확인 완료 처리하시겠습니까?\n10분 후 다시 재확인 대상이 됩니다.'))return;
  await v251Post('batchSafetyCheck',ids,{});
}
async function v251IsolationIds(ids,isolated,label){
  if(!ids||!ids.length)return;
  if(!confirm((label||ids.length+'명')+'을 '+(isolated?'고립대원으로 지정':'고립상태 해제')+'하시겠습니까?'))return;
  await v251Post('batchSetIsolation',ids,{isolated:isolated?'Y':'N'});
}
function v251SelectAllSafety(){
  const boxes=[...document.querySelectorAll('#v251SafetyTargets .v251SafetyCheck:not(:disabled)')];
  const all=boxes.length&&boxes.every(x=>x.checked); boxes.forEach(x=>x.checked=!all);
}
function v251BatchConfirmSelected(){
  const ids=[...document.querySelectorAll('#v251SafetyTargets .v251SafetyCheck:checked')].map(x=>x.dataset.id);
  v251SafetyCheckIds(ids);
}
function v251RenderSafetyTargets(){
  const box=document.getElementById('v251SafetyTargets'); if(!box)return;
  const list=(window.__dashboardInsideMembers||[]).filter(m=>Number(m.currentMinutes)>=31);
  if(!list.length){box.innerHTML='<div class="v251NoTargets">✅ 현재 31분 이상 안전확인 대상이 없습니다.</div>';return;}
  list.sort((a,b)=>Number(b.currentMinutes||0)-Number(a.currentMinutes||0));
  const rows=list.map(m=>{
    const st=v251MemberSafetyState(m), id=String(m.memberId||''), team=v251TeamName(m);
    const disabled=st.confirmed&&!st.isolated?' disabled':'';
    const meta=escapeHtml(team+' · '+(m.direction||'미지정')+' · '+(m.floor||'미지정')+' · '+Number(m.currentMinutes||0)+'분');
    return '<div class="v251SafetyItem"><input type="checkbox" class="v251SafetyCheck" data-id="'+escapeAttr(id)+'"'+disabled+'><div><div class="v251SafetyName">'+escapeHtml(getMemberDisplay(m.memberId,m.memberName||m.name||''))+'</div><div class="v251SafetyMeta">'+meta+'</div></div><div class="v251SafetyState '+(st.confirmed?'confirmed':'')+'">'+escapeHtml(st.text)+'</div></div>';
  }).join('');
  const due=list.filter(m=>v251MemberSafetyState(m).due&&!m.isolated).length;
  box.innerHTML='<div class="v251SafetyBox"><div class="v251SafetyHead"><strong>🚨 안전확인 대상 '+list.length+'명</strong><button type="button" class="v251SafetySelectAll" onclick="v251SelectAllSafety()">전체선택</button></div><div class="v251SafetyList">'+rows+'</div><div class="v251SafetyActions"><button type="button" class="v251SafetySelectAll" onclick="v251SelectAllSafety()">선택 전환</button><button type="button" class="v251BatchConfirm" onclick="v251BatchConfirmSelected()">✅ 선택 대원 안전확인 완료</button></div></div>';
}
function v251ApplyMemberRows(){
  ['dashboardInside','v34FloorMembers'].forEach(rootId=>{
    const root=document.getElementById(rootId); if(!root)return;
    root.querySelectorAll('.memberRow').forEach(row=>{
      const idEl=row.querySelector('.compactId'); if(!idEl)return;
      const m=v251FindMember(idEl.textContent.trim()); if(!m)return;
      const st=v251MemberSafetyState(m);
      row.classList.remove('stayNormal','stayCaution','stayWarning','stayCritical','v250Isolated','v251SafetyConfirmed','v251NeedsCheck','v251IsolationBlink');
      row.classList.add(st.className);
      if(st.confirmed)row.classList.add('v251SafetyConfirmed');
      if(st.due&&!st.isolated)row.classList.add('v251NeedsCheck');
      if(st.isolated)row.classList.add('v250Isolated','v251IsolationBlink');
      const status=row.querySelector('.insideStatus');
      if(status){
        status.className='insideStatus '+st.className+(st.confirmed?' v251SafetyConfirmed':'')+(st.due&&!st.isolated?' v251NeedsCheck':'');
        status.textContent=st.icon+' '+st.text;
      }
    });
  });
}
function v251UpdateCriticalSummary(){
  const box=document.getElementById('criticalSummary'); if(!box)return;
  const over=(window.__dashboardInsideMembers||[]).filter(m=>Number(m.currentMinutes)>=31);
  const due=over.filter(m=>v251MemberSafetyState(m).due).length;
  box.classList.remove('v251StableCritical');
  if(due>0){box.classList.add('hasCritical');box.textContent='⚠️ 안전확인 필요 '+due+'명 · 확인 후 10분 재확인';}
  else if(over.length){box.classList.remove('hasCritical');box.classList.add('v251StableCritical');box.textContent='🔴 31분 이상 '+over.length+'명 · 안전확인 완료';}
  else{box.classList.remove('hasCritical');box.textContent='✅ 31분 이상 즉시 확인 대상 0명';}
}
function v251ApplyCommanderCards(){
  const members=window.__dashboardInsideMembers||[];
  document.querySelectorAll('#v250CommanderTeams .v250CommanderTeamCard').forEach(card=>{
    const nameEl=card.querySelector('.v250CommanderTeamName'); if(!nameEl)return;
    const txt=nameEl.textContent.trim();
    const teams=[...new Set(members.map(v251TeamName))].sort((a,b)=>b.length-a.length);
    const team=teams.find(t=>txt.indexOf(t)===0); if(!team)return;
    const group=members.filter(m=>v251TeamName(m)===team);
    const states=group.map(v251MemberSafetyState);
    const isolated=states.some(x=>x.isolated), due=states.some(x=>x.due&&!x.isolated), confirmed=group.some(m=>Number(m.currentMinutes)>=31)&&!due&&!isolated;
    card.classList.remove('v251NeedsCheck','v251SafetyConfirmed','v251IsolationBlink');
    if(isolated)card.classList.add('v251IsolationBlink'); else if(due)card.classList.add('v251NeedsCheck'); else if(confirmed)card.classList.add('v251SafetyConfirmed');
    const badge=card.querySelector('.v250CommanderTeamBadge:not(.isolated)');
    if(badge){
      if(isolated)badge.textContent='🚨 고립대원 포함';
      else if(due){const re=states.some(x=>x.recheck);badge.textContent='🚨 '+(re?'재확인 필요':'즉시확인');}
      else if(confirmed){const last=group.filter(m=>m.safetyCheckedAt).sort((a,b)=>v251ParseTime(b.safetyCheckedAt)-v251ParseTime(a.safetyCheckedAt))[0];badge.textContent='🔴 안전확인 완료 '+(last?v251TimeHM(last.safetyCheckedAt):'');}
    }
  });
  document.querySelectorAll('#v29LocationBoard .v33FaceChip').forEach(chip=>{
    const text=chip.textContent.trim();
    const teams=[...new Set(members.map(v251TeamName))].sort((a,b)=>b.length-a.length);
    const team=teams.find(t=>text.indexOf(t)===0); if(!team)return;
    const group=members.filter(m=>v251TeamName(m)===team), states=group.map(v251MemberSafetyState);
    chip.classList.remove('v251NeedsCheck','v251SafetyConfirmed','v251IsolationBlink');
    if(states.some(x=>x.isolated))chip.classList.add('v251IsolationBlink');
    else if(states.some(x=>x.due))chip.classList.add('v251NeedsCheck');
    else if(group.some(m=>Number(m.currentMinutes)>=31))chip.classList.add('v251SafetyConfirmed');
  });
}
function v251RefreshEnhancements(){v251RenderSafetyTargets();v251ApplyMemberRows();v251UpdateCriticalSummary();v251ApplyCommanderCards();}

const v251OriginalMemberDetail=(typeof openDashboardMemberDetail==='function')?openDashboardMemberDetail:null;
if(v251OriginalMemberDetail){
  window.openDashboardMemberDetail=function(memberId,memberName){
    v251OriginalMemberDetail(memberId,memberName);
    const m=v251FindMember(memberId); if(!m)return;
    const actions=document.querySelector('#dashboardDetailOverlay .sheetActions'); if(!actions)return;
    const edit=actions.querySelector('#v238MemberEditBtn'); if(edit)edit.textContent='📍 개별 위치변경';
    if(!document.getElementById('v251MemberSafetyBtn')){
      const safe=document.createElement('button'); safe.type='button'; safe.id='v251MemberSafetyBtn'; safe.className='v251SafetyBtn'; safe.textContent='✅ 개별 안전확인';
      safe.onclick=()=>v251SafetyCheckIds([memberId]); actions.insertBefore(safe,actions.lastElementChild);
      const iso=document.createElement('button'); iso.type='button'; iso.id='v251MemberIsolationBtn'; iso.className=m.isolated?'v251IsolationReleaseBtn':'v251IsolationBtn'; iso.textContent=m.isolated?'✅ 고립상태 해제':'🚨 개별 고립지정';
      iso.onclick=()=>v251IsolationIds([memberId],!m.isolated,getMemberDisplay(m.memberId,m.memberName||m.name||'')); actions.insertBefore(iso,actions.lastElementChild);
    }
  };
}
function v251EnsureOverlay(){
  let overlay=document.getElementById('dashboardDetailOverlay');
  if(!overlay){overlay=document.createElement('div');overlay.id='dashboardDetailOverlay';overlay.className='dashboardDetailOverlay';document.body.appendChild(overlay);}
  return overlay;
}
const v251OriginalTeamLocationEdit=(typeof openDashboardTeamLocationEdit==='function')?openDashboardTeamLocationEdit:null;
if(v251OriginalTeamLocationEdit){
  window.openDashboardTeamLocationEdit=function(team){
    const members=(window.__dashboardInsideMembers||[]).filter(m=>v251TeamName(m)===team);
    if(!members.length){alert('해당 조의 현재 활동대원을 찾지 못했습니다.');return;}
    const first=members[0], allIsolated=members.every(m=>m.isolated);
    const overlay=v251EnsureOverlay();
    overlay.innerHTML='<div class="dashboardDetailSheet"><div class="sheetHeader"><b>🛡️ '+escapeHtml(team)+' · 조·대원 안전관리</b><button type="button" id="v251TeamManageClose" class="sheetClose">×</button></div><div class="v237TeamMoveTitle">'+escapeHtml(team)+' · '+members.length+'명</div><div class="v237TeamMoveSub">'+escapeHtml((first.direction||'미지정')+' · '+(first.floor||'미지정')+' · '+(first.detail||'세부장소 미지정'))+'</div><div class="v251ManageActions"><button type="button" id="v251TeamMove" class="sheetEdit">📍 조 위치변경</button><button type="button" id="v251TeamSafety" class="v251SafetyBtn">✅ 조 전체 안전확인</button><button type="button" id="v251TeamIsolation" class="'+(allIsolated?'v251IsolationReleaseBtn':'v251IsolationBtn')+'">'+(allIsolated?'✅ 조 전체 고립해제':'🚨 조 전체 고립지정')+'</button><button type="button" id="v251TeamClose" class="v237CloseBtn">닫기</button></div></div>';
    overlay.classList.add('show');
    const close=()=>overlay.classList.remove('show');
    document.getElementById('v251TeamManageClose').onclick=close; document.getElementById('v251TeamClose').onclick=close;
    document.getElementById('v251TeamMove').onclick=()=>{if(!v251NeedOfficer())return;close();v251OriginalTeamLocationEdit(team);};
    document.getElementById('v251TeamSafety').onclick=()=>v251SafetyCheckIds(members.map(m=>m.memberId));
    document.getElementById('v251TeamIsolation').onclick=()=>v251IsolationIds(members.map(m=>m.memberId),!allIsolated,team+' '+members.length+'명');
  };
}

function v251Init(){
  const el=document.getElementById('v251StatusOfficer');
  if(el){el.value=localStorage.getItem(V251_STATUS_OFFICER_KEY)||'';el.addEventListener('input',v251RememberStatusOfficer);}
  v251RefreshEnhancements();
}
document.addEventListener('DOMContentLoaded',()=>setTimeout(v251Init,0));
if(typeof loadDashboard==='function'){
  const v251OriginalLoadDashboard=loadDashboard;
  window.loadDashboard=async function(){const r=await v251OriginalLoadDashboard.apply(this,arguments);setTimeout(v251RefreshEnhancements,0);return r;};
}
if(typeof drawDashboardInside==='function'){
  const v251OriginalDrawDashboardInside=drawDashboardInside;
  window.drawDashboardInside=function(list){const r=v251OriginalDrawDashboardInside.apply(this,arguments);setTimeout(v251RefreshEnhancements,0);return r;};
}
if(typeof drawTeamBoardV29==='function'){
  const v251OriginalDrawTeamBoard=drawTeamBoardV29;
  window.drawTeamBoardV29=function(){const r=v251OriginalDrawTeamBoard.apply(this,arguments);setTimeout(v251RefreshEnhancements,0);return r;};
}
setInterval(v251RefreshEnhancements,30000);
</script>
'''
body_pos=s.rfind('</body>')
if body_pos<0: raise SystemExit('body close missing')
s=s[:body_pos]+js+s[body_pos:]

p.write_text(s,encoding='utf-8')
