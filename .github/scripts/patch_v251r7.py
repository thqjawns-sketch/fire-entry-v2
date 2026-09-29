from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('QR기반-진·출입 안전관리앱 V2.51-R6','QR기반-진·출입 안전관리앱 V2.51-R7')
insert=r'''

<!-- V2.51-R7 combined 31min/isolation confirmation summary -->
<style id="v251r7-style">
#v251R5SafetyAlert,#v251R6IsolationAlert{display:none!important}
</style>
<script>
(function(){
  function r7RemoveDuplicateAlerts(){
    const a=document.getElementById('v251R5SafetyAlert'); if(a)a.remove();
    const b=document.getElementById('v251R6IsolationAlert'); if(b)b.remove();
  }
  function r7UpdateCriticalSummary(){
    const box=document.getElementById('criticalSummary'); if(!box)return;
    const list=window.__dashboardInsideMembers||[];
    const over=list.filter(m=>Number(m.currentMinutes)>=31);
    const due=over.filter(m=>{try{return !!v251MemberSafetyState(m).due;}catch(e){return true;}});
    const iso=list.filter(m=>!!m.isolated);
    const targets=new Set();
    due.forEach(m=>targets.add(String(m.memberId)));
    iso.forEach(m=>targets.add(String(m.memberId)));

    box.classList.remove('v251StableCritical','hasCritical');
    if(iso.length>0){
      box.classList.add('hasCritical');
      const parts=[];
      if(due.length)parts.push('31분 이상 '+due.length+'명');
      parts.push('고립대원 '+iso.length+'명');
      box.textContent='🚨 확인대상 '+targets.size+'명 · '+parts.join(' · ');
    }else if(due.length>0){
      box.classList.add('hasCritical');
      box.textContent='⚠️ 안전확인 필요 '+due.length+'명 · 확인 후 10분 재확인';
    }else if(over.length>0){
      box.classList.add('v251StableCritical');
      box.textContent='🔴 31분 이상 '+over.length+'명 · 안전확인 완료';
    }else{
      box.textContent='✅ 31분 이상 또는 고립대원 확인대상 0명';
    }
  }
  window.v251UpdateCriticalSummary=r7UpdateCriticalSummary;
  document.addEventListener('DOMContentLoaded',function(){
    setTimeout(function(){r7RemoveDuplicateAlerts();r7UpdateCriticalSummary();},300);
  });
  setInterval(function(){r7RemoveDuplicateAlerts();r7UpdateCriticalSummary();},10000);
})();
</script>
'''
if '<!-- V2.51-R7 combined 31min/isolation confirmation summary -->' not in s:
    s=s.replace('</body>',insert+'\n</body>')
p.write_text(s,encoding='utf-8')
print('patched V2.51-R7')
