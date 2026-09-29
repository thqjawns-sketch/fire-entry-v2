from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

if 'V2.51-R5 COMMANDER CLEANUP' in s:
    print('already patched')
    raise SystemExit(0)

if 'V2.51-R4' not in s:
    raise SystemExit('V2.51-R4 marker not found')

s=s.replace('V2.51-R4','V2.51-R5')

css=r'''
<style id="v251r5-style">
/* ===== V2.51-R5 2번화면 즉시확인 가시성 + 지휘관 고립표시 정리 ===== */
.v251R5SafetyAlert{
  margin:0 0 12px;padding:15px 14px;border-radius:11px;text-align:center;
  font-size:18px;font-weight:950;line-height:1.35;border:2px solid #188038;
  background:#eef9f1;color:#137333;
}
.v251R5SafetyAlert.due{
  border-color:#b42318;background:#d93025;color:#fff;animation:dangerBlink 1s infinite;
}
.v251R5SafetyAlert.confirmed{
  border-color:#d93025;background:#fce8e6;color:#b3261e;animation:none;
}
#v250BoardEmergency.v251R5IsolationPanel{
  display:block!important;width:100%;box-sizing:border-box;margin-top:10px!important;padding:12px!important;
  border:2px solid #d93025!important;border-radius:12px!important;background:#fff7f7!important;
  color:#1f2937!important;text-align:left!important;font-weight:800!important;animation:none!important;
}
.v251R5IsolationHead{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:9px}
.v251R5IsolationTitle{font-size:18px;font-weight:950;color:#9f1d16}
.v251R5IsolationCount{
  flex:0 0 auto;padding:5px 10px;border-radius:999px;background:#d93025;color:#fff;
  font-size:14px;font-weight:950;animation:dangerBlink 1s infinite;
}
.v251R5IsolationGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.v251R5IsolationItem{
  min-width:0;padding:9px 11px;border:1px solid #efb7b3;border-left:5px solid #d93025;
  border-radius:9px;background:#fff;line-height:1.35;
}
.v251R5IsolationName{font-size:15px;font-weight:950;color:#8b1e18;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.v251R5IsolationMeta{margin-top:4px;font-size:12px;font-weight:850;color:#5a6673;white-space:normal}
/* 지휘관 화면은 큰 카드 전체가 깜빡이지 않고 고립 배지만 깜빡이게 */
#teamBoardPageV29 .v250CommanderTeamCard.v251IsolationBlink{
  animation:none!important;background:#fff5f5!important;border-color:#d93025!important;border-left:7px solid #b42318!important;
}
#teamBoardPageV29 .v250CommanderTeamCard.v251IsolationBlink .v250CommanderTeamBadge.isolated{
  animation:dangerBlink 1s infinite!important;
}
#teamBoardPageV29 .v33FaceChip.v251IsolationBlink{
  animation:none!important;background:#fff0f0!important;color:#b42318!important;border:2px solid #d93025!important;
}
@media(max-width:760px){.v251R5IsolationGrid{grid-template-columns:1fr}}
</style>
'''
marker='<link rel="manifest" href="./manifest.json">'
if marker not in s:
    raise SystemExit('manifest marker not found')
s=s.replace(marker,css+'\n'+marker,1)

js=r'''
<!-- V2.51-R5 COMMANDER CLEANUP -->
<script>
(function(){
  function esc(v){return typeof escapeHtml==='function'?escapeHtml(String(v??'')):String(v??'').replace(/[&<>"']/g,function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m];});}

  function ensureSafetyAlert(){
    let el=document.getElementById('v251R5SafetyAlert');
    if(el)return el;
    const officer=document.querySelector('.v251OfficerBox');
    if(!officer||!officer.parentNode)return null;
    el=document.createElement('div');
    el.id='v251R5SafetyAlert';
    el.className='v251R5SafetyAlert';
    officer.parentNode.insertBefore(el,officer);
    return el;
  }

  function renderSafetyAlert(){
    const el=ensureSafetyAlert(); if(!el)return;
    const list=window.__dashboardInsideMembers||[];
    const over=list.filter(function(m){return Number(m.currentMinutes)>=31;});
    const due=over.filter(function(m){try{return !!v251MemberSafetyState(m).due;}catch(e){return true;}});
    el.className='v251R5SafetyAlert';
    if(due.length){
      el.classList.add('due');
      el.textContent='🚨 31분 이상 즉시 확인 대상 '+due.length+'명';
    }else if(over.length){
      el.classList.add('confirmed');
      el.textContent='🔴 31분 이상 '+over.length+'명 · 안전확인 완료';
    }else{
      el.textContent='✅ 31분 이상 즉시 확인 대상 0명';
    }
  }

  function renderIsolationPanel(members){
    const emergency=document.getElementById('v250BoardEmergency'); if(!emergency)return;
    const iso=(members||window.__dashboardInsideMembers||[]).filter(function(m){return !!m.isolated;});
    if(!iso.length){
      emergency.className='';
      emergency.style.display='none';
      emergency.innerHTML='';
      return;
    }
    emergency.className='v251R5IsolationPanel';
    emergency.style.display='block';
    const items=iso.map(function(m){
      const display=(typeof getMemberDisplay==='function'?getMemberDisplay(m.memberId,m.memberName):m.memberName)||m.memberId||'';
      const parts=String(display).split(' / ');
      const name=parts.shift()||display;
      const org=parts.join(' / ');
      const floor=m.floor||'미지정';
      const dir=m.direction||'미지정';
      const meta=[org,floor,dir].filter(Boolean).join(' · ');
      return '<div class="v251R5IsolationItem"><div class="v251R5IsolationName">🚨 '+esc(name)+'</div><div class="v251R5IsolationMeta">'+esc(meta)+'</div></div>';
    }).join('');
    emergency.innerHTML='<div class="v251R5IsolationHead"><div class="v251R5IsolationTitle">고립대원 현황</div><div class="v251R5IsolationCount">🚨 '+iso.length+'명</div></div><div class="v251R5IsolationGrid">'+items+'</div>';
  }

  if(typeof window.v251UpdateCriticalSummary==='function'){
    const baseCritical=window.v251UpdateCriticalSummary;
    window.v251UpdateCriticalSummary=function(){
      const r=baseCritical.apply(this,arguments);
      renderSafetyAlert();
      return r;
    };
  }

  if(typeof window.v250RenderBoardSummary==='function'){
    const baseBoard=window.v250RenderBoardSummary;
    window.v250RenderBoardSummary=function(members){
      const r=baseBoard.apply(this,arguments);
      renderIsolationPanel(members);
      return r;
    };
  }

  document.addEventListener('DOMContentLoaded',function(){setTimeout(function(){renderSafetyAlert();renderIsolationPanel(window.__dashboardInsideMembers||[]);},300);});
  setInterval(function(){renderSafetyAlert();},10000);
})();
</script>
'''
if '</body>' not in s:
    raise SystemExit('body close not found')
s=s.replace('</body>',js+'\n</body>',1)

p.write_text(s,encoding='utf-8')
print('patched V2.51-R5')
