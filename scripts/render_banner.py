#!/usr/bin/env python3
"""Deterministic PNG/JPG banner renderer for one banner-matrix job."""
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
from typing import Any
try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError as exc:
    raise SystemExit("Pillow is required; install requirements.txt") from exc

ROOT = Path(__file__).resolve().parents[1]
PRESETS = ROOT / "config" / "layout-presets.json"

class RenderError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message); self.code = code

def load_presets(): return json.loads(PRESETS.read_text(encoding="utf-8"))

def resolve_family(presets, family):
    try: cur = dict(presets["families"][family])
    except KeyError: raise RenderError("FAIL_LAYOUT_FAMILY", f"unknown layout family: {family}")
    parent = cur.pop("inherits", None)
    if not parent: return cur
    base = resolve_family(presets, parent); out = dict(base)
    for k,v in cur.items():
        if k in {"slots","text"}: out[k] = {**base.get(k,{}), **v}
        else: out[k] = v
    return out

def color(value):
    if not isinstance(value,str) or not value.startswith("#") or len(value) not in {7,9}:
        raise RenderError("FAIL_COLOR", f"invalid color: {value!r}")
    try: return tuple(int(value[i:i+2],16) for i in range(1,len(value),2))
    except ValueError: raise RenderError("FAIL_COLOR", f"invalid color: {value!r}")

def luminance(rgb):
    c=[]
    for v in rgb[:3]:
        x=v/255; c.append(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4)
    return .2126*c[0]+.7152*c[1]+.0722*c[2]

def contrast_ratio(a,b):
    x,y=luminance(color(a)),luminance(color(b)); hi,lo=max(x,y),min(x,y)
    return (hi+.05)/(lo+.05)

