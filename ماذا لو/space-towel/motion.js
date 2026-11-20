// html-anime's on-twos replacement drawings, never cross-faded. Separate continuous motions are water/light/props.
const F=1/24, tl=gsap.timeline({paused:true});
function swap(from,to,frame){tl.set(from,{opacity:0},frame*F);tl.set(to,{opacity:1},frame*F)}
for (const [i,s] of SHEET.shots.entries()) {
  const start=s.start*F,end=s.end*F,dur=end-start,id='#'+s.id,fx=id+'fx';
  tl.set(id,{visibility:'visible'},start);if(i+1<SHEET.shots.length)tl.set(id,{visibility:'hidden'},end);
  let cur=0;for(const [to,offset] of s.keys.slice(1)){swap(id+'d'+cur,id+'d'+to,s.start+offset);cur=to;}
  if(i===0)tl.fromTo(id+'w',{scale:1},{scale:1.06,duration:dur,ease:'power1.inOut'},start);
  if(i>0){tl.to('#dip',{opacity:1,duration:.25,ease:'power2.in'},start-.25);tl.to('#dip',{opacity:0,duration:.35,ease:'power2.out'},start);}
  if(s.fx==='pearl') tl.fromTo(fx,{x:-3,y:8},{x:18,y:-29,duration:dur,ease:'sine.inOut'},start);
  if(s.fx==='drop') {
    for(const off of [.28,1.27,2.2]){tl.set(fx,{x:0,y:-24,opacity:1},start+off);tl.to(fx,{x:6,y:271,duration:.56,ease:'power2.in'},start+off);tl.set(fx,{opacity:0},start+off+.56);tl.fromTo('#ripple',{opacity:.9,scale:.28,svgOrigin:'289 535'},{opacity:0,scale:1.20,duration:.34,ease:'power1.out'},start+off+.56);}
  }
  if(s.fx==='few') tl.fromTo(fx,{x:0,y:0},{x:-49,y:-81,duration:dur,ease:'sine.inOut'},start);
  if(s.fx==='drift') tl.fromTo(fx,{x:0,y:8},{x:27,y:-67,duration:dur,ease:'sine.inOut'},start);
  if(s.fx==='water') tl.fromTo(fx,{x:0,y:0},{x:34,y:92,duration:dur-.15,ease:'power1.in'},start+.12);
  if(s.fx==='lead'){tl.fromTo(fx,{x:-22,y:-9},{x:13,y:34,duration:.88,ease:'sine.inOut'},start+.18);tl.to(fx,{x:-8,y:70,duration:.58,ease:'sine.inOut'},start+1.12);tl.to(fx,{x:16,y:196,duration:.88,ease:'power1.inOut'},start+1.73);}
  if(s.fx==='glint'||s.fx==='shine'){tl.fromTo(fx,{opacity:.15},{opacity:1,duration:.55,ease:'sine.out'},start+.3);tl.to(fx,{opacity:.12,duration:.63},start+1.02);tl.to(fx,{opacity:.9,duration:.46},start+2.11);}
}
tl.set('#s19text',{opacity:1},SHEET.voiceAt);tl.to('#out',{opacity:1,duration:7*F,ease:'power1.in'},60-8*F);tl.to({},{duration:F},60-F);
window.__timelines=window.__timelines||{};window.__timelines['space-towel']=tl;
