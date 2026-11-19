// Offline browser check of *text glyphs*, not the full-width alignment wrappers.
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const p=path.resolve(__dirname,'..'), puppeteer=require('puppeteer-core');
(async()=>{
 const browser=await puppeteer.launch({executablePath:process.env.CHROME||process.env.PUPPETEER_EXECUTABLE_PATH,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'],headless:true});
 try{
  const pg=await browser.newPage(); await pg.setViewport({width:1080,height:1920,deviceScaleFactor:1});await pg.goto(pathToFileURL(path.join(p,'index.html')).href);
  const result=await pg.evaluate(async()=>{
   await document.fonts.load('900 100px Cairo','العراق');await document.fonts.ready;
   const c=document.createElement('canvas').getContext('2d'),lim={x1:70,x2:1010,y1:150,y2:1700},ext={x1:1080,x2:0,y1:1920,y2:0},bad=[];let n=0;
   const shots=[...document.querySelectorAll('section.scene')];
   for(const s of shots){
    const start=+s.dataset.start,end=start+(+s.dataset.duration);
    for(let t=start+.1;t<end-.18;t+=.2){window.__timelines.warka.seek(t,false);
     for(const el of s.querySelectorAll('.word')){if(+getComputedStyle(el).opacity<.65)continue;
      const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let node;
      while(node=walker.nextNode()){
       if(!node.textContent.trim())continue; const range=new Range();range.selectNodeContents(node);const r=range.getBoundingClientRect(),style=getComputedStyle(node.parentElement);
       c.font=`${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;c.direction=style.direction;const m=c.measureText(node.textContent),base=r.top+m.fontBoundingBoxAscent;
       const rec={x1:r.left,x2:r.right,y1:base-m.actualBoundingBoxAscent,y2:base+m.actualBoundingBoxDescent};n++;
       for(const side of Object.keys(lim)){const isMin=side.endsWith('1');ext[side]=(isMin?Math.min:Math.max)(ext[side],rec[side]);if(isMin?rec[side]<lim[side]-.5:rec[side]>lim[side]+.5){bad.push({scene:s.id,time:t,text:node.textContent,side,edge:rec[side]});break;}}
      }
     }
    }
   }
   return {fontLoaded:document.fonts.check('900 100px Cairo','الوركاء'),positions:n,glyphExtent:ext,outside:bad,shots:shots.length};
  });fs.mkdirSync(path.join(p,'out'),{recursive:true});fs.writeFileSync(path.join(p,'out','layout-check.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,outside:result.outside.slice(0,8)}));if(result.outside.length||!result.fontLoaded)process.exitCode=1;
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
