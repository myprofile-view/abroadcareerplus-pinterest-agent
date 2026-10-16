#!/usr/bin/env python3
"""Beginner Pinterest pin agent for AbroadCareerPlus. No API key needed."""
import argparse, json, re
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont

BLUE = "#155EEF"
NAVY = "#102A43"
PALE = "#F2F7FF"
WHITE = "#FFFFFF"
MUTED = "#526579"

def font(size, bold=False):
    choices = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for p in choices:
        try: return ImageFont.truetype(p, size)
        except OSError: pass
    return ImageFont.load_default()

def wrap(draw, text, fnt, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= max_width:
            line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def make_pin(title, country, website):
    w,h=1000,1500
    im=Image.new("RGB",(w,h),PALE)
    d=ImageDraw.Draw(im)
    # simple, clean brand layout
    d.rounded_rectangle((45,45,955,1455),radius=44,fill=WHITE,outline="#D7E4F7",width=4)
    d.rounded_rectangle((75,75,925,240),radius=30,fill=BLUE)
    d.text((115,112),"ABROADCAREERPLUS",font=font(42,True),fill=WHITE)
    d.text((115,174),"OFFSHORE CAREER GUIDE",font=font(24,True),fill="#DDE8FF")
    d.rounded_rectangle((100,300,900,690),radius=34,fill=NAVY)
    d.text((145,345),"OFFSHORE JOBS",font=font(28,True),fill="#A9C7FF")
    lines=wrap(d,title,font(55,True),700)
    y=405
    for line in lines[:4]:
        d.text((145,y),line,font=font(55,True),fill=WHITE)
        y+=72
    d.rounded_rectangle((100,735,900,900),radius=28,fill="#E7F7D5")
    d.text((140,780),"LOCATION / CAREER FOCUS",font=font(23,True),fill="#365314")
    country_lines=wrap(d,country,font(40,True),700)
    y=820
    for line in country_lines[:2]:
        d.text((140,y),line,font=font(40,True),fill="#203D18")
        y+=48
    # checklist panel
    d.text((115,965),"BEFORE YOU APPLY",font=font(29,True),fill=BLUE)
    items=["Check the official vacancy notice","Confirm certificates and experience","Verify the employer and application link"]
    y=1025
    for item in items:
        d.ellipse((120,y+6,151,y+37),fill=BLUE)
        d.line((128,y+21,136,y+29),fill=WHITE,width=4)
        d.line((136,y+29,145,y+14),fill=WHITE,width=4)
        d.text((170,y),item,font=font(25),fill=NAVY)
        y+=65
    d.rounded_rectangle((100,1245,900,1335),radius=25,fill=BLUE)
    cta="EXPLORE CAREER RESOURCES"
    bb=d.textbbox((0,0),cta,font=font(28,True))
    d.text(((w-(bb[2]-bb[0]))//2,1272),cta,font=font(28,True),fill=WHITE)
    d.text((115,1380),website,font=font(22,True),fill=MUTED)
    d.text((115,1418),"General career information • Verify vacancies officially",font=font(18),fill=MUTED)
    return im

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--title",default="Offshore Instrument Technician Careers")
    p.add_argument("--country",default="North Sea")
    p.add_argument("--url",default="https://abroadcareerplus.com/")
    p.add_argument("--output",default="output")
    a=p.parse_args()
    out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    safe=re.sub(r"[^a-z0-9]+","-",a.title.lower()).strip("-")[:55] or "pinterest-pin"
    title=a.title.strip()
    description=(f"Explore {title} with AbroadCareerPlus. Learn about offshore career requirements, "
                 f"experience, and application checks for {a.country}. This is general career information, "
                 "not a confirmed vacancy. Verify current openings through official employer channels.")
    metadata={
        "title": title[:100],
        "description": description,
        "destination_url": a.url,
        "board_suggestion": "Offshore Jobs",
        "alt_text": f"Blue and white AbroadCareerPlus Pinterest pin about {title}, location focus {a.country}.",
        "hashtags": ["#OffshoreJobs","#OilAndGasJobs","#OffshoreCareers","#AbroadCareerPlus"],
        "image_size": "1000x1500 (2:3)",
        "review_before_publish": True,
        "created_utc": datetime.now(timezone.utc).isoformat()
    }
    make_pin(title,a.country,"abroadcareerplus.com").save(out/f"{safe}.png")
    (out/f"{safe}.json").write_text(json.dumps(metadata,indent=2,ensure_ascii=False),encoding="utf-8")
    (out/"README-output.txt").write_text("Review the pin image and metadata before posting. The first version does not publish to Pinterest automatically.\n",encoding="utf-8")
    print("Pin image and Pinterest metadata created in:",out)

if __name__=="__main__": main()
