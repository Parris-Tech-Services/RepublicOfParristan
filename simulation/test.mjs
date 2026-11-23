import test from 'node:test';
import assert from 'node:assert/strict';
import {seedWorld,advanceWorld,runTick,SETTLEMENTS,TICK_MS,JOBS} from './worker.js';

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
