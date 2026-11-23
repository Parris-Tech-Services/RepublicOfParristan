/**
 * Republic of Parristan — Living Nation (fictional simulation).
 * Cloudflare Worker + D1. No paid LLM, personal data or public mutation API.
 * Data never represents real citizenship, elections or government actions.
 */
export const TICK_MS = 15 * 60 * 1000;
export const SETTLEMENTS = [
  { id: 0, name: 'Founders Square', x: 49, y: 49, kind: 'capital' },
  { id: 1, name: 'Starhaven', x: 23, y: 18, kind: 'town' },
  { id: 2, name: 'Tealford', x: 66, y: 17, kind: 'town' },
  { id: 3, name: 'Goldmere', x: 85, y: 39, kind: 'town' },
  { id: 4, name: 'Westhaven', x: 12, y: 49, kind: 'town' },
  { id: 5, name: 'Bluewater', x: 81, y: 75, kind: 'port' },
  { id: 6, name: 'Birchfield', x: 36, y: 78, kind: 'village' },
  { id: 7, name: 'Rivermark', x: 56, y: 67, kind: 'town' },
  { id: 8, name: 'Dawnridge', x: 48, y: 12, kind: 'village' },
  { id: 9, name: 'Hearthbrook', x: 15, y: 78, kind: 'village' },
  { id: 10, name: 'Southridge', x: 62, y: 90, kind: 'village' },
  { id: 11, name: 'Lantern Point', x: 91, y: 12, kind: 'village' }
];
const FIRST = ['Amelia','Thomas','Maya','Oliver','Zara','Leo','Harper','Noah','Grace','Elias','Ruby','Aria','Ben','Willow','Ava','Riley','Oscar','Ivy','Samuel','Ella','Jasper','Luna','Ada','Miles','Sophie','Felix','Nora','Theo','Isla','Piper','Ezra','Hazel','Alice','Finn','Tahlia','Rowan','Mira','Hugo','Clara','Kai','Anika','Patrick','Elena','Toby','Sienna','Arthur','Freya','Nina','Liam','Milo'];
const LAST = ['Reed','Walker','Bennett','Nguyen','Singh','Morgan','Cole','Archer','Hawkins','Patel','Miller','Brooks','Cooper','Quinn','Bell','Carter','Wright','Turner','Scott','Hughes','Foster','Hall','Young','King','Hill','Price','Ward','Perry','Russell','Grant','Ellis','Murray','Doyle','Ash','Lee','Walsh','Harper','Dawson','Cook','Wilson','Blake','Ford','Gray','Campbell','Moore','Evans','Green','Hayes','Clarke','Taylor'];
export const JOBS = ['Baker','Teacher','Librarian','Nurse','Carpenter','Farmer','Mechanic','Software developer','Artist','Grocer','Bus driver','Gardener','Cafe worker','Accountant','Electrician','Builder','Ranger','Chef','Researcher','Shopkeeper','Translator','Counsellor','Postal worker','Musician'];
const GOALS = ['Make new friends','Save for a home','Grow a small business','Learn a new skill','Help the community','Visit every town','Improve local transport','Create something beautiful','Build a thriving garden','Spend more time with friends'];
const INTERESTS = ['gardening','music','books','sport','technology','cooking','nature','crafts','local history','volunteering'];
const ACTIVITIES = ['sleeping','at home','commuting','working','having breakfast','shopping','socialising','volunteering','exploring','travelling','at a cafe'];
const clamp = (x,a,b) => Math.max(a,Math.min(b,x));
const choose = (rng,items) => items[Math.floor(rng()*items.length)];
const rand = seed => { let a=seed>>>0; return () => {a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return ((t^(t>>>14))>>>0)/4294967296;}; };
const settle = id => SETTLEMENTS[id] || SETTLEMENTS[0];
const where = (town,rng) => ({x:clamp(town.x+(rng()-.5)*8,2,98),y:clamp(town.y+(rng()-.5)*8,3,97)});
const dayInfo = ms => {
  const parts = new Intl.DateTimeFormat('en-AU',{timeZone:'Australia/Sydney',weekday:'short',hour:'2-digit',hourCycle:'h23'}).formatToParts(new Date(ms));
  const val = key => parts.find(p=>p.type===key)?.value;
  return {hour:Number(val('hour')),weekend:['Sat','Sun'].includes(val('weekday'))};
};
export function seedWorld(now=Date.now(),count=500) {
  const rng=rand(0xC0FFEE);
  const citizens=[];
  for(let i=0;i<count;i++) {
    const homeTown=i%SETTLEMENTS.length;
    const home=where(settle(homeTown),rng);
    let workTown=homeTown;
    if(rng()<.12) workTown=Math.floor(rng()*SETTLEMENTS.length);
    const job=choose(rng,JOBS);
    citizens.push({
      id:i+1,name:FIRST[i%FIRST.length]+' '+LAST[Math.floor(i/FIRST.length)%LAST.length],
      homeTown,workTown,x:home.x,y:home.y,homeX:home.x,homeY:home.y,
      workX:where(settle(workTown),rng).x,workY:where(settle(workTown),rng).y,
      visitTown:null,visitUntil:0,occupation:job,goal:choose(rng,GOALS),
      interest:choose(rng,INTERESTS),character:{
        curiosity:Math.round(rng()*100),sociability:Math.round(rng()*100),diligence:Math.round(rng()*100)
      },
      credits:Math.round(80+rng()*480),energy:Math.round(55+rng()*40),mood:Math.round(50+rng()*45),
      activity:'at home',business:null,friends:[],memories:[],lastAction:'Settled into '+settle(homeTown).name
    });
  }
  return {schema:1,simulation:'fictional',startedAt:now,updatedAt:now,tick:0,settlements:SETTLEMENTS,
    citizens,events:[{id:0,at:now,type:'community',town:0,actor:0,
      text:'The fictional Living Nation simulation began with '+count+' residents across 12 settlements.'}]};
}
function remember(person,text) {
  person.memories.unshift(text);
  if(person.memories.length>5) person.memories.length=5;
  person.lastAction=text;
}
function record(world,person,time,type,text) {
  world.events.push({id:world.tick*1000+person.id,at:time,type,town:person.homeTown,actor:person.id,text});
  remember(person,text);
  if(world.events.length>800)world.events.splice(0,world.events.length-800);
}
function story(world,person,rng,time) {
  const event=Math.floor(rng()*7), town=settle(person.homeTown), others=world.citizens;
  let text,kind='community';
  if(event===0 && !person.business) {
    person.business=person.interest+' studio';
    person.credits=Math.max(0,person.credits-35);
    kind='business';text=person.name+' opened a '+person.business+' in '+town.name+'.';
  }else if(event===1) {
    const newJob=choose(rng,JOBS);
    if(newJob===person.occupation)return;
    person.occupation=newJob;person.credits+=15;
    kind='work';text=person.name+' started a new job as a '+newJob.toLowerCase()+' in '+town.name+'.';
  }else if(event===2) {
    const neighbour=others[Math.floor(rng()*others.length)];
    if(neighbour.id===person.id||person.friends.includes(neighbour.id))return;
    person.friends.push(neighbour.id);if(person.friends.length>12)person.friends.shift();
    if(!neighbour.friends.includes(person.id)){neighbour.friends.push(person.id);if(neighbour.friends.length>12)neighbour.friends.shift();}
    person.mood=clamp(person.mood+6,0,100);neighbour.mood=clamp(neighbour.mood+4,0,100);
    kind='friendship';text=person.name+' and '+neighbour.name+' became friends through their shared interest in '+person.interest+'.';
    remember(neighbour,'Became friends with '+person.name+'.');
  }else if(event===3) {
    let next=Math.floor(rng()*SETTLEMENTS.length);if(next===person.homeTown)next=(next+1)%SETTLEMENTS.length;
    person.visitTown=next;person.visitUntil=world.tick+8+Math.floor(rng()*12);
    kind='travel';text=person.name+' set out from '+town.name+' to explore '+settle(next).name+'.';
  }else if(event===4) {
    person.credits+=Math.round(8+rng()*20);
    kind='community';text=person.name+' volunteered at a community project in '+town.name+'.';
    person.mood=clamp(person.mood+5,0,100);
  }else if(event===5 && person.credits>65) {
    let next=Math.floor(rng()*SETTLEMENTS.length);if(next===person.homeTown)next=(next+1)%SETTLEMENTS.length;
    person.homeTown=next;person.workTown=next;const h=where(settle(next),rng);person.homeX=h.x;person.homeY=h.y;
    person.workX=where(settle(next),rng).x;person.workY=where(settle(next),rng).y;
    person.visitTown=null;person.visitUntil=0;person.credits-=35;
    kind='housing';text=person.name+' moved to a new home in '+settle(next).name+'.';
  }else {
    const friend=person.friends.length?others[person.friends[Math.floor(rng()*person.friends.length)]-1]:null;
    person.credits=clamp(person.credits-5,0,10000);
    kind='culture';text=person.name+' organised a '+person.interest+' gathering'+(friend?' with '+friend.name:'')+' in '+town.name+'.';
  }
  record(world,person,time,kind,text);
}
export function runTick(world,time) {
  world.tick+=1;
  const rng=rand((world.tick*2654435761+0xC0FFEE)>>>0);
  const {hour,weekend}=dayInfo(time);
  for(const p of world.citizens) {
    if(p.visitTown!==null&&world.tick>=p.visitUntil)p.visitTown=null;
    let destX=p.homeX,destY=p.homeY,activity='at home';
    if(hour<6||hour>=23)activity='sleeping';
    else if(hour<8)activity='having breakfast';
    else if(!weekend&&hour<9)activity='commuting';
    else if(!weekend&&hour<17){destX=p.workX;destY=p.workY;activity='working';}
    else if(hour<20&&rng()<.55){const t=settle(p.homeTown);destX=t.x+(rng()-.5)*6;destY=t.y+(rng()-.5)*6;activity=rng()<.45?'shopping':'socialising';}
    else if(hour<22&&rng()<.4){const t=settle(p.homeTown);destX=t.x;destY=t.y;activity='at a cafe';}
    if(p.visitTown!==null) {
      const t=settle(p.visitTown);destX=t.x;destY=t.y;
      activity='travelling';
    }
    p.x=Math.round((p.x+(destX-p.x)*.24)*100)/100;
    p.y=Math.round((p.y+(destY-p.y)*.24)*100)/100;
    p.activity=activity;
    if(activity==='working'){p.credits=clamp(p.credits+.8,0,10000);p.energy=clamp(p.energy-.6,0,100);}
    else if(activity==='sleeping')p.energy=clamp(p.energy+2,0,100);
    else if(activity==='shopping')p.credits=clamp(p.credits-1.4,0,10000);
    else if(activity==='socialising')p.mood=clamp(p.mood+.6,0,100);
    if(rng()<.0016)story(world,p,rng,time);
  }
  world.updatedAt=time;
}
export function advanceWorld(world,now=Date.now(),maxTicks=96) {
  const ticks=clamp(Math.floor((now-world.updatedAt)/TICK_MS),0,maxTicks);
  for(let i=0;i<ticks;i++)runTick(world,world.updatedAt+TICK_MS);
  return ticks;
}
async function loadWorld(db) {
  let row=await db.prepare('SELECT revision,state FROM worlds WHERE id=1').first();
  if(!row) {
    const now=Math.floor(Date.now()/TICK_MS)*TICK_MS;
    const state=seedWorld(now);
    await db.prepare('INSERT OR IGNORE INTO worlds (id,revision,state,updated_at) VALUES (1,0,?,?)')
      .bind(JSON.stringify(state),state.updatedAt).run();
    row=await db.prepare('SELECT revision,state FROM worlds WHERE id=1').first();
  }
  if(!row)throw new Error('Unable to load simulation');
  return {revision:row.revision,world:JSON.parse(row.state)};
}
export async function scheduledStep(db,now=Date.now()) {
  const {world,revision}=await loadWorld(db);
  const ticks=advanceWorld(world,now);
  if(!ticks)return {ticks:0,revision};
  const outcome=await db.prepare('UPDATE worlds SET revision=?,state=?,updated_at=? WHERE id=1 AND revision=?')
    .bind(revision+1,JSON.stringify(world),world.updatedAt,revision).run();
  if(outcome.meta?.changes!==1)throw new Error('Concurrent world update detected; retry on next schedule');
  return {ticks,revision:revision+1,updatedAt:world.updatedAt,events:world.events.length};
}
const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{
  'content-type':'application/json; charset=utf-8',
  'cache-control':'no-store, max-age=0','access-control-allow-origin':'*',
  'x-content-type-options':'nosniff'
}});
export default {
  async fetch(request,env) {
    if(request.method==='OPTIONS')return new Response(null,{status:204,headers:{
      'access-control-allow-origin':'*','access-control-allow-methods':'GET, HEAD, OPTIONS','access-control-allow-headers':'content-type'}});
    if(request.method!=='GET'&&request.method!=='HEAD')return json({error:'Read-only API'},405);
    const path=new URL(request.url).pathname;
    if(!['/','/api/world','/api/health'].includes(path))return json({error:'Not found'},404);
    try {
      const {world,revision}=await loadWorld(env.DB);
      const health={status:'ok',name:'Parristan Living Nation',fictional:true,
        latestTickAt:new Date(world.updatedAt).toISOString(),population:world.citizens.length,
        settlements:world.settlements.length,ticks:world.tick,revision,
        minutesSinceUpdate:Math.max(0,Math.floor((Date.now()-world.updatedAt)/60000)),
        scheduledIntervalMinutes:15};
      if(path==='/api/health')return json(health);
      if(path==='/')return json({name:health.name,api:'/api/world',health:'/api/health',
        website:'https://parristan.org/living-nation.html',fictional:true});
      return json({schema:world.schema,fictional:true,startedAt:world.startedAt,updatedAt:world.updatedAt,
        tick:world.tick,settlements:world.settlements,citizens:world.citizens,
        events:world.events.slice().reverse(),population:world.citizens.length});
    }catch(e){return json({error:'Simulation temporarily unavailable',message:String(e?.message||e)},503);}
  },
  async scheduled(event,env,ctx) {
    ctx.waitUntil(scheduledStep(env.DB,Date.now()));
  }
};
