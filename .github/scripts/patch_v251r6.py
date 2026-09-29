from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('QR기반-진·출입 안전관리앱 V2.51-R5','QR기반-진·출입 안전관리앱 V2.51-R6')
s=s.replace('🚒 QR기반-진·출입 안전관리앱 V2.51-R5','🚒 QR기반-진·출입 안전관리앱 V2.51-R6')
insert=r'''

<style id="v251r6-style">
/* ===== V2.51-R6 고립대원 요약표시 정리 ===== */
#v251R5SafetyAlert{display:none!important}
.v251R6IsolationAlert{
  margin:10px 0 0;padding:14px;border-radius:10px;text-align:center;
  font-size:18px;font-weight:950;line-height:1.35;border:2px solid #188038;
  background:#eef9f1;color:#137333;
}
.v251R6IsolationAlert.hasIsolation{
  border-color:#8b0000;background:#d93025;color:#fff;animation:dangerBlink 1s infinite;
}
#teamBoardPageV29 .v250CommanderTeamCard.v251IsolationBlink,
#teamBoardPageV29 .v33FaceChip.v251IsolationBlink{
  animation:none!important;
}
#teamBoardPageV29 .v250CommanderTeamCard.v251IsolationBlink{
  border-left-color:#8b0000!important;background:#fff4f4!important;
}
#teamBoardPageV29 .v33FaceChip.v251IsolationBlink{
  outline:3px solid #b42318!important;background:#fff0f0!important;color:#b42318!important;
}
#v250BoardEmergency.v251R6IsolationPanel{
  display:block!important;width:100%;box-sizing:border-box;margin-top:10px!important;
  padding:0!important;border:0!important;background:transparent!important;color:inherit!important;
}
.v251R6IsolationHead{
  padding:13px 14px;border-radius:11px;background:#d93025;color:#fff;
  font-size:20px;font-weight:950;text-align:center;animation:dangerBlink 1s infinite;
}
.v251R6IsolationList{
  display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:8px;
}
.v251R6IsolationPerson{
  padding:10px 12px;border:1px solid #e5b2b2;border-left:5px solid #b42318;border-radius:10px;
  background:#fff7f7;color:#263445;line-height:1.45;
}
.v251R6IsolationName{font-size:15px;font-weight:950;color:#8b0000}
.v251R6IsolationLoc{margin-top:3px;font-size:13px;font-weight:800;color:#5d4b4b}
@media(max-width:760px){.v251R6IsolationList{grid-template-columns:1fr}}
</style>
<script>
(function(){
  function esc(v){return typeof escapeHtml==='function'?escapeHtml(String(v??'')):String(v??'').replace(/[&<>"']/g,function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m];});}

  function ensureIsolationAlert(){
    let el=document.getElementById('v251R6IsolationAlert');
    if(el)return el;
    const base=document.getElementById('criticalSummary');
    if(!base||!base.parentNode)return null;
    el=document.createElement('div');
    el.id='v251R6IsolationAlert';
    el.className='v251R6IsolationAlert';
    base.parentNode.insertBefore(el,base.nextSibling);
    return el;
  }

  function renderIsolationAlert(){
    const el=ensureIsolationAlert(); if(!el)return;
    const iso=(window.__dashboardInsideMembers||[]).filter(function(m){return !!m.isolated;});
    el.className='v251R6IsolationAlert'+(iso.length?' hasIsolation':'');
    el.textContent=iso.length ? ('🚨 고립대원 '+iso.length+'명') : '✅ 고립대원 0명';
  }

  function renderCommanderIsolation(members){
    const emergency=document.getElementById('v250BoardEmergency'); if(!emergency)return;
    const iso=(members||window.__dashboardInsideMembers||[]).filter(function(m){return !!m.isolated;});
    if(!iso.length){emergency.className='';emergency.style.display='none';emergency.innerHTML='';return;}
    emergency.className='v251R6IsolationPanel';
    emergency.style.display='block';
    const cards=iso.map(function(m){
      const name=typeof getMemberDisplay==='function'?getMemberDisplay(m.memberId,m.memberName||m.name||''):String(m.memberName||m.name||m.memberId||'');
      const team=(typeof v251TeamName==='function'?v251TeamName(m):(m.team||'미지정'))||'미지정';
      const floor=m.floor||m.activityFloor||'미지정';
      const dir=m.direction||m.entryDirection||'미지정';
      return '<div class="v251R6IsolationPerson"><div class="v251R6IsolationName">🚨 '+esc(name)+'</div><div class="v251R6IsolationLoc">'+esc(team)+' · '+esc(floor)+' · '+esc(dir)+'</div></div>';
    }).join('');
    emergency.innerHTML='<div class="v251R6IsolationHead">🚨 고립대원 '+iso.length+'명</div><div class="v251R6IsolationList">'+cards+'</div>';
  }

  const oldRefresh=window.v251RefreshEnhancements;
  if(typeof oldRefresh==='function'){
    window.v251RefreshEnhancements=function(){
      const r=oldRefresh.apply(this,arguments);
      setTimeout(renderIsolationAlert,0);
      return r;
    };
  }
  const oldBoard=window.v250RenderBoardSummary;
  if(typeof oldBoard==='function'){
    window.v250RenderBoardSummary=function(members){
      const r=oldBoard.apply(this,arguments);
      renderCommanderIsolation(members);
      return r;
    };
  }
  document.addEventListener('DOMContentLoaded',function(){setTimeout(function(){renderIsolationAlert();renderCommanderIsolation(window.__dashboardInsideMembers||[]);},300);});
  setInterval(renderIsolationAlert,10000);
})();
</script>
'''
if '<!-- V2.51-R6 isolation summary -->' not in s:
    s=s.replace('</body>', '<!-- V2.51-R6 isolation summary -->'+insert+'\n</body>')
p.write_text(s,encoding='utf-8')
print('patched', len(s))
