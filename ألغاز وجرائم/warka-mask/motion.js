// Root timeline: absolute media time, deterministic even when sampled out of order.
const CUT = /*CUTS*/[];
const DURATION = /*DURATION*/0;
const tl = gsap.timeline({paused:true});
const clip = i => document.getElementById(`s${i}`);
const arr = (root, sel) => Array.from(root.querySelectorAll(sel));
CUT.slice(0,-1).forEach((at,i) => {
  const el = clip(i), d=CUT[i+1]-at;
  if(i){tl.set(el,{opacity:0},0);tl.set(clip(i-1),{opacity:0},at)}
  tl.set(el,{opacity:1},at);
  arr(el,'.drift').forEach(node => {
    tl.fromTo(node,{scale:1,x:0,y:0},{scale:+(node.dataset.zoom||1.04),x:+(node.dataset.dx||0),y:+(node.dataset.dy||0),duration:d,ease:'sine.inOut',immediateRender:false},at);
  });
  arr(el,'.art').filter(svg=>svg.style.zIndex==='0').forEach(node=>{
    tl.fromTo(node,{x:-10,y:14},{x:12,y:-12,duration:d,ease:'sine.inOut',immediateRender:false},at);
  });
  arr(el,'.pop').forEach(node=>{
    const lag=+node.dataset.in||0, t=at+lag;
    if(i===0 && lag===0) tl.set(node,{opacity:1},0);
    else {
      tl.set(node,{opacity:0},0);
      tl.fromTo(node,{opacity:0,y:28},{opacity:1,y:0,duration:.24,ease:'power3.out',immediateRender:false},t);
    }
    arr(node,'.hl').forEach(mark=>tl.fromTo(mark,{backgroundSize:'0% 78%'},{backgroundSize:'100% 78%',duration:.38,ease:'power2.inOut',immediateRender:false},t));
  });
  arr(el,'.draw').forEach(node=>{
    tl.set(node,{attr:{'stroke-dasharray':'1 1','stroke-dashoffset':1}},0);
    tl.to(node,{attr:{'stroke-dashoffset':0},duration:.55,ease:'power2.inOut'},at+(+node.dataset.in||.45));
  });
});
// A field of yellow passes through the actual cut. No chapter bars or persistent branding.
tl.set('#wipe',{opacity:0,x:1540},0);
CUT.slice(1,-1).forEach((at,i)=>{
  const sign=i%4===2?-1:1;
  tl.set('#wipe',{x:sign*1450,opacity:1},at-.16);
  tl.to('#wipe',{x:0,duration:.16,ease:'power2.in'},at-.16);
  tl.to('#wipe',{x:-sign*1460,duration:.195,ease:'power2.out'},at);
  tl.set('#wipe',{opacity:0},at+.2);
});
tl.to({},{duration:.01},DURATION-.01);
window.__timelines=window.__timelines||{};
window.__timelines.warka=tl;
