import test from 'node:test';
import assert from 'node:assert/strict';
import {seedWorld,advanceWorld,runTick,SETTLEMENTS,TICK_MS,JOBS} from './worker.js';
import {CIVIC_SCHEMA,ensureCivicState,publicCivicSnapshot,FIRST_CHARTERED_TOWN} from './civic.js';

test('generates 500 distinct fictional agents, never real membership',()=>{
  const world=seedWorld(Date.UTC(2026,10,23));
  assert.equal(world.citizens.length,500);
  assert.equal(world.settlements.length,12);
  assert.equal(new Set(world.citizens.map(c=>c.name)).size,500);
  assert.equal(world.simulation,'fictional');
  assert.ok(world.citizens.every(c=>JOBS.includes(c.occupation)));
  assert.ok(world.citizens.every(c=>c.homeTown>=0&&c.homeTown<12));
  assert.ok(world.citizens.every(c=>c.x>=0&&c.x<=100&&c.y>=0&&c.y<=100));
});

test('world ticks are deterministic and persist autonomous movement',()=>{
  const a=seedWorld(Date.UTC(2026,10,23));
  const b=seedWorld(Date.UTC(2026,10,23));
  const target=a.updatedAt+4*TICK_MS;
  assert.equal(advanceWorld(a,target),4);
  assert.equal(advanceWorld(b,target),4);
  assert.deepEqual(a,b);
  assert.equal(a.tick,4);
  assert.equal(a.updatedAt,target);
  assert.ok(a.citizens.some((c,i)=>c.x!==seedWorld(Date.UTC(2026,10,23)).citizens[i].x || c.y!==seedWorld(Date.UTC(2026,10,23)).citizens[i].y));
});

test('does not move forward twice for the same time',()=>{
  const a=seedWorld(1000000000);
  assert.equal(advanceWorld(a,a.updatedAt),0);
  assert.equal(advanceWorld(a,a.updatedAt+TICK_MS),1);
  assert.equal(advanceWorld(a,a.updatedAt),0);
});

test('limits cold-start catch-up to 96 ticks per invocation',()=>{
  const a=seedWorld(1000000000);
  const manyDays=a.updatedAt+TICK_MS*500;
  assert.equal(advanceWorld(a,manyDays),96);
  assert.equal(a.tick,96);
});

test('daily life changes status, energy, wealth and creates event history',()=>{
  const a=seedWorld(Date.UTC(2026,10,23));
  for(let i=0;i<24*4;i++) runTick(a,a.updatedAt+TICK_MS);
  assert.equal(a.tick,96);
  assert.ok(a.events.length>1);
  assert.ok(a.events.every(e=>e.actor===0||a.citizens.some(c=>c.id===e.actor)));
  assert.ok(a.citizens.some(c=>c.activity!=='at home'));
  assert.ok(a.citizens.every(c=>c.credits>=0&&c.energy>=0&&c.energy<=100&&c.mood>=0&&c.mood<=100));
  assert.ok(a.citizens.every(c=>c.memories.length<=5&&c.friends.length<=12));
});

test('supports small test worlds without out-of-range relationship references',()=>{
  const a=seedWorld(Date.UTC(2026,10,23),20);
  assert.equal(a.citizens.length,20);
  for(let i=0;i<128;i++)runTick(a,a.updatedAt+TICK_MS);
  assert.ok(a.citizens.every(c=>c.friends.every(id=>id>=1&&id<=20)));
});

test('settlements have unique identities and mappable coordinates',()=>{
  assert.equal(new Set(SETTLEMENTS.map(x=>x.id)).size,12);
  assert.equal(new Set(SETTLEMENTS.map(x=>x.name)).size,12);
  assert.ok(SETTLEMENTS.every(x=>x.x>=0&&x.x<=100&&x.y>=0&&x.y<=100));
});


