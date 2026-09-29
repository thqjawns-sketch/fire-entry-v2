from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

if 'V2.51-R2' not in s:
    raise SystemExit('expected V2.51-R2 title not found')
s=s.replace('V2.51-R2','V2.51-R3',1)

old="const DASHBOARD_AUTO_REFRESH_MS =\n60000;"
if old not in s:
    raise SystemExit('auto refresh constant not found')
s=s.replace(old,"const DASHBOARD_AUTO_REFRESH_MS =\n10000;",1)
s=s.replace('60초 자동갱신','10초 자동갱신')
s=s.replace('현장 현황 60초 자동갱신','현장 현황 10초 자동갱신')
s=s.replace('그 다음부터 60초마다 자동갱신','그 다음부터 10초마다 자동갱신')
s=s.replace('60초 자동갱신 시작','10초 자동갱신 시작')
s=s.replace('60초 자동갱신 중지','10초 자동갱신 중지')

old_css='.v250Isolated{outline:4px solid #b42318!important;background:#fff0f0!important;box-shadow:0 0 0 3px #ffd2d2 inset!important;cursor:pointer}.v250Isolated .memberLine{color:#b42318!important;font-weight:950!important}'
new_css='.v250Isolated{outline:4px solid #b42318!important;cursor:pointer}.v250Isolated .memberLine{font-weight:950!important}'
if old_css not in s:
    raise SystemExit('v250Isolated css not found')
s=s.replace(old_css,new_css,1)

old_blink='.v251IsolationBlink{animation:dangerBlink .8s infinite!important;outline:4px solid #8b0000!important}'
new_blink='.v251IsolationBlink{animation:dangerBlink 1s infinite!important;outline:none!important;box-shadow:none!important}.v251IsolationBlink .memberLine,.v251IsolationBlink .insideStatus{color:inherit!important}'
if old_blink not in s:
    raise SystemExit('isolation blink css not found')
s=s.replace(old_blink,new_blink,1)

old_post="""    if(typeof closeDashboardMemberDetail==='function')closeDashboardMemberDetail();
    await loadDashboard(false);
    v251RefreshEnhancements();
    return d;
"""
new_post="""    if(typeof closeDashboardMemberDetail==='function')closeDashboardMemberDetail();
    if(action!=='setIsolationBatch'){
      await loadDashboard(false);
    }
    v251RefreshEnhancements();
    return d;
"""
if old_post not in s:
    raise SystemExit('v251Post refresh block not found')
s=s.replace(old_post,new_post,1)

old_fn="""async function v251IsolationIds(ids,isolated,label){
  if(!ids||!ids.length)return;
  if(!confirm((label||ids.length+'명')+'을 '+(isolated?'고립대원으로 지정':'고립상태 해제')+'하시겠습니까?'))return;
  await v251Post('setIsolationBatch',ids,{isolated:isolated?'Y':'N'});
}
"""
new_fn="""async function v251IsolationIds(ids,isolated,label){
  if(!ids||!ids.length)return;
  if(!confirm((label||ids.length+'명')+'을 '+(isolated?'고립대원으로 지정':'고립상태 해제')+'하시겠습니까?'))return;

  const wanted=new Set((ids||[]).map(v=>String(v)));
  const list=window.__dashboardInsideMembers||[];
  const prev=[];
  list.forEach(m=>{
    if(!wanted.has(String(m.memberId)))return;
    prev.push({m:m,isolated:!!m.isolated,isolatedAt:m.isolatedAt||'',isolatedOfficer:m.isolatedOfficer||''});
    m.isolated=!!isolated;
    if(isolated){
      m.isolatedAt=new Date().toISOString();
      m.isolatedOfficer=v251GetOfficer? v251GetOfficer() : (document.getElementById('v251StatusOfficer')||{}).value||'';
    }else{
      m.isolatedAt='';
    }
  });

  v251RefreshEnhancements();
  const d=await v251Post('setIsolationBatch',ids,{isolated:isolated?'Y':'N'});
  if(!d){
    prev.forEach(x=>{x.m.isolated=x.isolated;x.m.isolatedAt=x.isolatedAt;x.m.isolatedOfficer=x.isolatedOfficer;});
    v251RefreshEnhancements();
  }
}
"""
if old_fn not in s:
    raise SystemExit('v251IsolationIds function not found')
s=s.replace(old_fn,new_fn,1)

p.write_text(s,encoding='utf-8')
print('patched V2.51-R3')
