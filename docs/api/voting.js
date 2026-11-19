import pg from "pg";
import { randomBytes, createHash, scryptSync, timingSafeEqual } from "node:crypto";
import { evaluate, enoughNotice, mayClose, mayVote } from "../lib/rules.js";

// Production data never belongs in the public Gazette repo.
const pool = globalThis.parristanVotingPool ||= new pg.Pool({
  connectionString:process.env.DATABASE_URL,ssl:{rejectUnauthorized:true},max:3,
  connectionTimeoutMillis:8000,idleTimeoutMillis:30000
});
const random=()=>randomBytes(32).toString("base64url");
const sha=x=>createHash("sha256").update(x).digest("hex");
const hashPassword=(p,s)=>scryptSync(p,s,64).toString("hex");
const secureEq=(a,b)=>{if(typeof a!=="string"||typeof b!=="string")return false;let x=Buffer.from(a),y=Buffer.from(b);return x.length===y.length&&timingSafeEqual(x,y)};
const canonical=v=>Array.isArray(v)?v.map(canonical):v&&typeof v==="object"?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):v;
const err=(code,message)=>Object.assign(new Error(message),{code});
const cookieName="__Host-parristan_session";
const headers={"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store","X-Content-Type-Options":"nosniff","X-Frame-Options":"DENY","Referrer-Policy":"no-referrer","Strict-Transport-Security":"max-age=31536000"};
const send=(res,status,obj,more={})=>{res.writeHead(status,{...headers,...more});res.end(JSON.stringify(obj))};
const tokenCookie=t=>cookieName+"="+t+"; Path=/; Max-Age=604800; Secure; HttpOnly; SameSite=Strict";
async function readJSON(req){if(!String(req.headers["content-type"]||"").startsWith("application/json"))throw err(415,"JSON required");let raw="";for await(const part of req){raw+=part.toString();if(raw.length>18000)throw err(413,"Request too large")}try{return JSON.parse(raw||"{}")}catch{throw err(400,"Invalid JSON")}}
const requirePassword=p=>{if(typeof p!=="string"||p.length<12||p.length>128)throw err(400,"Choose a password of 12 to 128 characters")};
const audit=(q,who,action,subject)=>q.query("INSERT INTO audit_log(actor_id,action,subject) VALUES ($1,$2,$3)",[who||null,action,subject]);
async function newSession(id){const raw=random(),csrf=random();await pool.query("INSERT INTO sessions(id_hash,member_id,csrf_token,expires_at) VALUES($1,$2,$3,now()+interval '7 days')",[sha(raw),id,csrf]);return{raw,csrf}}
async function current(req){const raw=(req.headers.cookie||"").split(";").map(s=>s.trim()).find(s=>s.startsWith(cookieName+"="))?.slice(cookieName.length+1);if(!raw||raw.length>128)return null;const q=await pool.query("SELECT m.id,m.full_name,m.role,m.admin,s.csrf_token FROM sessions s JOIN members m ON m.id=s.member_id WHERE s.id_hash=$1 AND s.expires_at>now() AND m.active=true",[sha(raw)]);return q.rows[0]||null}
function authCheck(req,u){if(!u)throw err(401,"Sign in required");if(!secureEq(String(req.headers["x-csrf-token"]||""),u.csrf_token))throw err(403,"Invalid session request token")}
function originCheck(req){if(!req.headers.host||!secureEq(String(req.headers.origin||""),"https://"+req.headers.host))throw err(403,"Untrusted origin")}
const isRO=u=>u?.role==="Returning Officer",isSecretary=u=>u?.role==="Secretary",manager=(p,u)=>p.kind==="election"?isRO(u):isSecretary(u);
async function actionPOST(req,res,action,d,u){
 if(action==="bootstrap"){
   if(!process.env.BOOTSTRAP_KEY||!secureEq(String(d.code||""),process.env.BOOTSTRAP_KEY))throw err(403,"Invalid setup code");
   requirePassword(d.password);const salt=random();
   const a=await pool.query("UPDATE members SET password_salt=$1,password_hash=$2,active=true WHERE id=1 AND active=false RETURNING id",[salt,hashPassword(d.password,salt)]);
   if(!a.rowCount)throw err(409,"Already configured");
   await audit(pool,1,"bootstrap","founder 1 activated");let s=await newSession(1);
   return send(res,200,{ok:true,csrf:s.csrf},{"Set-Cookie":tokenCookie(s.raw)});
 }
 if(action==="login"){
   const id=Number(d.memberId);
   if(!Number.isInteger(id)||id<1||id>5||typeof d.password!=="string")throw err(401,"Incorrect account or password");
   const key="founder-"+id;
   const gate=await pool.query("SELECT attempts,locked_until FROM login_throttle WHERE identity=$1",[key]);
   if(gate.rows[0]?.locked_until&&new Date(gate.rows[0].locked_until).getTime()>Date.now())throw err(429,"Too many attempts. Try again later");
   const m=(await pool.query("SELECT id,password_hash,password_salt,active FROM members WHERE id=$1",[id])).rows[0];
   const match=m?.password_salt?secureEq(hashPassword(d.password,m.password_salt),m.password_hash):false;
   if(!m?.active||!match){
     await pool.query("INSERT INTO login_throttle(identity,attempts,updated_at,locked_until) VALUES($1,1,now(),NULL) ON CONFLICT(identity) DO UPDATE SET attempts=CASE WHEN login_throttle.updated_at<now()-interval '15 minutes' THEN 1 ELSE login_throttle.attempts+1 END,updated_at=now(),locked_until=CASE WHEN login_throttle.attempts>=4 AND login_throttle.updated_at>now()-interval '15 minutes' THEN now()+interval '15 minutes' ELSE NULL END",[key]);
     throw err(401,"Incorrect account or password");
   }
   await pool.query("DELETE FROM login_throttle WHERE identity=$1",[key]);let s=await newSession(id);
   return send(res,200,{ok:true,csrf:s.csrf},{"Set-Cookie":tokenCookie(s.raw)});
 }
 if(action==="activate"){
   const id=Number(d.memberId);requirePassword(d.password);
   if(!Number.isInteger(id)||id<2||id>5||typeof d.token!=="string"||d.token.length>180)throw err(400,"Invalid invitation");
   const salt=random(),r=await pool.query("UPDATE members SET password_salt=$1,password_hash=$2,active=true,invite_hash=NULL,invite_expires=NULL WHERE id=$3 AND invite_hash=$4 AND invite_expires>now() AND active=false RETURNING id",[salt,hashPassword(d.password,salt),id,sha(d.token)]);
   if(!r.rowCount)throw err(403,"Invitation expired or already used");
   await audit(pool,id,"activate","founder activated");let s=await newSession(id);
   return send(res,200,{ok:true,csrf:s.csrf},{"Set-Cookie":tokenCookie(s.raw)});
 }
 authCheck(req,u);
 if(action==="logout"){
   const raw=(req.headers.cookie||"").split(";").map(s=>s.trim()).find(s=>s.startsWith(cookieName+"="))?.slice(cookieName.length+1);
   if(raw)await pool.query("DELETE FROM sessions WHERE id_hash=$1",[sha(raw)]);
   return send(res,200,{ok:true},{"Set-Cookie":cookieName+"=; Path=/; Max-Age=0; Secure; HttpOnly; SameSite=Strict"});
 }
 if(action==="invite"){
   if(!u.admin)throw err(403,"Only joint technical admins can invite founders");
   let id=Number(d.memberId);if(!Number.isInteger(id)||id<2||id>5)throw err(400,"Choose an unactivated founder");
   let token=random(),q=await pool.query("UPDATE members SET invite_hash=$1,invite_expires=now()+interval '48 hours' WHERE id=$2 AND active=false RETURNING full_name",[sha(token),id]);
   if(!q.rowCount)throw err(409,"Account already activated");
   await audit(pool,u.id,"invite","founder "+id);
   return send(res,200,{ok:true,memberId:id,name:q.rows[0].full_name,token,expiresHours:48});
 }
 if(action==="create"){
   const kind=String(d.kind||""),title=String(d.title||"").trim(),body=String(d.body||"").trim(),office=String(d.office||"").trim(),noticeRef=String(d.noticeRef||"").trim();
   if(!["motion","amendment","election"].includes(kind)||title.length<3||title.length>180||body.length>10000)throw err(400,"Invalid motion or ballot");
   if(kind==="amendment"&&body.length<20)throw err(400,"Full amendment text required");
   if(kind==="election"&&!isRO(u))throw err(403,"Only Matthew, the Returning Officer, may prepare an election");
   if(!noticeRef||noticeRef.length>120)throw err(400,"An official-channel notice reference is required");
   const notice=new Date(d.noticeAt||"");
   if(!Number.isFinite(notice.getTime())||notice.getTime()>Date.now())throw err(400,"Use the actual past published-notice time");
   let opts=kind==="election"&&Array.isArray(d.options)?d.options.map(x=>String(x).trim()):["YES","NO","ABSTAIN"];
   if(kind==="election"&&(!office||office.length>100||opts.length<1||opts.length>10||opts.some(x=>x.length<2||x.length>90)||new Set(opts).size!==opts.length))throw err(400,"Office and 1–10 certified candidates required");
   let opens=null,closes=null;
   if(kind==="election"){
     opens=new Date(d.opensAt||"");closes=new Date(d.closesAt||"");
     if(!Number.isFinite(opens.getTime())||!Number.isFinite(closes.getTime())||closes<=opens)throw err(400,"Returning Officer must choose real opening and closing times");
     const day=x=>new Intl.DateTimeFormat("en-CA",{timeZone:"Australia/Sydney",year:"numeric",month:"2-digit",day:"2-digit"}).format(x);
     if(office.trim().toLowerCase()==="president" && day(opens)<"2028-11-19") throw err(409,"The first Presidency is recorded as filled until 19 November 2028 (Gazette 2026-013). A fresh vacancy decision needs separately adopted election rules before another presidential poll.");
   }
   let q=await pool.query("INSERT INTO polls(kind,title,body,office,options,notice_ref,notice_at,opens_at,closes_at,created_by) VALUES ($1,$2,$3,$4,$5::jsonb,$6,$7,$8,$9,$10) RETURNING id",[kind,title,body,office||null,JSON.stringify(opts),noticeRef,notice,opens,closes,u.id]);
   await audit(pool,u.id,"create draft","poll "+q.rows[0].id);
   return send(res,201,{ok:true,id:q.rows[0].id});
 }
 if(action==="open"){
   const id=Number(d.pollId);if(!Number.isSafeInteger(id)||id<1)throw err(400,"Invalid poll");
   const poll=(await pool.query("SELECT * FROM polls WHERE id=$1",[id])).rows[0];
   if(!poll||poll.status!=="draft")throw err(409,"Ballot unavailable or already opened");
   if(!manager(poll,u))throw err(403,"Responsible officer only");
   if(!poll.notice_ref||!poll.notice_at||!enoughNotice(poll.kind,new Date(poll.notice_at).toISOString(),Date.now()))throw err(400,"Notice missing or fourteen-day amendment period not met");
   if(poll.kind==="election"&&process.env.SECRET_ELECTIONS_ENABLED!=="true")throw err(423,"Secret elections locked until Returning Officer approval and independent security review");
   let starts=poll.kind==="election"?poll.opens_at:new Date(),ends=poll.kind==="election"?poll.closes_at:new Date(Date.now()+48*3600000);
   if(poll.kind==="election"&&(!starts||!ends))throw err(400,"Election clock times required");
   const result=await pool.query("UPDATE polls SET status='open',opens_at=$2,closes_at=$3 WHERE id=$1 AND status='draft' RETURNING id",[id,starts,ends]);
   if(!result.rowCount)throw err(409,"This draft was opened already");
   await audit(pool,u.id,"open","poll "+id);return send(res,200,{ok:true});
 }
 if(action==="vote"){
   const id=Number(d.pollId),choice=String(d.choice||"");if(!Number.isSafeInteger(id)||id<1)throw err(400,"Invalid poll");
   const c=await pool.connect();try{
     await c.query("BEGIN");
     const p=(await c.query("SELECT * FROM polls WHERE id=$1 FOR UPDATE",[id])).rows[0];
     if(!p||!mayVote(p,Date.now()))throw err(409,"Poll is not currently open");
     if(p.kind==="election"&&process.env.SECRET_ELECTIONS_ENABLED!=="true")throw err(423,"Election remains locked");
     const choices=p.kind==="election"?(p.options.length===1?["YES","NO"]:p.options):["YES","NO","ABSTAIN"];
     if(!choices.includes(choice))throw err(400,"Invalid choice");
     const one=await c.query("INSERT INTO participation(poll_id,member_id) VALUES($1,$2) ON CONFLICT DO NOTHING RETURNING member_id",[id,u.id]);
     if(!one.rowCount)throw err(409,"You have already voted");
     // Ballot choices deliberately omit voter identifiers and timestamps.
     await c.query("INSERT INTO ballots(poll_id,choice) VALUES($1,$2)",[id,choice]);await c.query("COMMIT");
     return send(res,200,{ok:true,message:"Your ballot is received and cannot be changed."});
   }catch(e){await c.query("ROLLBACK").catch(()=>{});throw e}finally{c.release()}
 }
 if(["close","tally","check","certify"].includes(action)){
   const id=Number(d.pollId);if(!Number.isSafeInteger(id)||id<1)throw err(400,"Invalid poll");
   const c=await pool.connect();try{
     await c.query("BEGIN");
     const p=(await c.query("SELECT * FROM polls WHERE id=$1 FOR UPDATE",[id])).rows[0];if(!p)throw err(404,"Unknown poll");
     const voted=Number((await c.query("SELECT count(*)::int n FROM participation WHERE poll_id=$1",[id])).rows[0].n);
     const eligible=Number((await c.query("SELECT count(*)::int n FROM members",[ ])).rows[0].n);
     if(action==="close"){
       if(!manager(p,u)||p.status!=="open")throw err(403,"Responsible officer must close an open ballot");
       if(!mayClose(p.kind,eligible,voted,p.closes_at,Date.now()))throw err(409,"Wait 48 hours or all five member ballots; elections cannot close early");
       await c.query("UPDATE polls SET status='closed' WHERE id=$1",[id]);
     }
     if(action==="tally"){
       if(!manager(p,u)||p.status!=="closed")throw err(403,"Responsible officer must tally a closed ballot");
       const q=await c.query("SELECT choice,count(*)::int n FROM ballots WHERE poll_id=$1 GROUP BY choice",[id]);
       const outcome=evaluate(p.kind,p.options,Object.fromEntries(q.rows.map(x=>[x.choice,x.n])),voted);
       await c.query("UPDATE polls SET status='tallied',result=$2::jsonb,tallied_by=$3 WHERE id=$1",[id,JSON.stringify(outcome),u.id]);
     }
     if(action==="check"){
       if(p.status!=="tallied"||p.tallied_by===u.id)throw err(403,"Different checker required after tally");
       if(p.kind==="election"&&(u.admin||isRO(u)||p.options.includes(u.full_name)))throw err(403,"Election checker cannot be a candidate, technical admin or Returning Officer");
       const q=await c.query("SELECT choice,count(*)::int n FROM ballots WHERE poll_id=$1 GROUP BY choice",[id]);
       const verified=evaluate(p.kind,p.options,Object.fromEntries(q.rows.map(x=>[x.choice,x.n])),voted);
       if(JSON.stringify(canonical(verified))!==JSON.stringify(canonical(p.result)))throw err(409,"Independent count differs");
       await c.query("UPDATE polls SET status='checked',checked_by=$2 WHERE id=$1",[id,u.id]);
     }
     if(action==="certify"){
       if(!manager(p,u)||p.status!=="checked"||!p.checked_by||p.checked_by===u.id)throw err(403,"Independent verification and responsible officer required");
       await c.query("UPDATE polls SET status='certified',certified_by=$2,certified_at=now() WHERE id=$1",[id,u.id]);
     }
     await audit(c,u.id,action,"poll "+id);await c.query("COMMIT");return send(res,200,{ok:true});
   }catch(e){await c.query("ROLLBACK").catch(()=>{});throw e}finally{c.release()}
 }
 throw err(404,"Unknown action");
}
export default async function handler(req,res){
 try{
   const url=new URL(req.url,"https://"+(req.headers.host||"localhost"));
   const action=url.searchParams.get("action")||"status";
   if(!["GET","POST"].includes(req.method))return send(res,405,{error:"Method not allowed"},{Allow:"GET, POST"});
   if(!process.env.DATABASE_URL)return send(res,503,{error:"Voting database not connected"});
   const u=await current(req);
   if(req.method==="GET"){
     if(action==="status"){const q=await pool.query("SELECT active FROM members WHERE id=1");return send(res,200,{ok:true,setupRequired:!q.rows[0]?.active,secretElectionEnabled:process.env.SECRET_ELECTIONS_ENABLED==="true"})}
     if(!u)throw err(401,"Sign in required");
     if(action==="me"){const m=await pool.query("SELECT id,full_name,role,admin,active FROM members ORDER BY id");return send(res,200,{ok:true,me:u,members:m.rows,csrf:u.csrf_token,secretElectionEnabled:process.env.SECRET_ELECTIONS_ENABLED==="true"})}
     if(action==="polls"){
       const p=await pool.query("SELECT p.*, (SELECT count(*)::int FROM participation WHERE poll_id=p.id) participation_count FROM polls p ORDER BY id DESC LIMIT 100");
       const mine=(await pool.query("SELECT poll_id FROM participation WHERE member_id=$1",[u.id])).rows.map(x=>Number(x.poll_id));
       return send(res,200,{ok:true,polls:p.rows.map(x=>({...x,result:x.status==="certified"?x.result:null,checked_by:x.status==="certified"?x.checked_by:null,certified_by:x.status==="certified"?x.certified_by:null})),participated:mine});
     }
     if(action==="audit"&&u.admin){const a=await pool.query("SELECT actor_id,action,subject,created_at FROM audit_log ORDER BY id DESC LIMIT 100");return send(res,200,{ok:true,events:a.rows})}
     throw err(404,"Unknown action");
   }
   originCheck(req);const data=await readJSON(req);
   return await actionPOST(req,res,action,data,u);
 }catch(e){console.error("Private voting API",String(e.message||e).slice(0,100));return send(res,e.code||500,{error:e.code?e.message:"Service unavailable"})}
}
