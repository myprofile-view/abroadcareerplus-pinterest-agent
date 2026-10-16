#!/usr/bin/env python3
"""Create an attractive country-themed Pinterest pin. Photo is optional and must be licensed."""
import argparse, json, re, io
from pathlib import Path
from datetime import datetime, timezone
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

THEMES = {
    "norway": ("#C8102E", "#003087", "#F5F8FC"),
    "uk": ("#C8102E", "#012169", "#FFFFFF"),
    "united kingdom": ("#C8102E", "#012169", "#FFFFFF"),
    "france": ("#0055A4", "#EF4135", "#FFFFFF"),
    "denmark": ("#C8102E", "#FFFFFF", "#F7F7F7"),
    "netherlands": ("#AE1C28", "#21468B", "#FFFFFF"),
    "canada": ("#D80621", "#FFFFFF", "#F8F8F8"),
    "usa": ("#B22234", "#3C3B6E", "#FFFFFF"),
    "united states": ("#B22234", "#3C3B6E", "#FFFFFF"),
    "romania": ("#002B7F", "#FCD116", "#CE1126"),
    "brunei": ("#F7E017", "#000000", "#FFFFFF"),
    "international": ("#155EEF", "#102A43", "#FFFFFF"),
}
W, H = 1000, 1500

def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for p in paths:
        try: return ImageFont.truetype(p, size)
        except OSError: pass
    return ImageFont.load_default()

def wrap(draw, text, fnt, max_width):
    words, lines, line = str(text).split(), [], ""
    for word in words:
        test=(line+" "+word).strip()
        if draw.textbbox((0,0),test,font=fnt)[2] <= max_width: line=test
        else:
            if line: lines.append(line)
            line=word
    if line: lines.append(line)
    return lines

def slug(s):
    return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")[:58] or "offshore-careers"

def load_photo(url):
    if not url: return None
    try:
        r=requests.get(url, timeout=25, headers={"User-Agent":"AbroadCareerPlusPinAgent/2.0"})
        r.raise_for_status()
        if "image" not in r.headers.get("content-type","").lower():
            raise ValueError("Photo URL did not return an image. Use a direct image URL.")
        im=Image.open(io.BytesIO(r.content)).convert("RGB")
        if im.width < 400 or im.height < 400:
            raise ValueError("Image is too small. Use an image at least 400x400.")
        return im
    except Exception as e:
        raise SystemExit(f"Could not load photo: {e}. Leave photo URL blank to use the graphic background.")

def crop_fill(im, size):
    w,h=size
    scale=max(w/im.width,h/im.height)
    im=im.resize((int(im.width*scale),int(im.height*scale)),Image.Resampling.LANCZOS)
    x=(im.width-w)//2; y=(im.height-h)//2
    return im.crop((x,y,x+w,y+h))

