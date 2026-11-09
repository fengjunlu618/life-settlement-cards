#!/usr/bin/env python3
# 从《高性价比人生指南》正文生成「人生结算单」随机抽卡页
import json, random, re, html, os

BASE = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(BASE, 'items.json'), encoding='utf-8'))
random.seed()

def esc(s):
    return html.escape(s or '', quote=True)

def linkify(s):
    s = esc(s)
    return re.sub(r'&lt;(https?://[^&]+?)&gt;', r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)

def stamp_cls(e):
    return 'stamp-' + (e[0].lower() if e else 'c')

def card(it, idx, new=True):
    sec = f'第 {it["sec"]} 节 · {it["secName"]}'
    aud = f'<p class="aud">适用人群：{esc(it["audience"])}</p>' if it.get('audience') else ''
    gain_val = it['benefit'] or '—'
    basis = it['basis'] or '—'
    return f'''<article class="slip" style="--i:{idx}"{' data-new="1"' if new else ''}>
  <div class="slip-head"><span class="sec">{esc(sec)}</span><span class="num">{idx+1:02d}</span></div>
  <h2 class="slip-title">{esc(it['title'])}</h2>
  <p class="slip-plain">{esc(it['plain'])}</p>
  <div class="cost">
    <div class="cost-cell"><span class="k">钱</span><span class="v">{esc(it['money'])}</span></div>
    <div class="cost-cell"><span class="k">时间</span><span class="v">{esc(it['time'])}</span></div>
    <div class="cost-cell"><span class="k">毅力</span><span class="v">{esc(it['will'])}</span></div>
  </div>
  <div class="gain">
    <span class="gain-val">收益 <b>{esc(gain_val)}</b><span class="basis">口径 {esc(basis)}</span></span>
    <span class="stamp {stamp_cls(it['evidence'])}">证据 {esc(it['evidence'] or '—')}</span>
  </div>
  {aud}
  <div class="slip-foot">
    <span class="coord">第 {it['no']} 条</span>
    <button class="more" type="button" aria-expanded="false">
      <span>原文与来源</span>
      <svg class="chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 6l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>
    </button>
  </div>
  <div class="detail" hidden>
    <div class="d-block"><h3>成本</h3><p>{linkify(it['cost'])}</p></div>
    <div class="d-block"><h3>收益 · 书里怎么算的</h3><p>{linkify(it['gain'])}</p></div>
    <div class="d-block"><h3>备注</h3><p>{linkify(it['note'])}</p></div>
    <div class="d-block"><h3>来源</h3><p class="src">{linkify(it['source'])}</p></div>
  </div>
</article>'''

def pick(n=10):
    return random.sample(items, n)

def summary(sel):
    order = ['死亡率', '金钱', '时间', '自由']
    c = {k: sum(1 for i in sel if i['basis'] == k) for k in order}
    parts = [f'{k} <b>{v}</b>' for k, v in c.items() if v]
    return '本次口径分布　' + '　'.join(parts)

initial = pick(10)
cards_html = '\n'.join(card(it, i, new=False) for i, it in enumerate(initial))
summary_html = summary(initial)

