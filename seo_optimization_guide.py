#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ALL THAT HYMN - 전체 영상 SEO 최적화 가이드 PDF 생성
모든 영상의 변경 제목, 설명, 태그를 복사-붙여넣기 가능하도록 작성"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

FONT_DIR = os.path.expanduser("~/Library/Fonts")
pdfmetrics.registerFont(TTFont("Gothic", os.path.join(FONT_DIR, "PyeojinGothic-Regular.ttf")))
pdfmetrics.registerFont(TTFont("GothicBold", os.path.join(FONT_DIR, "PyeojinGothic-Bold.ttf")))
pdfmetrics.registerFont(TTFont("GothicSemibold", os.path.join(FONT_DIR, "PyeojinGothic-Semibold.ttf")))
pdfmetrics.registerFont(TTFont("GothicLight", os.path.join(FONT_DIR, "PyeojinGothic-Light.ttf")))

PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")
ACCENT2 = HexColor("#0f3460")
LIGHT_BG = HexColor("#f5f5f5")
TABLE_HEADER = HexColor("#1a1a2e")
TABLE_ALT = HexColor("#f0f4f8")
BORDER_COLOR = HexColor("#d5dbdb")
BLUE_LIGHT = HexColor("#ebf5fb")

styles = {
    "cover_title": ParagraphStyle("ct", fontName="GothicBold", fontSize=26, textColor=white, alignment=TA_CENTER, leading=36),
    "cover_sub": ParagraphStyle("cs", fontName="Gothic", fontSize=13, textColor=HexColor("#cccccc"), alignment=TA_CENTER, leading=20),
    "section": ParagraphStyle("sec", fontName="GothicBold", fontSize=16, textColor=PRIMARY, spaceBefore=16, spaceAfter=8, leading=24),
    "subsection": ParagraphStyle("sub", fontName="GothicSemibold", fontSize=12, textColor=ACCENT2, spaceBefore=12, spaceAfter=6, leading=18),
    "subsubsection": ParagraphStyle("subsub", fontName="GothicSemibold", fontSize=10, textColor=HexColor("#2c3e50"), spaceBefore=8, spaceAfter=4, leading=15),
    "body": ParagraphStyle("body", fontName="Gothic", fontSize=9, textColor=HexColor("#2c3e50"), leading=14, spaceBefore=2, spaceAfter=3),
    "body_small": ParagraphStyle("bs", fontName="Gothic", fontSize=8, textColor=HexColor("#444444"), leading=12, spaceBefore=1, spaceAfter=1),
    "label": ParagraphStyle("label", fontName="GothicSemibold", fontSize=8.5, textColor=ACCENT, leading=12, spaceBefore=6, spaceAfter=2),
    "copybox": ParagraphStyle("copy", fontName="Gothic", fontSize=8.5, textColor=HexColor("#1a1a1a"), leading=13),
    "th": ParagraphStyle("th", fontName="GothicBold", fontSize=8.5, textColor=white, alignment=TA_CENTER, leading=12),
    "tc": ParagraphStyle("tc", fontName="Gothic", fontSize=8.5, textColor=HexColor("#2c3e50"), leading=12),
    "tcc": ParagraphStyle("tcc", fontName="Gothic", fontSize=8.5, textColor=HexColor("#2c3e50"), alignment=TA_CENTER, leading=12),
    "caption": ParagraphStyle("cap", fontName="GothicLight", fontSize=7, textColor=HexColor("#999999"), alignment=TA_CENTER, spaceBefore=4),
    "highlight": ParagraphStyle("hl", fontName="GothicSemibold", fontSize=9, textColor=ACCENT, leading=14, spaceBefore=4, spaceAfter=4, leftIndent=8),
    "num": ParagraphStyle("num", fontName="GothicBold", fontSize=11, textColor=ACCENT2, spaceBefore=14, spaceAfter=4, leading=16),
}

W = 170 * mm

def copybox(text):
    """Create a copy-paste ready box"""
    p = Paragraph(text.replace("\n", "<br/>"), styles["copybox"])
    t = Table([[p]], colWidths=[W - 6 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t

def highlight_box(text):
    p = Paragraph(text, styles["highlight"])
    t = Table([[p]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE_LIGHT),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEBEFOREDECOR", (0, 0), (0, -1), 3, ACCENT2),
    ]))
    return t