def resolve_font_path(path):
    candidates=[path,os.getenv("BANNER_FONT_PATH"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf","/System/Library/Fonts/Supplemental/Arial.ttf"]
    for p in candidates:
        if p and Path(p).is_file(): return str(p)
    raise RenderError("FAIL_FONT","provide brand.font_regular or BANNER_FONT_PATH")

def box_px(w,h,v):
    if not isinstance(v,list) or len(v)!=4 or v[2]<=0 or v[3]<=0: raise RenderError("FAIL_LAYOUT",f"bad slot: {v!r}")
    x,y,bw,bh=v; return round(x*w),round(y*h),round((x+bw)*w),round((y+bh)*h)

def wrap(draw,text,font,max_w,max_lines):
    words=" ".join(str(text).split()).split(); lines=[]; cur=""
    for word in words:
        if draw.textlength(word,font=font)>max_w: return None
        nxt=word if not cur else cur+" "+word
        if draw.textlength(nxt,font=font)<=max_w: cur=nxt
        else:
            lines.append(cur); cur=word
            if len(lines)>=max_lines: return None
    if cur: lines.append(cur)
    return lines if len(lines)<=max_lines else None

def fit(draw,text,box,font_path,rules):
    l,t,r,b=box; mw,mh=max(1,r-l),max(1,b-t)
    mn,mx,ml=int(rules["min_px"]),int(rules["max_px"]),int(rules.get("max_lines",1))
    if mn<1 or mx<mn: raise RenderError("FAIL_TEXT_RULE",f"bad text rules: {rules}")
    for size in range(mx,mn-1,-1):
        font=ImageFont.truetype(font_path,size); lines=wrap(draw,text,font,mw,ml)
        if lines is None: continue
        spacing=max(1,round(size*.16)); rendered="\n".join(lines)
        bb=draw.multiline_textbbox((0,0),rendered,font=font,spacing=spacing)
        rw,rh=bb[2]-bb[0],bb[3]-bb[1]
        if rw<=mw and rh<=mh: return font,size,lines,spacing,rw,rh
    raise RenderError("FAIL_COPY_OVERFLOW",f"copy cannot fit at minimum {mn}px: {text!r}")

def text_in_box(canvas,text,box,font_path,rules,fill,align="left"):
    if not text or not box: return None
    draw=ImageDraw.Draw(canvas); font,size,lines,spacing,rw,rh=fit(draw,text,box,font_path,rules)
    l,t,r,b=box; y=t+max(0,(b-t-rh)//2); x=l; anchor="la"
    if align=="center": x=l+(r-l)//2; anchor="ma"
    draw.multiline_text((x,y),"\n".join(lines),font=font,fill=color(fill),spacing=spacing,align=align,anchor=anchor)
    return {"text":text,"box":list(box),"font_size":size,"lines":lines}

def paste(canvas,path,box,mode="cover",focal=(.5,.5)):
    p=Path(path)
    if not p.is_file(): raise RenderError("FAIL_ASSET",f"asset not found: {path}")
    with Image.open(p) as src:
        size=(max(1,box[2]-box[0]),max(1,box[3]-box[1]))
        if mode=="cover": img=ImageOps.fit(src.convert("RGB"),size,Image.Resampling.LANCZOS,centering=(max(0,min(1,float(focal[0]))),max(0,min(1,float(focal[1]))))).convert("RGBA"); pos=box[:2]
        elif mode=="contain":
            img=src.convert("RGBA"); img.thumbnail(size,Image.Resampling.LANCZOS); pos=(box[0]+(size[0]-img.width)//2,box[1]+(size[1]-img.height)//2)
        else: raise RenderError("FAIL_ASSET",f"bad fit mode: {mode}")
        canvas.alpha_composite(img,dest=pos)

def apply_lighting(canvas,cfg):
    w,h=canvas.size
    s=cfg.get("spotlight") or {}
    if s.get("enabled"):
        cx,cy=s.get("center",[.5,.4]); rx,ry=s.get("radius",[.35,.25]); mask=Image.new("L",(w,h),0); d=ImageDraw.Draw(mask)
        d.ellipse([round((cx-rx)*w),round((cy-ry)*h),round((cx+rx)*w),round((cy+ry)*h)],fill=max(0,min(255,int(s.get("opacity",80)))))
        mask=mask.filter(ImageFilter.GaussianBlur(max(0,int(s.get("blur",max(8,min(w,h)*.08)))))); ov=Image.new("RGBA",(w,h),(*color(s.get("color","#FFFFFF"))[:3],255)); ov.putalpha(mask); canvas.alpha_composite(ov)
    s=cfg.get("copy_scrim") or {}
    if s.get("enabled"):
        side=s.get("side","bottom"); extent=max(.05,min(1,float(s.get("extent",.55)))); opacity=max(0,min(255,int(s.get("max_opacity",128)))); mask=Image.new("L",(w,h),0); d=ImageDraw.Draw(mask)
        steps=h if side in {"top","bottom"} else w; edge=max(1,round(steps*extent))
        for i in range(edge):
            a=round(opacity*(i/max(1,edge-1))); a=opacity-a if side in {"top","left"} else a
            if side=="bottom": d.line((0,h-edge+i,w,h-edge+i),fill=a)
            elif side=="top": d.line((0,i,w,i),fill=a)
            elif side=="right": d.line((w-edge+i,0,w-edge+i,h),fill=a)
            elif side=="left": d.line((i,0,i,h),fill=a)
            else: raise RenderError("FAIL_LIGHTING",f"bad scrim side: {side}")
        ov=Image.new("RGBA",(w,h),(*color(s.get("color","#000000"))[:3],255)); ov.putalpha(mask); canvas.alpha_composite(ov)
    s=cfg.get("vignette") or {}
    if s.get("enabled"):
        opacity=max(0,min(255,int(s.get("opacity",80)))); softness=max(.05,min(.95,float(s.get("softness",.45)))); mask=Image.radial_gradient("L").resize((w,h),Image.Resampling.BILINEAR)
        threshold=round(255*(1-softness)); mask=mask.point(lambda p: 0 if p<threshold else round(opacity*(p-threshold)/max(1,255-threshold)))
        ov=Image.new("RGBA",(w,h),(*color(s.get("color","#000000"))[:3],255)); ov.putalpha(mask); canvas.alpha_composite(ov)

def pill(canvas,text,box,font_path,rules,fill,text_color,radius):
    if not text or not box:return None
    d=ImageDraw.Draw(canvas); d.rounded_rectangle(box,radius=max(0,radius),fill=color(fill)); l,t,r,b=box; pad=max(2,round(min(r-l,b-t)*.1))
    return text_in_box(canvas,text,(l+pad,t+pad,r-pad,b-pad),font_path,rules,text_color,"center")

def save(canvas,path,out):
    fmt=out.get("format",path.suffix.lstrip(".") or "png").lower(); fmt="jpg" if fmt=="jpeg" else fmt; target=out.get("target_max_bytes")
    if target is not None and int(target)<1000: raise RenderError("FAIL_FILE_SIZE_RULE","target_max_bytes < 1000")
    target=int(target) if target else None; path.parent.mkdir(parents=True,exist_ok=True)
    if fmt=="png":
        canvas.convert("RGB").save(path,"PNG",optimize=True); n=path.stat().st_size
        if target and n>target: raise RenderError("FAIL_FILE_SIZE",f"PNG {n} > {target} bytes")
        return {"format":"png","bytes":n}
    if fmt=="jpg":
        hi,lo=int(out.get("jpeg_quality",92)),int(out.get("min_jpeg_quality",70))
        if not 20<=lo<=hi<=100: raise RenderError("FAIL_FILE_SIZE_RULE","invalid JPEG quality range")
        for q in range(hi,lo-1,-2):
            canvas.convert("RGB").save(path,"JPEG",quality=q,optimize=True,progressive=True); n=path.stat().st_size
            if not target or n<=target:return {"format":"jpg","bytes":n,"jpeg_quality":q}
        raise RenderError("FAIL_FILE_SIZE",f"JPEG remains above {target} bytes at quality {lo}")
    raise RenderError("FAIL_FORMAT",f"renderer supports png/jpg, got {fmt}")

def render_banner(spec: dict[str,Any]):
    required=["job_id","width","height","layout_family","copy","brand","output"]
    missing=[x for x in required if x not in spec]
    if missing: raise RenderError("FAIL_SPEC","missing: "+", ".join(missing))
    w,h=int(spec["width"]),int(spec["height"])
    if w<1 or h<1: raise RenderError("FAIL_DIMENSIONS","width/height must be positive")
    layout=resolve_family(load_presets(),str(spec["layout_family"])); overrides=spec.get("overrides") or {}; slots={**layout.get("slots",{}),**(overrides.get("slots") or {})}; rules=dict(layout.get("text",{}))
    for k,v in (overrides.get("text") or {}).items(): rules[k]={**rules.get(k,{}),**v}
    bg=(spec.get("background") or {}).get("color","#FFFFFF"); canvas=Image.new("RGBA",(w,h),(*color(bg)[:3],255)); hero=spec.get("hero") or {}; hero_path=hero.get("path")
    if hero_path:
        mode=hero.get("mode",layout.get("hero_mode","slot")); hb=(0,0,w,h) if mode in {"full_bleed","full_bleed_optional"} else box_px(w,h,slots.get("hero")); paste(canvas,hero_path,hb,"cover",hero.get("focal_point",[.5,.5]))
    apply_lighting(canvas,spec.get("lighting") or {}); brand=spec.get("brand") or {}; regular=resolve_font_path(brand.get("font_regular")); bold=resolve_font_path(brand.get("font_bold") or regular); tc=brand.get("text_color","#111111"); muted=brand.get("muted_text_color",tc)
    def b(name): return box_px(w,h,slots[name]) if slots.get(name) else None
    elements={}; logo=spec.get("logo") or {}
    if logo.get("path") and b("logo"): paste(canvas,logo["path"],b("logo"),"contain"); elements["logo"]={"box":list(b("logo")),"asset":logo["path"]}
    elif logo.get("brand_name") and b("logo"): elements["brand_name"]=text_in_box(canvas,logo["brand_name"],b("logo"),bold,{"min_px":max(8,round(h*.035)),"max_px":max(10,round(h*.08)),"max_lines":1},tc)
    copy=spec.get("copy") or {}
    for name,font,fill in [("headline",bold,tc),("support",regular,muted)]:
        if copy.get(name):
            if name not in rules: raise RenderError("FAIL_LAYOUT",f"no {name} rules")
            elements[name]=text_in_box(canvas,copy[name],b(name),font,rules[name],fill)
    if copy.get("offer"): elements["offer"]=pill(canvas,copy["offer"],b("offer"),bold,rules["offer"],brand.get("offer_fill",brand.get("accent_color","#F0EAE2")),brand.get("offer_text",tc),int(brand.get("offer_radius_px",max(2,(b("offer")[3]-b("offer")[1])//4))))
    if copy.get("cta"): elements["cta"]=pill(canvas,copy["cta"],b("cta"),bold,rules["cta"],brand.get("cta_fill",brand.get("accent_color","#111111")),brand.get("cta_text","#FFFFFF"),int(brand.get("cta_radius_px",max(2,(b("cta")[3]-b("cta")[1])//5))))
    ratios={"cta_text_vs_fill":round(contrast_ratio(brand.get("cta_text","#FFFFFF"),brand.get("cta_fill",brand.get("accent_color","#111111"))),3) if copy.get("cta") else None,"flat_text_vs_background":None}
    full=bool(hero_path and hero.get("mode",layout.get("hero_mode","slot")) in {"full_bleed","full_bleed_optional"})
    if not full: ratios["flat_text_vs_background"]=round(contrast_ratio(tc,bg),3)
    qa=spec.get("qa") or {}
    if qa.get("min_cta_contrast") is not None and ratios["cta_text_vs_fill"]<float(qa["min_cta_contrast"]): raise RenderError("FAIL_CONTRAST",f"CTA contrast {ratios['cta_text_vs_fill']}:1 below minimum")
    if qa.get("min_flat_text_contrast") is not None and ratios["flat_text_vs_background"] is not None and ratios["flat_text_vs_background"]<float(qa["min_flat_text_contrast"]): raise RenderError("FAIL_CONTRAST",f"flat contrast {ratios['flat_text_vs_background']}:1 below minimum")
    out=spec["output"] or {}; path=Path(out.get("path",""));
    if not str(path): raise RenderError("FAIL_SPEC","output.path required")
    saved=save(canvas,path,out); lighting=spec.get("lighting") or {}
    return {"status":"PASS","job_id":spec["job_id"],"width":w,"height":h,"layout_family":spec["layout_family"],"output_path":path.as_posix(),"output":saved,"elements":elements,"lighting_applied":[x for x in ("spotlight","copy_scrim","vignette") if (lighting.get(x) or {}).get("enabled")],"contrast":ratios}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--spec",type=Path,required=True); p.add_argument("--report",type=Path); a=p.parse_args()
    try: report=render_banner(json.loads(a.spec.read_text(encoding="utf-8")))
    except (OSError,json.JSONDecodeError,RenderError) as exc:
        print(json.dumps({"status":"FAIL","code":getattr(exc,"code","FAIL_RENDER"),"error":str(exc)},ensure_ascii=False,indent=2),file=sys.stderr); return 2
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if a.report: a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(text+"\n",encoding="utf-8")
    else: print(text)
    return 0
if __name__=="__main__": raise SystemExit(main())
