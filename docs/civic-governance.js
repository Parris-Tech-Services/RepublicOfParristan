// Public, read-only view of the fictional Civic Service simulation.
'use strict';
const API='https://parristan-living-nation.parris-neathaustralia.workers.dev/api/civic';
const $=id=>document.getElementById(id);
const format=x=>Number(x||0).toLocaleString('en-AU',{minimumFractionDigits:2,maximumFractionDigits:2});
const date=x=>new Date(x).toLocaleString('en-AU',{timeZone:'Australia/Sydney',dateStyle:'medium',timeStyle:'short'});
const text=(tag,s,cls)=>{const el=document.createElement(tag);el.textContent=String(s??'');if(cls)el.className=cls;return el;};
function card(a){
  const el=text('article','', 'civic-card');
  el.append(text('span',a.charter==='chartered'?'Chartered in game policy':'Proposed / not yet chartered','civic-chip'));
  el.append(text('h3',a.name));
  el.append(text('p',a.settlement+' · '+a.residents+' fictional residents','civic-quiet'));
  const group=text('div','', 'civic-metrics');
  for(const [name,value] of [['Balance',format(a.budgetParri)+' Parri'],['Receipts',format(a.receivedParri)+' Parri'],
    ['Spent',format(a.spentParri)+' Parri'],['Programmes funded',a.fundedProgrammes]]){
    const item=text('div','', 'civic-metric');item.append(text('small',name),text('strong',value));group.append(item);
  }
  el.append(group);
  const last=a.lastFundedService?'Last funded in simulation: '+a.lastFundedService:'No funded programme recorded yet';
  el.append(text('p',last,'civic-quiet'));
  if(a.charter==='chartered'){
    const roles=a.serviceRoles||[];
    el.append(text('h4','Local service-related professions'));
    const list=text('p',roles.length?roles.slice(0,8).map(r=>r.name+' ('+r.occupation+(r.currentlyWorking?', working':'')+')').join(', '):'No matching workers in the current simulation snapshot.','civic-quiet');
    el.append(list);
  }
  return el;
}
async function refreshCivic(){
  const button=$('civic-refresh'),status=$('civic-status');button.disabled=true;
  status.textContent='Loading persistent fictional world data…';
  const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),12000);
  try{
    const response=await fetch(API,{cache:'no-store',signal:controller.signal});
    if(!response.ok)throw Error('HTTP '+response.status);
    const civic=await response.json();
    if(civic?.fictional!==true||civic?.realWorldFees!==false||civic?.legalAuthority!==false||
      civic?.votesFromAIResidents!==false||!Array.isArray(civic.associations)||civic.associations.length!==12)
      throw Error('Unexpected or unsafe simulation response');
    $('civic-summary').replaceChildren();
    for(const [label,value] of [['Simulation tick',civic.tick],['Settlements',civic.associations.length],
      ['Chartered local associations',civic.associations.filter(a=>a.charter==='chartered').length],
      ['Last world update',date(civic.updatedAt)] ]){
      const item=text('div','','civic-stat');item.append(text('span',label),text('strong',value));$('civic-summary').append(item);
    }
    const sorted=civic.associations.slice().sort((a,b)=>(b.charter==='chartered')-(a.charter==='chartered')||a.town-b.town);
    $('civic-cards').replaceChildren(...sorted.map(card));
    const ledger=(civic.ledger||[]).slice(0,25);
    const nodes=ledger.map(x=>{
      const row=text('div','','civic-entry');
      row.append(text('span',date(x.at)+' · '+x.description));
      const value=text('strong',(x.amountCents>=0?'+':'')+format(x.amountCents/100)+' Parri');
      row.append(value);return row;
    });
    $('civic-ledger').replaceChildren(...(nodes.length?nodes:[text('p','The civic ledger has not recorded any transactions yet.','civic-quiet')]));
    status.textContent='Connected · Last simulation tick: '+date(civic.updatedAt)+'. All amounts are fictional Parri.';
  }catch(e){
    status.textContent='Live fictional civic data unavailable: '+String(e?.message||e)+'. The published ordinary policy remains in the Gazette.';
    if(!$('civic-cards').children.length)$('civic-cards').append(text('p','No live budget figures can be verified at present.','civic-quiet'));
  }finally{clearTimeout(timeout);button.disabled=false;}
}
$('civic-refresh')?.addEventListener('click',refreshCivic);
refreshCivic();