CSS = r'''
:root{--bg:#131409;--ink:#F2EFE4;--dim:#B3AE9C;--paper:#F2EFE4;--paper-ink:#1D1C16;--rule:#CDC6B2;--muted:#6B675A;--red:#B23A2E;--blue:#26456B;--amber:#8A6A2F}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:radial-gradient(1100px 620px at 18% -12%, #24261B 0%, #15160E 52%, #0D0E08 100%) no-repeat, #0D0E08;color:var(--ink);
  font-family:"Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;font-size:15px;line-height:1.6}
.wrap{max-width:1180px;margin:0 auto;padding:26px 16px 56px}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;
  border-top:1px solid rgba(242,239,228,.22);border-bottom:1px solid rgba(242,239,228,.22);padding:9px 0;
  font-size:12px;letter-spacing:.05em;color:var(--dim)}
.topbar a{color:var(--dim);text-decoration:none;border-bottom:1px solid rgba(242,239,228,.3)}
h1{font-family:"Noto Serif SC","Songti SC",serif;font-weight:700;font-size:clamp(38px,8.4vw,72px);line-height:1.08;
  margin:20px 0 12px;letter-spacing:.02em}
.lede{font-size:14.5px;line-height:1.75;color:#C9C4B3;max-width:34em;margin:0}
.lede b{color:var(--ink);font-weight:600}
.action{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:22px}
.refresh{display:inline-flex;align-items:center;gap:10px;height:52px;padding:0 22px;border:0;border-radius:3px;
  background:var(--red);color:#FDF6E9;font:inherit;font-size:15px;font-weight:600;letter-spacing:.02em;cursor:pointer;
  transition:background .15s ease,transform .1s ease}
.refresh:hover{background:#9C2F25}
.refresh:active{transform:translateY(1px)}
.refresh:focus-visible{outline:2px solid #FDF6E9;outline-offset:2px}
.refresh svg{width:17px;height:17px}
.refresh.spin svg{animation:spin .55s ease}
@keyframes spin{to{transform:rotate(360deg)}}
.round{font-size:12.5px;color:#A8A393}
.round b{color:var(--ink);font-weight:600}
.stats{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:20px;font-size:12.5px;color:var(--dim)}
.stats span{display:inline-flex;align-items:baseline;gap:6px}
.stats i{font-family:"Noto Serif SC",serif;font-style:normal;font-weight:700;font-size:19px;color:var(--ink)}
.summary{display:flex;justify-content:space-between;align-items:baseline;gap:8px 16px;flex-wrap:wrap;
  border-top:1px solid rgba(242,239,228,.2);border-bottom:1px solid rgba(242,239,228,.2);
  padding:10px 0;margin:28px 0 22px;font-size:13px;color:var(--dim)}
.summary .dist{color:#EAE6D6}
.summary .dist b{font-family:"Noto Serif SC",serif;font-weight:700;font-size:16px;color:var(--ink);margin-left:2px}
.list{column-count:1;column-gap:24px}
@media (min-width:880px){.list{column-count:2}}
.slip{background:var(--paper);color:var(--paper-ink);border-radius:2px;padding:16px 18px 10px;margin:0 0 24px;
  break-inside:avoid;position:relative;box-shadow:0 1px 0 rgba(0,0,0,.45),0 18px 30px -26px rgba(0,0,0,.9)}
.slip::before{content:"";position:absolute;left:0;top:0;width:100%;height:3px;
  background:linear-gradient(90deg,var(--red) 0 46px,var(--rule) 46px 100%)}
.slip[data-new]{animation:rise .5s cubic-bezier(.2,.72,.2,1) both;animation-delay:calc(var(--i) * 45ms)}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.slip-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.sec{font-size:12px;color:var(--muted);letter-spacing:.04em}
.num{font-family:"Noto Serif SC",serif;font-weight:700;font-size:30px;line-height:1;color:var(--red)}
.slip-title{font-family:"Noto Serif SC","Songti SC",serif;font-weight:700;font-size:clamp(19px,2.1vw,23px);
  line-height:1.38;margin:6px 0 10px}
.slip-plain{font-size:14.5px;line-height:1.8;color:#34322A;margin:0 0 12px}
.cost{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--rule)}
.cost-cell{padding:7px 0 7px;border-bottom:1px solid var(--rule);display:flex;align-items:baseline;gap:7px}
.cost-cell:nth-child(n+2){padding-left:10px;border-left:1px solid var(--rule)}
.cost-cell .k{font-size:11.5px;color:var(--muted);letter-spacing:.08em}
.cost-cell .v{font-family:"Noto Serif SC",serif;font-weight:700;font-size:17px}
.gain{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 0 8px;
  border-bottom:1px solid var(--rule)}
.gain-val{font-size:12px;color:var(--muted);letter-spacing:.04em}
.gain-val b{font-family:"Noto Serif SC",serif;font-weight:700;font-size:16px;color:var(--paper-ink);margin:0 8px 0 4px}
.basis{font-size:11.5px;color:var(--muted)}
.stamp{font-family:"Noto Serif SC",serif;font-weight:700;font-size:12px;letter-spacing:.06em;
  padding:2px 7px;border:1.5px solid currentColor;border-radius:3px;transform:rotate(-7deg);white-space:nowrap}
.stamp-a{color:var(--red)}
.stamp-b{color:var(--amber)}
.stamp-c{color:var(--muted)}
.aud{font-size:12px;color:var(--amber);margin:8px 0 0;letter-spacing:.02em}
.slip-foot{display:flex;justify-content:space-between;align-items:center;gap:10px;padding-top:4px}
.coord{font-size:11.5px;color:var(--muted);letter-spacing:.06em}
.more{display:inline-flex;align-items:center;gap:5px;min-height:44px;padding:0 2px;border:0;background:none;
  color:var(--blue);font:inherit;font-size:13px;cursor:pointer}
.more:hover span{text-decoration:underline;text-underline-offset:3px}
.more .chev{transition:transform .2s ease;margin-top:1px}
.more[aria-expanded="true"] .chev{transform:rotate(180deg)}
.more:focus-visible{outline:2px solid var(--blue);outline-offset:-2px}
.detail{border-top:1px dashed var(--rule);margin-top:2px;padding-top:2px}
.d-block h3{font-size:11.5px;font-weight:500;letter-spacing:.1em;color:var(--muted);margin:12px 0 4px}
.d-block p{font-size:13px;line-height:1.78;color:#3C3A30;margin:0}
.d-block a{color:var(--blue);word-break:break-all}
.src{font-size:12px !important;line-height:1.7 !important;color:#565346 !important}
footer{border-top:1px solid rgba(242,239,228,.2);margin-top:34px;padding-top:14px;
  display:flex;justify-content:space-between;gap:10px 24px;flex-wrap:wrap;font-size:12px;line-height:1.7;color:#A8A393}
footer a{color:#C9C4B3}
footer .note{max-width:44em}
@media (max-width:520px){
  .wrap{padding:20px 14px 44px}
  .refresh{width:100%;justify-content:center}
  .action{gap:10px}
  .summary{margin:22px 0 18px}
}
@media (prefers-reduced-motion:reduce){.slip{animation:none !important}.refresh svg{animation:none !important}}
'''

