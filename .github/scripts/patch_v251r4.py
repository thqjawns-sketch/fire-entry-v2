from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Version labels
s=s.replace('<title>QR기반-진·출입 안전관리앱 V2.51-R3</title>','<title>QR기반-진·출입 안전관리앱 V2.51-R4</title>')
s=s.replace('🚒 QR기반-진·출입 안전관리앱 V2.50-R2','🚒 QR기반-진·출입 안전관리앱 V2.51-R4')
s=s.replace('<b>위치정보 수정</b>','<b>대원정보 수정</b>')

marker='<!-- V2.51-R4 SAFETY-MANAGEMENT UI -->'
if marker not in s:
    css=r'''
<style>
/* V2.51-R4 통합 안전관리 / 반영상태 */
.v251R4ApplyStatus{position:fixed;left:50%;top:14px;transform:translateX(-50%);z-index:30000;min-width:210px;max-width:90vw;padding:12px 18px;border-radius:12px;text-align:center;font-size:16px;font-weight:950;box-shadow:0 4px 18px rgba(0,0,0,.22);display:none}
.v251R4ApplyStatus.busy{display:block;background:#fff3cd;color:#7a4b00;border:2px solid #e0a800}
.v251R4ApplyStatus.done{display:block;background:#e6f4ea;color:#137333;border:2px solid #188038}
.v251R4ApplyStatus.error{display:block;background:#fce8e6;color:#b3261e;border:2px solid #d93025}
.v251R4IsoBox{margin-top:4px;padding:12px;border:1px solid #e0a7a3;border-radius:10px;background:#fff8f7}
.v251R4IsoBox label{margin:0 0 6px!important;color:#8b1d1d!important}
.v251R4CurrentState{margin:6px 0 10px;padding:9px 10px;border-radius:9px;background:#f6f8fa;font-size:13px;font-weight:850;color:#44546a}
.v251R4FormNote{margin-top:8px;font-size:12px;line-height:1.5;color:#607387;font-weight:700}
.v251R4Save{background:#1769c2!important;color:#fff!important}
</style>
'''
    js=r'''
<!-- V2.51-R4 SAFETY-MANAGEMENT UI -->
<script>
(function(){
  function r4Esc(v){return typeof escapeHtml==='function'?escapeHtml(String(v??'')):String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}
  function r4Attr(v){return typeof escapeAttr==='function'?escapeAttr(String(v??'')):r4Esc(v);}
  function r4Overlay(){return typeof v251EnsureOverlay==='function'?v251EnsureOverlay():document.getElementById('dashboardDetailOverlay');}
  function r4Officer(){return typeof v251NeedOfficer==='function'?v251NeedOfficer():((document.getElementById('v251StatusOfficer')||{}).value||'').trim();}
  function r4Site(){return typeof v251CurrentSiteId==='function'?v251CurrentSiteId():'';}
  function r4Status(text,type,autoHide){
    let el=document.getElementById('v251R4ApplyStatus');
    if(!el){el=document.createElement('div');el.id='v251R4ApplyStatus';el.className='v251R4ApplyStatus';document.body.appendChild(el);}
    el.className='v251R4ApplyStatus '+(type||'busy');el.textContent=text||'';
    clearTimeout(window.__v251R4StatusTimer);
    if(autoHide)window.__v251R4StatusTimer=setTimeout(()=>{el.style.display='none';el.className='v251R4ApplyStatus';},autoHide);
    else el.style.display='block';
  }
  async function r4Post(action,ids,extra,btn){
    const officer=r4Officer(); if(!officer)return null;
    const siteId=r4Site(); if(!siteId){alert('화재현장을 선택하세요.');return null;}
    const form=new URLSearchParams();
    form.set('action',action);form.set('siteId',siteId);form.set('officer',officer);
    form.set('members',JSON.stringify((ids||[]).map(id=>({id:String(id)}))));
    Object.keys(extra||{}).forEach(k=>form.set(k,extra[k]));
    const oldText=btn?btn.textContent:'';
    if(btn){btn.disabled=true;btn.textContent='⏳ 반영중...';}
    r4Status('⏳ 반영중...','busy');
    try{
      const call=(window.v2CallPost||((typeof v2CallPost==='function')?v2CallPost:null));
      if(!call)throw new Error('서버 호출 함수를 찾을 수 없습니다.');
      const d=await call(form);
      if(!d||(!d.ok&&!d.success))throw new Error((d&&d.error)||(d&&d.message)||'처리 실패');
      if(btn)btn.textContent='✅ 반영완료';
      r4Status('✅ 반영완료','done',1300);
      await loadDashboard(false);
      if(typeof v251RefreshEnhancements==='function')v251RefreshEnhancements();
      return d;
    }catch(e){
      r4Status('❌ 반영 실패','error',2200);
      alert((e&&e.message)||'반영에 실패했습니다.');
      return null;
    }finally{
      if(btn){setTimeout(()=>{btn.disabled=false;btn.textContent=oldText;},700);}
    }
  }
  window.v251R4Post=r4Post;

  function commonVal(members,key){
    const vals=[...new Set(members.map(m=>String((m&&m[key])||'')))];
    return vals.length===1?vals[0]:'';
  }
  function teamInfo(m){try{return v19TeamInfo(m);}catch(e){return {team:m.team||'',activityNo:m.activityNo||m.entryCount||1,direction:m.direction||'',floor:m.floor||'',detail:m.detail||''};}}

  window.v251R4OpenTeamSafety=function(team){
    const members=(window.__dashboardInsideMembers||[]).filter(m=>(typeof v251TeamName==='function'?v251TeamName(m):teamInfo(m).team)===team);
    if(!members.length){alert('해당 조의 현재 활동대원을 찾지 못했습니다.');return;}
    if(!r4Officer())return;
    const infos=members.map(teamInfo);
    const dir=[...new Set(infos.map(x=>String(x.direction||'')))];
    const floor=[...new Set(infos.map(x=>String(x.floor||'')))];
    const detail=[...new Set(infos.map(x=>String(x.detail||'')))];
    const curDir=dir.length===1?dir[0]:'';
    const curFloor=floor.length===1?floor[0]:'';
    const curDetail=detail.length===1?detail[0]:'';
    const activityNo=Math.max(...infos.map(x=>Number(x.activityNo)||1));
    const isoCount=members.filter(m=>m.isolated).length;
    const floors=['','옥상','상층','직상층','화점층','직하층','하층','지하층'];
    const ov=r4Overlay(); if(!ov)return;
    ov.innerHTML='<div class="dashboardDetailSheet">'+
      '<div class="sheetHeader"><b>🛡️ '+r4Esc(team)+' · 조 안전관리</b><button type="button" id="r4TeamClose" class="sheetClose">×</button></div>'+ 
      '<div class="v237TeamMoveTitle">'+r4Esc(team)+' 전체 · '+members.length+'명</div>'+ 
      '<div class="v251R4CurrentState">현재 고립 '+isoCount+'명 · 위치와 고립상태를 한 번에 반영합니다.</div>'+ 
      '<div class="locationEditForm">'+
        '<label>방면<select id="r4TeamDirection"><option value="">현재 위치 유지</option>'+['A방면','B방면','C방면','D방면'].map(v=>'<option value="'+v+'" '+(v===curDir?'selected':'')+'>'+v+'</option>').join('')+'</select></label>'+ 
        '<label>활동층<select id="r4TeamFloor">'+floors.map(v=>'<option value="'+r4Attr(v)+'" '+(v===curFloor?'selected':'')+'>'+(v||'현재 위치 유지')+'</option>').join('')+'</select></label>'+ 
        '<label>세부장소<input id="r4TeamDetail" value="'+r4Attr(curDetail)+'" placeholder="예: 기계실 / 1203호 / 계단실"></label>'+ 
        '<div class="v251R4IsoBox"><label>고립상태</label><select id="r4TeamIsolation"><option value="KEEP">변경없음</option><option value="Y">🚨 조 전체 고립지정</option><option value="N">✅ 조 전체 고립해제</option></select></div>'+ 
      '</div>'+ 
      '<div class="v251R4FormNote">위치만 바꾸거나, 고립상태만 바꾸거나, 둘을 동시에 변경할 수 있습니다.</div>'+ 
      '<button type="button" id="r4TeamSave" class="sheetSave v251R4Save">조 안전관리 반영</button>'+ 
      '</div>';
    ov.classList.add('show');
    document.getElementById('r4TeamClose').onclick=()=>ov.classList.remove('show');
    document.getElementById('r4TeamSave').onclick=async function(){
      const extra={team:team,activityNo:String(activityNo),direction:document.getElementById('r4TeamDirection').value,floor:document.getElementById('r4TeamFloor').value,detail:document.getElementById('r4TeamDetail').value,isolationMode:document.getElementById('r4TeamIsolation').value};
      const d=await r4Post('updateSafetyManagement',members.map(m=>m.memberId),extra,this);
      if(d)setTimeout(()=>ov.classList.remove('show'),350);
    };
  };

  window.v251R4OpenMemberSafety=function(memberId,memberName){
    const m=(typeof v251FindMember==='function'?v251FindMember(memberId):(window.__dashboardInsideMembers||[]).find(x=>String(x.memberId)===String(memberId)));
    if(!m){alert('현재 활동대원을 찾지 못했습니다.');return;}
    if(!r4Officer())return;
    const info=teamInfo(m), meta=(typeof v23LoadMeta==='function'?v23LoadMeta():{}), old=meta[String(memberId)]||{};
    const team=old.teamName||info.team||'';
    const dir=old.entryDirection||info.direction||'';
    const floor=old.activityFloor||info.floor||'';
    const detail=old.detailLocation||info.detail||'';
    const activityNo=Number(old.teamActivityNo||info.activityNo||m.entryCount||1)||1;
    const teams=[...new Set((window.__dashboardInsideMembers||[]).map(x=>{try{return v19TeamInfo(x).team}catch(e){return x.team||''}}).filter(Boolean))];
    if(team&&!teams.includes(team))teams.push(team);
    teams.sort((a,b)=>{try{return v19TeamNumber(a)-v19TeamNumber(b)}catch(e){return String(a).localeCompare(String(b))}});
    const floors=['','옥상','상층','직상층','화점층','직하층','하층','지하층'];
    const ov=r4Overlay(); if(!ov)return;
    ov.innerHTML='<div class="dashboardDetailSheet">'+
      '<div class="sheetHeader"><b>🛡️ 대원정보 수정</b><button type="button" id="r4MemberClose" class="sheetClose">×</button></div>'+ 
      '<div class="sheetMemberTitle">'+r4Esc(typeof getMemberDisplay==='function'?getMemberDisplay(memberId,memberName):memberName||memberId)+'</div>'+ 
      '<div class="v251R4CurrentState">현재 상태: '+(m.isolated?'🚨 고립대원':'정상')+' · 위치와 고립상태를 한 번에 반영합니다.</div>'+ 
      '<div class="locationEditForm">'+
        '<label>조 편성<select id="r4MemberTeam"><option value="">현재 조 유지</option>'+teams.map(v=>'<option value="'+r4Attr(v)+'" '+(v===team?'selected':'')+'>'+r4Esc(v)+'</option>').join('')+'</select></label>'+ 
        '<label>진입방면<select id="r4MemberDirection"><option value="">현재 위치 유지</option>'+['A방면','B방면','C방면','D방면'].map(v=>'<option value="'+v+'" '+(v===dir?'selected':'')+'>'+v+'</option>').join('')+'</select></label>'+ 
        '<label>활동층<select id="r4MemberFloor">'+floors.map(v=>'<option value="'+r4Attr(v)+'" '+(v===floor?'selected':'')+'>'+(v||'현재 위치 유지')+'</option>').join('')+'</select></label>'+ 
        '<label>세부장소<input id="r4MemberDetail" value="'+r4Attr(detail)+'" placeholder="예: 기계실 / 1203호 / 계단실"></label>'+ 
        '<div class="v251R4IsoBox"><label>고립상태</label><select id="r4MemberIsolation"><option value="KEEP">변경없음</option><option value="Y">🚨 고립대원 지정</option><option value="N">✅ 고립상태 해제</option></select></div>'+ 
      '</div>'+ 
      '<div class="v251R4FormNote">위치와 고립상태를 한 번의 반영으로 저장합니다.</div>'+ 
      '<button type="button" id="r4MemberSave" class="sheetSave v251R4Save">개별 안전관리 반영</button>'+ 
      '</div>';
    ov.classList.add('show');
    document.getElementById('r4MemberClose').onclick=()=>ov.classList.remove('show');
    document.getElementById('r4MemberSave').onclick=async function(){
      const extra={team:document.getElementById('r4MemberTeam').value,activityNo:String(activityNo),direction:document.getElementById('r4MemberDirection').value,floor:document.getElementById('r4MemberFloor').value,detail:document.getElementById('r4MemberDetail').value,isolationMode:document.getElementById('r4MemberIsolation').value};
      const d=await r4Post('updateSafetyManagement',[memberId],extra,this);
      if(d)setTimeout(()=>ov.classList.remove('show'),350);
    };
  };

  // 조 카드: 조 안전관리 + 조 전체 안전확인. 고립은 조 안전관리 안으로 통합
  window.openDashboardTeamLocationEdit=function(team){
    const members=(window.__dashboardInsideMembers||[]).filter(m=>(typeof v251TeamName==='function'?v251TeamName(m):teamInfo(m).team)===team);
    if(!members.length){alert('해당 조의 현재 활동대원을 찾지 못했습니다.');return;}
    const ov=r4Overlay(); if(!ov)return;
    const first=teamInfo(members[0]);
    ov.innerHTML='<div class="dashboardDetailSheet"><div class="sheetHeader"><b>🛡️ '+r4Esc(team)+' · 조·대원 안전관리</b><button type="button" id="r4TeamMenuClose" class="sheetClose">×</button></div>'+ 
      '<div class="v237TeamMoveTitle">'+r4Esc(team)+' · '+members.length+'명</div>'+ 
      '<div class="v237TeamMoveSub">'+r4Esc((first.direction||'미지정')+' · '+(first.floor||'미지정')+' · '+(first.detail||'세부장소 미지정'))+'</div>'+ 
      '<div class="v251ManageActions"><button type="button" id="r4TeamManage" class="sheetEdit">🛡️ 조 안전관리</button><button type="button" id="r4TeamSafety" class="v251SafetyBtn">✅ 조 전체 안전확인</button><button type="button" id="r4TeamMenuDone" class="v237CloseBtn">닫기</button></div></div>';
    ov.classList.add('show');
    const close=()=>ov.classList.remove('show');
    document.getElementById('r4TeamMenuClose').onclick=close;document.getElementById('r4TeamMenuDone').onclick=close;
    document.getElementById('r4TeamManage').onclick=()=>v251R4OpenTeamSafety(team);
    document.getElementById('r4TeamSafety').onclick=()=>{if(typeof v251SafetyCheckIds==='function')v251SafetyCheckIds(members.map(m=>m.memberId));};
  };

  // 개별 상세: 개별 안전관리 + 개별 안전확인. 별도 고립 버튼은 제거
  const prevDetail=window.openDashboardMemberDetail;
  if(typeof prevDetail==='function'){
    window.openDashboardMemberDetail=function(memberId,memberName){
      prevDetail(memberId,memberName);
      const actions=document.querySelector('#dashboardDetailOverlay .sheetActions');if(!actions)return;
      const edit=actions.querySelector('#v238MemberEditBtn');
      if(edit){edit.textContent='🛡️ 개별 안전관리';edit.onclick=function(ev){if(ev)ev.preventDefault();v251R4OpenMemberSafety(memberId,memberName);};}
      const iso=document.getElementById('v251MemberIsolationBtn');if(iso)iso.remove();
      const safe=document.getElementById('v251MemberSafetyBtn');if(safe)safe.textContent='✅ 개별 안전확인';
    };
  }

  // 혹시 남아있는 고립 단독 호출도 반영중 표시 + R4 최적화 서버 action 사용
  window.v251IsolationIds=async function(ids,isolated,label){
    if(!ids||!ids.length)return;
    if(!confirm((label||ids.length+'명')+'을 '+(isolated?'고립대원으로 지정':'고립상태 해제')+'하시겠습니까?'))return;
    const d=await r4Post('setIsolationBatch',ids,{isolated:isolated?'Y':'N'},null);
    return d;
  };
})();
</script>
'''
    s=s.replace('</head>',css+'</head>',1)
    s=s.replace('</body>',js+'</body>',1)

# Required validations
checks=['V2.51-R4','조 안전관리','개별 안전관리','대원정보 수정','updateSafetyManagement','⏳ 반영중...']
for c in checks:
    if c not in s: raise SystemExit('missing '+c)
p.write_text(s,encoding='utf-8')
print('patched V2.51-R4')
