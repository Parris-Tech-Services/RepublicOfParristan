/**
 * Temporary public preview of the verifiable GitHub Gazette/docs snapshot.
 * Safe fallback while Vercel free-tier deployment quota blocks public domain.
 * The official domain remains parristan.org; this mirror has NO write API.
 */
const COMMIT='debff8e02e2853b5c750852b7a895e66a4467852';
const BASE='https://raw.githubusercontent.com/Parris-Tech-Services/RepublicOfParristan/'+COMMIT+'/docs';
const types={html:'text/html; charset=utf-8',css:'text/css; charset=utf-8',js:'text/javascript; charset=utf-8',json:'application/json; charset=utf-8',svg:'image/svg+xml',png:'image/png',ico:'image/x-icon',webp:'image/webp',jpg:'image/jpeg',jpeg:'image/jpeg',txt:'text/plain; charset=utf-8',xml:'application/xml'};
export default {
 async fetch(request){
   if(!['GET','HEAD'].includes(request.method))return new Response('Read-only preview',{status:405,headers:{allow:'GET, HEAD'}});
   const u=new URL(request.url);
   const path=u.pathname==='/'?'/index.html':u.pathname;
   if(!/^\/[a-zA-Z0-9_./-]+$/.test(path)||path.includes('..')||path.includes('//'))return new Response('Invalid path',{status:400});
   const ext=path.split('.').at(-1).toLowerCase();
   if(!types[ext])return new Response('Unsupported file',{status:404});
   const upstream=await fetch(BASE+path,{headers:{'accept':'*/*'}});
   if(!upstream.ok)return new Response('Not found in pinned Gazette revision',{status:upstream.status===404?404:502});
   const headers=new Headers({
     'content-type':types[ext],
     'cache-control':'public,max-age=300',
     'x-content-type-options':'nosniff',
     'referrer-policy':'strict-origin-when-cross-origin',
     'x-parristan-preview-commit':COMMIT,
     'x-parristan-mirror':'read-only-unofficial-preview'
   });
   if(request.method==='HEAD')return new Response(null,{status:200,headers});
   return new Response(upstream.body,{status:200,headers});
 }
};