JS = r'''
const DATA = __DATA__;

function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function linkify(s){return esc(s).replace(/&lt;(https?:[^&]*?)&gt;/g, function(_,u){return '<a href="'+u+'" target="_blank" rel="noopener">'+u+'</a>';});}
function stampCls(e){return 'stamp-'+((e||'c')[0].toLowerCase());}

function cardHTML(it, idx){
  var sec = '第 '+it.sec+' 节 · '+esc(it.secName);
  var aud = it.audience ? '<p class="aud">适用人群：'+esc(it.audience)+'</p>' : '';
  return '<article class="slip" style="--i:'+idx+'" data-new="1">'
    + '<div class="slip-head"><span class="sec">'+sec+'</span><span class="num">'+String(idx+1).padStart(2,'0')+'</span></div>'
    + '<h2 class="slip-title">'+esc(it.title)+'</h2>'
    + '<p class="slip-plain">'+esc(it.plain)+'</p>'
    + '<div class="cost">'
    + '<div class="cost-cell"><span class="k">钱</span><span class="v">'+esc(it.money)+'</span></div>'
    + '<div class="cost-cell"><span class="k">时间</span><span class="v">'+esc(it.time)+'</span></div>'
    + '<div class="cost-cell"><span class="k">毅力</span><span class="v">'+esc(it.will)+'</span></div>'
    + '</div>'
    + '<div class="gain"><span class="gain-val">收益 <b>'+esc(it.benefit||'—')+'</b><span class="basis">口径 '+esc(it.basis||'—')+'</span></span>'
    + '<span class="stamp '+stampCls(it.evidence)+'">证据 '+esc(it.evidence||'—')+'</span></div>'
    + aud
    + '<div class="slip-foot"><span class="coord">第 '+it.no+' 条</span>'
    + '<button class="more" type="button" aria-expanded="false"><span>原文与来源</span>'
    + '<svg class="chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 6l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button></div>'
    + '<div class="detail" hidden>'
    + '<div class="d-block"><h3>成本</h3><p>'+linkify(it.cost)+'</p></div>'
    + '<div class="d-block"><h3>收益 · 书里怎么算的</h3><p>'+linkify(it.gain)+'</p></div>'
    + '<div class="d-block"><h3>备注</h3><p>'+linkify(it.note)+'</p></div>'
    + '<div class="d-block"><h3>来源</h3><p class="src">'+linkify(it.source)+'</p></div>'
    + '</div></article>';
}

function pick(n){
  var a = DATA.slice(), out=[], k=Math.min(n,a.length);
  for(var i=0;i<k;i++){
    var j = i + Math.floor(Math.random()*(a.length-i));
    var t = a[i]; a[i]=a[j]; a[j]=t;
    out.push(a[i]);
  }
  return out;
}

var listEl = document.getElementById('list');
var distEl = document.getElementById('dist');
var roundEl = document.getElementById('round');
var btn = document.getElementById('refresh');
var round = 1;
var busy = false;

function summarize(sel){
  var order=['死亡率','金钱','时间','自由'], out=[];
  order.forEach(function(k){
    var c = sel.filter(function(i){return i.basis===k;}).length;
    if(c) out.push(k+' <b>'+c+'</b>');
  });
  distEl.innerHTML = '本次口径分布　' + out.join('　');
}

function reveal(sel){
  listEl.innerHTML = sel.map(cardHTML).join('');
  summarize(sel);
  roundEl.innerHTML = '第 <b>'+round+'</b> 次抽取';
}

btn.addEventListener('click', function(){
  if(busy) return;
  busy = true;
  btn.classList.add('spin');
  var sel = pick(10);
  round += 1;
  setTimeout(function(){
    reveal(sel);
    btn.classList.remove('spin');
    busy = false;
  }, 260);
});

document.addEventListener('click', function(ev){
  var b = ev.target.closest('.more');
  if(!b) return;
  var detail = b.closest('.slip').querySelector('.detail');
  var open = b.getAttribute('aria-expanded') === 'true';
  b.setAttribute('aria-expanded', open ? 'false' : 'true');
  detail.hidden = open;
});

document.addEventListener('keydown', function(ev){
  if(ev.key === 'r' || ev.key === 'R'){
    if(document.activeElement && /input|textarea/i.test(document.activeElement.tagName)) return;
    btn.click();
  }
});
'''

