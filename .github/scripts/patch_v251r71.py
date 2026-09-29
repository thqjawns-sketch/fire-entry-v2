from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '''    }catch(e){
      const idx=entryQueue.findIndex(x=>String(x.id).trim()===memberId);
      if(idx>=0){ entryQueue.splice(idx,1); selectedTeamMemberIds.delete(memberId); renderQueue(); }
      showTemporaryMessage("⚠️ "+member.name+" 대원 활동상태 확인 실패 · 투입대기에서 제외했습니다.");
    }finally{ v249QueueAddPending.delete(memberId); }
'''

new = '''    }catch(e){
      console.warn("대원 활동상태 확인 지연",memberId,e);
      const idx=entryQueue.findIndex(x=>String(x.id).trim()===memberId);
      if(idx>=0){
        entryQueue[idx].__activeCheckPending=false;
        renderQueue();
      }
      showTemporaryMessage("⚠️ "+member.name+" 대원 활동상태 확인 지연 · 투입대기 유지");
    }finally{ v249QueueAddPending.delete(memberId); }
'''

if old not in s:
    raise SystemExit('target block not found')

s = s.replace(old, new, 1)
s = s.replace('QR기반-진·출입 안전관리앱 V2.51-R7</title>', 'QR기반-진·출입 안전관리앱 V2.51-R7.1</title>', 1)
s = s.replace('🚒 QR기반-진·출입 안전관리앱 V2.51-R7\n', '🚒 QR기반-진·출입 안전관리앱 V2.51-R7.1\n', 1)

p.write_text(s, encoding='utf-8')
print('Applied V2.51-R7.1 queue retention fix')
