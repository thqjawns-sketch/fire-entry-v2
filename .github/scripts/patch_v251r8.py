from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Version
s=s.replace('V2.51-R7','V2.51-R8')

# First screen isolated firefighter: use same blink class as screen 2.
s=s.replace('row.className="memberRow "+stay.className+(member.isolated?" v250Isolated":"");',
            'row.className="memberRow "+stay.className+(member.isolated?" v250Isolated v251IsolationBlink":"");')

# Also let enhancement pass include the first-screen current-inside list.
s=s.replace("['dashboardInside','v34FloorMembers'].forEach(rootId=>{",
            "['insideList','dashboardInside','v34FloorMembers'].forEach(rootId=>{")

# Team safety: derive the actual current location from live member data/meta, not v19TeamInfo alone.
old="function teamInfo(m){try{return v19TeamInfo(m);}catch(e){return {team:m.team||'',activityNo:m.activityNo||m.entryCount||1,direction:m.direction||'',floor:m.floor||'',detail:m.detail||''};}}"
new="""function teamInfo(m){
    let base={}; try{base=v19TeamInfo(m)||{};}catch(e){}
    let vm={}; try{vm=(v23LoadMeta&&v23LoadMeta()[String(m.memberId)])||{};}catch(e){}
    return {
      team:base.team||m.team||vm.teamName||'',
      activityNo:Number(base.activityNo||m.activityNo||m.entryCount||vm.teamActivityNo||1)||1,
      direction:m.direction||m.entryDirection||vm.entryDirection||'',
      floor:m.floor||m.activityFloor||vm.activityFloor||'',
      detail:m.detail||m.detailLocation||vm.detailLocation||''
    };
  }"""
if old not in s:
    raise SystemExit('teamInfo target not found')
s=s.replace(old,new,1)

# Current-value labels in team safety dialog.
s=s.replace('<label>방면<select id=\"r4TeamDirection\"><option value=\"\">현재 위치 유지</option>',
            '<label>방면<select id=\"r4TeamDirection\"><option value=\"\">미지정</option>')
s=s.replace("+(v||'현재 위치 유지')+", "+(v||'미지정')+")

# R4 write response: update local state immediately and refresh server state in background.
needle="""  async function r4Post(action,ids,extra,btn){"""
helper="""  function r8ApplyServerResult(d){
    const rows=(d&&d.succeeded)||[];
    if(!rows.length)return;
    const members=window.__dashboardInsideMembers||[];
    let meta={}; try{meta=v23LoadMeta?v23LoadMeta():{};}catch(e){meta={};}
    rows.forEach(function(x){
      const id=String(x.id||x.memberId||'');
      const m=members.find(function(v){return String(v.memberId)===id;});
      if(m){
        if(x.team!==undefined)m.team=x.team;
        if(x.activityNo!==undefined)m.activityNo=x.activityNo;
        if(x.direction!==undefined){m.direction=x.direction;m.entryDirection=x.direction;}
        if(x.floor!==undefined){m.floor=x.floor;m.activityFloor=x.floor;}
        if(x.detail!==undefined){m.detail=x.detail;m.detailLocation=x.detail;}
        if(x.isolated!==undefined)m.isolated=!!x.isolated;
        if(x.isolatedAt!==undefined)m.isolatedAt=x.isolatedAt||'';
        if(x.isolatedOfficer!==undefined)m.isolatedOfficer=x.isolatedOfficer||'';
      }
      if(id){
        const v=meta[id]||(meta[id]={});
        if(x.team!==undefined)v.teamName=x.team;
        if(x.activityNo!==undefined)v.teamActivityNo=x.activityNo;
        if(x.direction!==undefined)v.entryDirection=x.direction;
        if(x.floor!==undefined)v.activityFloor=x.floor;
        if(x.detail!==undefined)v.detailLocation=x.detail;
      }
    });
    try{if(v23SaveMeta)v23SaveMeta(meta);}catch(e){}
  }

  async function r4Post(action,ids,extra,btn){"""
if needle not in s:
    raise SystemExit('r4Post target not found')
s=s.replace(needle,helper,1)

old_success="""      if(btn)btn.textContent='✅ 반영완료';
      r4Status('✅ 반영완료','done',1300);
      await loadDashboard(false);
      if(typeof v251RefreshEnhancements==='function')v251RefreshEnhancements();
      return d;"""
new_success="""      if(btn)btn.textContent='✅ 반영완료';
      r8ApplyServerResult(d);
      if(typeof v251RefreshEnhancements==='function')v251RefreshEnhancements();
      if(typeof drawTeamBoardV29==='function')try{drawTeamBoardV29();}catch(e){}
      r4Status('✅ 반영완료'+(d.serverMs?(' · 서버 '+(d.serverMs/1000).toFixed(1)+'초') : ''),'done',1500);
      setTimeout(function(){
        try{
          Promise.resolve(loadDashboard(false)).then(function(){
            if(typeof v251RefreshEnhancements==='function')v251RefreshEnhancements();
            if(typeof drawTeamBoardV29==='function')try{drawTeamBoardV29();}catch(e){}
          }).catch(function(){});
        }catch(e){}
      },250);
      return d;"""
