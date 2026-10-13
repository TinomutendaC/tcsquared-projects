const $=id=>document.getElementById(id);
const el=(t,x,c)=>{const e=document.createElement(t);if(x!=null)e.textContent=x;if(c)e.className=c;return e};
const ALL=PROJECTS.flatMap(p=>(p.files||[]).map(f=>({...f,project:p.title})));
const KINDS=[["all","All"],["image","Pictures"],["video","Videos"],["doc","Documents"],["link","Links"]];
let filter="all";
function draw(){
  $("filters").replaceChildren(...KINDS.map(([k,l])=>{const b=el("button",l);b.className=k===filter?"on":"";b.onclick=()=>{filter=k;draw()};return b}));
  const list=ALL.filter(f=>filter==="all"||f.kind===filter);
  $("none").hidden=list.length>0;
  $("grid").replaceChildren(...list.map(f=>{
    const c=el("div",null,"item");
    if(f.kind==="image"){const i=el("img");i.src=f.path;i.alt=f.name;i.loading="lazy";c.append(i)}
    if(f.kind==="video"){const v=el("video");v.src=f.path;v.controls=true;v.preload="metadata";c.append(v)}
    const a=el("a",(f.kind==="doc"?"📄 ":f.kind==="link"?"🔗 ":"")+f.name);a.href=f.path;a.target="_blank";a.rel="noopener";c.append(a,el("small",f.project));
    return c}));
}
draw();$("yr").textContent=new Date().getFullYear();
$("burger").onclick=()=>{const o=$("nav").classList.toggle("open");$("burger").setAttribute("aria-expanded",o)};
