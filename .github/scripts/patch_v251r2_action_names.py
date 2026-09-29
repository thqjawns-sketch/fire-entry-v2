from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('QR기반-진·출입 안전관리앱 V2.51-R1','QR기반-진·출입 안전관리앱 V2.51-R2')
s=s.replace("v251Post('batchSetIsolation'","v251Post('setIsolationBatch'")
s=s.replace("v251Post('batchSafetyCheck'","v251Post('setSafetyCheck'")
assert "batchSetIsolation" not in s
assert "batchSafetyCheck" not in s
assert "setIsolationBatch" in s
assert "setSafetyCheck" in s
p.write_text(s,encoding='utf-8')
print('patched V2.51-R2 action names')
