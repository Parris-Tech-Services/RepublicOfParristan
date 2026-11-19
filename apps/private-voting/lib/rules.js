// Rules derived from Constitution v0.1 and Gazette 2026-007/009.
export const MIN_QUORUM = 3;
export function evaluate(kind,options,counts,participantCount) {
 const total=Number(participantCount),n=Object.values(counts).reduce((a,b)=>a+Number(b),0);
 if(!Number.isInteger(total)||n!==total||total<0)throw Error("Count mismatch");
 const quorum=total>=3,yes=Number(counts.YES||0),no=Number(counts.NO||0),valid=yes+no;
 if(kind==="motion")return {quorum,total,yes,no,abstain:Number(counts.ABSTAIN||0),passed:quorum&&yes>no,basis:"Motion 4: majority YES over NO; at least three voters"};
 if(kind==="amendment")return {quorum,total,yes,no,abstain:Number(counts.ABSTAIN||0),passed:quorum&&valid>0&&3*yes>=2*valid,basis:"Constitution Article XI: 14 days notice; two-thirds valid votes"};
 if(kind==="election"){
  if(options.length===1)return {quorum,total,yes,no,confirmed:quorum&&valid>0&&yes*2>valid,needsRunoff:false,basis:"Single candidate YES/NO confirmation (draft election rules)"};
  const ranked=options.map(name=>({name,votes:Number(counts[name]||0)})).sort((a,b)=>b.votes-a.votes),validVotes=ranked.reduce((a,v)=>a+v.votes,0),won=quorum&&validVotes>0&&ranked[0].votes*2>validVotes;
  return {quorum,total,validVotes,ranked,winner:won?ranked[0].name:null,needsRunoff:quorum&&!won,basis:"More than half valid votes or separate runoff (draft election rules)"};
 }
 throw Error("Unknown ballot type")
}
export function enoughNotice(kind,noticeAt,now){return kind!=="amendment"||(Number.isFinite(Date.parse(noticeAt))&&now-Date.parse(noticeAt)>=14*86400000)}
export function mayClose(kind,eligible,voted,endsAt,now){return kind==="election"?now>=Date.parse(endsAt):now>=Date.parse(endsAt)||voted>=eligible}
export function mayVote(p,now){return p.status==="open"&&Number.isFinite(Date.parse(p.opens_at))&&Number.isFinite(Date.parse(p.closes_at))&&now>=Date.parse(p.opens_at)&&now<Date.parse(p.closes_at)}