def video_entry(num, old_title, new_title, description, tags):
    """Create a single video SEO entry"""
    elements = []
    elements.append(Paragraph(f"#{num}", styles["num"]))

    # Old title
    elements.append(Paragraph("현재 제목:", styles["label"]))
    elements.append(Paragraph(old_title, styles["body_small"]))

    # New title
    elements.append(Paragraph("변경 제목 (복사용):", styles["label"]))
    elements.append(copybox(new_title))

    # Description
    elements.append(Paragraph("영상 설명 (복사용):", styles["label"]))
    elements.append(copybox(description))

    # Tags
    elements.append(Paragraph("태그 (복사용):", styles["label"]))
    elements.append(copybox(tags))

    elements.append(Spacer(1, 4 * mm))
    return KeepTogether(elements)

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("GothicLight", 7)
    canvas.setFillColor(HexColor("#999999"))
    canvas.drawCentredString(A4[0] / 2, 15 * mm, f"ALL THAT HYMN SEO 최적화 가이드  |  {doc.page}")
    canvas.setStrokeColor(HexColor("#e0e0e0"))
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, A4[1] - 18 * mm, A4[0] - 20 * mm, A4[1] - 18 * mm)
    canvas.restoreState()

def make_desc(hymn_name_kr, hymn_num, hymn_name_en, style_desc, lyrics_note=""):
    """Generate standardized description"""
    base = f'찬송가 {hymn_num}장 "{hymn_name_kr}"을 {style_desc} 편곡하여 연주했습니다.\n\n'
    if lyrics_note:
        base += f'{lyrics_note}\n\n'
    base += f'[가사 전문을 여기에 입력하세요]\n\n'
    base += f'더 많은 찬송가 편곡:\n'
    base += f'- 교회에서 자주 부르는 찬송가 모음 1시간: [PLAYLIST 링크]\n'
    base += f'- 새벽기도 찬송가 PLAYLIST: [PLAYLIST 링크]\n\n'
    base += f'#찬송가 #찬송가{hymn_num}장 #{hymn_name_kr.replace(" ", "")} #{hymn_name_en.replace(" ", "")} #찬송가편곡 #찬송가기타 #찬송가보컬 #예배음악 #hymn #worshipmusic #ALLTHATHYMN'
    return base

def make_tags(hymn_name_kr, hymn_num, hymn_name_en, extras=[]):
    tags = f'찬송가, 찬송가 {hymn_num}장, {hymn_name_kr}, {hymn_name_en}, 찬송가 편곡, 찬송가 기타, 찬송가 보컬, 예배 음악, 찬양, hymn, hymn cover, hymn arrangement, worship music, ALL THAT HYMN'
    if extras:
        tags += ", " + ", ".join(extras)
    return tags

# ===================== VIDEO DATA =====================