if old_success not in s:
    raise SystemExit('r4 success block not found')
s=s.replace(old_success,new_success,1)

# Alarm + mute UI for screen 2/3 only. WebAudio is unlocked after first user interaction.
alarm='''\n\n<!-- V2.51-R8 warning sound manager -->\n<style id="v251r8-alarm-style">\n#v251R8AlarmMute{\n  position:fixed;right:14px;bottom:16px;z-index:32000;width:auto!important;min-width:150px;\n  margin:0!important;padding:10px 13px!important;border:1px solid #b42318!important;border-radius:999px!important;\n  background:#fff!important;color:#b42318!important;font-size:13px!important;font-weight:950!important;\n  box-shadow:0 3px 14px rgba(0,0,0,.18);display:none;\n}\n#v251R8AlarmMute.muted{border-color:#607387!important;color:#44546a!important;background:#f6f8fa!important}\n</style>\n<script>\n(function(){\n  let audioCtx=null, alarmMode='none', alarmStarted=0, lastBeepKey='', muteUntil=0;\n  function visible(id){\n    const el=document.getElementById(id);\n    return !!(el && getComputedStyle(el).display!=='none');\n  }\n  function alarmScreenVisible(){return visible('dashboardPage')||visible('teamBoardPageV29');}\n  function unlockAudio(){\n    try{\n      if(!audioCtx)audioCtx=new (window.AudioContext||window.webkitAudioContext)();\n      if(audioCtx.state==='suspended')audioCtx.resume();\n    }catch(e){}\n  }\n  ['pointerdown','touchstart','keydown'].forEach(function(ev){document.addEventListener(ev,unlockAudio,{passive:true});});\n\n  function currentAlarmMode(){\n    if(!alarmScreenVisible()||document.hidden)return 'none';\n    const list=window.__dashboardInsideMembers||[];\n    if(list.some(function(m){return !!m.isolated;}))return 'isolation';\n    const due=list.some(function(m){\n      if(Number(m.currentMinutes)<31)return false;\n      try{return !!(v251MemberSafetyState(m).due)&&!m.isolated;}catch(e){return true;}\n    });\n    return due?'safety':'none';\n  }\n  function tone(freq,duration,delay){\n    if(!audioCtx||audioCtx.state!=='running'||Date.now()<muteUntil)return;\n    try{\n      const osc=audioCtx.createOscillator(), gain=audioCtx.createGain();\n      const t=audioCtx.currentTime+(delay||0);\n      osc.type='sine';osc.frequency.setValueAtTime(freq,t);\n      gain.gain.setValueAtTime(0.0001,t);\n      gain.gain.exponentialRampToValueAtTime(0.055,t+0.025);\n      gain.gain.exponentialRampToValueAtTime(0.0001,t+duration);\n      osc.connect(gain);gain.connect(audioCtx.destination);osc.start(t);osc.stop(t+duration+0.03);\n    }catch(e){}\n  }\n  function beep(mode){\n    unlockAudio();\n    if(mode==='isolation'){tone(980,0.20,0);tone(1220,0.18,0.28);}\n    else{tone(820,0.20,0);}\n  }\n  function ensureMuteButton(){\n    let b=document.getElementById('v251R8AlarmMute');\n    if(b)return b;\n    b=document.createElement('button');b.type='button';b.id='v251R8AlarmMute';\n    b.onclick=function(){muteUntil=Date.now()+60000;lastBeepKey='';renderMuteButton();};\n    document.body.appendChild(b);return b;\n  }\n  function renderMuteButton(){\n    const b=ensureMuteButton(), mode=currentAlarmMode();\n    if(mode==='none'){b.style.display='none';return;}\n    b.style.display='block';\n    const remain=Math.max(0,Math.ceil((muteUntil-Date.now())/1000));\n    if(remain>0){b.classList.add('muted');b.textContent='🔇 '+remain+'초 후 경고음 재개';}\n    else{b.classList.remove('muted');b.textContent='🔇 경고음 1분 정지';}\n  }\n  function tick(){\n    const mode=currentAlarmMode();\n    if(mode!==alarmMode){alarmMode=mode;alarmStarted=Date.now();lastBeepKey='';}\n    renderMuteButton();\n    if(mode==='none'||Date.now()<muteUntil)return;\n    const activeMs=mode==='isolation'?10000:5000;\n    const cycleMs=30000;\n    const pos=(Date.now()-alarmStarted)%cycleMs;\n    if(pos>=activeMs)return;\n    const slot=Math.floor(pos/1000);\n    const key=mode+':'+Math.floor((Date.now()-alarmStarted)/cycleMs)+':'+slot;\n    if(key===lastBeepKey)return;\n    lastBeepKey=key;beep(mode);\n  }\n  setInterval(tick,250);\n  document.addEventListener('visibilitychange',function(){if(document.hidden)lastBeepKey='';});\n  document.addEventListener('DOMContentLoaded',function(){setTimeout(tick,400);});\n})();\n</script>\n'''
if '<!-- V2.51-R8 warning sound manager -->' not in s:
    s=s.replace('</body>',alarm+'\n</body>')

p.write_text(s,encoding='utf-8')
print('patched index.html to V2.51-R8')
