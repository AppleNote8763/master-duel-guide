const E=require('./engine.js'); const fs=require('fs');
const d=JSON.parse(fs.readFileSync('../bundle_dt.json','utf8'));
const want=process.argv[2]; const lim=+(process.argv[3]||30000);
const known=new Set(Object.values(E.N)); known.add('패사고'); known.add('패의 드래곤테일 이외 몬스터');
const inGroups=new Set(d.custom.groups.flatMap(g=>g.items.map(i=>i[0])));
let ok=0,bad=0,skip=0;
for(const c of d.combos){ if(!inGroups.has(c.id)) continue; if(want&&want!=='all'&&c.id!==want) continue;
  const dk=d.decks[c.deck]; const hand=c.steps[0].hand; const last=c.steps[c.steps.length-1];
  const names=[...hand,...Object.values(last.zones).map(z=>z.name),...last.hand];
  const un=names.filter(n=>!known.has(n)); if(un.length){skip++; if(want)console.log('SKIP',c.id,[...new Set(un)].join(',')); continue;}
  const main={},extra={}; for(const [n,v] of dk.main) main[n]=v; for(const [n,v] of dk.extra) extra[n]=v; const rq=d.custom.req[c.id]||{main:{},extra:{}}; for(const n in rq.main) main[n]=Math.max(main[n]||0,rq.main[n]); for(const n in rq.extra) extra[n]=Math.max(extra[n]||0,rq.extra[n]);
  const r=E.search(hand,main,extra,{maxMs:lim,maxStates:6000000});
  let tf=Object.entries(last.zones).filter(([z])=>z[0]!=='S').map(([z,v])=>v.name).sort().join(','), ts0=Object.entries(last.zones).filter(([z])=>z[0]==='S').map(([z,v])=>v.name); const TR=['드래곤테일 플레임','드래곤테일 혼','드래곤테일 스팅']; const nt=ts0.filter(n=>TR.includes(n)).length; const TRA=TR.filter(n=>(main[n]||0)>0); const ts=ts0.filter(n=>!TR.includes(n)).concat(TRA.slice(0,nt)).sort().join(',');
  const hit=r.results.find(x=>x.field.slice().sort().join(',')===tf && x.set.slice().sort().join(',')===ts);
  const best=r.results[0];
  if(hit){ok++; console.log('OK ',c.id,c.title,'| states',r.states,r.done?'':'(중단)',r.ms+'ms','| 가이드판 점수',hit.score,'최고',best.score);}
  else {bad++; console.log('MISS',c.id,c.title,'| states',r.states,r.done?'':'(중단)',r.ms+'ms','| 목표',tf,'/',ts,'| 최고',best&&best.score,best&&best.field.join(','),'/',best&&best.set.join(','));}
}
console.log('ok',ok,'miss',bad,'skip',skip);