def main():
    data_json = json.dumps(items, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html_doc = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>人生结算单 · 随机十条</title>
<meta name="description" content="从《高性价比人生指南》772 条正文里随机抽 10 条人生建议，带成本标签、收益口径与证据等级。">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect x='4' y='3' width='24' height='26' fill='%23F2EFE4'/%3E%3Crect x='4' y='3' width='24' height='4' fill='%23B23A2E'/%3E%3Cpath d='M8 13h16M8 18h16M8 23h10' stroke='%231D1C16' stroke-width='1.4'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://miaoda.feishu.cn">
<link rel="preconnect" href="https://sf3-scmcdn-cn.feishucdn.com" crossorigin>
<link rel="stylesheet" href="https://miaoda.feishu.cn/fonts/css2?family=Noto+Serif+SC:wght@700&amp;family=Noto+Sans+SC:wght@400;500&amp;display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <span>《高性价比人生指南》· 正文抽取</span>
    <a href="https://github.com/eternity4719/HowToLiveBetter" target="_blank" rel="noopener">原文仓库</a>
  </div>

  <h1>人生结算单</h1>
  <p class="lede">从书里 <b>772 条</b>建议中每次随机抽 <b>10 条</b>。每条都按书自己的算法标出成本（钱 / 时间 / 毅力）、收益量级与口径、证据等级；点开可看原文数据和出处。按 <b>R</b> 也能换一批。</p>

  <div class="action">
    <button class="refresh" id="refresh" type="button">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11a8 8 0 1 0-2.3 5.7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 4v7h-7" fill="none" stroke="currentColor" stroke-width="2"/></svg>
      重新抽十条
    </button>
    <span class="round" id="round">第 <b>1</b> 次抽取</span>
  </div>

  <div class="stats">
    <span><i>772</i>条建议</span>
    <span><i>34</i>节正文</span>
    <span><i>497</i>条 A 级证据</span>
    <span><i>223</i>条 B 级</span>
  </div>

  <div class="summary">
    <span class="dist" id="dist">{summary_html}</span>
    <span>收益口径不同不互相折算，各排各的</span>
  </div>

  <div class="list" id="list">
{cards_html}
  </div>

  <footer>
    <span class="note">数据来自《高性价比人生指南》正文（CC BY 4.0），共 772 条；成本与收益档位为作者判断。这里给的是通用口径，不替代医生、律师、会计。</span>
    <a href="https://github.com/eternity4719/HowToLiveBetter" target="_blank" rel="noopener">github.com/eternity4719/HowToLiveBetter</a>
  </footer>
</div>
<script>{JS.replace('__DATA__', data_json)}</script>
</body>
</html>'''
    out = os.path.join(BASE, '人生结算单-随机十条.html')
    open(out, 'w', encoding='utf-8').write(html_doc)
    print('written', out, round(os.path.getsize(out)/1024/1024, 2), 'MB')

if __name__ == '__main__':
    main()