def make_pin(title, country, website, photo_url, out_path):
    accent, dark, light = THEMES.get(country.lower().strip(), THEMES["international"])
    photo=load_photo(photo_url)
    if photo:
        im=crop_fill(photo,(W,H)).convert("RGBA")
        overlay=Image.new("RGBA",(W,H),(6,22,36,100))
        im=Image.alpha_composite(im,overlay).convert("RGB")
    else:
        im=Image.new("RGB",(W,H),"#102A43")
        d0=ImageDraw.Draw(im)
        d0.rectangle((0,0,W,500),fill=dark)
        d0.rectangle((0,0,28,H),fill=accent)
        # abstract waves/platform silhouettes as fallback background
        d0.polygon([(0,430),(220,365),(420,420),(650,330),(1000,405),(1000,760),(0,760)],fill="#1C4660")
        for x in range(150,900,180):
            d0.rectangle((x,350,x+12,720),fill="#6E8798")
            d0.line((x-45,460,x+55,460),fill="#A8BAC6",width=8)
            d0.line((x-45,560,x+55,560),fill="#A8BAC6",width=8)
        im=im.filter(ImageFilter.GaussianBlur(0.4))
    d=ImageDraw.Draw(im,"RGBA")
    # top brand capsule
    d.rounded_rectangle((58,55,942,220),radius=34,fill=(7,24,38,210),outline=(255,255,255,100),width=2)
    d.text((95,88),"ABROADCAREERPLUS",font=font(43,True),fill="white")
    d.text((97,151),"OFFSHORE CAREER GUIDE",font=font(25,True),fill="#DDE9FF")
    # accent strip
    d.rounded_rectangle((70,285,360,345),radius=18,fill=accent)
    d.text((91,299),"OFFSHORE JOBS",font=font(25,True),fill="white")
    # headline card
    d.rounded_rectangle((60,385,940,755),radius=34,fill=(5,20,35,218),outline=(255,255,255,100),width=2)
    lines=wrap(d,title,font(61,True),760)
    y=445
    for line in lines[:4]:
        d.text((100,y),line,font=font(61,True),fill="white",stroke_width=1,stroke_fill=(0,0,0,80))
        y+=78
    # country panel
    d.rounded_rectangle((75,805,925,965),radius=28,fill=(248,251,255,238))
    d.text((112,830),"COUNTRY / REGION",font=font(22,True),fill=dark)
    d.text((112,875),country.upper(),font=font(43,True),fill=accent if accent not in ("#FFFFFF","#F7F7F7") else dark)
    # three quick points
    d.text((85,1020),"BEFORE YOU APPLY",font=font(31,True),fill="white")
    checks=["Verify the official vacancy notice","Check experience and certificates","Confirm employer and application link"]
    y=1080
    for item in checks:
        d.ellipse((90,y+3,128,y+41),fill=accent)
        d.line((100,y+22,108,y+30),fill="white",width=5)
        d.line((108,y+30,120,y+13),fill="white",width=5)
        d.text((150,y),item,font=font(25,True),fill="white",stroke_width=1,stroke_fill=(0,0,0,130))
        y+=66
    d.rounded_rectangle((75,1300,925,1390),radius=24,fill=accent)
    cta="EXPLORE CAREER RESOURCES"
    f=font(28,True); bb=d.textbbox((0,0),cta,font=f)
    d.text(((W-(bb[2]-bb[0]))//2,1326),cta,font=f,fill="white")
    d.text((85,1410),website,font=font(23,True),fill="white",stroke_width=1,stroke_fill=(0,0,0,150))
    d.text((85,1450),"General career information • Verify vacancies officially",font=font(18),fill="white",stroke_width=1,stroke_fill=(0,0,0,150))
    im.convert("RGB").save(out_path,quality=94)
    return slug(title)+".jpg"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--title",default="Norway Offshore Jobs")
    p.add_argument("--country",default="Norway")
    p.add_argument("--url",default="https://abroadcareerplus.com/")
    p.add_argument("--photo-url",default="")
    p.add_argument("--output",default="output")
    a=p.parse_args()
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    filename=slug(a.title)+".jpg"
    make_pin(a.title,a.country,"abroadcareerplus.com",a.photo_url,out/filename)
    description=(f"Explore {a.title} with AbroadCareerPlus. Learn about offshore career requirements, "
        f"experience, safety training and application checks for {a.country}. This is general career information, "
        "not a confirmed vacancy. Verify current openings through official employer channels.")
    data={
      "title":a.title[:100],"description":description,"destination_url":a.url,
      "board_suggestion":"Offshore Jobs",
      "alt_text":f"AbroadCareerPlus offshore career pin about {a.title}, focused on {a.country}.",
      "hashtags":["#OffshoreJobs","#OilAndGasJobs","#OffshoreCareers","#AbroadCareerPlus"],
      "image_file":filename,"image_size":"1000x1500 (2:3)","review_before_publish":True,
      "photo_used":bool(a.photo_url),"created_utc":datetime.now(timezone.utc).isoformat()
    }
    (out/"pin.json").write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"image_file":filename,"metadata":"pin.json"}))
if __name__=="__main__": main()
