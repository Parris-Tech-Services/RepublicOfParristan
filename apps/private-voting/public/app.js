const api="/api";let me=null,csrf="",polls=[],participated=new Set(),members=[],secretEnabled=false;
const el=id=>document.getElementById(id),safe=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const local=t=>t?new Date(t).toLocaleString("en-AU",{timeZone:"Australia/Sydney",dateStyle:"medium",timeStyle:"short"})+" Sydney":"Unscheduled";
const form=f=>Object.fromEntries(new FormData(f).entries());
function alertUser(s){el("message").textContent=s;scrollTo({top:0,behavior:"smooth"})}
async function get(action){const r=await fetch(api+"?action="+action,{credentials:"same-origin",cache:"no-store"});const j=await r.json();if(!r.ok)throw Error(j.error||"Request failed");return j}
async function post(action,data){const r=await fetch(api+"?action="+action,{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json","X-CSRF-Token":csrf},body:JSON.stringify(data)});const j=await r.json();if(!r.ok)throw Error(j.error||"Request failed");return j}
function authPage(setup){el("app").hidden=true;el("signout").hidden=true;const q=new URLSearchParams(location.search),token=q.get("invite"),id=q.get("member");
 if(token&&id){el("auth").innerHTML='<div class="panel"><h2>Activate your private founder account</h2><p>This single-use invitation expires after 48 hours.</p><form id="activate"><label>Create password (at least 12 characters)<input name="password" type="password" autocomplete="new-password" minlength="12" required></label><button>Activate account</button></form></div>';el("activate").onsubmit=async e=>{e.preventDefault();try{await post("activate",{memberId:id,token,password:form(e.target).password});history.replaceState(null,"","/");await load()}catch(x){alertUser(x.message)}};return}
 if(setup){el("auth").innerHTML='<div class="panel"><h2>Initial organiser setup</h2><p>Enter the private setup code and choose a password for founder account #1. No voting has opened.</p><form id="bootstrap"><label>Private setup code<input name="code" type="password" autocomplete="off" required></label><label>Create password<input name="password" type="password" autocomplete="new-password" minlength="12" required></label><button>Activate organiser account</button></form></div>';el("bootstrap").onsubmit=async e=>{e.preventDefault();try{await post("bootstrap",form(e.target));await load()}catch(x){alertUser(x.message)}};return}
 el("auth").innerHTML='<div class="panel"><h2>Private founder sign-in</h2><p>Only previously activated accounts may access private ballots.</p><form id="login"><label>Account<select name="memberId"><option value="1">Joshua Parris</option><option value="2">Glenn Peterson</option><option value="3">Matthew Walker</option><option value="4">Fred Carbunkle</option><option value="5">Jane Carbunkle</option></select></label><label>Password<input type="password" name="password" autocomplete="current-password" required></label><button>Sign in</button></form></div>';el("login").onsubmit=async e=>{e.preventDefault();try{await post("login",form(e.target));await load()}catch(x){alertUser(x.message)}}}
function pollCard(p){const done=participated.has(Number(p.id)),now=Date.now(),start=Date.parse(p.opens_at),end=Date.parse(p.closes_at);
 const canVote=p.status==="open"&&now>=start&&now<end&&!done&&!(p.kind==="election"&&!secretEnabled);
 const choices=p.kind==="election"?(p.options.length===1?["YES","NO"]:p.options):["YES","NO","ABSTAIN"];
 const title=p.kind==="election"?"Election — "+safe(p.office):p.kind==="amendment"?"Constitutional amendment":"Written motion";
 let out='<article class="ballot"><div class="meta">'+title+' <span class="badge">'+safe(p.status)+'</span></div><h3>'+safe(p.title)+'</h3><p>'+safe(p.body)+'</p><p class="meta">Notice: '+safe(p.notice_ref)+' · Opens: '+local(p.opens_at)+' · Closes: '+local(p.closes_at)+'</p><p class="meta">Participation: '+p.participation_count+' of 5 '+(done?"· Your ballot received":"")+'</p>';
 if(p.kind==="election"&&p.options.length===1)out+='<p>Sole candidate: '+safe(p.options[0])+'. Confirm YES or NO.</p>';
 if(canVote)out+='<form class="voteform" data-id="'+p.id+'"><fieldset class="voteopts"><legend>Your one final ballot</legend>'+choices.map(v=>'<label><input type="radio" name="choice" value="'+safe(v)+'" required>'+safe(v)+'</label>').join("")+'</fieldset><button>Submit final ballot</button></form>';
 else if(p.kind==="election"&&!secretEnabled)out+='<p><strong>Election voting locked:</strong> awaiting Returning Officer and independent security approval.</p>';
 if(p.status==="certified"&&p.result)out+='<pre aria-label="Certified aggregate result">'+safe(JSON.stringify(p.result,null,2))+'</pre>';
 const officer=p.kind==="election"?me?.role==="Returning Officer":me?.role==="Secretary";
 const early=p.kind==="election"?now>=end:now>=end||p.participation_count>=5;
 out+='<div class="actionrow">';
 if(officer&&p.status==="draft")out+='<button data-action="open" data-id="'+p.id+'">Open after notice check</button>';
 if(officer&&p.status==="open"&&early)out+='<button data-action="close" data-id="'+p.id+'">Close ballot</button>';
 if(officer&&p.status==="closed")out+='<button data-action="tally" data-id="'+p.id+'">Count ballots</button>';
 if(p.status==="tallied"&&p.tallied_by!==me.id&&(p.kind!=="election"||!me.admin&&me.role!=="Returning Officer"))out+='<button data-action="check" data-id="'+p.id+'">Verify count</button>';
 if(officer&&p.status==="checked")out+='<button data-action="certify" data-id="'+p.id+'">Certify result</button>';
 return out+'</div></article>'
}
function render(){
 el("auth").innerHTML="";el("app").hidden=false;el("signout").hidden=false;el("welcome").textContent="Signed in: "+me.full_name+" · "+me.role;
 el("polls").innerHTML=polls.length?polls.map(pollCard).join(""):"<p>No new motions have been created. Existing founding resolutions are held separately in the public Gazette; no historical votes have been recreated here.</p>";
 const kind=el("newPoll").elements.kind;kind.querySelector('option[value="election"]').disabled=me.role!=="Returning Officer";const sync=()=>el("electionFields").hidden=kind.value!=="election";kind.onchange=sync;sync();
 el("membersPanel").hidden=!me.admin;
 if(me.admin)el("members").innerHTML=members.map(m=>'<p><strong>'+safe(m.full_name)+'</strong> · '+(m.active?"Activated":"Awaiting invitation")+(m.id!==1&&!m.active?' <button class="invite" data-id="'+m.id+'">Create private invitation</button>':"")+'</p>').join("");
 el("polls").querySelectorAll(".voteform").forEach(f=>f.onsubmit=async e=>{e.preventDefault();if(!confirm("Submit this final ballot? You cannot change it."))return;try{await post("vote",{pollId:Number(f.dataset.id),choice:form(f).choice});alertUser("Your ballot was received, without linking your choice to your account in the ballot table.");await refresh()}catch(x){alertUser(x.message)}});
 el("polls").querySelectorAll("[data-action]").forEach(b=>b.onclick=async()=>{if(!confirm("Confirm "+b.dataset.action+" for poll "+b.dataset.id+"?"))return;try{await post(b.dataset.action,{pollId:Number(b.dataset.id)});alertUser("Officer action recorded. Publication in the official Matrix channel and Gazette remains separate.");await refresh()}catch(x){alertUser(x.message)}});
 el("members").querySelectorAll(".invite").forEach(b=>b.onclick=async()=>{try{const x=await post("invite",{memberId:Number(b.dataset.id)});const link=location.origin+"/?member="+x.memberId+"&invite="+encodeURIComponent(x.token);prompt("Share this one-use link privately with "+x.name+". Do not put it in the public Gazette.",link);await refresh()}catch(x){alertUser(x.message)}});
}
async function refresh(){const r=await get("polls");polls=r.polls;participated=new Set(r.participated);render()}
async function load(){try{const r=await get("me");me=r.me;members=r.members;csrf=r.csrf;secretEnabled=r.secretElectionEnabled;await refresh()}catch{me=null;const r=await get("status");authPage(r.setupRequired)}}
el("newPoll").onsubmit=async e=>{e.preventDefault();const d=form(e.target);d.options=String(d.options||"").split("\n").map(x=>x.trim()).filter(Boolean);
for(const k of ["noticeAt","opensAt","closesAt"])if(d[k])d[k]=new Date(d[k]).toISOString();
try{await post("create",d);e.target.reset();alertUser("Draft saved; no vote has opened.");await refresh()}catch(x){alertUser(x.message)}};
el("signout").onclick=async()=>{try{await post("logout",{})}finally{location.assign("/")}};
load().catch(x=>alertUser("Service not available: "+x.message));
