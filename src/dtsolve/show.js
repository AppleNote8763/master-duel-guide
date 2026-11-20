const E=require('./engine.js'); const fs=require('fs');
const d=JSON.parse(fs.readFileSync('../bundle_dt.json','utf8'));
const id=process.argv[2], top=+(process.argv[3]||1), lim=+(process.argv[4]||30000);
const c=d.combos.find(x=>x.id===id); const dk=d.decks[c.deck]; const main={},extra={}; for(const [n,v] of dk.main) main[n]=v; for(const [n,v] of dk.extra) extra[n]=v;
const r=E.search(c.steps[0].hand,main,extra,{maxMs:lim,maxStates:6000000});
console.log('states',r.states,r.done,r.ms,'boards',r.results.length);
for(const x of r.results.slice(0,top)){ console.log('\n== 점수',x.score,x.kind,'| 필드',x.field.join(' · '),'| 세트',x.set.join('·'),'| 패',x.handCards.join('·'));
  for(const i of x.items) console.log('   *',i[0],'['+i[1]+']');
  x.steps.forEach((s,i)=>console.log('  ',i+1,s.title,'|',s.act,'|',s.desc)); x.end.forEach(s=>console.log('   E',s.title,'|',s.desc)); }