videos = [
    # --- 단독 곡 (찬송가 번호순) ---
    {
        "old": "찬송가 1장 | 만복의 근원 하나님 | ALL THAT HYMN",
        "new": "찬송가 1장 만복의 근원 하나님 | 어쿠스틱 편곡 | Praise God from Whom All Blessings Flow",
        "num": "1", "kr": "만복의 근원 하나님", "en": "Praise God from Whom All Blessings Flow",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["만복의 근원", "doxology"],
    },
    {
        "old": "[다시, 찬송가] 새해에도 주님과 함께 | 8 온 천하 만물 우러러",
        "new": "찬송가 8장 온 천하 만물 우러러 | 어쿠스틱 편곡 | All Creatures of Our God and King",
        "num": "8", "kr": "온 천하 만물 우러러", "en": "All Creatures of Our God and King",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["새해 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 20 큰 영광 중에 계신 주",
        "new": "찬송가 20장 큰 영광 중에 계신 주 | 어쿠스틱 편곡 | O Worship the King",
        "num": "20", "kr": "큰 영광 중에 계신 주", "en": "O Worship the King",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["경배 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 21 다 찬양하여라",
        "new": "찬송가 21장 다 찬양하여라 | 어쿠스틱 편곡 | Praise to the Lord the Almighty",
        "num": "21", "kr": "다 찬양하여라", "en": "Praise to the Lord the Almighty",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["찬양 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 27 주 하나님 지으신 모든 세계",
        "new": "찬송가 27장 주 하나님 지으신 모든 세계 | 어쿠스틱 편곡 | How Great Thou Art",
        "num": "27", "kr": "주 하나님 지으신 모든 세계", "en": "How Great Thou Art",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["주하나님지으신모든세계", "how great thou art piano"],
    },
    {
        "old": "[다시, 찬송가] 30 만 입이 내게 있으면",
        "new": "찬송가 30장 만 입이 내게 있으면 | 어쿠스틱 편곡 | O for a Thousand Tongues to Sing",
        "num": "30", "kr": "만 입이 내게 있으면", "en": "O for a Thousand Tongues to Sing",
        "style": "어쿠스틱 기타와 보컬로", "extras": [],
    },
    {
        "old": "[다시, 찬송가] 79 이 세상의 모든 것 주관하시는",
        "new": "찬송가 79장 이 세상의 모든 것 주관하시는 | 어쿠스틱 편곡 | This Is My Father's World",
        "num": "79", "kr": "이 세상의 모든 것 주관하시는", "en": "This Is My Fathers World",
        "style": "어쿠스틱 기타와 보컬로", "extras": [],
    },
    {
        "old": "[성탄 찬송가] 임마누엘, 평강의 왕 | 112 그 맑고 환한 밤중에",
        "new": "찬송가 112장 그 맑고 환한 밤중에 | 성탄 찬송가 편곡 | It Came Upon the Midnight Clear",
        "num": "112", "kr": "그 맑고 환한 밤중에", "en": "It Came Upon the Midnight Clear",
        "style": "성탄 분위기의 어쿠스틱 편곡으로", "extras": ["성탄절 찬송가", "크리스마스 찬송가", "캐롤"],
    },
    {
        "old": "[성탄 찬송가] 115 기쁘다 구주 오셨네",
        "new": "찬송가 115장 기쁘다 구주 오셨네 | 성탄 찬송가 편곡 | Joy to the World",
        "num": "115", "kr": "기쁘다 구주 오셨네", "en": "Joy to the World",
        "style": "성탄 분위기의 어쿠스틱 편곡으로", "extras": ["성탄절 찬송가", "크리스마스 찬송가", "캐롤", "기쁘다구주오셨네"],
    },
    {
        "old": "[성탄 찬송가] 122 고요한 밤 거룩한 밤",
        "new": "찬송가 122장 고요한 밤 거룩한 밤 | 성탄 찬송가 편곡 | Silent Night",
        "num": "122", "kr": "고요한 밤 거룩한 밤", "en": "Silent Night",
        "style": "성탄 분위기의 어쿠스틱 편곡으로", "extras": ["성탄절 찬송가", "크리스마스 찬송가", "캐롤", "고요한밤"],
    },
    {
        "old": "[성탄 찬송가] 126 참 반가운 신도여",
        "new": "찬송가 126장 참 반가운 신도여 | 성탄 찬송가 편곡 | O Come All Ye Faithful",
        "num": "126", "kr": "참 반가운 신도여", "en": "O Come All Ye Faithful",
        "style": "성탄 분위기의 어쿠스틱 편곡으로", "extras": ["성탄절 찬송가", "크리스마스 찬송가", "캐롤"],
    },
    {
        "old": "[다시, 찬송가] 구원주를 향한 외침 | 141 호산나 호산나 | 종려주일 찬양",
        "new": "찬송가 141장 호산나 호산나 | 종려주일 찬양 편곡 | Hosanna",
        "num": "141", "kr": "호산나 호산나", "en": "Hosanna",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["종려주일", "사순절", "고난주간 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 사랑의 완성, 십자가 | 143 웬말인가 날 위하여",
        "new": "찬송가 143장 웬말인가 날 위하여 | 사순절 찬양 편곡 | Alas and Did My Savior Bleed",
        "num": "143", "kr": "웬말인가 날 위하여", "en": "Alas and Did My Savior Bleed",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["사순절 찬송가", "고난주간", "십자가 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 십자가 앞에 선 우리 | 144 내 구주 예수를 더욱 사랑",
        "new": "찬송가 144장 내 구주 예수를 더욱 사랑 | 어쿠스틱 편곡 | More Love to Thee O Christ",
        "num": "144", "kr": "내 구주 예수를 더욱 사랑", "en": "More Love to Thee O Christ",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["사랑 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 149 전능의 하나님",
        "new": "찬송가 149장 전능의 하나님 | 부활절 찬양 편곡 | All Hail the Power of Jesus Name",
        "num": "149", "kr": "전능의 하나님", "en": "All Hail the Power of Jesus Name",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["부활절 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 150 장 주님께 영광",
        "new": "찬송가 150장 주님께 영광 | 부활절 찬양 편곡 | Thine Is the Glory",
        "num": "150", "kr": "주님께 영광", "en": "Thine Is the Glory",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["부활절 찬송가", "부활 찬양"],
    },
    {
        "old": "[다시, 찬송가] 십자가의 은혜 | 152 십자가를 질 수 있나",
        "new": "찬송가 152장 십자가를 질 수 있나 | 사순절 찬양 편곡 | Must Jesus Bear the Cross Alone",
        "num": "152", "kr": "십자가를 질 수 있나", "en": "Must Jesus Bear the Cross Alone",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["사순절 찬송가", "십자가 찬송가", "고난주간"],
    },
    {
        "old": "[다시, 찬송가] 153장 - 십자가의 사랑",
        "new": "찬송가 153장 오 거룩하신 주님 | 사순절 찬양 편곡 | O Sacred Head Now Wounded",
        "num": "153", "kr": "오 거룩하신 주님", "en": "O Sacred Head Now Wounded",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["사순절 찬송가", "십자가 찬송가", "고난주간"],
    },
    {
        "old": "[다시, 찬송가] 213 나의 생명 드리니",
        "new": "찬송가 213장 나의 생명 드리니 | 어쿠스틱 편곡 | I Surrender All",
        "num": "213", "kr": "나의 생명 드리니", "en": "I Surrender All",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["헌신 찬송가", "결단 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 212 겸손히 주를 섬길 때",
        "new": "찬송가 212장 겸손히 주를 섬길 때 | 어쿠스틱 편곡 | Make Me a Servant",
        "num": "212", "kr": "겸손히 주를 섬길 때", "en": "Make Me a Servant",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["섬김 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 구주의 십자가 보혈로 | 250",
        "new": "찬송가 250장 구주의 십자가 보혈로 | 어쿠스틱 편곡 | Are You Washed in the Blood",
        "num": "250", "kr": "구주의 십자가 보혈로", "en": "Are You Washed in the Blood",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["보혈 찬송가", "십자가 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 288 나 주를 멀리 떠났다",
        "new": "찬송가 288장 나 주를 멀리 떠났다 | 어쿠스틱 편곡 | Lord Im Coming Home",
        "num": "288", "kr": "나 주를 멀리 떠났다", "en": "Lord Im Coming Home",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["회개 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 고난 중 우리의 소망 | 338 내 주를 가까이 하게 함은",
        "new": "찬송가 338장 내 주를 가까이 하게 함은 | 어쿠스틱 편곡 | Nearer My God to Thee",
        "num": "338", "kr": "내 주를 가까이 하게 함은", "en": "Nearer My God to Thee",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["묵상 찬송가", "기도 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 소망이 솟는 찬양 | 384 주 예수 내 맘에 들어와",
        "new": "찬송가 384장 주 예수 내 맘에 들어와 | 어쿠스틱 편곡 | Into My Heart",
        "num": "384", "kr": "주 예수 내 맘에 들어와", "en": "Into My Heart",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["소망 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 예수 믿으면 일어나는 일 | 421 내가 예수 믿고서",
        "new": "찬송가 421장 내가 예수 믿고서 | 어쿠스틱 편곡 | Since I Have Been Redeemed",
        "num": "421", "kr": "내가 예수 믿고서", "en": "Since I Have Been Redeemed",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["구원 찬송가", "감사 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 새해에도 주님과 함께 | 435 나의 갈 길 다 가도록",
        "new": "찬송가 435장 나의 갈 길 다 가도록 | 어쿠스틱 편곡 | God Be with You Till We Meet Again",
        "num": "435", "kr": "나의 갈 길 다 가도록", "en": "God Be with You Till We Meet Again",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["축복 찬송가", "송영"],
    },
    {
        "old": "[다시, 찬송가] 거듭난 성도의 고백 | 438 내 주 되신 주를 참 사랑하고",
        "new": "찬송가 438장 내 주 되신 주를 참 사랑하고 | 어쿠스틱 편곡 | My Jesus I Love Thee",
        "num": "438", "kr": "내 주 되신 주를 참 사랑하고", "en": "My Jesus I Love Thee",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["사랑 찬송가", "고백 찬송가"],
    },
    {
        "old": "찬송가 455장 | 주님의 마음을 본받는 자 | ALL THAT HYMN",
        "new": "찬송가 455장 주님의 마음을 본받는 자 | 어쿠스틱 편곡 | O to Be Like Thee",
        "num": "455", "kr": "주님의 마음을 본받는 자", "en": "O to Be Like Thee",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["성화 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 461 나 가나안 땅 귀한 성에",
        "new": "찬송가 461장 나 가나안 땅 귀한 성에 | 어쿠스틱 편곡 | Ill Be Living That Beautiful Life",
        "num": "461", "kr": "나 가나안 땅 귀한 성에", "en": "Ill Be Living That Beautiful Life",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["천국 찬송가", "소망 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 470 나의 사랑하는 책",
        "new": "찬송가 470장 나의 사랑하는 책 | 어쿠스틱 편곡 | Holy Bible Book Divine",
        "num": "470", "kr": "나의 사랑하는 책", "en": "Holy Bible Book Divine",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["성경 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 486 주 하나님 크신 은혜",
        "new": "찬송가 486장 주 하나님 크신 은혜 | 어쿠스틱 편곡 | Grace Greater Than Our Sin",
        "num": "486", "kr": "주 하나님 크신 은혜", "en": "Grace Greater Than Our Sin",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["은혜 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 495 나 이제 주님의 새 생명 얻은 몸",
        "new": "찬송가 495장 나 이제 주님의 새 생명 얻은 몸 | 어쿠스틱 편곡 | Redeemed How I Love to Proclaim It",
        "num": "495", "kr": "나 이제 주님의 새 생명 얻은 몸", "en": "Redeemed How I Love to Proclaim It",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["구원 찬송가"],
    },
    {
        "old": "찬송가 563장 | 예수 사랑하심을 | ALL THAT HYMN",
        "new": "찬송가 563장 예수 사랑하심을 | 어쿠스틱 편곡 | Jesus Loves Me",
        "num": "563", "kr": "예수 사랑하심을", "en": "Jesus Loves Me",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["어린이 찬송가", "예수사랑하심을"],
    },
    {
        "old": "[다시, 찬송가] 찬송가 580장 | 예수는 나의 힘이요",
        "new": "찬송가 580장 예수는 나의 힘이요 | 어쿠스틱 편곡 | Jesus Is My Strength",
        "num": "580", "kr": "예수는 나의 힘이요", "en": "Jesus Is My Strength",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["힘 찬송가", "위로 찬송가"],
    },
    {
        "old": "[다시, 찬송가] 645 아멘",
        "new": "찬송가 645장 아멘 | 어쿠스틱 편곡 | Amen",
        "num": "645", "kr": "아멘", "en": "Amen",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["아멘 송영"],
    },
    # --- 복음성가 ---
    {
        "old": "복음성가 | 주의 자녀로 산다는 것은 | ALL THAT HYMN",
        "new": "주의 자녀로 산다는 것은 | 복음성가 어쿠스틱 편곡 | ALL THAT HYMN",
        "num": "복음성가", "kr": "주의 자녀로 산다는 것은", "en": "Living as Gods Child",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["복음성가", "CCM", "한국 복음성가"],
        "type": "gospel",
    },
    {
        "old": "복음성가 | 꽃들도(花も) | ALL THAT HYMN",
        "new": "꽃들도 (花も) | 복음성가 어쿠스틱 편곡 | ALL THAT HYMN",
        "num": "복음성가", "kr": "꽃들도", "en": "Flowers Also",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["복음성가", "일본 찬양", "CCM"],
        "type": "gospel",
    },
    {
        "old": "축복송 | 잠 못드는 밤에 듣는 축복의 찬양 | ALL THAT HYMN",
        "new": "축복송 | 잠잘 때 듣는 축복의 찬양 | 어쿠스틱 편곡 | ALL THAT HYMN",
        "num": "복음성가", "kr": "축복송", "en": "Blessing Song",
        "style": "어쿠스틱 기타와 보컬로", "extras": ["복음성가", "축복", "수면 찬양", "잠잘 때 듣는 찬양"],
        "type": "gospel",
    },
]

# PLAYLIST data
playlists = [
    {
        "old": "[다시, 찬송가] 1시간 PLAYLIST | 교회에서 자주 부르는 은혜로운 찬송가 모음",
        "new": "교회에서 자주 부르는 찬송가 모음 1시간 | 중간광고없음 | 예배 전 묵상음악 | ALL THAT HYMN",
        "desc": '교회에서 자주 부르는 은혜로운 찬송가를 어쿠스틱 기타와 보컬로 편곡하여 1시간 모음으로 만들었습니다.\n예배 전 묵상, 새벽기도, 개인 큐티 시간에 함께 들어보세요.\n\n00:00 시작\n[타임스탬프를 여기에 입력하세요]\n\n더 많은 찬송가 편곡:\n- 새벽기도 찬송가 PLAYLIST: [링크]\n- 잠잘 때 듣는 찬송가 모음: [링크]\n\n#찬송가 #찬송가모음 #찬송가1시간 #교회찬송가 #예배음악 #중간광고없음 #묵상음악 #찬양모음 #hymn #hymnplaylist #worshipmusic #ALLTHATHYMN',
        "tags": "찬송가, 찬송가 모음, 찬송가 1시간, 교회 찬송가, 교회에서 자주 부르는 찬송가, 예배 음악, 중간광고없음, 묵상 음악, 찬양 모음, 새벽기도 음악, hymn, hymn playlist, hymn medley, worship music, 1 hour hymn, ALL THAT HYMN",
    },
    {
        "old": "[다시, 찬송가] 1시간 PLAYLIST | 기타와 보컬로만 부르는 새벽 감성 찬양 모음",
        "new": "새벽기도 찬송가 모음 1시간 | 기타와 보컬 편곡 | 중간광고없음 | ALL THAT HYMN",
        "desc": '새벽기도 시간에 듣기 좋은 찬송가를 기타와 보컬로만 편곡하여 1시간 모음으로 만들었습니다.\n새벽기도, 묵상, 조용한 예배 시간에 함께 들어보세요.\n\n00:00 시작\n[타임스탬프를 여기에 입력하세요]\n\n#찬송가 #새벽기도음악 #찬송가모음 #중간광고없음 #묵상음악 #기타찬양 #보컬찬양 #새벽찬양 #hymn #morningprayer #worshipmusic #ALLTHATHYMN',
        "tags": "찬송가, 새벽기도 음악, 새벽 찬양, 찬송가 모음, 중간광고없음, 묵상 음악, 기타 찬양, 보컬 찬양, 잔잔한 찬송가, hymn, morning prayer music, acoustic worship, ALL THAT HYMN",
    },
    {
        "old": "[다시, 찬송가] 사순절 찬송가 모음 1시간 PLAYLIST | ALL THAT HYMN",
        "new": "사순절 찬송가 모음 1시간 | 고난주간 찬양 | 중간광고없음 | ALL THAT HYMN",
        "desc": '사순절과 고난주간에 묵상하며 부를 수 있는 찬송가를 어쿠스틱 편곡으로 1시간 모음으로 만들었습니다.\n십자가의 사랑을 묵상하는 시간에 함께 들어보세요.\n\n00:00 시작\n[타임스탬프를 여기에 입력하세요]\n\n#찬송가 #사순절찬송가 #고난주간 #사순절찬양 #중간광고없음 #십자가찬송가 #찬송가모음 #lent #holyweekhymns #worshipmusic #ALLTHATHYMN',
        "tags": "찬송가, 사순절 찬송가, 고난주간, 사순절 찬양, 중간광고없음, 십자가 찬송가, 찬송가 모음, 부활절, lent, holy week hymns, worship music, ALL THAT HYMN",
    },
    {
        "old": "찬양예배 콘티에 꼭 들어가는 CCM PLAYLIST (1시간)",
        "new": "찬양예배 콘티 CCM 모음 1시간 | 중간광고없음 | 예배팀 추천 | ALL THAT HYMN",
        "desc": '찬양예배 콘티에 꼭 들어가는 인기 CCM을 어쿠스틱 편곡으로 1시간 모음으로 만들었습니다.\n예배 준비, 기도 모임, 소그룹 모임에서 활용하세요.\n\n00:00 시작\n[타임스탬프를 여기에 입력하세요]\n\n#CCM #찬양예배 #예배콘티 #CCM모음 #중간광고없음 #찬양모음 #예배팀 #worshipplaylist #ccmplaylist #ALLTHATHYMN',
        "tags": "CCM, 찬양예배, 예배 콘티, CCM 모음, 중간광고없음, 찬양 모음, 예배팀, 예배 음악, worship playlist, ccm playlist, ALL THAT HYMN",
    },
    {
        "old": "PLAYLIST | 고난과 부활, 그리고 우리 (1시간)",
        "new": "고난과 부활 찬송가 모음 1시간 | 중간광고없음 | 부활절 찬양 | ALL THAT HYMN",
        "desc": '고난과 부활의 의미를 묵상할 수 있는 찬송가를 1시간 모음으로 만들었습니다.\n사순절부터 부활절까지, 십자가와 부활의 은혜를 함께 나누는 시간입니다.\n\n00:00 시작\n[타임스탬프를 여기에 입력하세요]\n\n#찬송가 #고난주간 #부활절 #부활절찬송가 #중간광고없음 #사순절 #찬송가모음 #easter #easterhymns #worshipmusic #ALLTHATHYMN',
        "tags": "찬송가, 고난주간, 부활절, 부활절 찬송가, 중간광고없음, 사순절, 찬송가 모음, 십자가, easter, easter hymns, worship music, ALL THAT HYMN",
    },
    {
        "old": "[성탄 찬송가] PLAYLIST | 성탄 찬송가 모음",
        "new": "성탄절 찬송가 모음 1시간 | 크리스마스 캐롤 | 중간광고없음 | ALL THAT HYMN",
        "desc": '성탄절에 부르는 아름다운 찬송가와 캐롤을 어쿠스틱 편곡으로 1시간 모음으로 만들었습니다.\n성탄 예배, 가정 예배, 크리스마스 파티에서 함께 들어보세요.\n\n00:00 시작\n[타임스탬프를 여기에 입력하세요]\n\n#찬송가 #성탄절찬송가 #크리스마스캐롤 #성탄절찬양 #중간광고없음 #크리스마스음악 #찬송가모음 #christmas #christmascarol #christmashymn #ALLTHATHYMN',
        "tags": "찬송가, 성탄절 찬송가, 크리스마스 캐롤, 성탄절 찬양, 중간광고없음, 크리스마스 음악, 찬송가 모음, christmas, christmas carol, christmas hymn, ALL THAT HYMN",
    },
]

# Shorts titles
shorts_data = [
    ("1장 만복의 근원 하나님", "찬송가 1장 만복의 근원 하나님 | 어쿠스틱 편곡 #shorts #찬송가 #hymn"),
    ("8장 온 천하 만물 우러러", "찬송가 8장 온 천하 만물 우러러 | 어쿠스틱 편곡 #shorts #찬송가 #hymn"),
    ("20장 큰 영광 중에 계신 주", "찬송가 20장 큰 영광 중에 계신 주 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("21장 다 찬양하여라", "찬송가 21장 다 찬양하여라 | 어쿠스틱 편곡 #shorts #찬송가 #hymn"),
    ("27장 주 하나님 지으신 모든 세계", "찬송가 27장 주 하나님 지으신 모든 세계 | How Great Thou Art #shorts #찬송가"),
    ("30장 만 입이 내게 있으면", "찬송가 30장 만 입이 내게 있으면 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("79장 이 세상의 모든 것", "찬송가 79장 이 세상의 모든 것 주관하시는 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("112장 그 맑고 환한 밤중에", "찬송가 112장 그 맑고 환한 밤중에 | 성탄 찬송가 #shorts #찬송가 #christmas"),
    ("115장 기쁘다 구주 오셨네", "찬송가 115장 기쁘다 구주 오셨네 | Joy to the World #shorts #찬송가 #christmas"),
    ("122장 고요한 밤 거룩한 밤", "찬송가 122장 고요한 밤 거룩한 밤 | Silent Night #shorts #찬송가 #christmas"),
    ("126장 참 반가운 신도여", "찬송가 126장 참 반가운 신도여 | 성탄 찬송가 #shorts #찬송가 #christmas"),
    ("141장 호산나 호산나", "찬송가 141장 호산나 호산나 | 종려주일 찬양 #shorts #찬송가 #사순절"),
    ("143장 웬말인가 날 위하여", "찬송가 143장 웬말인가 날 위하여 | 사순절 찬양 #shorts #찬송가 #사순절"),
    ("144장 내 구주 예수를 더욱 사랑", "찬송가 144장 내 구주 예수를 더욱 사랑 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("149장 전능의 하나님", "찬송가 149장 전능의 하나님 | 부활절 찬양 #shorts #찬송가 #부활절"),
    ("150장 주님께 영광", "찬송가 150장 주님께 영광 | 부활절 찬양 #shorts #찬송가 #부활절"),
    ("152장 십자가를 질 수 있나", "찬송가 152장 십자가를 질 수 있나 | 사순절 찬양 #shorts #찬송가 #사순절"),
    ("153장 오 거룩하신 주님", "찬송가 153장 오 거룩하신 주님 | 사순절 찬양 #shorts #찬송가 #사순절"),
    ("213장 나의 생명 드리니", "찬송가 213장 나의 생명 드리니 | 어쿠스틱 편곡 #shorts #찬송가 #hymn"),
    ("212장 겸손히 주를 섬길 때", "찬송가 212장 겸손히 주를 섬길 때 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("250장 구주의 십자가 보혈로", "찬송가 250장 구주의 십자가 보혈로 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("288장 나 주를 멀리 떠났다", "찬송가 288장 나 주를 멀리 떠났다 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("338장 내 주를 가까이", "찬송가 338장 내 주를 가까이 하게 함은 | Nearer My God to Thee #shorts #찬송가"),
    ("384장 주 예수 내 맘에", "찬송가 384장 주 예수 내 맘에 들어와 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("421장 내가 예수 믿고서", "찬송가 421장 내가 예수 믿고서 | 어쿠스틱 편곡 #shorts #찬송가 #hymn"),
    ("435장 나의 갈 길 다 가도록", "찬송가 435장 나의 갈 길 다 가도록 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("438장 내 주 되신 주를", "찬송가 438장 내 주 되신 주를 참 사랑하고 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("455장 주님의 마음을 본받는 자", "찬송가 455장 주님의 마음을 본받는 자 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("461장 나 가나안 땅 귀한 성에", "찬송가 461장 나 가나안 땅 귀한 성에 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("470장 나의 사랑하는 책", "찬송가 470장 나의 사랑하는 책 | 어쿠스틱 편곡 #shorts #찬송가 #hymn"),
    ("486장 주 하나님 크신 은혜", "찬송가 486장 주 하나님 크신 은혜 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("495장 나 이제 주님의 새 생명", "찬송가 495장 나 이제 주님의 새 생명 얻은 몸 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("563장 예수 사랑하심을", "찬송가 563장 예수 사랑하심을 | Jesus Loves Me #shorts #찬송가 #hymn"),
    ("580장 예수는 나의 힘이요", "찬송가 580장 예수는 나의 힘이요 | 어쿠스틱 편곡 #shorts #찬송가"),
    ("645장 아멘", "찬송가 645장 아멘 | 어쿠스틱 편곡 #shorts #찬송가 #hymn"),
    ("주의 자녀로 산다는 것은", "주의 자녀로 산다는 것은 | 복음성가 어쿠스틱 편곡 #shorts #복음성가 #찬양"),
    ("꽃들도 花も", "꽃들도 (花も) | 복음성가 어쿠스틱 편곡 #shorts #복음성가 #찬양"),
    ("축복송", "축복송 | 잠잘 때 듣는 축복의 찬양 #shorts #찬양 #복음성가"),
    ("부활의 기쁨", "부활의 기쁨을 선포합니다 | 부활절 찬양 #shorts #찬송가 #부활절"),
    ("고난주간 추천 찬양", "고난주간에 듣기 좋은 찬송가 추천 #shorts #찬송가 #사순절 #고난주간"),
]

def build_guide():
    output_path = "/Users/dawonder/allthathynm/ALL_THAT_HYMN_SEO_복사붙여넣기_가이드.pdf"
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=25 * mm, bottomMargin=25 * mm,
    )
    story = []

    # Cover
    story.append(Spacer(1, 35 * mm))
    cover_items = [
        Spacer(1, 18 * mm),
        Paragraph("ALL THAT HYMN", styles["cover_title"]),
        Spacer(1, 4 * mm),
        Paragraph("SEO 최적화 복사-붙여넣기 가이드", ParagraphStyle("cs2", fontName="GothicSemibold", fontSize=18, textColor=ACCENT, alignment=TA_CENTER, leading=26)),
        Spacer(1, 10 * mm),
        Paragraph("모든 영상의 제목, 설명, 태그를 그대로 복사하여 사용하세요", styles["cover_sub"]),
        Spacer(1, 4 * mm),
        Paragraph("2026년 3월", styles["cover_sub"]),
    ]
    inner = Table([[c] for c in cover_items], colWidths=[W - 10 * mm])
    cover = Table([[inner]], colWidths=[W], rowHeights=[110 * mm])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
    ]))
    story.append(cover)
    story.append(PageBreak())

    # ===== PART 1: 단독 곡 + 복음성가 =====
    story.append(Paragraph("Part 1: 단독 곡 영상 - 제목/설명/태그 변경 가이드", styles["section"]))
    story.append(highlight_box("아래의 내용을 YouTube Studio에서 각 영상의 제목, 설명, 태그에 그대로 복사-붙여넣기 하세요."))
    story.append(Spacer(1, 4 * mm))

    for i, v in enumerate(videos, 1):
        is_gospel = v.get("type") == "gospel"

        if is_gospel:
            desc = f'{v["kr"]}을 {v["style"]} 편곡하여 연주했습니다.\n\n[가사 전문을 여기에 입력하세요]\n\n더 많은 찬송가 편곡:\n- 교회에서 자주 부르는 찬송가 모음 1시간: [PLAYLIST 링크]\n- 새벽기도 찬송가 PLAYLIST: [PLAYLIST 링크]\n\n#{v["kr"].replace(" ", "")} #복음성가 #CCM #찬양 #어쿠스틱편곡 #worshipmusic #ALLTHATHYMN'
            tags = f'{v["kr"]}, 복음성가, CCM, 찬양, 어쿠스틱 편곡, worship music, ALL THAT HYMN'
            if v["extras"]:
                tags += ", " + ", ".join(v["extras"])
        else:
            desc = make_desc(v["kr"], v["num"], v["en"], v["style"])
            tags = make_tags(v["kr"], v["num"], v["en"], v["extras"])

        story.append(video_entry(i, v["old"], v["new"], desc, tags))

    story.append(PageBreak())

    # ===== PART 2: PLAYLIST =====
    story.append(Paragraph("Part 2: PLAYLIST 영상 - 제목/설명/태그 변경 가이드", styles["section"]))
    story.append(highlight_box("PLAYLIST 영상은 채널 성장의 핵심 엔진입니다. 반드시 '중간광고없음' 키워드를 포함하세요."))
    story.append(Spacer(1, 4 * mm))

    for i, pl in enumerate(playlists, 1):
        elements = []
        elements.append(Paragraph(f"PLAYLIST #{i}", styles["num"]))
        elements.append(Paragraph("현재 제목:", styles["label"]))
        elements.append(Paragraph(pl["old"], styles["body_small"]))
        elements.append(Paragraph("변경 제목 (복사용):", styles["label"]))
        elements.append(copybox(pl["new"]))
        elements.append(Paragraph("영상 설명 (복사용):", styles["label"]))
        elements.append(copybox(pl["desc"]))
        elements.append(Paragraph("태그 (복사용):", styles["label"]))
        elements.append(copybox(pl["tags"]))
        elements.append(Spacer(1, 6 * mm))
        story.append(KeepTogether(elements))

    story.append(PageBreak())

    # ===== PART 3: SHORTS =====
    story.append(Paragraph("Part 3: Shorts 영상 - 제목 변경 가이드", styles["section"]))
    story.append(highlight_box("현재 모든 Shorts의 제목이 동일합니다. 아래 제목으로 각각 변경하세요. 해당 곡의 Shorts를 찾아 제목만 변경하면 됩니다."))
    story.append(Spacer(1, 4 * mm))

    # Make a table for shorts
    shorts_header = [
        Paragraph("곡명", styles["th"]),
        Paragraph("변경할 Shorts 제목 (복사용)", styles["th"]),
    ]
    shorts_rows = [shorts_header]
    for song, title in shorts_data:
        shorts_rows.append([
            Paragraph(song, styles["tc"]),
            Paragraph(title, styles["tc"]),
        ])

    shorts_table = Table(shorts_rows, colWidths=[W * 0.32, W * 0.68], repeatRows=1)
    st_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(2, len(shorts_rows), 2):
        st_cmds.append(("BACKGROUND", (0, i), (-1, i), TABLE_ALT))
    shorts_table.setStyle(TableStyle(st_cmds))
    story.append(shorts_table)

    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("본 가이드는 2026년 3월 22일 기준으로 작성되었습니다.", styles["caption"]))

    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=add_page_number)
    print(f"SEO 가이드 PDF 생성 완료: {output_path}")

if __name__ == "__main__":
    build_guide()