test('first local association charter is only fictional Tealford, not an Australian authority',()=>{
  const world=seedWorld(Date.UTC(2026,10,23));
  const snapshot=publicCivicSnapshot(world);
  assert.equal(world.civic.schema,CIVIC_SCHEMA);
  assert.equal(snapshot.associations.length,12);
  assert.deepEqual(snapshot.associations.filter(a=>a.charter==='chartered').map(a=>a.town),[FIRST_CHARTERED_TOWN]);
  assert.equal(snapshot.votesFromAIResidents,false);
  assert.equal(snapshot.legalAuthority,false);
  assert.equal(snapshot.realPolicePowers,false);
  assert.equal(snapshot.realWorldFees,false);
  assert.equal(snapshot.constitutionArticleXIII,'proposed-not-ratified');
  assert.equal(snapshot.ledger.length,0);
  assert.ok(snapshot.associations.every(a=>a.fictional&&a.budgetParri===0));
});
test('Tealford charges only simulated wage-linked service rates and funds actual virtual programmes',()=>{
  const world=seedWorld(Date.UTC(2026,10,23));
  const initialCitizenIds=world.citizens.map(p=>p.id);
  for(let i=0;i<48;i++)runTick(world,world.updatedAt+TICK_MS);
  const civic=publicCivicSnapshot(world);
  const tealford=civic.associations.find(a=>a.town===2);
  assert.equal(world.tick,48);
  assert.ok(tealford.receivedParri>0,'positive simulation-only levy receipts from workers');
  assert.ok(tealford.fundedProgrammes>0,'actual booked fictional service costs');
  assert.ok(tealford.spentParri>0);
  assert.ok(tealford.budgetParri>=0);
  assert.equal(Math.round((tealford.receivedParri-tealford.spentParri)*100),Math.round(tealford.budgetParri*100));
  assert.ok(civic.ledger.every(e=>e.town===2));
  assert.ok(civic.ledger.some(e=>e.kind==='simulated-revenue'));
  assert.ok(civic.ledger.some(e=>e.kind==='simulated-expenditure'));
  assert.ok(world.events.some(e=>e.actor===0&&e.town===2&&e.text.includes('fictional')));
  assert.deepEqual(world.citizens.map(p=>p.id),initialCitizenIds,'migration preserves citizen IDs');
  assert.ok(civic.associations.filter(a=>a.town!==2).every(a=>a.receivedParri===0&&a.spentParri===0));
});
test('old persisted D1 world migrates in place on next tick without reset',()=>{
  const world=seedWorld(Date.UTC(2026,10,23));
  delete world.civic;
  world.tick=23;world.updatedAt=Date.UTC(2026,10,23);
  const before=world.citizens.map(p=>({id:p.id,name:p.name,memories:p.memories}));
  runTick(world,world.updatedAt+TICK_MS);
  assert.equal(world.civic.startedTick,24);
  assert.equal(world.civic.schema,1);
  assert.equal(world.tick,24);
  assert.deepEqual(world.citizens.map(p=>p.id),before.map(p=>p.id));
  assert.equal(world.citizens.length,500);
  assert.equal(ensureCivicState(world),world.civic,'idempotent migration');
});
test('fictional Civic Service recruits on-duty residents and pays for actual assistance',()=>{
  const world=seedWorld(Date.UTC(2026,10,23));
  for(let i=0;i<96;i++)runTick(world,world.updatedAt+TICK_MS);
  const c=publicCivicSnapshot(world),tealford=c.associations.find(a=>a.town===2);
  assert.ok(tealford.assistedCases>0,'non-coercive help should have happened during a workday');
  const payouts=c.ledger.filter(e=>e.kind==='simulated-assistance');
  assert.ok(payouts.length>0,'virtual assistance transactions in civic ledger');
  for(const p of payouts){
    assert.equal(p.town,2);
    assert.equal(p.amountCents,-75);
    const worker=world.citizens.find(w=>w.id===p.recipientCitizenId);
    assert.ok(worker&&['Ranger','Postal worker','Librarian','Gardener'].includes(worker.occupation));
    assert.ok(worker.memories.some(m=>m.includes('fictional')));
  }
  assert.ok(world.events.some(e=>e.text.includes('Tealford Civic Service')&&e.type==='community'));
  assert.ok(world.citizens.every(c=>c.credits>=0),'no negative citizen money');
  assert.equal(Math.round((tealford.receivedParri-tealford.spentParri)*100),Math.round(tealford.budgetParri*100));
});
test('public snapshot never exposes real member records or voter eligibility',()=>{
  const world=seedWorld(Date.UTC(2026,10,23));
  const out=JSON.stringify(publicCivicSnapshot(world));
  assert.ok(!out.includes('email'));
  assert.ok(!out.includes('ballot'));
  assert.ok(!out.includes('password'));
  assert.ok(!out.includes('eligibleVoters'));
});
