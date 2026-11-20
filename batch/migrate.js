// main 의 site/batch 에서 목록(manifest)에 있는 파일만 결과 전용 폴더로 옮긴다.  node migrate.js <site/batch> <pub/batch>
const fs = require('fs'), path = require('path');
const [src, dst] = [process.argv[2], process.argv[3]]; let n = 0;
if (!fs.existsSync(src)) { console.log('옮길 것이 없음'); process.exit(0); }
for (const m of fs.readdirSync(src).filter(x => /-manifest-.*\.json$/.test(x))) { const man = JSON.parse(fs.readFileSync(path.join(src, m), 'utf8'));
  fs.copyFileSync(path.join(src, m), path.join(dst, m));
  for (const f of man.files || []) if (fs.existsSync(path.join(src, f.name))) { fs.copyFileSync(path.join(src, f.name), path.join(dst, f.name)); n++; } }
console.log('옮긴 조각', n);
