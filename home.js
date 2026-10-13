const $=id=>document.getElementById(id);
const el=(t,x,c)=>{const e=document.createElement(t);if(x!=null)e.textContent=x;if(c)e.className=c;return e};
let filter="All";
const types=["All",...new Set(PROJECTS.map(p=>p.type))];
function draw(){
  $("filters").replaceChildren(...types.map(t=>{const b=el("button",t);b.className=t===filter?"on":"";b.onclick=()=>{filter=t;draw()};return b}));
  $("grid").replaceChildren(...PROJECTS.filter(p=>filter==="All"||p.type===filter).map(p=>{
    const c=el("article",null,"card"),th=el("div",p.image?"":p.icon,"thumb "+p.tone);
    if(p.image){const i=new Image();i.onload=()=>th.style.backgroundImage=`linear-gradient(rgba(6,16,39,.25),rgba(6,16,39,.25)),url(${p.image})`;i.src=p.image}
    const b=el("div",null,"body"),ch=el("div",null,"chips");p.tags.forEach(t=>ch.append(el("span",t)));
    b.append(el("div",p.type,"kind"),el("h3",p.title),el("p",p.desc),ch);c.append(th,b);
    requestAnimationFrame(()=>c.classList.add("in"));return c}));
}
draw();
$("chips").replaceChildren(...SKILLS.map(s=>el("span",s)));
$("tools-grid").replaceChildren(...TOOLS.map(t=>{const c=el("div",null,"tool"),i=el("i",t.icon);c.append(i,el("span",t.name));return c}));
$("yr").textContent=new Date().getFullYear();
$("burger").onclick=()=>{const o=$("nav").classList.toggle("open");$("burger").setAttribute("aria-expanded",o)};
document.querySelectorAll("#nav a").forEach(a=>a.addEventListener("click",()=>$("nav").classList.remove("open")));
