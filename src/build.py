import json
data=json.load(open('data.json'))
html=r'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#121218;--pn:#1d1d26;--ln:#2e2e3a;--tx:#ececf2;--mu:#9a9aab;--ac:#f0c35a}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font-family:system-ui,-apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;font-size:14px}
.wrap{max-width:760px;margin:0 auto;padding:14px 12px 300px}
h1{font-size:19px;font-weight:800;margin:4px 2px 10px}
.tabs{display:flex;gap:6px;overflow-x:auto;padding-bottom:6px;scrollbar-width:none}
.tabs.drag{cursor:grabbing;user-select:none}.top{display:flex;align-items:center;gap:8px;margin:0 0 8px}.top:empty{display:none}.back{background:var(--pn);border:1px solid var(--ln);color:var(--tx);border-radius:9px;padding:7px 10px;font-size:13px;cursor:pointer}.dn{font-weight:800;font-size:15px}.lead{color:var(--mu);margin:4px 2px 10px}.dcard{display:block;width:100%;text-align:left;background:var(--pn);border:1px solid var(--ln);border-radius:14px;padding:14px;margin-bottom:10px;color:var(--tx);cursor:pointer}.dcard:hover{border-color:var(--ac)}.dcard b{display:block;font-size:16px;margin-bottom:4px}.dcard span{display:block;color:#cfcfda;font-size:13px;line-height:1.5;word-break:keep-all}.lnk{display:flex;flex-wrap:wrap;gap:6px;margin-top:7px}.lnk a{font-size:12px;color:#9cc4ff;background:#1b2433;border:1px solid #2c3d57;border-radius:7px;padding:4px 8px;text-decoration:none}.hd .lnk{margin-top:6px}
.dcard em{display:block;font-style:normal;color:var(--ac);font-size:12px;margin-top:6px}
.cats{display:grid;grid-template-columns:repeat(auto-fit,minmax(0,1fr));gap:4px;background:var(--pn);border:1px solid var(--ln);border-radius:12px;padding:4px;margin-bottom:8px}.cat{border:0;background:transparent;color:var(--mu);border-radius:9px;padding:9px 4px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap}.cat.on{background:var(--ac);color:#1a1a1a}.tab.on{background:#3a3220;color:var(--ac);border-color:var(--ac)}
.lv{font-size:11px;color:var(--mu);margin:2px 2px 5px;font-weight:700}.res2{display:flex;flex-direction:column;gap:5px;margin-bottom:10px}.rb{display:block;width:100%;text-align:left;background:var(--pn);border:1px solid var(--ln);color:var(--tx);border-radius:10px;padding:7px 11px;font-size:13px;cursor:pointer;line-height:1.4;word-break:keep-all}.rb small{display:block;color:var(--mu);font-size:11.5px;margin-top:2px}.rb.on{border-color:var(--ac);background:#2a2618}.rb.on b{color:var(--ac)}.br{margin-top:8px;font-size:12.5px;color:#cfe3c8;background:#1c2a1c;border:1px solid #2f4a2f;border-radius:9px;padding:7px 9px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}.br button{background:#2f4a2f;border:0;color:#e6f5e1;border-radius:7px;padding:4px 8px;font-size:12px;cursor:pointer}.dot.sh{opacity:.45}
.df{margin-top:9px;display:grid;gap:6px}.df .bx{border-radius:10px;padding:8px 9px;border:1px solid}.df .ad{background:#15281c;border-color:#2f5a3a}.df .rm{background:#2a1718;border-color:#5a2f33}.df h5{margin:0 0 5px;font-size:12.5px}.df .ad h5{color:#8fe0a6}.df .rm h5{color:#f19aa0}.df .ln{display:flex;gap:6px;align-items:flex-start;margin-top:4px;font-size:12px}.df .ln>em{flex:none;font-style:normal;color:var(--mu);width:58px;padding-top:3px}.df .cs{display:flex;flex-wrap:wrap;gap:4px}.df .k{font-size:12px;border-radius:6px;padding:2px 7px;background:#ffffff14;color:#f2f2f6;font-weight:700}.df .k.g{font-weight:400;color:#c4c4cf;background:#ffffff0b}.df .k i{font-style:normal;font-weight:400;font-size:11px;color:#bdbdc9}.df .k s{color:#ff8a8a;text-decoration:none;font-size:10.5px;margin-left:3px}.df .nt{font-size:11px;color:var(--mu);margin-top:2px}
.oth{background:#ffffff08;border:1px solid var(--ln);border-radius:10px;padding:7px 9px}.nt2{font-size:12px;color:#d4d4de;margin-bottom:3px;line-height:1.5}.dcard .oth b,.nt2 b{display:inline;font-size:12px;color:#fff;margin:0 4px 0 0}
.cn{font-weight:800}
.how{margin-top:8px;font-size:13px;line-height:1.55;color:#dadae4}.how p{margin:0 0 5px;word-break:keep-all}
.tab{flex:none;border:1px solid var(--ln);background:var(--pn);color:var(--tx);border-radius:999px;padding:7px 12px;font-size:13px;cursor:pointer}
.tab.on{font-weight:700}
.hd{margin:12px 2px 8px}.hd b{font-size:16px}.hd span{color:var(--mu);font-size:12.5px;display:block;margin-top:3px}
.board{background:#191922;border:1px solid var(--ln);border-radius:14px;padding:10px 8px}
.grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px}.z.pile{border-style:solid;border-color:#33334a;background:#14141c;flex-direction:column;overflow:hidden}.z.pile.chg{border-color:var(--ac);box-shadow:0 0 0 1px var(--ac)}.pile .pi{position:absolute;inset:0;background-size:100% 100%;opacity:.55}.pile .pl{position:relative;font-size:11px;word-break:keep-all;font-weight:800;color:#fff;text-shadow:0 1px 2px #000;text-align:center;line-height:1.2}.pile .pc{position:relative;font-size:20px;font-weight:800;color:var(--ac);text-shadow:0 1px 2px #000}.pile .pn{position:absolute;left:0;right:0;bottom:0;font-size:10px;line-height:1.15;padding:2px 2px 3px;background:#000b;color:#ffe08a;text-align:center;word-break:keep-all}
.z{aspect-ratio:65/94;border-radius:8px;border:1px dashed #3a3a48;position:relative;display:flex;align-items:center;justify-content:center;font-size:10px;color:#55556a}
.z.em{border-color:#5a4a20}.z.off{visibility:hidden}
.z.st{aspect-ratio:65/94}
.c{position:absolute;inset:0;border-radius:7px;padding:16px 4px 4px;font-size:10.5px;line-height:1.25;color:#141418;font-weight:700;word-break:keep-all;overflow-wrap:anywhere;overflow:hidden;border:2px solid transparent}
.c.ci{background-size:100% 100%;background-color:#000;padding:0;border-width:0}.c.ci .nm{position:absolute;left:0;right:0;bottom:0;padding:14px 3px 3px;font-size:9.5px;line-height:1.2;color:#fff;background:linear-gradient(transparent,rgba(0,0,0,.85) 45%);text-shadow:0 1px 2px #000}.c.ci .lk,.c.ci .mt{bottom:auto;top:auto;bottom:30px}.c.ci .nm{padding-top:8px;font-size:8px;line-height:1.15;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;word-break:keep-all}
.c .tg{position:absolute;left:0;right:0;top:0;z-index:2;background:rgba(10,10,14,.88);color:#ffd36b;font-size:8px;font-weight:700;line-height:1.2;padding:2px 3px;text-align:center;word-break:keep-all;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}.c .k{position:absolute;top:0;left:0;right:0;font-size:9px;color:#fff;padding:2px 4px;font-weight:700}
.c.chg{box-shadow:0 0 0 3px var(--ac)}
.c .lk{position:absolute;bottom:3px;right:3px;background:#0e6a3a;color:#fff;font-size:8.5px;padding:1px 4px;border-radius:4px}
.c .mt{position:absolute;bottom:3px;left:3px;background:#333;color:#fff;font-size:8.5px;padding:1px 4px;border-radius:4px}
.ar{position:absolute;width:0;height:0;border:5px solid transparent;z-index:2}
.lab{display:flex;justify-content:space-between;color:var(--mu);font-size:11px;margin:8px 2px 4px}
.zone-lbl{grid-column:1/-1;color:var(--mu);font-size:11px;margin:4px 2px 0}
.step{background:var(--pn);border:1px solid var(--ln);border-radius:14px;padding:12px 14px;margin-top:10px}
.step .n{color:var(--ac);font-weight:800;font-size:12px}
.step .t{font-size:16px;font-weight:800;margin:3px 0 4px;word-break:keep-all}
.step .a{display:inline-block;background:#2b2b38;border-radius:6px;padding:3px 8px;font-size:12.5px;margin-bottom:5px;word-break:keep-all}
.step .d{color:#cfcfda;line-height:1.55;word-break:keep-all}
.foot{position:fixed;left:0;right:0;bottom:0;z-index:20;background:rgba(18,18,24,.97);border-top:1px solid var(--ln);padding:8px 12px calc(10px + env(safe-area-inset-bottom));max-width:760px;margin:0 auto;box-shadow:0 -8px 20px rgba(0,0,0,.4)}.foot .board-sum{margin:0 0 8px;max-height:40vh;overflow-y:auto;padding:8px 10px;font-weight:500}.bsh{font-weight:800;margin-bottom:4px}.bsr{display:flex;gap:6px;align-items:flex-start;margin-top:3px}.bsr>em{flex:none;width:30px;font-style:normal;font-size:11.5px;color:#e8d9b0;padding-top:2px}.bsr>div{flex:1;min-width:0;display:flex;flex-wrap:wrap;gap:3px}.bc{font-size:11.5px;background:#00000040;border-radius:5px;padding:1px 6px;word-break:keep-all;line-height:1.5}.bc.no{opacity:.5}.foot .step{margin:0 0 8px;padding:9px 12px;max-height:34vh;overflow-y:auto}.foot .step .t{font-size:15px}.foot .step .d{font-size:13px}.foot .board-sum{margin:0 0 8px}.nav{display:flex;gap:8px;align-items:center}.nav .cnt{flex:none;min-width:58px;text-align:center;color:var(--mu);font-size:12.5px;font-weight:700}
.btn{flex:1;background:var(--pn);border:1px solid var(--ln);color:var(--tx);border-radius:10px;padding:12px;font-size:15px;font-weight:700;cursor:pointer}
.btn.pri{background:var(--ac);color:#1a1a1a;border-color:var(--ac)}
.btn:disabled{opacity:.35}
.piles{display:grid;grid-template-columns:1fr;gap:6px;margin-top:10px}
.pile{background:var(--pn);border:1px solid var(--ln);border-radius:10px;padding:8px 10px}
.pile h4{font-size:12px;color:var(--mu);font-weight:600;margin-bottom:5px}
.chip{display:inline-block;font-size:11.5px;border-radius:6px;padding:3px 7px;margin:0 4px 4px 0;background:#2b2b38;word-break:keep-all}
.res{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px}.res.one{grid-template-columns:1fr}.rz{background:#22222d;border:1px solid var(--ln);border-radius:8px;padding:6px 7px;min-height:44px}.rz h4{font-size:11px;color:var(--mu);font-weight:600;margin-bottom:4px}.rz h4 em{font-style:normal;color:var(--ac);margin-left:3px}.rz .chip{font-size:10.5px;padding:2px 5px;margin:0 3px 3px 0}.chip.new{background:#5a4815;color:#ffe7a6;box-shadow:0 0 0 1px var(--ac)}.done{margin-top:10px;color:var(--mu);font-size:12.5px;line-height:1.5;word-break:keep-all;padding:0 2px}.done span{display:block;font-size:11px;color:#7d7d90}.done i{font-style:normal;color:#8d8da0}
.board-sum{margin-top:10px;background:#2a2312;border:1px solid var(--ac);color:#f6dc9a;border-radius:12px;padding:10px 12px;font-weight:700;line-height:1.5;word-break:keep-all}
.dots{display:flex;flex-wrap:wrap;gap:4px;margin-top:10px}
.dot{width:26px;height:26px;border-radius:7px;background:var(--pn);border:1px solid var(--ln);color:var(--mu);font-size:11px;cursor:pointer}
.dot.on{background:var(--ac);color:#1a1a1a;font-weight:800}
.slots{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:6px 0 4px}.slots div{background:#2a2312;border:1px solid var(--ac);border-radius:10px;padding:8px 6px;text-align:center}.slots b{display:block;font-size:20px;color:var(--ac)}.slots span{font-size:11px;color:#e8d9b0;line-height:1.35}.deck h2 small{color:var(--mu);font-weight:500;font-size:12px;margin-left:4px}
.deck h2{font-size:15px;margin:16px 2px 2px;border-bottom:1px solid var(--ln);padding-bottom:5px}.deck h3{font-size:13.5px;color:var(--ac);margin:10px 2px 6px}.deck h3 small{color:var(--mu);font-weight:500;font-size:11.5px;margin-left:4px}
.row{display:flex;align-items:center;gap:8px;background:var(--pn);border:1px solid var(--ln);border-radius:8px;padding:7px 10px;margin-bottom:5px}
.row .th{width:30px;height:43px;object-fit:fill;border-radius:3px;border:0;flex:none}
.row i{width:10px;height:22px;border-radius:3px;flex:none}.row span{flex:1;word-break:keep-all}.row b{color:var(--ac)}
.note,.okb,#lv1,#lv2,#fnote,#legend,.hd>span{display:none!important}.note{color:var(--mu);font-size:12px;line-height:1.6;margin-top:10px;word-break:keep-all}
.row.lock{border:2px solid #3b82f6;border-radius:16px;background:#16213a}.row .lt{display:inline-block;font-style:normal;font-size:10.5px;font-weight:700;color:#fff;background:#3b82f6;border-radius:5px;padding:1px 6px;margin-top:3px}.pm{flex:none;width:32px;height:32px;border-radius:9px;border:1px solid var(--ln);background:#2b2b38;color:#fff;font-size:18px;line-height:1;cursor:pointer}.pm:disabled{opacity:.25;cursor:default}.row .ct{min-width:18px;text-align:center;position:relative}.row .lk2{position:absolute;top:calc(100% + 2px);left:50%;transform:translateX(-50%);white-space:nowrap;font-size:9.5px;font-weight:700;color:#ff8a8f}
.bchips{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;margin:6px 0 10px}.bch{border:1px solid var(--ln);background:var(--pn);color:var(--tx);border-radius:10px;padding:9px 6px;font-size:13px;line-height:1.25;text-align:center;word-break:keep-all;cursor:pointer}.bch.on{border-color:#3b82f6;box-shadow:inset 0 0 0 1px #3b82f6;background:#16213a;color:#cfe0ff;font-weight:700}
.warn{background:#3a1416;border:1px solid #e5484d;color:#ffd6d8;border-radius:12px;padding:10px 12px;margin:8px 0;line-height:1.55;font-size:13px;word-break:keep-all}.warn button{display:block;margin-top:7px;background:#e5484d;color:#fff;border:0;border-radius:8px;padding:8px 12px;font-weight:700;font-size:13px;cursor:pointer}
.okb{background:#15281c;border:1px solid #2f5a3a;color:#bfe9cb;border-radius:12px;padding:9px 12px;margin:8px 0;font-size:13px;line-height:1.5}
.cat:disabled{opacity:.4;cursor:default}details.more{margin-top:10px}details.more summary{cursor:pointer;color:var(--ac);font-weight:700;font-size:13.5px;padding:6px 2px}.rst{margin-top:12px;background:transparent;border:1px solid var(--ln);color:var(--mu);border-radius:9px;padding:8px 12px;font-size:12.5px;cursor:pointer}
.opp{margin-top:10px;background:#16202e;border:1px solid #2c4a6e;border-radius:14px;padding:10px 12px}.opp h4{font-size:14px;color:#9cc4ff;margin-bottom:6px}.opp h4 small{display:block;font-size:11px;color:#7f9bbd;font-weight:500;margin-top:2px}.oi{background:#1d2a3c;border-radius:10px;padding:8px 10px;margin-top:6px}.oi .ot{font-size:13.5px;font-weight:700}.oi i{display:inline-block;font-style:normal;font-size:11px;color:#bcd3f0;background:#2a3d57;border-radius:5px;padding:1px 6px;margin-top:3px}.oi p{font-size:12.5px;color:#d6e2f2;line-height:1.5;margin-top:4px;word-break:keep-all}
#hf{margin-bottom:6px}#hf .hr{display:flex;gap:5px;overflow-x:auto;scrollbar-width:none;margin-bottom:5px}#hf button{flex:none;border:1px solid var(--ln);background:var(--pn);color:var(--mu);border-radius:8px;padding:6px 11px;font-size:12.5px;font-weight:700;cursor:pointer}#tabs .gtg{display:inline-flex;align-items:center;gap:3px;margin-left:6px;vertical-align:1px;height:auto;line-height:1}#tabs .gtg i{display:inline-block;width:auto;height:auto;line-height:1.4;font-style:normal;font-size:10px;font-weight:700;padding:1px 5px;border-radius:4px}.g-ns{background:#4a3018;color:#ffc58a}.bcq{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:4px 8px;text-align:left;padding:7px 8px}.bcq .bn{flex:1;min-width:0;font-weight:700}.bq{display:inline-flex;align-items:center;gap:7px;flex:none}.bqm{width:28px;height:28px;border-radius:8px;border:1px solid var(--ln);background:#22222d;color:var(--tx);font-size:16px;font-weight:800;line-height:1;cursor:pointer}.bq b{min-width:12px;text-align:center;font-size:14px}.bcq .bh{flex-basis:100%;height:18px;line-height:18px;overflow:hidden}.bchips{grid-auto-rows:1fr}.bcq{align-content:space-between}.bcq{display:grid;grid-template-columns:minmax(0,1fr) auto;grid-template-rows:auto auto;align-content:center;align-items:center;column-gap:8px;row-gap:3px;min-height:72px;padding:7px 8px}.bcq.hb .bn{grid-row:1}.bcq .bn{grid-column:1;grid-row:1/3;display:block;min-height:0;max-height:2.5em;overflow:hidden;line-height:1.25}.bcq .bh{grid-column:1;grid-row:2;height:18px;line-height:18px}.bcq .bh:empty{display:none}.bcq .bq{grid-column:2;grid-row:1/3;align-self:center}.bcq .gn{margin-left:0}.bch .gw{display:block;margin-top:3px;font-style:normal;font-size:10px;font-weight:600;color:#9aa3b8}.bch .gn{display:inline-block;margin-left:5px;font-style:normal;font-size:10.5px;font-weight:800;padding:1px 5px;border-radius:4px;background:#1f3d2a;color:#a8e6bd;vertical-align:1px}.g-gen{background:#3d1f4a;color:#e6b8ff}.g-only{background:#1f3d2a;color:#a8e6bd}.hd span.need{color:#e8d9b0;font-weight:600}.g-sr{background:#123a2e;color:#4fd8a8}.g-dr{background:#4a1a26;color:#ff8fa8}.g-mc{background:#16304a;color:#8fc4ff}.g-lk{background:#3a3a46;color:#e0e0ea}#hf button:disabled{opacity:.3;cursor:default}#hf button.on{background:#2a2618;color:var(--ac);border-color:var(--ac)}#hf .sz button{flex:1}
#hf{margin-bottom:0}#hf .sz{display:grid;grid-template-columns:repeat(auto-fit,minmax(0,1fr));gap:8px;margin-bottom:12px}
#hf .hr:not(.sz){flex-wrap:wrap;overflow:visible;gap:10px 8px;margin-bottom:0;padding-top:12px;border-top:1px solid var(--ln)}
#hf .hr:not(.sz) button{padding:5px 10px;font-size:12px;border-radius:999px}
.tabs{flex-wrap:wrap;overflow:visible;gap:10px 8px;padding:12px 0 0;margin-top:12px;margin-bottom:16px;border-top:1px solid var(--ln)}
.tabs .tab{flex:none;padding:7px 12px;font-size:13px;border-radius:999px;min-height:0;line-height:1.3;max-width:100%;white-space:normal;text-align:left}.tabs{display:grid;grid-template-columns:minmax(0,1fr);gap:6px}@media(min-width:700px){.tabs{grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 8px}}#tabs .tab{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:5px;width:100%;border-radius:10px;padding:9px 12px}.tab .tn{font-weight:700;min-width:0}#tabs .gtg{margin-left:0;flex-wrap:wrap;gap:3px}#tabs .gtg:empty{display:none}.tsec{grid-column:1/-1;font-size:12px;font-weight:700;color:var(--mu);margin-top:8px}.tsec:first-child{margin-top:0}
.res2{gap:10px;margin-bottom:16px}
.row.zero{background:#1c1c22}.row.zero .th{filter:grayscale(1);opacity:.45}.row.zero>span{color:#8a8a96}.row.zero .ut{color:#7e8f84}.row.zero .nb:not(.bad){background:#55555f;color:#ddd}.row.need0{border:2px solid #e5484d;border-radius:16px}.thw{position:relative;flex:none;display:flex}.thw .rx{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);margin:0;padding:3px 3px;font-size:10px;white-space:nowrap;background:#e5484d;color:#fff;border:0;border-radius:6px;box-shadow:0 1px 4px #000a}.rx{flex:none;margin-left:2px;background:#3a1d20;border:1px solid #e5484d;color:#ffd0d3;border-radius:8px;padding:3px 7px;font-size:10.5px;line-height:1.2;font-weight:700;cursor:pointer}
#stk.on{position:sticky;top:0;z-index:15;background:var(--bg);padding:6px 0 4px;margin:0 -2px;box-shadow:0 6px 10px -8px #000}#stk .cats{margin-bottom:10px}#sbar{display:none}#sbar.on{display:block}.sst{font-size:12.5px;color:var(--mu);padding:6px 2px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.sst b{color:var(--tx)}.sst .bad{color:#ff8a8f}#sbar{position:relative}.sch{display:none;gap:5px;overflow-x:auto;scrollbar-width:none;padding:6px 0 6px;position:absolute;left:0;right:0;top:100%;background:var(--bg);box-shadow:0 6px 10px -8px #000}#sbar.chips .sch{display:flex}@media(hover:hover){.sch,#hf .hr{scrollbar-width:thin;scrollbar-color:#555 transparent;cursor:grab}.sch{padding-bottom:3px}}.sch .bch{flex:none;padding:6px 10px;font-size:12px;border-radius:999px}
.row.use{border:2px solid #3fb86b;border-radius:16px;background:#16261c}.row .ut{display:block;font-style:normal;font-size:10.5px;color:#8fe0a6;margin-top:1px;line-height:1.7}.row>span{min-width:0}.row .ut.bad{color:#ff8a8f;font-weight:700}.row .ub.ubb{background:#2f8f55}.row .ut.bad .ubb{background:#e5484d}.row .ub{display:inline-block;vertical-align:0;font-style:normal;font-size:10px;font-weight:700;color:#fff;background:#3b82f6;border-radius:4px;padding:0 5px;line-height:1.5;margin:0 1px}
.lvr{display:flex;align-items:center;justify-content:space-between;margin-top:6px}.lvr .lv{margin:0}.rst2{background:#2b2b38;border:1px solid var(--ln);color:var(--tx);border-radius:8px;padding:6px 12px;font-size:12.5px;font-weight:700;cursor:pointer}
.row .nb{display:inline-block;font-style:normal;font-size:10.5px;font-weight:700;color:#1a1a1a;background:var(--ac);border-radius:5px;padding:1px 6px;margin-top:3px}.row .nb.bad{background:#e5484d;color:#fff}.row .nl{display:block;font-style:normal;font-size:10.5px;font-weight:700;color:#ff8a8f;margin-top:1px;white-space:nowrap}
.vt{display:grid;grid-template-columns:1fr 1fr;gap:4px;background:var(--pn);border:1px solid var(--ln);border-radius:10px;padding:3px;margin:12px 0 4px}.vt button{border:0;background:transparent;color:var(--mu);border-radius:8px;padding:8px 4px;font-size:12.5px;font-weight:700;cursor:pointer}.vt button.on{background:#3a3220;color:var(--ac)}
.gd{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:4px;margin-top:6px}@media(min-width:560px){.gd{grid-template-columns:repeat(10,minmax(0,1fr))}}.gt{position:relative;aspect-ratio:65/94;border:0;padding:0;border-radius:5px;overflow:hidden;background:#000;cursor:pointer;outline:2px solid transparent;outline-offset:-2px}.gt img{width:100%;height:100%;object-fit:fill;display:block}.gt span{display:flex;align-items:center;justify-content:center;width:100%;height:100%;font-size:9px;color:#111;padding:2px;word-break:keep-all}.gt.lk{outline-color:#3b82f6}.gt{cursor:default}.gq{position:absolute;bottom:2px;width:36%;max-width:26px;aspect-ratio:1;border-radius:6px;border:1px solid rgba(255,255,255,.4);background:rgba(10,10,14,.85);color:#fff;font-size:15px;font-weight:800;line-height:1;padding:0;cursor:pointer;display:flex;align-items:center;justify-content:center}.gq.gqm{left:2px}.gq.gqp{right:2px}.gq:disabled{opacity:.35;cursor:default}.gq:active{background:var(--ac);color:#111}.gt.us{outline-color:#3fb86b}.gt.bd{outline:2px dashed #e5484d}.gt.sel{outline:3px solid var(--ac);outline-offset:-3px}
.gsel{position:sticky;top:96px;z-index:5;background:var(--bg);padding:6px 0;display:flex;gap:6px;align-items:stretch}.gsel .row{flex:1;margin:0}.gx{flex:none;background:#2b2b38;border:1px solid var(--ln);color:var(--tx);border-radius:8px;padding:0 10px;font-size:12px;cursor:pointer}
.arc{display:grid;grid-template-columns:repeat(auto-fit,minmax(0,1fr));gap:4px;margin:0 0 10px}.arc:empty{display:none}.arc button{border:1px solid var(--ln);background:var(--pn);color:var(--mu);border-radius:10px;padding:9px 4px;font-size:12.5px;font-weight:800;cursor:pointer;word-break:keep-all}.arc button.on{background:#e8e8f0;color:#141418;border-color:#e8e8f0}
.bk2{grid-column:1/-1;justify-self:start;background:var(--pn);border:1px solid var(--ln);color:var(--tx);border-radius:9px;padding:7px 12px;font-size:13px;font-weight:700;cursor:pointer}
#hl{display:flex;flex-direction:column;gap:8px}.hc{display:flex;align-items:stretch;background:var(--pn);border:1px solid var(--ln);border-radius:14px;cursor:pointer;user-select:none;-webkit-user-select:none;-webkit-touch-callout:none}#hl{position:relative}.hc{position:relative}.hc.drg{border-color:var(--ac);box-shadow:0 8px 20px #000a;background:#262630;z-index:2}.hcb{flex:1;padding:14px;min-width:0}.hcb b{display:block;font-size:17px}.hcb span{display:block;color:var(--mu);font-size:12.5px;margin-top:2px}.hcb em{display:block;font-style:normal;color:var(--ac);font-size:12px;margin-top:6px}.hg{flex:none;width:46px;display:flex;align-items:center;justify-content:center;font-size:22px;color:var(--mu);border-left:1px solid var(--ln);touch-action:none;cursor:grab}
.sst{display:flex;align-items:center;gap:6px}.sst .stt{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}#sbar:not(.rsts) .rst3{visibility:hidden}.rst3{flex:none;background:#2b2b38;border:1px solid var(--ln);color:var(--tx);border-radius:7px;padding:3px 9px;font-size:11.5px;font-weight:700;cursor:pointer}.rst3.warn2{background:#e5484d;border-color:#e5484d;color:#fff}
.sk{display:inline;white-space:nowrap;border-radius:4px;padding:0 4px;font-weight:700;-webkit-box-decoration-break:clone;box-decoration-break:clone}.sk-ns{background:#5a3a1a;color:#ffc58a}.sk-ss{background:#3a3a46;color:#f2f2f7}.sk-fu{background:#3d2a5c;color:#d4b5ff}.sk-sy{background:#e8e8ee;color:#22222a}.sk-xy{background:#111116;color:#d8d8e0;box-shadow:inset 0 0 0 1px #55556a}.sk-lk{background:#1d3558;color:#9cc8ff}
.sk{display:inline;white-space:nowrap;font-weight:700;background:none!important;box-shadow:none!important;padding:0!important}
.sk-ns{color:#ffc58a}.sk-ss{color:#f2f2f7}.sk-fu{color:#d4b5ff}.sk-sy{color:#f2f2f7}.sk-xy{color:#c4c4cc}.sk-lk{color:#9cc8ff}
.cx{border-radius:4px;padding:0 4px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.cx-ef{background:#4a3018;color:#ffc58a!important}.cx-fu{background:#3d2a5c;color:#d4b5ff!important}.cx-sy{background:#e8e8ee;color:#22222a!important}.cx-xy{background:#111116;color:#d8d8e0!important;box-shadow:inset 0 0 0 1px #55556a}.cx-lk{background:#1d3558;color:#9cc8ff!important}
.pile .pi{background-size:cover;background-position:center top}
body:not(.fshow) .foot>.step,body:not(.fshow) .foot>.board-sum{display:none}
.board .zone-lbl{display:none}
.board .res .rz{white-space:nowrap;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;min-height:0}.board .res .rz::-webkit-scrollbar{display:none}.board .res .rz .chip{margin-bottom:0}.pile .pl{font-size:9px}.pile .pc{font-size:16px}.foot{background:#121218}.board .res .rz.ov{-webkit-mask-image:linear-gradient(90deg,#000 80%,transparent);mask-image:linear-gradient(90deg,#000 80%,transparent)}.board .res .rz.ov.end{-webkit-mask-image:none;mask-image:none}
.legend{display:flex;flex-wrap:wrap;gap:6px 12px;font-size:11px;color:var(--mu);margin-top:10px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:-1px}
.svp{background:var(--pn);border:1px solid var(--ln);border-radius:12px;padding:12px;margin:10px 0}.svp h4{margin:0 0 8px;font-size:14px}.svp h4 small{color:var(--mu);font-weight:600;margin-left:6px}
.svhand{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px}.svc{display:flex;align-items:center;justify-content:space-between;gap:6px;border:1px solid var(--ln);border-radius:10px;padding:6px 8px;font-size:13px;font-weight:700;min-width:0}.svc>span:first-child{min-width:0;line-height:1.25;word-break:keep-all}.svc.on{border-color:var(--ac);background:#3a3220}
.svx summary{cursor:pointer;font-size:14px;list-style:none}.svx summary::-webkit-details-marker{display:none}.svx summary small{color:var(--mu);font-weight:600;margin-left:6px}.svx[open] summary{margin-bottom:10px}.svc.unk{opacity:.6}.svc i{font-style:normal;font-weight:600;color:var(--mu);font-size:11px}.svg{margin:10px 0 6px;font-size:12px;color:var(--mu);font-weight:700}.svp h4+.svg,.svx summary+.svg{margin-top:0}.svhh{display:flex;align-items:center;justify-content:space-between;gap:8px}.svp .rst3{visibility:visible;flex:none}.svp .rst3:disabled{opacity:.4}.svxr{display:flex;justify-content:flex-end;margin-bottom:4px}.svinfo .rst3{visibility:visible;margin-left:6px}.svtg{display:flex;flex-wrap:wrap;gap:5px}.svtg button{border:1px solid var(--ln);background:#22222d;color:var(--tx);border-radius:8px;padding:6px 10px;font-size:12.5px;font-weight:700;cursor:pointer}.svtg button.on{background:#4a1a26;border-color:#e5484d;color:#ffb3bd;text-decoration:line-through}.svnf{margin:6px 0 8px}.svnf>span{display:block;font-size:12px;color:var(--mu);font-weight:700;margin-bottom:5px}.svbt{background:transparent;color:var(--tx);cursor:pointer;text-align:left;min-height:44px}.svbt em{font-style:normal;font-size:11px;font-weight:700;border-radius:6px;padding:2px 7px;background:#1f3d2a;color:#a8e6bd;flex:none}.svbt.off{border-color:#e5484d;background:#3a151c}.svbt.off>span:first-child{text-decoration:line-through;color:#ffb3bd}.svbt.off em{background:#e5484d;color:#fff}.svbt.cost{border-color:#d9a13a;background:#33280f}.svbt.cost em{background:#d9a13a;color:#1a1300}.svbh{margin:0 0 8px;line-height:1.55}.svbo{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-bottom:8px}.svbo label{font-size:12.5px;color:var(--mu);font-weight:700;display:flex;align-items:center;gap:6px}.svbo select{background:#22222d;color:var(--tx);border:1px solid var(--ln);border-radius:8px;padding:6px 8px;font-size:13px}.svbo .btn{margin-left:auto}.svbe .btn{margin-left:0;padding:8px 12px;font-size:12.5px;min-width:0}.svbe{margin-top:4px}.svbta{width:100%;box-sizing:border-box;height:64px;background:#15151c;color:var(--tx);border:1px solid var(--ln);border-radius:9px;padding:8px;font-size:12px;margin-bottom:8px;resize:none}.svbl{display:grid;gap:5px}@media(min-width:700px){.svbl{grid-template-columns:1fr 1fr}}.svbr{display:flex;align-items:center;gap:8px;text-align:left;border:1px solid var(--ln);background:#1b1b24;color:var(--tx);border-radius:9px;padding:8px 10px;font-size:13px;cursor:pointer;min-height:40px}.svbr b{min-width:0;flex:1}.svbr i{font-style:normal;font-size:11px;color:var(--mu);flex:none}.svbr .svs{flex:none}.svfoot .svgo{margin-top:6px}.svfh{font-size:12.5px;font-weight:700;color:var(--tx);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.svfoot .svm{margin:0}.svgo{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:10px}.svgo label{font-size:12.5px;color:var(--mu)}.svgo select{background:#22222d;color:var(--tx);border:1px solid var(--ln);border-radius:8px;padding:6px 8px;font-size:13px;margin-left:4px}.svgo .btn{flex:none;min-width:96px}
.svm{color:var(--mu);font-size:12.5px;margin:8px 0 0}.svinfo{font-size:12.5px;color:var(--mu);margin:8px 2px}
.svf .hr{display:flex;gap:5px;overflow-x:auto;scrollbar-width:none;margin-bottom:5px}.svf button{flex:none;border:1px solid var(--ln);background:var(--pn);color:var(--mu);border-radius:8px;padding:6px 11px;font-size:12.5px;font-weight:700;cursor:pointer}.svf button.on{background:#3a3220;color:var(--ac);border-color:var(--ac)}
.svl{display:grid;gap:6px;margin-top:6px}.svr{border:1px solid var(--ln);border-radius:10px;background:var(--pn);overflow:hidden}.svr.on{border-color:var(--ac)}
.svh{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;width:100%;text-align:left;border:0;background:transparent;color:var(--tx);padding:10px 12px;font-size:13px;cursor:pointer;line-height:1.45}.svh b{flex-basis:100%;font-weight:700}.svh i{flex-basis:100%;font-style:normal;color:var(--mu);font-size:12px}
.svs{background:#3a3220;color:var(--ac);border-radius:6px;padding:1px 7px;font-weight:800;font-size:12px}.svk{border-radius:6px;padding:1px 7px;font-weight:700;font-size:11px}.svk-dt{background:#16304a;color:#8fc4ff}.svk-brand{background:#4a1a26;color:#ff8fa8}.svk-mix{background:#3d1f4a;color:#e6b8ff}
.svb{border-top:1px solid var(--ln);padding:10px 12px}.svb h5{margin:8px 0 6px;font-size:12.5px;color:var(--mu)}.svb h5:first-child{margin-top:0}.svi{font-size:12.5px;margin-bottom:5px;line-height:1.5}.svi em{font-style:normal;font-size:11px;background:#22222d;border-radius:5px;padding:1px 6px;margin:0 6px;color:var(--mu)}.svi>span{display:block;color:var(--mu)}
.svst{margin:0;padding-left:22px;font-size:12.5px;line-height:1.55}.svst li{margin-bottom:4px}.svst li>span{display:block;color:var(--mu)}.svst i{font-style:normal;color:var(--mu)}
.sva{margin-top:10px}.sva .btn{width:100%}.svmore{width:100%;margin-top:8px}.svfd{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:12.5px;padding:6px 0;border-top:1px solid var(--ln)}.svfd:first-of-type{border-top:0}.svfd>span:first-child{min-width:0}.svfd>span:last-child{display:flex;gap:6px;flex:none}.svfd .btn{padding:6px 10px;font-size:12px;min-width:0}
</style></head><body><div class="wrap">
<div class="arc" id="arc"></div><h1 id="ttl">__TITLE__</h1>
<div class="top" id="top"></div><div id="stk"><div class="cats" id="cats"></div><div id="sbar"></div></div><div id="hf"></div><div class="lv" id="lv1">초동 (패에 잡힌 카드)</div><div class="tabs" id="tabs"></div><div class="lv" id="lv2">결과물 (엔드 보드)</div><div class="res2" id="res2"></div>
<div id="view"></div>
<div class="legend" id="legend"></div>
<p class="note" id="fnote">카드명은 코나미 한국어 공식 DB 기준. 엑스트라 덱에서 링크 소환할 때의 위치와 링크 소재 수치는 프로그램으로 룰 검증을 마쳤습니다. 필드는 지금 상태, 아래 카드는 다음에 할 행동입니다. 노란 테두리(묘지·제외·패는 노란 칩)는 방금 바뀐 것, 초록 "링크"는 링크 상태(그리폰 봉인 확인용)입니다.</p>
</div>
<script>
const ALL=__DATA__;const AKS=Object.keys(ALL);let AK=(location.hash.match(/^#([a-z]+):/)||[])[1];if(!ALL[AK]){try{AK=localStorage.getItem('guide-ak')}catch(e){}}if(!ALL[AK])AK=AKS[0];try{localStorage.setItem('guide-ak',AK)}catch(e){}
let HOME=AKS.length>1&&!/^#[a-z]+:/.test(location.hash);let D=ALL[AK];let HP=AKS.length>1?AK+':':'';function rh(){const h=location.hash.slice(1);if(!HP)return h;return h.startsWith(HP)?h.slice(HP.length):''}
function setArc(){if(AKS.length<2)return;const arc=document.getElementById('arc');if(HOME){arc.innerHTML='';return}if(D.title){document.getElementById('ttl').textContent=D.title;document.title=D.title}arc.innerHTML=`<button class="bk2" id="bk2">← 덱 선택</button>`;document.getElementById('bk2').onclick=()=>goHome()}
const COL={synchro:'#d9d9e0',eff:'#c9783a',spell:'#1a8f6c',field:'#1a8f6c',trap:'#a3355f',fusion:'#7442a8',xyz:'#2b2b30',link:'#1f5fa8',equip:'#1a8f6c'};
const BG={synchro:'#f4f4f7',eff:'#f3dcc6',spell:'#cdeee2',field:'#cdeee2',trap:'#f4d3df',fusion:'#e3d4f3',xyz:'#d9d9df',link:'#d2e2f6',equip:'#cdeee2'};
const KL={synchro:'싱크로',eff:'효과 몬스터',spell:'마법',field:'필드 마법',trap:'함정',fusion:'융합',xyz:'엑시즈',link:'링크',equip:'장착 마법'};
const KIND={};
const tabs=document.getElementById('tabs'),view=document.getElementById('view');
const cats=document.getElementById('cats'),topEl=document.getElementById('top');let SEL=D.decksel;let single=SEL.length===1;
let dk=null,cur=null,step=0;
function groupsOf(x){return x.groups||x.combos.map(id=>({name:(x.labels||{})[id]||id,items:[[id,'']]}))}
function grpOf(x,id){return groupsOf(x).find(g=>g.items.some(i=>i[0]===id))}
function resLabel(x,id){const g=grpOf(x,id);const it=g&&g.items.find(i=>i[0]===id);return it&&it[1]}
const sig=s=>JSON.stringify([s.zones,s.gy,s.ban,s.hand]);
function shared(a,b){const A=D.combos.find(c=>c.id===a),B=D.combos.find(c=>c.id===b);if(!A||!B)return 0;let n=0;while(n<A.steps.length&&n<B.steps.length&&sig(A.steps[n])===sig(B.steps[n]))n++;return n}
const HC={eff:'#f2a96a',spell:'#4fd8a8',field:'#4fd8a8',equip:'#4fd8a8',trap:'#f27aa9',fusion:'#bb92f5',synchro:'#e9e9f2',xyz:'#c4c4cc',link:'#72adf5'};
let NAMES=null;function names(){if(NAMES)return NAMES;const s=new Set(Object.keys(D.kinds||{}));for(const c of D.combos)for(const st of c.steps){Object.values(st.zones).forEach(z=>s.add(z.name.replace(' (장착)','')));st.gy.concat(st.ban,st.hand).forEach(n=>s.add(n))}NAMES=[...s].filter(n=>n&&n.length>1&&kindOf(n)).sort((a,b)=>b.length-a.length);return NAMES}
function hl(t){let h=esc(t);const ns=names();if(!ns.length)return skw(h);const re=new RegExp(ns.map(n=>esc(n).replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|'),'g');return skw(h.replace(re,m=>{const n=m.replace(/&amp;/g,'&');const k=kindOf(n);return`<b class="cn${EXK[k]?' cx cx-'+EXK[k]:''}" style="color:${HC[k]||'#fff'}">${m}</b>`}))}
const EXK={eff:'ef',fusion:'fu',synchro:'sy',xyz:'xy',link:'lk'};SKM={'일반 소환':'ns','특수 소환':'ss','융합 소환':'fu','싱크로 소환':'sy','엑시즈 소환':'xy','링크 소환':'lk'};function skw(h){return h.replace(/(<[^>]+>)|(일반 소환|특수 소환|융합 소환|싱크로 소환|엑시즈 소환|링크 소환)/g,(m,tag,kw)=>tag?tag:`<span class="sk sk-${SKM[kw]}">${kw}</span>`)}
function esc(s){return String(s).replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]))}
function arrows(a){if(!a)return'';const p={U:'top:-6px;left:calc(50% - 5px);border-bottom-color:#ff6b6b;border-top:0',D:'bottom:-6px;left:calc(50% - 5px);border-top-color:#ff6b6b;border-bottom:0',L:'left:-6px;top:calc(50% - 5px);border-right-color:#ff6b6b;border-left:0',R:'right:-6px;top:calc(50% - 5px);border-left-color:#ff6b6b;border-right:0',UL:'top:-4px;left:-4px;border-bottom-color:#ff6b6b;border-top:0;transform:rotate(-45deg)',UR:'top:-4px;right:-4px;border-bottom-color:#ff6b6b;border-top:0;transform:rotate(45deg)',DL:'bottom:-4px;left:-4px;border-top-color:#ff6b6b;border-bottom:0;transform:rotate(45deg)',DR:'bottom:-4px;right:-4px;border-top-color:#ff6b6b;border-bottom:0;transform:rotate(-45deg)'};return a.map(x=>`<span class="ar" style="${p[x]}"></span>`).join('')}
function cell(s,k,cls){const z=s.zones[k];let inner=k.startsWith('S')?'':'';if(!z)return`<div class="z ${cls}">${{EL:'EX',ER:'EX'}[k]||''}</div>`;const kd=z.kind;const chg=s.changed.includes(k)?' chg':'';
const nm=z.name.replace(" (장착)","");const im=(D.img||{})[nm];
if(im)return`<div class="z ${cls}"><div class="c ci${chg}" style="background-image:url('${im}')">${TAGON&&TAGS[nm]?`<span class="tg">${esc(TAGS[nm])}</span>`:''}<span class="nm">${esc(nm)}</span>${z.mats?`<span class="mt">소재 ${z.mats}</span>`:''}${z.linked?'<span class="lk">링크</span>':''}</div>${arrows(z.arrows)}</div>`;
return`<div class="z ${cls}"><div class="c${chg}" style="background:${BG[kd]};border-color:${COL[kd]}"><span class="k" style="background:${COL[kd]}">${KL[kd]}</span>${esc(nm)}${TAGON&&TAGS[nm]?`<span class="tg">${esc(TAGS[nm])}</span>`:''}${z.mats?`<span class="mt">소재 ${z.mats}</span>`:''}${z.linked?'<span class="lk">링크</span>':''}</div>${arrows(z.arrows)}</div>`}
function chips(a){return a.length?a.map(x=>`<span class="chip">${esc(x)}</span>`).join(''):'<span class="chip" style="opacity:.5">없음</span>'}


let TAGON=false;const TAGS={"The Fallen & The Virtuous": "앞면 1장 파괴 or 묘지 몬스터 소생", "검은 용의 에클레시아": "제외 → 알버스 → 상대와 융합", "드래곤테일 그라멜": "드래곤테일 발동 시 1장 파괴", "드래곤테일 무루루": "상대 턴 드래곤테일 융합", "드래곤테일 플레임": "마법 무효 + 드로우", "드래곤테일 혼": "공격 표시 몬스터 되돌리기 + 드로우", "빙검룡 미라제이드": "몬스터 1장 제외", "사크라멘툼 드라군": "특소 드래곤·마법사 효과 봉인", "순백의 성녀 에클레시아": "릴리스 → 알버스 → 상대와 융합", "인도하는 성녀 쿠엠": "엑덱 이동 시 알버스 관련 몬스터 소생", "진염룡 알비온": "양쪽 묘지 1장씩 소생", "혁언룡 그랑기뇰": "상대 효과 특소 시 데스피아 소환", "혁의 성녀 카르테시아": "상대 턴 레벨 8 이상 융합", "혼효하는 믹시아": "아이온 융합 → 제외", "DDD 노도대왕 이그제큐티브 시져": "특소 효과 무효 후 파괴", "Evil★Twin's 트러블 써니": "릴리스 → 키스킬·리일라 소생", "데먼스미스 레퀴엠": "릴리스 → 데먼스미스 특소", "데먼스미스 디에스이레": "장착 링크 수만큼 무효", "빛 없는 그림자 아＝바오 아 쿠": "패 1장 버려 파괴 or 묘지 소생", "언체인드소울 라기아": "상대 특소 몬스터 먹고 링크", "우:피 팬시볼": "효과 무효·제외 or 상대 턴 링크", "트로이메어 그리폰": "특소 몬스터 효과 봉인", "No.65 재단마인 저지 버스터": "몬스터 효과 무효 + 500 데미지", "언체인드 쌍극": "패·묘지의 언체인드 특소 (라기아)", "데카네로그－발드라스": "발동 무효 (소재 1개 더 떼면 파괴)", "팬텀 오브 유벨": "몬스터 효과를 유벨 파괴로 바꿈", "나이트메어 쓰론": "유벨 몬스터가 효과로 떠나면 레벨±1 유벨 서치·특소"};
function myEnd(c){const i=c.steps.findIndex(x=>/^상대 턴/.test(x.title||''));return i>0?c.steps[i-1]:c.steps[c.steps.length-1]}
function boardSum(c){const s=myEnd(c);const zn=k=>s.zones[k]?s.zones[k].name.replace(' (장착)',''):null;
const mon=['EL','ER','M1','M2','M3','M4','M5'].map(zn).filter(Boolean),st=['S1','S2','S3','S4','S5'].map(zn).filter(Boolean);
const hand=s.hand.filter(n=>!n.startsWith('패사고')&&!n.startsWith('패의 '));
const row=(l,a)=>`<div class="bsr"><em>${l}</em><div>${a.length?a.map(n=>`<span class="bc">${hl(n)}</span>`).join(''):'<span class="bc no">없음</span>'}</div></div>`;
return`<div class="board-sum"><div class="bsh">완성</div>${row('필드',mon)}${row('마함',st)}${row('패',hand)}${row('묘지',s.gy)}${row('제외',s.ban)}</div>`}
function footBox(c,i){const last=c.steps.length-1,nx=i<last?c.steps[i+1]:null;return nx?`<div class="step"><div class="n">다음에 할 것 · ${i+1}단계</div><div class="t">${hl(nx.title)}</div>${nx.act?`<div class="a">${hl(nx.act)}</div>`:''}<div class="d">${hl(nx.desc)}</div></div>`:boardSum(c)}
let FH={};function footFix(c){const ft=view.querySelector('.foot');if(!ft)return;const box=ft.firstElementChild;if(!box)return;const w=ft.clientWidth-24;const k=c.id+'|'+w;
if(!FH[k]){const m=document.createElement('div');m.style.cssText=`position:absolute;visibility:hidden;left:0;top:0;width:${w}px`;ft.appendChild(m);let mx=0;for(let i=0;i<c.steps.length-1;i++){m.innerHTML=footBox(c,i);const e=m.firstElementChild;e.style.minHeight='0';mx=Math.max(mx,e.offsetHeight)}m.remove();FH[k]=mx}
if(!box.classList.contains('board-sum'))box.style.minHeight=FH[k]+'px';box.style.boxSizing='border-box'}


const RH={};function resFix(c){const rz=[...view.querySelectorAll('.board .res .rz')];if(rz.length<3)return;const w=rz.map(e=>e.offsetWidth).join(',');const k=c.id+'|'+w;
if(!RH[k]){const lists=[s=>s.gy,s=>s.ban,s=>s.hand];RH[k]=rz.map((e,i)=>{const m=e.cloneNode(false);m.style.cssText=`position:absolute;visibility:hidden;left:0;top:0;width:${e.offsetWidth}px;min-height:0`;e.parentNode.appendChild(m);let mx=0;for(const s of c.steps){const a=lists[i](s);m.innerHTML=`<h4>x <em>${a.length}</em></h4>`+(a.length?a.map(x=>`<span class="chip">${esc(x)}</span>`).join(''):'<span class="chip">없음</span>');mx=Math.max(mx,m.offsetHeight)}m.remove();return mx})}
rz.forEach((e,i)=>e.style.minHeight=RH[k][i]+'px')}
function rzOv(){view.querySelectorAll('.board .res .rz').forEach(e=>{const u=()=>{e.classList.toggle('ov',e.scrollWidth>e.clientWidth+2);e.classList.toggle('end',e.scrollLeft+e.clientWidth>=e.scrollWidth-2)};u();e.onscroll=u})}
function fitBoard(c){const g=view.querySelector('.board .grid'),bd=view.querySelector('.board'),ft=view.querySelector('.foot');if(!g||!bd||!ft)return;g.style.gridTemplateColumns='';g.style.justifyContent='';
const cell=g.querySelector('.z');if(!cell)return;const nav=ft.querySelector('.nav'),box=ft.firstElementChild;const w=ft.clientWidth-24;const k=c.id+'|'+w;
const boxH=box&&!box.classList.contains('board-sum')?(FH[k]||box.offsetHeight):(box?box.offsetHeight:0);
const footH=(nav?nav.offsetHeight:56)+boxH+30;const avail=window.innerHeight-footH-8;
const cellH=cell.offsetHeight,rest=bd.offsetHeight-3*cellH;const nh=Math.max(48,(avail-rest)/3);
if(nh<cellH){const cw=Math.floor(nh*65/94);g.style.gridTemplateColumns=`repeat(5,${cw}px)`;g.style.justifyContent='center'}}
window.addEventListener('resize',()=>{if(dk&&cur&&cur!=='list'){const c=D.combos.find(x=>x.id===cur);}});
function renderCombo(c){const s=c.steps[step];TAGON=step>=c.steps.indexOf(myEnd(c));const g=[];
const pvs=step>0?c.steps[step-1]:null;const fr=s.from||[];
const pile=(lbl,arr,prev,src)=>{const top=arr&&arr.length?arr[arr.length-1]:null;const moved=fr.filter(x=>x[1]===src).map(x=>x[0]);const im=top&&(D.img||{})[top];const ch=arr?(prev&&JSON.stringify(prev)!==JSON.stringify(arr)):moved.length>0;
return`<div class="z pile${ch&&step>0?' chg':''}">${im?`<div class="pi" style="background-image:url('${im}')"></div>`:''}<div class="pl">${lbl}</div>${arr?`<div class="pc">${arr.length}</div>`:''}${moved.length&&step>0?`<div class="pn">${esc(moved.join(', '))} ↗</div>`:''}</div>`};
g.push('<div class="zone-lbl">엑스트라 덱 · 엑스트라 몬스터 존 · 제외 · 묘지</div>');g.push(pile('엑스트라 덱',null,null,'extra'));g.push(cell(s,'EL','em'));g.push(pile('제외',s.ban,pvs&&pvs.ban));g.push(cell(s,'ER','em'));g.push(pile('묘지',s.gy,pvs&&pvs.gy));
g.push('<div class="zone-lbl">몬스터 존 (왼쪽부터 1~5번째)</div>');['M1','M2','M3','M4','M5'].forEach(k=>g.push(cell(s,k,'')));
g.push('<div class="zone-lbl">마법 & 함정 존</div>');['S1','S2','S3','S4','S5'].forEach(k=>g.push(cell(s,k,'st')));
const last=c.steps.length-1;
const nx=step<last?c.steps[step+1]:null, pv=step>0?c.steps[step-1]:null;
const diff=(a,b)=>{const m={};(b||[]).forEach(x=>m[x]=(m[x]||0)+1);return a.map(x=>{if(m[x]){m[x]--;return[x,0]}return[x,1]})};
const pchips=(a,b)=>a.length?diff(a,b).map(([x,n])=>`<span class="chip${n?' new':''}">${esc(x)}</span>`).join(''):'<span class="chip" style="opacity:.5">없음</span>';
const X=SEL.find(v=>v.key===dk)||{};const G=grpOf(X,c.id);const base=G&&G.items[0][0];const sh=base&&base!==c.id?shared(base,c.id):0;const bl=base?resLabel(X,base):'';
const brHtml=sh>1?`<div class="br">0~${sh-1}단계는 「${esc(bl.split(':')[0])}」 전개와 똑같고, ${sh}단계부터 갈라집니다.${step<sh?` <button id="tobr">${sh}단계로 이동</button>`:''}</div>`:'';
view.innerHTML=`<div class="hd"><b>${esc(G?G.name:c.title)}${resLabel(X,c.id)?' → '+esc(resLabel(X,c.id)):''}</b><span>${esc(c.sub)}</span>${c.need?`<span class="need">${esc(c.need)}</span>`:''}${links((X.clinks||{})[c.id])}${brHtml}</div>
<div class="board"><div class="grid">${g.join('')}</div>
<div class="res"><div class="rz"><h4>묘지 <em>${s.gy.length}</em></h4>${pchips(s.gy,pv&&pv.gy)}</div><div class="rz"><h4>제외 <em>${s.ban.length}</em></h4>${pchips(s.ban,pv&&pv.ban)}</div></div>
<div class="res one"><div class="rz"><h4>패 <em>${s.hand.length}</em></h4>${pchips(s.hand,pv&&pv.hand)}</div></div></div>
${step===last&&c.opp&&c.opp.length?`<div class="opp"><h4>상대 턴에 할 수 있는 것 <small>순서 없음 · 상황에 맞게 골라 씀 · 상대 턴이라 1턴에 1번 효과도 다시 쓸 수 있음</small></h4>${c.opp.map(([w,t,d])=>`<div class="oi"><div class="ot">${hl(w)}</div>${t?`<i>${esc(t)}</i>`:''}<p>${hl(d)}</p></div>`).join('')}</div>`:''}${step>0?`<div class="done"><span>방금 한 것 · ${step}단계</span>${hl(s.title)}${s.act?` <i>(${hl(s.act)})</i>`:''}</div>`:''}
<div class="foot">${footBox(c,step)}
<div class="nav"><button class="btn" id="pv" ${step===0?'disabled':''}>이전</button><span class="cnt">${step} / ${last}</span><button class="btn pri" id="nx" ${step===last?'disabled':''}>다음</button></div></div>
<div class="dots">${c.steps.map((_,i)=>`<button class="dot ${i===step?'on':''}${i<sh&&sh>1?' sh':''}" data-i="${i}">${i}</button>`).join('')}</div>`;
fshow();footFix(c);rzOv();document.getElementById('pv').onclick=()=>{step--;draw()};document.getElementById('nx').onclick=()=>{step++;draw()};
view.querySelectorAll('.dot').forEach(b=>b.onclick=()=>{step=+b.dataset.i;draw()});const tb=document.getElementById('tobr');if(tb)tb.onclick=()=>{step=sh;draw()};}
function kindOf(n){if(D.kinds&&D.kinds[n])return D.kinds[n];for(const c of D.combos)for(const s of c.steps)for(const z of Object.values(s.zones))if(z.name===n)return z.kind;return null}
function renderDeck(key){if(CU)return renderCustomDeck();const d=D.decks[key];const tot=a=>a.reduce((x,y)=>x+y[1],0);
const row=([n,c])=>{const k=kindOf(n)||'eff';const im=(D.img||{})[n];return`<div class="row">${im?`<img class="th" src="${im}" style="border-color:${COL[k]}">`:`<i style="background:${COL[k]}"></i>`}<span>${esc(n)}</span><b>×${(d.range||{})[n]||c}</b></div>`};
const isGen=n=>D.gen.some(g=>n===g||n.startsWith(g+' '));
const sec=(t,a,sub)=>a.length?`<h3>${t} <small>${tot(a)}장${sub?' · '+sub:''}</small></h3>${a.map(row).join('')}`:'';
const mc=d.main.filter(x=>!isGen(x[0])),mg=d.main.filter(x=>isGen(x[0])),ec=d.extra.filter(x=>!isGen(x[0])),eg=d.extra.filter(x=>isGen(x[0]));
const cm=tot(mc),ce=tot(ec);
const X=SEL.find(v=>v.key===dk)||{};view.innerHTML=`<div class="hd"><b>${esc(d.title)}</b><span>전개 필수 카드만 표시 · 메인 ${cm}장 · 엑스트라 ${ce}장${d.rangeNote?' · '+esc(d.rangeNote):''}</span>${d.how?`<div class="how">${d.how.map(t=>`<p>${esc(t)}</p>`).join('')}</div>`:''}${diffHtml(X.diff,X.baseName)}</div><div class="deck">
<div class="slots"><div><b>${Math.max(0,40-cm)}장</b><span>메인 범용 최소<br>(40장 맞추기)</span></div><div><b>${60-cm}장</b><span>메인 범용 최대<br>(60장 상한)</span></div><div><b>${Math.max(0,15-ce)}장</b><span>엑스트라 범용<br>(15장 상한)</span></div></div>
<h2>메인 덱 · 전개 필수 <small>${cm}장</small></h2>${mc.map(row).join('')}
<h2>엑스트라 덱 · 전개 필수 <small>${ce}장</small></h2>${ec.map(row).join('')}
<p class="note">패 트랩 · 돌파 카드 같은 범용 카드는 목록에서 뺐습니다. 위 칸 수만큼 원하는 범용 카드로 채우시면 됩니다. ${esc(d.note)}</p></div>`}
function diffHtml(df,bn){if(!df)return'';bn=bn||'내 덱';const o=df.oth||{add:[],rem:[]};
const ch=(a,x)=>a.map(([n,c,g,ban,f,t,h])=>`<span class="k${g||x?' g':''}">${esc(n)} <i>${f}→${t}장${h?' · '+esc(h):''}${x&&!g?' · 전개 외':''}${g?' · 범용':''}</i>${ban?'<s>금지</s>':''}</span>`).join('');
const ex=(arr,p)=>arr.filter(r=>r[0]===p&&(p==='extra'||!r[3])).map(r=>r.slice(1));
const bx=(k,t,d,oa)=>{const L=[['메인 덱','main'],['엑스트라 덱','extra']].map(([l,p])=>[l,d[p]||[],ex(oa,p)]).filter(x=>x[1].length||x[2].length);return L.length?`<div class="bx ${k}"><h5>${t}</h5>${L.map(([l,a,b])=>`<div class="ln"><em>${l}</em><div class="cs">${ch(a)}${ch(b,1)}</div></div>`).join('')}</div>`:''};
return`<div class="df">${bx('ad',bn+'에 추가된 카드',df.add,o.add)}${bx('rm',bn+'에서 빠진 카드',df.rem,o.rem)}<div class="nt">굵은 글씨는 이 가이드 전개에 쓰는 카드, 흐린 글씨(전개 외·범용)는 칸을 맞추거나 다른 용도로 넣고 뺀 카드입니다. 메인 덱 범용 카드 교체와 장수만 바뀐 카드는 덱 리스트에서 확인하세요. 숫자는 ${bn} 장수 → 이 구축 장수입니다.</div></div>`}
function links(L){return L&&L.length?`<div class="lnk">${L.map(l=>`<a href="${l.u}" target="_blank" rel="noopener">${esc(l.t)} ↗</a>`).join('')}</div>`:''}
function home(){['lv1','lv2','res2'].forEach(i=>document.getElementById(i).style.display='none');topEl.innerHTML='';cats.innerHTML='';tabs.style.display='none';cats.style.display='none';document.getElementById('legend').style.display='none';
view.innerHTML=`<p class="lead">덱을 고르면 그 덱으로 할 수 있는 전개법으로 이동합니다.</p>${SEL.map(x=>`<div class="dcard" role="button" data-k="${x.key}"><b>${esc(x.name)}</b><span>${esc(x.sub)}</span>${diffHtml(x.diff,x.baseName)}${links(x.links)}<em>${x.combos.length?`초동 ${groupsOf(x).length}개 · 전개 ${x.combos.length}개${x.deck?' · 덱 리스트 포함':''}`:'덱 리스트 보기'} →</em></div>`).join('')}`;view.querySelectorAll('.dcard a').forEach(a=>a.onclick=e=>e.stopPropagation());
view.querySelectorAll('.dcard').forEach(b=>b.onclick=()=>go(b.dataset.k))}
function draw(){if(!dk){home();return}const sy=window.scrollY;const x=SEL.find(v=>v.key===dk);document.getElementById('legend').style.display='';
topEl.innerHTML=`${single?'':'<button class="back" id="bk">← 덱 선택</button>'}<span class="dn">${esc(x.name)}</span>`;if(!single)document.getElementById('bk').onclick=()=>go('');
const isList=cur==='list';cats.style.display=x.deck?'':'none';cats.innerHTML=CU?`<button class="cat${isList?' on':''}" data-c="list">덱 리스트</button><button class="cat${isList||cur==='solve'?'':' on'}" data-c="${x.combos[0]||''}"${cuOver()>0||!x.combos.length?' disabled':''}>${cuOver()>0?'전개법 (엑스트라 초과)':'전개법 '+x.combos.length+'개'}</button>${D.solver?`<button class="cat${cur==='solve'?' on':''}" data-c="solve"${cuOver()>0?' disabled':''}>탐색</button>`:''}`:`${x.combos.length?`<button class="cat${isList?'':' on'}" data-c="${x.combos[0]}">전개법</button>`:''}<button class="cat${isList?' on':''}" data-c="list">덱 리스트</button>`;
cats.querySelectorAll('.cat').forEach(b=>b.onclick=()=>go(dk+'/'+b.dataset.c));
if(cur==='solve'){document.getElementById('hf').style.display='none';const sb=document.getElementById('sbar');sb.className='';sb.innerHTML='';document.getElementById('stk').classList.remove('on');['lv1','lv2','res2'].forEach(i=>document.getElementById(i).style.display='none');tabs.style.display='none';document.getElementById('legend').style.display='none';renderSolve();return}
document.getElementById('hf').style.display=(CU&&!isList)?'':'none';if(CU&&!isList){const sb=document.getElementById('sbar');sb.className='';sb.innerHTML='';document.getElementById('stk').classList.remove('on')}if(isList){['lv1','lv2','res2'].forEach(i=>document.getElementById(i).style.display='none');tabs.style.display='none';renderDeck(x.deck);return}
const GS0=groupsOf(x);const G=grpOf(x,cur);const GS=CU?hfRender(GS0,G):GS0;
const GT=GS.map((g,i)=>[g,gTag(g),i]).sort((a,b)=>((a[0].size||0)-(b[0].size||0))||(a[1].dr-b[1].dr)||(a[1].ns-b[1].ns)||(a[1].lk-b[1].lk)||((a[1].pu+a[1].fu)-(b[1].pu+b[1].fu))||(a[2]-b[2]));
const _szs=[...new Set(GT.map(v=>v[0].size||0))];let _ps=-1;tabs.innerHTML=GT.map(([g,t])=>`${_szs.length>1&&g.size&&g.size!==_ps?(_ps=g.size,`<div class="tsec">${g.size}장 초동</div>`):''}<button class="tab${g===G?' on':''}" data-id="${g.items[0][0]}"><span class="tn">${esc(g.name)}</span><span class="gtg">${(c0=>c0&&c0.need?(c0.gen?`<i class="g-gen">아무 몬스터 ${c0.gen}장 필요</i>`:'<i class="g-only">이 카드만</i>'):'')(D.combos.find(x=>x.id===g.items[0][0]))}${t.ns?'<i class="g-ns">일소</i>':''}${t.dr?'<i class="g-dr">드롤</i>':''}${t.lk?'<i class="g-lk">제약</i>':''}${t.pu?`<i class="g-mc">푸루 ${t.pu}</i>`:''}${t.fu?`<i class="g-mc">후와 ${t.fu}</i>`:''}</span></button>`).join('');tabs.style.display=(CU||GS.length>1)?'':'none';document.getElementById('lv1').style.display=(CU||GS.length>1)?'':'none';
const r2=document.getElementById('res2'),multi=G.items.length>1;r2.style.display=multi?'':'none';document.getElementById('lv2').style.display=multi?'':'none';
r2.innerHTML=G.items.map(([id,l],k)=>{const c=D.combos.find(z=>z.id===id);const n=k?shared(G.items[0][0],id):0;return`<button class="rb${id===cur?' on':''}" data-id="${id}"><b>${esc(l)}</b>${n>1?`<small>${n}단계부터 갈라짐</small>`:''}</button>`}).join('');
r2.querySelectorAll('.rb').forEach(b=>b.onclick=()=>{HFA={a:'#res2 .rb[data-id="'+b.dataset.id+'"]',t:b.getBoundingClientRect().top};const nid=b.dataset.id,n=shared(cur,nid),keepStep=n>1&&step<n;const st=step;go(dk+'/'+nid);if(keepStep){step=st;draw()}});
tabs.querySelectorAll('.tab').forEach(t=>t.onclick=e=>{if(tabs.dataset.moved==='1'){e.preventDefault();return}HFA={a:'#tabs .tab[data-id="'+t.dataset.id+'"]',t:t.getBoundingClientRect().top};go(dk+'/'+t.dataset.id)});
renderCombo(D.combos.find(c=>c.id===cur));const on=tabs.querySelector('.tab.on');if(on&&tabs.scrollWidth>tabs.clientWidth){const l=on.offsetLeft-tabs.offsetLeft,r=l+on.offsetWidth;if(l<tabs.scrollLeft)tabs.scrollLeft=l-8;else if(r>tabs.scrollLeft+tabs.clientWidth)tabs.scrollLeft=r-tabs.clientWidth+8}window.scrollTo(0,sy);}
function go(h,keep){const [k,c]=String(h||'').split('/');const x=SEL.find(v=>v.key===k)||(single?SEL[0]:null);const pd=dk,pc=cur;dk=x?x.key:null;cur=x?((c==='list'&&x.deck)||x.combos.includes(c)?c:(x.combos[0]||'list')):null;if(CU&&x)cur=(c==='solve'&&D.solver&&cuOver()<=0)?'solve':(c&&c!=='list'&&x.combos.includes(c)&&cuOver()<=0)?c:'list';if(!keep||pd!==dk||pc!==cur)step=0;draw();const nh=dk?dk+'/'+cur:'';if(rh()!==nh||(HP&&!location.hash.startsWith('#'+HP)))history.replaceState(null,'',nh?'#'+HP+nh:(HP?'#'+HP:location.pathname));window.scrollTo(0,0)}
(()=>{let down=false,sx=0,sl=0;tabs.addEventListener('mousedown',e=>{down=true;sx=e.pageX;sl=tabs.scrollLeft;tabs.dataset.moved='0'});
window.addEventListener('mousemove',e=>{if(!down)return;const dx=e.pageX-sx;if(Math.abs(dx)>4){tabs.dataset.moved='1';tabs.classList.add('drag')}tabs.scrollLeft=sl-dx});
window.addEventListener('mouseup',()=>{down=false;tabs.classList.remove('drag');setTimeout(()=>tabs.dataset.moved='0',0)});
tabs.addEventListener('wheel',e=>{if(tabs.scrollWidth>tabs.clientWidth&&Math.abs(e.deltaY)>Math.abs(e.deltaX)){tabs.scrollLeft+=e.deltaY;e.preventDefault()}},{passive:false});
const cur0=tabs.querySelector('.tab.on');})();
window.addEventListener('hashchange',()=>{if(AKS.length>1){const m=location.hash.match(/^#([a-z]+):/);if(!m){if(!HOME)goHome(true);return}if(m[1]!==AK||HOME){openDeck(m[1],true);return}}const h=rh();if(h!==(dk?dk+'/'+cur:''))go(h)});
document.getElementById('legend').innerHTML=Object.entries(KL).filter(([k])=>!['field','equip'].includes(k)).map(([k,v])=>`<span><i style="background:${COL[k]}"></i>${v}</span>`).join('')+'<span><i style="background:#ff6b6b"></i>링크 마커</span>'+'<span style="flex-basis:100%;height:0"></span>'+Object.keys(SKM).map(k=>`<span class="sk sk-${SKM[k]}">${k}</span>`).join('');

let CU=D.custom||null;let DS=null;
const SV_ENGINE=__SVENGINE__;
__SVUI__

function sum(o){return Object.values(o).reduce((a,b)=>a+b,0)}
function cuInit(){let s=null;try{s=JSON.parse(localStorage.getItem(CU.key)||'null')}catch(e){}
DS=s&&s.main&&s.extra&&s.on?s:cuBase();if(D.solver)svInject();cuSync()}
function cuBase(){const d={main:Object.fromEntries(CU.base.main),extra:Object.fromEntries(CU.base.extra),on:[]};const o=DS;DS=d;(CU.defOn||[]).forEach(k=>cuToggle(k));DS=o;return d}
function cuSave(){try{localStorage.setItem(CU.key,JSON.stringify(DS))}catch(e){}}
function lockOf(p,n){let m=0;const by=[];for(const b of CU.builds)if(DS.on.includes(b.key))for(const[q,k,c,mn]of b.cards)if(q===p&&k===n){m=Math.max(m,mn);by.push(b.name)}return[m,by]}
function cuOver(){return CU?sum(DS.extra)-15:0}
function cuOk(id){const r=CU.req[id];if(!r)return true;for(const p of['main','extra'])for(const[n,c]of Object.entries(r[p]||{}))if((DS[p][n]||0)<c)return false;return true}
function hscroll(el){if(!el||el._hs)return;el._hs=1;el.addEventListener('wheel',e=>{if(el.scrollWidth<=el.clientWidth||Math.abs(e.deltaX)>Math.abs(e.deltaY))return;el.scrollLeft+=e.deltaY;e.preventDefault()},{passive:false});let d=null,mv=0;el.addEventListener('mousedown',e=>{d={x:e.clientX,s:el.scrollLeft};mv=0});el.addEventListener('mousemove',e=>{if(!d)return;mv=Math.max(mv,Math.abs(e.clientX-d.x));if(mv>5){el.scrollLeft=d.s-(e.clientX-d.x);e.preventDefault()}});const end=()=>{d=null};el.addEventListener('mouseup',end);el.addEventListener('mouseleave',end);el.addEventListener('click',e=>{if(mv>5){e.stopPropagation();e.preventDefault()}mv=0},true)}
function cuGain(b){const cb=b.key.startsWith('c:');if(!cb&&DS.on.includes(b.key))return null;const add={};for(const[p,n,c]of b.cards)add[p+'|'+n]=cb?(DS[p][n]||0)+1:c;const ok=(id,th)=>{const r=CU.req[id];if(!r)return false;for(const p of['main','extra'])for(const[n,c]of Object.entries(r[p]||{})){const h=DS[p][n]||0;if((th?Math.max(h,add[p+'|'+n]||0):h)<c)return false}return true};const sh=(id,th)=>ok(id,th)&&!((CU.sup||{})[id.split('~')[0]]||[]).some(h=>ok(h,th));let g=0,rep=0;for(const gr of CU.groups)for(const it of gr.items){const a=sh(it[0],false),z=sh(it[0],true);if(!a&&z)g++;if(a&&!z)rep++}return g?{g,rep}:null}
function cuWith(b){const cb=b.key.startsWith('c:');if(!cb&&DS.on.includes(b.key))return null;const mine=new Set(b.cards.map(c=>c[0]+'|'+c[1]));const add={};for(const[p,n,c]of b.cards)add[p+'|'+n]=cb?(DS[p][n]||0)+1:c;let g=0;const oth=new Set();for(const gr of CU.groups)for(const it of gr.items){const r=CU.req[it[0]];if(!r)continue;let needMine=false;const lack=[];for(const p of['main','extra'])for(const[n,c]of Object.entries(r[p]||{})){const h=DS[p][n]||0;if(h<c){if(mine.has(p+'|'+n))needMine=true;if(Math.max(h,add[p+'|'+n]||0)<c)lack.push(n)}}if(needMine&&lack.length){g++;lack.forEach(n=>oth.add(n.replace('드래곤테일 ','').replace('데스피아의 도화 ','').replace('데스피아안 ','').replace('인도하는 성녀 ','')))}}return g?{g,oth:[...oth]}:null}
function cuSup(id){const k=id.split('~')[0];return((CU.sup||{})[k]||[]).some(h=>cuOk(h))}
function cuBtn(b){const hint=(q=>!q?'':`<i class="gn">${q.g>q.rep?`전개 +${q.g-q.rep}`:`교체 ${q.g}`}</i>`)(cuGain(b));if(!b.key.startsWith('c:'))return`<button class="bch${DS.on.includes(b.key)?' on':''}" data-b="${b.key}">${esc(b.name)}${hint}</button>`;const[p,n]=b.cards[0],c=DS[p][n]||0;return`<div class="bch bcq${c>0?' on':''}${hint?' hb':''}" data-b="${b.key}"><span class="bn">${esc(b.name)}</span><span class="bq"><button class="bqm" data-p="${p}" data-n="${esc(n)}" data-d="-1">−</button><b>${c}</b><button class="bqm" data-p="${p}" data-n="${esc(n)}" data-d="1">+</button></span><span class="bh">${hint}</span></div>`}
function cuQty(root){root.querySelectorAll('.bqm').forEach(b=>b.onclick=e=>{e.stopPropagation();const p=b.dataset.p,n=b.dataset.n;const mn=(CU.baseMap[p]||{})[n]||0;DS[p][n]=Math.max(mn,Math.min(3,(DS[p][n]||0)+Number(b.dataset.d)));cuRedraw()})}
function cuSync(){if(CU.builds.length&&CU.builds.every(b=>b.key.startsWith('c:')))DS.on=CU.builds.filter(b=>b.cards.every(([p,n])=>(DS[p][n]||0)>((CU.baseMap[p]||{})[n]||0))).map(b=>b.key);const x=SEL[0];const gs=[];for(const g of CU.groups){const it=g.items.filter(i=>cuOk(i[0])&&!cuSup(i[0]));if(it.length)gs.push({name:g.name,items:it,size:g.size,cards:g.cards})}
x.groups=gs;x.combos=gs.flatMap(g=>g.items.map(i=>i[0]));x.clinks=CU.clinks;
D.decks.my={title:'내 덱',main:Object.entries(DS.main).filter(e=>e[1]>0),extra:Object.entries(DS.extra).filter(e=>e[1]>0),note:''};cuSave()}
function cuToggle(k){const b=CU.builds.find(v=>v.key===k);if(DS.on.includes(k)){DS.on=DS.on.filter(v=>v!==k);for(const[p,n]of b.cards){const[m]=lockOf(p,n);const bc=(CU.baseMap[p]||{})[n]||0;DS[p][n]=Math.max(m,bc)}}else{DS.on.push(k);for(const[p,n,c]of b.cards)DS[p][n]=Math.max(DS[p][n]||0,c)}}
function cuCut(){let o=cuOver();for(const[n,fl]of CU.cut){if(o<=0)break;const[m]=lockOf('extra',n);const floor=Math.max(fl,m);while(o>0&&(DS.extra[n]||0)>floor){DS.extra[n]--;o--}}}
function cuRedraw(){const y=window.scrollY;cuSync();draw();window.scrollTo(0,y)}
function renderCustomDeck(){const over=cuOver(),cm=sum(DS.main),ce=sum(DS.extra),x=SEL[0];
const act=[...CU.baseCombos.map(id=>[id,'기본 전개'])];CU.builds.filter(b=>DS.on.includes(b.key)).forEach(b=>(b.combos||[]).forEach(id=>act.push([id,b.name+' 전개'])));
const NEED={};for(const[id,src]of act){const r=CU.req[id];if(!r)continue;for(const p of['main','extra'])for(const[n,k]of Object.entries(r[p]||{})){const e=NEED[p+'|'+n]=NEED[p+'|'+n]||{max:0,by:[],ids:new Set(),need:{}};e.max=Math.max(e.max,k);if(!e.by.includes(src))e.by.push(src);e.need[id]=k}}
for(const[k,e]of Object.entries(NEED)){const[p,n]=k.split('|');const c=DS[p][n]||0;e.lack=Object.values(e.need).filter(v=>v>c).length}
const row=(p,n)=>{const c=DS[p][n]||0,k=kindOf(n)||(p==='extra'?'fusion':'eff'),im=(D.img||{})[n],[m,by]=lockOf(p,n);const z=c===0,kp=z&&(DS.keep||[]).includes(p+'|'+n);const nd=NEED[p+'|'+n],ub=m||!nd?[]:nd.by;return`<div class="row${m?' lock':''}${ub.length&&!z?' use':''}${z?' zero':''}${z&&ub.length?' need0':''}"><div class="thw">${im?`<img class="th" src="${im}" style="border-color:${COL[k]}">`:`<i style="background:${COL[k]}"></i>`}${kp?`<button class="rx" data-p="${p}" data-n="${esc(n)}">제외</button>`:''}</div><span>${esc(n)}${m?`<br><em class="lt">${esc(by.join(' · '))} 구축 카드${m>1||c>m?` · 최소 ${m}장`:''}</em>`:''}${ub.length?`<em class="ut${nd&&c<nd.max?' bad':''}">${ub.map(s=>s==='기본 전개'?'<mark class="ub ubb">기본 전개</mark>':`<mark class="ub">${esc(s.replace(/ 전개$/,''))}</mark>`).join(' ')}</em>`:''}${nd&&nd.max>1?`<em class="nb${c<nd.max?' bad':''}">${nd.max}장 필요</em>`:''}</span><button class="pm" data-p="${p}" data-n="${esc(n)}" data-d="-1"${c<=m?' disabled':''}>−</button><b class="ct">${c}${nd&&c<nd.max?`<small class="lk2">전개 ${nd.lack}개 불가</small>`:''}</b><button class="pm" data-p="${p}" data-n="${esc(n)}" data-d="1"${c>=3?' disabled':''}>+</button></div>`};
const GEN=CU.gen||[];const gsum=GEN.reduce((a,n)=>a+(DS.main[n]||0),0);const kept=n=>(DS.keep||[]).includes(p0+'|'+n);let p0='';const list=(p,on)=>(p0=p,CU.pool[p].filter(n=>!GEN.includes(n)).filter(n=>on?((DS[p][n]||0)>0||kept(n)):!((DS[p][n]||0)>0||kept(n)))).map(n=>row(p,n)).join('');
const KO={eff:0,spell:1,trap:2,fusion:3,synchro:4,xyz:5,link:6};
const tiles=p=>{const ns=CU.pool[p].concat(p==='main'?GEN:[]).filter((n,ix,a)=>a.indexOf(n)===ix&&(DS[p][n]||0)>0);ns.sort((a,b)=>(KO[kindOf(a)]??9)-(KO[kindOf(b)]??9));
return ns.flatMap(n=>{const c=DS[p][n],[m]=lockOf(p,n),nd=NEED[p+'|'+n],im=(D.img||{})[n],k=kindOf(n)||'eff';const cls=m?'lk':(nd&&nd.max>c?'bd':(nd?'us':''));const sel=window._gs===p+'|'+n?' sel':'';
return Array.from({length:c},()=>`<div class="gt ${cls}" title="${esc(n)}">${im?`<img src="${im}">`:`<span style="background:${COL[k]}">${esc(n)}</span>`}<button class="gq gqm" data-p="${p}" data-n="${esc(n)}" data-d="-1" aria-label="${esc(n)} 1장 빼기">−</button><button class="gq gqp" data-p="${p}" data-n="${esc(n)}" data-d="1" aria-label="${esc(n)} 1장 넣기"${c>=3?' disabled':''}>+</button></div>`)}).join('')};
const gridHtml=()=>{
return `<p class="note" style="margin:6px 2px">카드 아래의 − + 로 장수를 바꿉니다. 초록 테두리는 전개에 쓰는 카드, 빨간 점선은 장수가 모자라는 카드입니다.</p><h2>메인 덱 <small>${cm}장</small></h2><div class="gd">${tiles('main')}</div><h2>엑스트라 덱 <small>${ce}장${over>0?' · '+over+'장 초과':''}</small></h2><div class="gd">${tiles('extra')}</div>`};
const hows=CU.builds.filter(b=>DS.on.includes(b.key)&&b.how&&b.how.length);
view.innerHTML=`<div class="hd"><b>내 덱 · 전개 카드</b><span>추가 구축을 켜면 그 구축 카드가 들어가고 파란 테두리로 고정됩니다(구축을 끄면 빠짐). 나머지 카드는 − / + 로 넣고 뺄 수 있고, 지금 덱으로 가능한 전개만 전개법에 나옵니다. 설정은 이 기기에 저장됩니다.</span></div>
<div class="lvr"><span class="lv">추가 카드 (− + 로 장수 조절)</span><button class="rst2" id="rst2">${window._rq?"한 번 더 누르면 초기화":"초기화"}</button></div><div class="bchips">${CU.builds.map(b=>`${cuBtn(b)}`).join('')}</div>
${over>0?`<div class="warn"><b>엑스트라 덱이 ${ce}장입니다.</b> ${over}장을 더 빼야 전개법을 볼 수 있습니다. 아래 엑스트라 덱 목록에서 직접 빼 주세요.</div>`:`<div class="okb">이 덱으로 가능한 전개 <b>${x.combos.length}개</b> · 초동 ${x.groups.length}종 — 위의 "전개법"에서 볼 수 있습니다.</div>`}
<div class="deck"><div class="slots"><div><b>${cm}장</b><span>메인 덱 합계<br>${cm<40?`40장까지 ${40-cm}장 남음`:cm>60?'60장 초과':'40~60장 OK'}</span></div><div><b>${gsum}장</b><span>그중 범용 카드<br>(패 트랩 등)</span></div><div><b>${ce}장</b><span>엑스트라 덱<br>${ce>15?'15장 초과':`범용 칸 ${15-ce}장`}</span></div></div>
<div class="vt"><button data-v="list" class="${DS.view!=='grid'?'on':''}">목록 보기</button><button data-v="grid" class="${DS.view==='grid'?'on':''}">카드 보기 (마스터 듀얼처럼)</button></div>${DS.view==='grid'?gridHtml():`<h2>메인 덱 · 전개 카드 <small>${cm-gsum}장 (메인 합계 ${cm}장)</small></h2>${list('main',1)}
<h2>엑스트라 덱 · 전개 카드 <small>${ce}장${over>0?' · '+over+'장 초과':''}</small></h2>${list('extra',1)}
<h2>메인 덱 · 범용 카드 <small>${gsum}장 · 패 트랩 등</small></h2>${GEN.map(n=>row('main',n)).join('')}
`}<details class="more"><summary>덱에 없는 카드 추가하기</summary><h3>메인 덱</h3>${list('main',0)||'<p class="note">없음</p>'}<h3>엑스트라 덱</h3>${list('extra',0)||'<p class="note">없음</p>'}</details>
${CU.notes?`<details class="more"><summary>초동 손패 안내 (같은 결과 · 안 되는 손패)</summary><div class="how">${CU.notes.map(t=>`<p>${esc(t)}</p>`).join('')}</div></details>`:''}${hows.length?`<details class="more"><summary>켠 구축 카드 설명</summary>${hows.map(b=>`<h3>${esc(b.name)}</h3><div class="how">${b.how.map(t=>`<p>${esc(t)}</p>`).join('')}</div>`).join('')}</details>`:''}
<p class="note">범용 카드는 전개 계산에 쓰지 않고 장수만 셉니다. 목록에 없는 범용 카드는 남은 칸에 직접 채우시면 됩니다.</p><button class="rst" id="rst">초기화 (기본 파츠로 되돌리기)</button></div>`;
const sbar=document.getElementById('sbar');document.getElementById('stk').classList.add('on');const _wc=sbar.classList.contains('chips');sbar.className='on'+(_wc?' chips':'');
const _sl=(sbar.querySelector('.sch')||{}).scrollLeft||0;sbar.innerHTML=`<div class="sst"><span class="stt">메인 <b>${cm}장</b> · 엑스트라 <b class="${over>0?'bad':''}">${ce}장${over>0?` (${over}장 초과)`:''}</b> · 가능한 전개 <b>${x.combos.length}개</b></span><button class="rst3${window._rq?' warn2':''}" id="rst3">${window._rq?'한 번 더':'초기화'}</button></div><div class="sch">${CU.builds.map(b=>`${cuBtn(b)}`).join('')}</div>`;
{const sc=sbar.querySelector('.sch');if(sc){sc.scrollLeft=_sl;hscroll(sc)}}sbar.querySelectorAll('.bch').forEach(b=>b.onclick=()=>{cuToggle(b.dataset.b);cuRedraw()});cuQty(sbar);document.getElementById('rst3').onclick=()=>document.getElementById('rst2').click();
cuStick();
view.querySelectorAll('.pm').forEach(b=>b.onclick=()=>{const p=b.dataset.p,n=b.dataset.n;DS[p][n]=Math.max(0,Math.min(3,(DS[p][n]||0)+Number(b.dataset.d)));DS.keep=DS.keep||[];const k=p+'|'+n;if(DS[p][n]===0&&!GEN.includes(n)){if(!DS.keep.includes(k))DS.keep.push(k)}else DS.keep=DS.keep.filter(v=>v!==k);cuRedraw()});
view.querySelectorAll('.vt button').forEach(b=>b.onclick=()=>{DS.view=b.dataset.v;window._gs='';cuRedraw()});
view.querySelectorAll('.gq').forEach(b=>b.onclick=()=>{const p=b.dataset.p,n=b.dataset.n;DS[p][n]=Math.max(0,Math.min(3,(DS[p][n]||0)+Number(b.dataset.d)));DS.keep=DS.keep||[];const k=p+'|'+n;if(DS[p][n]===0&&!GEN.includes(n)){if(!DS.keep.includes(k))DS.keep.push(k)}else DS.keep=DS.keep.filter(v=>v!==k);cuRedraw()});
const gx=document.getElementById('gx');if(gx)gx.onclick=()=>{window._gs='';cuRedraw()};
view.querySelectorAll('.rx').forEach(b=>b.onclick=()=>{const k=b.dataset.p+'|'+b.dataset.n;DS.keep=(DS.keep||[]).filter(v=>v!==k);cuRedraw()});
view.querySelectorAll('.bch').forEach(b=>b.onclick=()=>{cuToggle(b.dataset.b);cuRedraw()});cuQty(view);

document.getElementById('rst').onclick=()=>{DS=cuBase();window._rq=0;cuRedraw()};document.getElementById('rst2').onclick=()=>{if(window._rq){DS=cuBase();window._rq=0}else{window._rq=1;setTimeout(()=>{if(window._rq){window._rq=0;cuRedraw()}},3000)}cuRedraw()}}


function cuStick(){const sbar=document.getElementById('sbar');if(!sbar||!sbar.classList.contains('on'))return;const sst=sbar.querySelector('.sst');if(!sst)return;const lim=sst.getBoundingClientRect().bottom;
const gr=view.querySelector('.bchips'),r2=document.getElementById('rst2');
sbar.classList.toggle('chips',!!gr&&gr.getBoundingClientRect().top<lim);
sbar.classList.toggle('rsts',!!r2&&r2.getBoundingClientRect().top<lim);
const gs=view.querySelector('.gsel');if(gs){const sc=sbar.querySelector('.sch');gs.style.top=(document.getElementById('stk').offsetHeight+(sbar.classList.contains('chips')&&sc?sc.offsetHeight:0))+'px'}}
function fshow(){const bd=view&&view.querySelector('.board'),ft=view&&view.querySelector('.foot');if(!bd||!ft){document.body.classList.remove('fshow');return}const nav=ft.querySelector('.nav'),bx=ft.firstElementChild;const bh=bx&&bx!==nav?(parseFloat(bx.style.minHeight)||bx.offsetHeight||180):0;const lim=innerHeight-(nav?nav.offsetHeight:56)-bh-30;document.body.classList.toggle('fshow',bd.getBoundingClientRect().top<lim)}window.addEventListener('scroll',()=>{if(CU)cuStick();fshow()},{passive:true});
let hfS=0,hfC=[];
function hfRender(GS,G){const hf=document.getElementById('hf');HFX=GS.length>30;
if(G&&!hfMatch(G))hfS=0,hfC=[];
const sizes=[...new Set(GS.map(g=>g.size||0))].sort();
const inS=GS.filter(g=>!hfS||g.size===hfS);
const cards=[...new Set(GS.flatMap(g=>g.cards||[]))].filter(c=>inS.some(g=>(g.cards||[]).includes(c)));
const _hl=[...hf.querySelectorAll('.hr')].map(e=>e.scrollLeft);hf.innerHTML=`<div class="hr sz"><button data-s="0" class="${hfS?'':'on'}">전체</button>${sizes.map(s=>`<button data-s="${s}" class="${hfS===s?'on':''}">${s}장 초동</button>`).join('')}</div>${cards.length>1?`<div class="hr"><button data-c="" class="${hfC.length?'':'on'}">${GS.length>30?'선택 해제':'모든 카드'}</button>${cards.map(c=>{const on=hfC.includes(c);const ok=on||inS.some(g=>[...hfC,c].every(x=>(g.cards||[]).includes(x))&&(!HFX||(g.cards||[]).every(x=>[...hfC,c].includes(x))));return`<button data-c="${esc(c)}" class="${on?'on':''}"${ok?'':' disabled'}>${esc(c)}</button>`}).join('')}</div>`:''}`;hf.querySelectorAll('.hr').forEach((e,k)=>{e.scrollLeft=_hl[k]||0;hscroll(e)});
hf.querySelectorAll('[data-s],[data-c]').forEach(b=>b.addEventListener('click',()=>{HFA={a:b.dataset.s!==undefined?'#hf [data-s="'+b.dataset.s+'"]':'#hf [data-c="'+CSS.escape(b.dataset.c)+'"]',t:b.getBoundingClientRect().top}},true));
hf.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>{hfS=Number(b.dataset.s);hfC=hfC.filter(x=>GS.some(g=>(!hfS||g.size===hfS)&&hfC.every(y=>(g.cards||[]).includes(y))));hfGo(GS)});
hf.querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>{const v=b.dataset.c;if(!v)hfC=[];else hfC=hfC.includes(v)?hfC.filter(x=>x!==v):[...hfC,v];hfGo(GS)});
if(HFA){const A=HFA;const fix=()=>{const e=document.querySelector(A.a);if(e)window.scrollBy(0,e.getBoundingClientRect().top-A.t)};fix();requestAnimationFrame(()=>{fix();requestAnimationFrame(()=>{fix();HFA=null})})}
const big=GS.length>30;if(big&&!hfC.length){const n=document.createElement('div');n.className='hr';n.style.cssText='font-size:12px;opacity:.7;padding:2px 4px';n.textContent='위에서 고른 카드로만 이루어진 손패가 아래에 나옵니다 (NDM·F&V는 자동 포함, 여러 장 선택 가능)';hf.appendChild(n)}
return GS.filter(g=>hfMatch(g)&&(!big||hfC.length||g===G))}
const GLK=/이 턴은|이 턴에는|이후 이 턴|만 특수 소환|특수 소환할 수 없|에서만 특수/;function gTag(g){const c=D.combos.find(z=>z.id===g.items[0][0]);if(!c)return{ns:0,dr:0,lk:0,pu:0,fu:0};const m=c.mc||{sr:0,pu:0,fu:0};const ns=c.steps.some(s=>/일반 소환/.test(s.title))?1:0;const st=c.steps.slice(1).filter(s=>(g.cards||[]).some(k=>s.title.includes(k)));const t=st.map(s=>(s.act||'')+' '+(s.desc||'')).join(' ');return{ns,dr:m.sr>=2?1:0,lk:GLK.test(t)?1:0,pu:m.pu,fu:m.fu}}
let HFA=null,HFX=false;function hfMatch(g){return(!hfS||g.size===hfS)&&(hfC.every(x=>(g.cards||[]).includes(x)))&&(!HFX||!hfC.length||(g.cards||[]).every(x=>hfC.includes(x)))}
function hfGo(GS){const f=GS.filter(hfMatch);const G=grpOf(SEL[0],cur);if(G&&hfMatch(G)){draw();return}if(f.length)go(dk+'/'+f[0].items[0][0]);else draw()}

function homeOrder(){let o=[];try{o=JSON.parse(localStorage.getItem('guide-order')||'[]')}catch(e){}o=o.filter(k=>ALL[k]);AKS.forEach(k=>{if(!o.includes(k))o.push(k)});return o}
function renderHome(){document.getElementById('ttl').textContent='마스터 듀얼 전개 필드 가이드';document.title='마스터 듀얼 전개 필드 가이드';
['lv1','lv2','res2','legend','hf','fnote'].forEach(i=>{const e=document.getElementById(i);if(e)e.style.display='none'});tabs.style.display='none';cats.style.display='none';topEl.innerHTML='';
const ord=homeOrder();
view.innerHTML=`<div id="hl">${ord.map(k=>{const d=ALL[k],cu=d.custom||{};const n=(cu.groups||[]).reduce((a,g)=>a+g.items.length,0);return`<div class="hc" data-a="${k}"><div class="hcb"><b>${esc(d.short||k)}</b><span>${esc(d.title||'')}</span><em>전개 ${n}개${cu.builds&&cu.builds.length?` · 추가 구축 ${cu.builds.length}개`:''}</em></div><div class="hg" aria-label="순서 이동">≡</div></div>`}).join('')}</div>`;
const hl=document.getElementById('hl');let drag=null,timer=null,sy=0,moved=false;
const save=()=>{try{localStorage.setItem('guide-order',JSON.stringify([...hl.children].map(e=>e.dataset.a)))}catch(e){}};
let grab=0;const place=y=>{const nat=hl.getBoundingClientRect().top+drag.offsetTop;drag.style.transform=`translateY(${y-grab-nat}px) scale(1.02)`};const start=(el,y)=>{drag=el;grab=y-el.getBoundingClientRect().top;el.classList.add('drg');el.style.transition='none';place(y);if(navigator.vibrate)try{navigator.vibrate(15)}catch(e){}};
const move=y=>{if(!drag)return;const mid=y-grab+drag.offsetHeight/2-hl.getBoundingClientRect().top;const sib=[...hl.children].filter(e=>e!==drag);let tgt=null;for(const e of sib){if(mid<e.offsetTop+e.offsetHeight/2){tgt=e;break}}if(drag.nextElementSibling!==tgt||(tgt===null&&hl.lastElementChild!==drag)){const before=new Map(sib.map(e=>[e,e.offsetTop]));hl.insertBefore(drag,tgt);sib.forEach(e=>{const d=before.get(e)-e.offsetTop;if(d){e.style.transition='none';e.style.transform=`translateY(${d}px)`;e.offsetHeight;e.style.transition='transform .18s ease';e.style.transform=''}})}place(y)};
const end=()=>{if(timer){clearTimeout(timer);timer=null}if(drag){const d=drag;drag=null;d.style.transition='transform .18s ease';d.style.transform='';setTimeout(()=>{d.classList.remove('drg');d.style.transition=''},190);save();return true}return false};
hl.querySelectorAll('.hc').forEach(el=>{
 const grip=el.querySelector('.hg');
 grip.addEventListener('touchstart',e=>{start(el,e.touches[0].clientY);e.preventDefault()},{passive:false});
 grip.addEventListener('mousedown',e=>{start(el,e.clientY);e.preventDefault()});
 el.addEventListener('touchstart',e=>{if(drag)return;moved=false;const y0=e.touches[0].clientY;sy=y0;timer=setTimeout(()=>{timer=null;if(!moved)start(el,y0)},450)},{passive:true});
 el.addEventListener('touchmove',e=>{const y=e.touches[0].clientY;if(drag){e.preventDefault();move(y);return}if(Math.abs(y-sy)>8){moved=true;if(timer){clearTimeout(timer);timer=null}}},{passive:false});
 el.addEventListener('touchend',e=>{if(end()){e.preventDefault();return}});
 el.addEventListener('mousedown',e=>{if(e.target.closest('.hg'))return;moved=false;sy=e.clientY;timer=setTimeout(()=>{timer=null;if(!moved)start(el,e.clientY)},450)});
 el.addEventListener('click',e=>{if(e.target.closest('.hg')||el.dataset.nc){delete el.dataset.nc;return}openDeck(el.dataset.a)});
});
window.addEventListener('mousemove',e=>{if(drag)move(e.clientY);else if(timer&&Math.abs(e.clientY-sy)>6){moved=true;clearTimeout(timer);timer=null}});
window.addEventListener('mouseup',e=>{const d=drag;if(end()&&d)d.dataset.nc='1'});
}

function resetUI(){['lv1','lv2','res2','hf'].forEach(i=>{const e=document.getElementById(i);if(e)e.style.display='none'});const lg=document.getElementById('legend');if(lg)lg.style.display='';const fn=document.getElementById('fnote');if(fn)fn.style.display='';const sb=document.getElementById('sbar');sb.className='';sb.innerHTML='';document.getElementById('stk').classList.remove('on');tabs.style.display='';cats.style.display='';hfS=0;hfC=[];window._gs='';window._rq=0}
function openDeck(k,fromHash){if(!ALL[k])return;AK=k;D=ALL[k];HP=k+':';HOME=false;SEL=D.decksel;single=SEL.length===1;CU=D.custom||null;NAMES=null;FH={};DS=null;dk=null;cur=null;step=0;try{localStorage.setItem('guide-ak',k)}catch(e){}
resetUI();setArc();if(CU)cuInit();if(!fromHash)history.replaceState(null,'','#'+HP);go(fromHash?rh():'');window.scrollTo(0,0)}
function goHome(fromHash){HOME=true;dk=null;cur=null;resetUI();setArc();if(!fromHash)history.replaceState(null,'',location.pathname+location.search+'#');renderHome();window.scrollTo(0,0)}
setArc();if(HOME)renderHome();else{if(CU)cuInit();
go(rh());}
document.addEventListener('keydown',e=>{if(!dk||cur==='list'||cur==='solve')return;const c=D.combos.find(x=>x.id===cur);if(e.key==='ArrowRight'&&step<c.steps.length-1){step++;draw()}if(e.key==='ArrowLeft'&&step>0){step--;draw()}});
</script></body></html>'''

import os
GEN=['하루 우라라','이펙트 뵐러','드롤 & 로크 버드','증식의 G','마루챠미 후와로스','마루챠미 푸루리아','유령토끼','저택 와라시','무한포영','원시생명체 니비루','삼전의 재','에너미 컨트롤러','말살의 지명자','금지된 일적','무덤의 지명자','에스:피 리틀나이트','로기어스텔라 티 폰']
os.makedirs('site_yubel',exist_ok=True); os.makedirs('site_twin',exist_ok=True)
def _diff(base,deck,dat=None):
    dat=dat or data
    from collections import Counter
    out={'add':{},'rem':{}}
    isgen=lambda n:any(n==g or n.startswith(g+' ') for g in GEN)
    for part in ('main','extra'):
        a=Counter(dict(dat['decks'][base][part]));b=Counter(dict(dat['decks'][deck][part]));rg=dat['decks'][deck].get('range',{})
        for key,c in (('add',b-a),('rem',a-b)):
            out[key][part]=sorted([[n.replace(' (현재 금지 · 빼야 함)',''),v,isgen(n),'(현재 금지' in n,a.get(n,0),rg.get(n,b.get(n,0))] for n,v in c.items()],key=lambda r:(r[2],r[0]))
    return out
def page(path,title,decksel,img=None,dat=None,gen=None,custom=None):
    global GEN
    if gen is not None: GEN=gen
    dat=dat or data
    for x in decksel:
        if x.get('base'):
            df=_diff(x['base'],x['deck'],dat)
            bx=next((y for y in decksel if y['deck']==x['base'] or y['key']==x['base']),None)
            def used(ids):
                u=set()
                for c in dat['combos']:
                    if c['id'] in ids:
                        for st in c['steps']:
                            u.update(z['name'].replace(' (장착)','') for z in st['zones'].values()); u.update(st['hand']); u.update(st['gy']); u.update(st['ban'])
                            u.update(n for n in dat['decks'][x['deck']]['main']+dat['decks'][x['deck']]['extra'] for n in [n[0]] if n in st['title'] or n in st['desc'])
                return u
            ua=used(x['combos']); ub=used(bx['combos']) if bx else set()
            df['oth']={'add':[],'rem':[]}
            for part in ('main','extra'):
                fs=x.get('force',{})
                ka=[r+[fs.get(r[0],'')] for r in df['add'][part] if r[4]==0 and not r[2] and (not x['combos'] or r[0] in ua or r[0] in fs)]
                kr=[r for r in df['rem'][part] if str(r[5])=='0' and not r[2] and (not bx or not bx['combos'] or r[0] in ub)]
                df['oth']['add']+=[[part]+r for r in df['add'][part] if r[4]==0 and r[0] not in [k[0] for k in ka]]
                df['oth']['rem']+=[[part]+r for r in df['rem'][part] if str(r[5])=='0' and r not in kr]
                df['add'][part]=ka; df['rem'][part]=kr
            x['diff']=df
    ids=[i for x in decksel for i in x['combos']]
    d={'combos':[c for c in dat['combos'] if c['id'] in ids],'decks':dat['decks'],'kinds':dat.get('kinds',{}),'gen':GEN,'decksel':decksel,'img':img or {},'custom':custom,'title':title}
    if path: open(path,'w').write(_sv(html).replace('__TITLE__',title).replace('__DATA__',json.dumps({'x':d},ensure_ascii=False)))
    return d
def page_multi(path,title,sets):
    open(path,'w').write(_sv(html).replace('__TITLE__',title).replace('__DATA__',json.dumps(sets,ensure_ascii=False)))
if __name__=='__main__':
    page('site_yubel/index.html','유벨 데먼스미스 전개 필드 가이드',[
     {'key':'yubel','name':'유벨 데먼스미스 덱','sub':'참고 구축','deck':'yubel','combos':['y1','y2','y3','y4'],'labels':{'y1':'로터스 1장','y2':'초래신 또는 해문 1장','y3':'마세데 1장','y4':'초래신 + 로터스'}}],json.load(open('img2.json')))
    page('site_twin/index.html','이빌트윈 데먼스미스 전개 필드 가이드',[
     {'key':'mine','name':'내 덱','sub':'보내주신 덱 캡처 기준. 전개 카드는 김빠방 영상 신청자 덱과 거의 같고 리일라 스위트 1장 · 트러블상 2장','deck':'mine','combos':['my','g1','g2','f1','f2','v1'],
      'groups':[{'name':'키스킬 또는 리일라 1장','items':[['my','기본: 시져·써니·아바오 → 상대 턴 그리폰'],['g1','선턴 그리폰 A: 그리폰 + 써니 남김'],['g2','선턴 그리폰 B: 그리폰 + 시져 남김']]},
       {'name':'키스킬 프로스트 1장','items':[['f1','시져·아바오·세퀜티아']]},
       {'name':'프로스트 + 리일라 스위트','items':[['f2','시져·써니·아바오·세퀜티아']]},
       {'name':'트러블상 + 리일라','items':[['v1','라기아·시져·써니·아바오 (영상 1판)']]}],
      'labels':{'my':'키스킬/리일라 1장 (기본)','g1':'1장 · 그리폰+써니','g2':'1장 · 그리폰+시져','f1':'프로스트 1장','f2':'프로스트 + 스위트','v1':'트러블상 + 리일라'},
      'links':[{'t':'전개 영상 (김빠방, 1판 0:29~)','u':'https://www.youtube.com/watch?v=NBOZD7IEm6Q&t=29s'}],
      'clinks':{'my':[{'t':'기본 엔진 영상 (김빠방 1판)','u':'https://www.youtube.com/watch?v=NBOZD7IEm6Q&t=29s'}],'v1':[{'t':'영상 1판 0:29~1:58','u':'https://www.youtube.com/watch?v=NBOZD7IEm6Q&t=29s'}]}},
     {'key':'kim','name':'재단마인 추가 구축','force':{'언체인드소울 샤바라':'슈야마 대신, 야마로 서치'},'sub':'No.65 재단마인 저지 버스터를 먼저 깔아 두고 전개해서, 니비루를 맞아도 무효 1장이 남게 하는 니비루 대비 구축 (저지 버스터를 내기 위해 리일라 트리트를 같이 넣음)','base':'mine','deck':'vid_own','combos':['o1'],
      'labels':{'o1':'키스킬 + 트리트 (니비루 대비)'},
      'links':[{'t':'덱 리스트 (영상 설명란 덱 코드 9rppb77)','u':'https://www.youtube.com/watch?v=NBOZD7IEm6Q'},{'t':'전개 설명 글 (콤보 1)','u':'https://ygoprodeck.com/deck/fiendsmith-live-twins-post-alin-593378'}],
      'clinks':{'o1':[{'t':'전개 설명 글 (콤보 1)','u':'https://ygoprodeck.com/deck/fiendsmith-live-twins-post-alin-593378'}]}},
     {'key':'ref','name':'언체인드 쌍극 추가 구축','sub':'언체인드 쌍극과 디에스이레를 넣어 디에스이레 무효 3과 그리폰 봉인을 같이 세우는 구축','base':'mine','deck':'twin','combos':['t1'],
      'labels':{'t1':'키스킬 1장 (디에스이레·쌍극)'},
      'links':[{'t':'전개 설명 글 (Master Duel Meta)','u':'https://www.masterduelmeta.com/top-decks/dice-rally---fusion-synchro-link/february-2026/live%E2%98%86twin/waffle/doT4a'}],
      'clinks':{'t1':[{'t':'전개 설명 글 (Master Duel Meta)','u':'https://www.masterduelmeta.com/top-decks/dice-rally---fusion-synchro-link/february-2026/live%E2%98%86twin/waffle/doT4a'}]}},
    ],json.load(open('img2.json')))

def _sv(h):
    import os
    b=os.path.dirname(os.path.abspath(__file__))
    eng=open(os.path.join(b,'dtsolve','engine.js')).read(); ui=open(os.path.join(b,'dtsolve','ui.js')).read()
    return h.replace('__SVENGINE__',json.dumps(eng,ensure_ascii=False).replace('</','<\\/')).replace('__SVUI__',ui.replace('</','<\\/'))
