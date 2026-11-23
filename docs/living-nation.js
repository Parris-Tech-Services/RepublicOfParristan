// Republic of Parristan Living Nation — public, read-only client.
// Fictional residents are deliberately separate from real membership records.
const API = 'https://parristan-living-nation.parris-neathaustralia.workers.dev/api/world';
const CACHE_KEY = 'parristan-fictional-world-v1';
const $ = selector => document.querySelector(selector);
const escape = value => String(value??'').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const fmt = value => Number(value||0).toLocaleString('en-AU');
const townName = (world,id) => world.settlements.find(t=>t.id===id)?.name||'Unknown town';
const initial = name => name.split(/\s+/).slice(0,2).map(p=>p[0]).join('').toUpperCase();
const map = $('#world-map'),ctx = map.getContext('2d');
let world=null,selectedId=1,eventFilter='all',loading=false;
let townFilter='all',activityFilter='all',clockFrame=0,staticMap=null;
const eventIcons={community:'✦',friendship:'♡',business:'▣',travel:'➜',work:'⚒',housing:'⌂',culture:'♫'};
function localClock(date) {
  return new Intl.DateTimeFormat('en-AU',{timeZone:'Australia/Sydney',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).format(date);
}
function ago(ms) {
  const minutes=Math.max(0,Math.floor((Date.now()-Number(ms))/60000));
  if(minutes<2)return 'Just now';
  if(minutes<60)return minutes+' min ago';
  if(minutes<1440)return Math.floor(minutes/60)+' h ago';
  return Math.floor(minutes/1440)+' d ago';
}
function connection(label,detail,mode) {
  $('#connection-label').textContent=label;
  $('#last-update').textContent=detail;
  $('#connection-dot').className='dot '+(mode||'');
}
function statusFromWorld(cached=false) {
  if(!world)return;
  const age=Math.max(0,Math.floor((Date.now()-world.updatedAt)/60000));
  if(cached)connection('Cached snapshot','Backend unavailable · '+ago(world.updatedAt),'amber');
  else if(world.tick===0)connection('World initialised','First 15-minute update pending','amber');
  else if(age>45)connection('Updates delayed','Last world tick '+ago(world.updatedAt),'amber');
  else connection('World is running','Last world tick '+ago(world.updatedAt),'');
}
function renderMetrics() {
  $('#population').textContent=fmt(world.citizens.length);
  $('#settlement-count').textContent=world.settlements.length;
  $('#tick-count').textContent=fmt(world.tick);
  $('#world-time').textContent=localClock(new Date());
}
function populateTowns() {
  const select=$('#town-select'),prev=select.value;
  select.replaceChildren();
  const all=document.createElement('option');all.value='all';all.textContent='All settlements';select.append(all);
  for(const t of world.settlements){const option=document.createElement('option');option.value=t.id;option.textContent=t.name;select.append(option);}
  select.value=prev&&[...select.options].some(o=>o.value===prev)?prev:'all';
  townFilter=select.value;
}
function matches(c) {
  return (townFilter==='all'||String(c.homeTown)===townFilter) &&
    (activityFilter==='all'||c.activity===activityFilter);
}
function findCitizen(id) {return world?.citizens.find(c=>c.id===id);}
function renderList() {
  if(!world)return;
  const query=$('#citizen-search').value.trim().toLocaleLowerCase();
  const people=world.citizens.filter(c=>matches(c)&&(!query||(c.name+' '+c.occupation+' '+c.interest).toLocaleLowerCase().includes(query))).slice(0,12);
  const container=$('#citizen-list');container.replaceChildren();
  if(!people.length){const p=document.createElement('p');p.className='citizen-empty';p.textContent='No residents match. Try another name or filter.';container.append(p);return;}
  people.forEach(c=>{
    const button=document.createElement('button');button.type='button';
    button.className='citizen-option'+(c.id===selectedId?' active':'');
    button.setAttribute('aria-pressed',String(c.id===selectedId));
    const avatar=document.createElement('span');avatar.className='mini-avatar';avatar.textContent=initial(c.name);
    const body=document.createElement('span');const name=document.createElement('strong');name.textContent=c.name;
    const description=document.createElement('small');description.textContent=c.occupation+' · '+townName(world,c.homeTown);
    body.append(name,description);button.append(avatar,body);
    button.addEventListener('click',()=>selectCitizen(c.id));container.append(button);
  });
}
function score(label,value) {
  const n=Math.max(0,Math.min(100,Number(value)||0));
  return '<div class="score-row"><span>'+escape(label)+'</span><b>'+Math.round(n)+'%</b></div><div class="bar"><i style="width:'+n+'%"></i></div>';
}
function renderProfile() {
  const c=findCitizen(selectedId),container=$('#citizen-profile');
  if(!c){container.textContent='Select a resident.';return;}
  const connections=c.friends.slice(0,4).map(id=>findCitizen(id)?.name).filter(Boolean);
  const memory=c.memories.length?c.memories.map(s=>'<li>'+escape(s)+'</li>').join(''):'<li>Still writing their story…</li>';
  container.innerHTML='<div class="profile-header"><div class="avatar">'+escape(initial(c.name))+'</div><div><h3 class="profile-name">'+escape(c.name)+'</h3><p class="profile-job">'+escape(c.occupation)+' · Citizen #'+c.id+'</p></div></div>'+
    '<div class="profile-grid"><div><span>Lives in</span><strong>'+escape(townName(world,c.homeTown))+'</strong></div><div><span>Currently</span><strong>'+escape(c.activity)+'</strong></div>'+
    '<div><span>Workplace</span><strong>'+escape(townName(world,c.workTown))+'</strong></div><div><span>Savings</span><strong>'+fmt(Math.floor(c.credits))+' Parri</strong></div></div>'+
    '<div class="profile-focus"><label>Personal ambition</label><p>'+escape(c.goal)+'</p></div>'+
    '<div class="profile-focus"><label>Interest</label><p>'+escape(c.interest)+(c.business?' · Runs a '+escape(c.business):'')+'</p></div>'+
    '<div class="profile-focus"><label>Wellbeing</label>'+score('Energy',c.energy)+score('Mood',c.mood)+'</div>'+
    '<div class="profile-focus"><label>Connections</label><p>'+(connections.length?escape(connections.join(', ')):'No close friendships recorded yet')+'</p></div>'+
    '<div class="profile-focus"><label>Recent memories</label><ul class="memories">'+memory+'</ul></div>';
}
function selectCitizen(id) {
  selectedId=id;renderList();renderProfile();draw(performance.now());
}
function renderEvents() {
  if(!world)return;
  const events=world.events.filter(e=>eventFilter==='all'||e.type===eventFilter);
  $('#events-count').textContent=fmt(events.length)+' stories saved';
  const feed=$('#event-feed');feed.replaceChildren();
  if(!events.length){const empty=document.createElement('p');empty.className='muted';empty.textContent='No stories in this category yet. Residents create new events as the world advances.';feed.append(empty);return;}
  for(const event of events.slice(0,40)) {
    const card=document.createElement('article');card.className='event';
    const icon=document.createElement('span');icon.className='event-symbol';icon.setAttribute('aria-hidden','true');icon.textContent=eventIcons[event.type]||'✦';
    const inner=document.createElement('div');const title=document.createElement('p');title.className='event-text';title.textContent=event.text;
    const meta=document.createElement('p');meta.className='event-meta';meta.textContent=ago(event.at)+' · '+townName(world,event.town)+' · '+event.type;
    inner.append(title,meta);card.append(icon,inner);
    if(event.actor){card.style.cursor='pointer';card.setAttribute('title','View resident');card.addEventListener('click',()=>{selectCitizen(event.actor);$('#citizen-profile').scrollIntoView({behavior:'smooth',block:'nearest'});});}
    feed.append(card);
  }
}
function coords(t){return [t.x*10,t.y*6.2];}
function makeMap() {
  if(!world)return;
  const bg=document.createElement('canvas');bg.width=map.width;bg.height=map.height;
  const g=bg.getContext('2d'),W=map.width,H=map.height;
  const ocean=g.createLinearGradient(0,0,W,H);ocean.addColorStop(0,'#102d40');ocean.addColorStop(1,'#0c3441');
  g.fillStyle=ocean;g.fillRect(0,0,W,H);
  g.strokeStyle='#2f576355';g.lineWidth=1;
  for(let i=0;i<=W;i+=50){g.beginPath();g.moveTo(i,0);g.lineTo(i,H);g.stroke();}
  for(let i=0;i<=H;i+=50){g.beginPath();g.moveTo(0,i);g.lineTo(W,i);g.stroke();}
  g.save();g.shadowColor='#051623';g.shadowBlur=25;
  const ground=g.createLinearGradient(100,20,800,580);ground.addColorStop(0,'#274d4b');ground.addColorStop(.58,'#1b4344');ground.addColorStop(1,'#365549');
  g.beginPath();[[32,48],[240,20],[445,54],[658,15],[936,30],[983,120],[952,303],[987,510],[832,574],[610,610],[404,585],[217,605],[62,522],[14,313]].forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));
  g.closePath();g.fillStyle=ground;g.fill();g.restore();g.strokeStyle='#68918a';g.lineWidth=2;g.stroke();
  // Decorative uplands, fields and waterways. This is intentionally not a geographical claim.
  g.fillStyle='#60867525';
  for(const [x,y,r] of [[200,160,80],[700,200,130],[530,480,95],[280,460,120]]){g.beginPath();g.ellipse(x,y,r,r*.43,-.4,0,Math.PI*2);g.fill();}
  g.strokeStyle='#79a7b477';g.lineWidth=10;g.beginPath();g.moveTo(430,43);g.bezierCurveTo(475,190,690,300,725,590);g.stroke();
  g.strokeStyle='#b1d6d045';g.lineWidth=3;g.stroke();
  // Road connections between each settlement and its two closest neighbours.
  const edges=new Set();
  world.settlements.forEach(a=>{
    const others=world.settlements.filter(b=>b.id!==a.id).sort((b,c)=>Math.hypot(a.x-b.x,a.y-b.y)-Math.hypot(a.x-c.x,a.y-c.y));
    const targets=[...others.slice(0,2),world.settlements[0]].filter(b=>b.id!==a.id);
    for(const b of targets){const key=[a.id,b.id].sort((x,y)=>x-y).join('-');if(edges.has(key))continue;edges.add(key);
      const [x1,y1]=coords(a),[x2,y2]=coords(b);
      g.beginPath();g.moveTo(x1,y1);g.lineTo(x2,y2);g.lineWidth=3;g.strokeStyle='#95ac9869';g.stroke();
      g.lineWidth=1;g.strokeStyle='#d6ceb89a';g.stroke();
    }
  });
  g.textAlign='center';
  for(const t of world.settlements) {
    const [x,y]=coords(t),big=t.kind==='capital';g.fillStyle='#0b232c';
    g.beginPath();g.arc(x,y,big?14:10,0,Math.PI*2);g.fill();
    g.strokeStyle='#d1c18f';g.lineWidth=big?3:2;g.stroke();
    g.fillStyle=big?'#e4c781':'#a9d6c4';g.beginPath();g.arc(x,y,big?5:3,0,Math.PI*2);g.fill();
    g.font=(big?'bold 19px ':'bold 15px ')+'system-ui';g.fillStyle='#ebf5e6';
    g.shadowColor='#09222b';g.shadowBlur=7;
    g.fillText(t.name,x,Math.max(18,y-19));g.shadowBlur=0;
  }
  g.font='italic 12px Georgia,serif';g.fillStyle='#8db4bb';
  g.fillText('THE LIVING NATION · ILLUSTRATIVE ATLAS',225,594);
  staticMap=bg;
}
function colour(c) {
  if(c.activity==='travelling')return '#f8ca70';
  if(c.activity==='working')return '#83e5a3';
  if(c.activity==='sleeping')return '#829cac';
  return '#d4fff2';
}
function draw(t) {
  if(!world||!staticMap)return;
  ctx.clearRect(0,0,map.width,map.height);ctx.drawImage(staticMap,0,0);
  const selected=findCitizen(selectedId);
  for(const c of world.citizens){
    if(!matches(c)&&c.id!==selectedId)continue;
    const x=c.x*10+Math.sin(t/2200+c.id*1.21)*1.6;
    const y=c.y*6.2+Math.cos(t/2500+c.id*.91)*1.6;
    if(c.id===selectedId)continue;
    ctx.beginPath();ctx.arc(x,y,2.45,0,Math.PI*2);ctx.fillStyle=colour(c);ctx.globalAlpha=.86;ctx.fill();
  }
  ctx.globalAlpha=1;
  if(selected) {
    const x=selected.x*10,y=selected.y*6.2;
    ctx.beginPath();ctx.arc(x,y,11+Math.sin(t/500)*2,0,Math.PI*2);ctx.strokeStyle='#ffe3a0';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.arc(x,y,4.5,0,Math.PI*2);ctx.fillStyle='#fff7df';ctx.fill();
  }
}
function animate(t) {
  if(t-clockFrame>55){draw(t);clockFrame=t;}
  requestAnimationFrame(animate);
}
function renderAll(){
  if(!world)return;
  renderMetrics();populateTowns();renderList();renderProfile();renderEvents();makeMap();draw(performance.now());
}
async function loadWorld() {
  if(loading)return;
  loading=true;$('#refresh').disabled=true;
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);
  try {
    const response=await fetch(API,{cache:'no-store',signal:controller.signal});
    if(!response.ok)throw new Error('HTTP '+response.status);
    const next=await response.json();
    if(next.fictional!==true||next.population!==500||!Array.isArray(next.citizens)||next.citizens.length!==500)throw new Error('Unexpected world format');
    world=next;try{localStorage.setItem(CACHE_KEY,JSON.stringify(next));}catch{}
    renderAll();statusFromWorld(false);
  }catch(error){
    if(!world){try{const cached=JSON.parse(localStorage.getItem(CACHE_KEY)||'null');if(cached?.fictional&&Array.isArray(cached.citizens)){world=cached;renderAll();}}catch{}}
    if(world)statusFromWorld(true);
    else {connection('Connection unavailable','No saved snapshot on this device','error');$('#event-feed').textContent='Could not load the world: '+String(error.message||error)+'. Try Refresh.';}
  }finally{clearTimeout(timer);loading=false;$('#refresh').disabled=false;}
}
map.addEventListener('click',e=>{
  if(!world)return;
  const rect=map.getBoundingClientRect(),mx=(e.clientX-rect.left)/rect.width*map.width,my=(e.clientY-rect.top)/rect.height*map.height;
  const people=world.citizens.filter(matches).map(c=>({id:c.id,d:Math.hypot(c.x*10-mx,c.y*6.2-my)})).sort((a,b)=>a.d-b.d);
  if(people.length&&people[0].d<32){selectCitizen(people[0].id);return;}
  const towns=world.settlements.map(t=>({id:t.id,d:Math.hypot(t.x*10-mx,t.y*6.2-my)})).sort((a,b)=>a.d-b.d);
  if(towns.length&&towns[0].d<40){$('#town-select').value=String(towns[0].id);townFilter=$('#town-select').value;renderList();}
});
$('#citizen-search').addEventListener('input',renderList);
$('#town-select').addEventListener('change',e=>{townFilter=e.target.value;renderList();});
$('#activity-select').addEventListener('change',e=>{activityFilter=e.target.value;renderList();});
$('#refresh').addEventListener('click',loadWorld);
document.querySelectorAll('[data-event]').forEach(button=>button.addEventListener('click',()=>{
  eventFilter=button.dataset.event;
  document.querySelectorAll('[data-event]').forEach(b=>b.classList.toggle('chosen',b===button));
  renderEvents();
}));
document.addEventListener('visibilitychange',()=>{if(!document.hidden)loadWorld();});
setInterval(()=>{if(world){renderMetrics();statusFromWorld(false);renderEvents();}},60000);
setInterval(loadWorld,90000);
requestAnimationFrame(animate);
loadWorld();
