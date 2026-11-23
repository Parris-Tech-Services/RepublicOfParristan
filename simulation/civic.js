/**
 * Fictional Local Civic Associations, PA-2026-001.
 * Persistent, simulation-only budgets. No real member or payment data.
 * v1 charters Tealford (#2); remaining settlements are proposals only.
 */
export const CIVIC_SCHEMA = 1;
export const FIRST_CHARTERED_TOWN = 2;
export const SIMULATED_SERVICE_RATE_CENTS = 8; // 0.08 Parri of fictional wages
const services=['community hall programme','street and verge upkeep','library activities','postal counter supplies','community gardens'];
const money=cents=>Math.round(cents)/100;
export function ensureCivicState(world) {
  // Non-destructive migration: existing D1 world, citizen IDs and events survive.
  if(world.civic?.schema===CIVIC_SCHEMA&&Array.isArray(world.civic.associations))return world.civic;
  const previous=world.civic;
  if(previous && previous.schema!==undefined) throw Error('Unsupported civic state schema: '+previous.schema);
  world.civic={
    schema:CIVIC_SCHEMA,fictional:true,startedTick:world.tick,
    associationPolicy:'PA-2026-001',
    associations:world.settlements.map(t=>({
      id:'civic:'+t.id,town:t.id,name:t.name+' Civic Association (Simulation)',
      charter:t.id===FIRST_CHARTERED_TOWN?'chartered':'proposed',
      budgetCents:0,receivedCents:0,spentCents:0,
      contributions:0,serviceEvents:0,services:services.slice(),
      lastFundedService:null
    })),
    ledger:[] // last 160 simulated transactions; aggregate per tick, never identity-bearing
  };
  return world.civic;
}
const boundedLedger=(state,entry)=>{
  state.ledger.push(entry);
  if(state.ledger.length>160)state.ledger.splice(0,state.ledger.length-160);
};
export function applyCivicTick(world,time,workersByTown) {
  const state=ensureCivicState(world);
  const t=state.associations.find(a=>a.town===FIRST_CHARTERED_TOWN);
  if(!t||t.charter!=='chartered')return;
  const paying=workersByTown.get(FIRST_CHARTERED_TOWN)||[];
  const revenue=paying.length*SIMULATED_SERVICE_RATE_CENTS;
  if(revenue){
    t.budgetCents+=revenue;t.receivedCents+=revenue;t.contributions+=paying.length;
    boundedLedger(state,{tick:world.tick,at:time,town:t.town,kind:'simulated-revenue',
      amountCents:revenue,description:'In-game wage-linked civic service contributions ('+paying.length+' residents)'});
  }
  // A funded programme has a real virtual cost; it is never announced before
  // the funds exist. No assertion that a 3D interior or real provider exists.
  const serviceCost=180; // 1.80 virtual Parri
  if(world.tick%8===0 && t.budgetCents>=serviceCost) {
    const service=services[t.serviceEvents%services.length];
    t.budgetCents-=serviceCost;t.spentCents+=serviceCost;
    t.serviceEvents++;t.lastFundedService=service;
    boundedLedger(state,{tick:world.tick,at:time,town:t.town,kind:'simulated-expenditure',
      amountCents:-serviceCost,description:'Funded fictional '+service+' programme'});
    world.events.push({
      id:world.tick*1000+900,at:time,type:'community',town:t.town,actor:0,
      text:'Tealford Civic Association funded a fictional '+service+' programme using 1.80 virtual Parri.'
    });
    if(world.events.length>800)world.events.splice(0,world.events.length-800);
  }
}
export function publicCivicSnapshot(world) {
  const state=world.civic?.schema===CIVIC_SCHEMA?world.civic:null;
  const associations=(state?.associations||world.settlements.map(t=>({
    id:'civic:'+t.id,town:t.id,name:t.name+' Civic Association (Simulation)',
    charter:t.id===FIRST_CHARTERED_TOWN?'chartered':'proposed',
    budgetCents:0,receivedCents:0,spentCents:0,contributions:0,
    serviceEvents:0,services:services.slice(),lastFundedService:null
  }))).map(a=>{
    const residents=world.citizens.filter(c=>c.homeTown===a.town);
    const relevant=world.citizens.filter(c=>c.workTown===a.town&&
      ['Librarian','Postal worker','Ranger','Gardener'].includes(c.occupation));
    return {id:a.id,town:a.town,settlement:world.settlements.find(s=>s.id===a.town)?.name||'Unknown',
      name:a.name,charter:a.charter,fictional:true,
      residents:residents.length,
      serviceRoles:relevant.map(p=>({citizenId:p.id,name:p.name,occupation:p.occupation,
        currentlyWorking:p.activity==='working'})),
      services:a.services.map(name=>({name,status:a.serviceEvents&&name===a.lastFundedService?'last-funded-in-ledger':'planned'})),
      budgetParri:money(a.budgetCents),receivedParri:money(a.receivedCents),
      spentParri:money(a.spentCents),contributions:a.contributions,
      fundedProgrammes:a.serviceEvents,lastFundedService:a.lastFundedService};
  });
  return {schema:CIVIC_SCHEMA,fictional:true,legalAuthority:false,
    votesFromAIResidents:false,realWorldFees:false,realPolicePowers:false,
    charter:'PA-2026-001',constitutionArticleXIII:'proposed-not-ratified',
    tick:world.tick,updatedAt:world.updatedAt,
    associations,ledger:(state?.ledger||[]).slice(-40).reverse()};
}
