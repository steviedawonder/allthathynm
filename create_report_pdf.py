#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ALL THAT HYMN 채널 성장 전략 보고서 PDF 생성"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# --- Font Registration ---
FONT_DIR = os.path.expanduser("~/Library/Fonts")
pdfmetrics.registerFont(TTFont("Gothic", os.path.join(FONT_DIR, "PyeojinGothic-Regular.ttf")))
pdfmetrics.registerFont(TTFont("GothicBold", os.path.join(FONT_DIR, "PyeojinGothic-Bold.ttf")))
pdfmetrics.registerFont(TTFont("GothicSemibold", os.path.join(FONT_DIR, "PyeojinGothic-Semibold.ttf")))
pdfmetrics.registerFont(TTFont("GothicLight", os.path.join(FONT_DIR, "PyeojinGothic-Light.ttf")))

# --- Colors ---
PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")
ACCENT2 = HexColor("#0f3460")
LIGHT_BG = HexColor("#f5f5f5")
TABLE_HEADER = HexColor("#1a1a2e")
TABLE_ALT = HexColor("#f0f4f8")
SUCCESS = HexColor("#27ae60")
WARNING = HexColor("#e67e22")
DANGER = HexColor("#e74c3c")
BLUE_LIGHT = HexColor("#ebf5fb")
BORDER_COLOR = HexColor("#d5dbdb")

# --- Styles ---
styles = {
    "cover_title": ParagraphStyle("cover_title", fontName="GothicBold", fontSize=28, textColor=white, alignment=TA_CENTER, leading=38),
    "cover_sub": ParagraphStyle("cover_sub", fontName="Gothic", fontSize=14, textColor=HexColor("#cccccc"), alignment=TA_CENTER, leading=20),
    "section_title": ParagraphStyle("section_title", fontName="GothicBold", fontSize=18, textColor=PRIMARY, spaceBefore=20, spaceAfter=10, leading=26, borderPadding=(0, 0, 4, 0)),
    "subsection": ParagraphStyle("subsection", fontName="GothicSemibold", fontSize=14, textColor=ACCENT2, spaceBefore=14, spaceAfter=8, leading=20),
    "subsubsection": ParagraphStyle("subsubsection", fontName="GothicSemibold", fontSize=11, textColor=HexColor("#2c3e50"), spaceBefore=10, spaceAfter=6, leading=16),
    "body": ParagraphStyle("body", fontName="Gothic", fontSize=9.5, textColor=HexColor("#2c3e50"), leading=16, spaceBefore=2, spaceAfter=4),
    "body_bold": ParagraphStyle("body_bold", fontName="GothicBold", fontSize=9.5, textColor=HexColor("#2c3e50"), leading=16, spaceBefore=2, spaceAfter=4),
    "bullet": ParagraphStyle("bullet", fontName="Gothic", fontSize=9.5, textColor=HexColor("#2c3e50"), leading=16, leftIndent=16, bulletIndent=6, spaceBefore=1, spaceAfter=1),
    "bullet2": ParagraphStyle("bullet2", fontName="Gothic", fontSize=9, textColor=HexColor("#555555"), leading=14, leftIndent=30, bulletIndent=18, spaceBefore=1, spaceAfter=1),
    "caption": ParagraphStyle("caption", fontName="GothicLight", fontSize=8, textColor=HexColor("#888888"), alignment=TA_CENTER, spaceBefore=4, spaceAfter=8),
    "table_header": ParagraphStyle("th", fontName="GothicBold", fontSize=9, textColor=white, alignment=TA_CENTER, leading=13),
    "table_cell": ParagraphStyle("tc", fontName="Gothic", fontSize=9, textColor=HexColor("#2c3e50"), leading=13),
    "table_cell_center": ParagraphStyle("tcc", fontName="Gothic", fontSize=9, textColor=HexColor("#2c3e50"), alignment=TA_CENTER, leading=13),
    "highlight_box": ParagraphStyle("highlight", fontName="GothicSemibold", fontSize=10, textColor=ACCENT, leading=16, spaceBefore=6, spaceAfter=6, leftIndent=10),
    "toc_item": ParagraphStyle("toc", fontName="Gothic", fontSize=11, textColor=ACCENT2, leading=20, spaceBefore=4),
    "footer": ParagraphStyle("footer", fontName="GothicLight", fontSize=7, textColor=HexColor("#999999"), alignment=TA_CENTER),
    "page_header": ParagraphStyle("page_header", fontName="GothicLight", fontSize=8, textColor=HexColor("#aaaaaa"), alignment=TA_RIGHT),
}

def make_table(headers, rows, col_widths=None, full_width=True):
    """Create a styled table"""
    w = 170 * mm if full_width else None
    header_cells = [Paragraph(h, styles["table_header"]) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(str(c), styles["table_cell_center"] if i > 0 and len(str(c)) < 30 else styles["table_cell"]) for i, c in enumerate(row)])

    if col_widths:
        t = Table(data, colWidths=col_widths, repeatRows=1)
    elif full_width:
        n = len(headers)
        t = Table(data, colWidths=[w / n] * n, repeatRows=1)
    else:
        t = Table(data, repeatRows=1)

    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), TABLE_ALT))
    t.setStyle(TableStyle(style_cmds))
    return t

def make_highlight_box(text, bg_color=BLUE_LIGHT, border_color=ACCENT2):
    """Create a highlighted info box"""
    p = Paragraph(text, styles["highlight_box"])
    t = Table([[p]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LINEBEFOREDECOR", (0, 0), (0, -1), 3, border_color),
    ]))
    return t

def make_number_badge(number, label, color=ACCENT):
    """Create a number stat badge"""
    n = Paragraph(f'<font color="{color.hexval()}">{number}</font>', ParagraphStyle("n", fontName="GothicBold", fontSize=20, alignment=TA_CENTER, leading=26))
    l = Paragraph(label, ParagraphStyle("l", fontName="Gothic", fontSize=8, alignment=TA_CENTER, textColor=HexColor("#666666"), leading=12))
    return [n, l]

def add_page_number(canvas, doc):
    """Add page number and header to each page"""
    canvas.saveState()
    canvas.setFont("GothicLight", 7)
    canvas.setFillColor(HexColor("#999999"))
    canvas.drawCentredString(A4[0] / 2, 15 * mm, f"ALL THAT HYMN 성장 전략 보고서  |  {doc.page}")
    # Top line
    canvas.setStrokeColor(HexColor("#e0e0e0"))
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, A4[1] - 18 * mm, A4[0] - 20 * mm, A4[1] - 18 * mm)
    canvas.restoreState()

def build_report():
    output_path = "/Users/dawonder/allthathynm/ALL_THAT_HYMN_성장전략_보고서.pdf"
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=25 * mm, bottomMargin=25 * mm,
    )
    story = []
    W = 170 * mm  # usable width

    # ========== COVER PAGE ==========
    story.append(Spacer(1, 30 * mm))
    cover_bg = Table([[""]], colWidths=[W], rowHeights=[120 * mm])
    cover_bg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    # Build cover content
    cover_content = []
    cover_content.append(Spacer(1, 20 * mm))
    cover_content.append(Paragraph("ALL THAT HYMN", styles["cover_title"]))
    cover_content.append(Spacer(1, 4 * mm))
    cover_content.append(Paragraph("채널 성장 전략 보고서", ParagraphStyle("cs2", fontName="GothicSemibold", fontSize=20, textColor=ACCENT, alignment=TA_CENTER, leading=28)))
    cover_content.append(Spacer(1, 12 * mm))
    cover_content.append(Paragraph("@ALLTHATHYMN645", styles["cover_sub"]))
    cover_content.append(Spacer(1, 4 * mm))
    cover_content.append(Paragraph("2026년 3월", styles["cover_sub"]))

    inner = Table([[c] for c in cover_content], colWidths=[W - 10 * mm])
    inner.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))

    cover = Table([[inner]], colWidths=[W], rowHeights=[120 * mm])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
    ]))
    story.append(cover)
    story.append(Spacer(1, 15 * mm))
    story.append(Paragraph("본 보고서는 ALL THAT HYMN 유튜브 채널의 현황 분석과 성장 전략을 담고 있습니다.\n유튜브 SEO 최적화, 콘텐츠 전략, 수익 다각화 방안을 포함합니다.", ParagraphStyle("intro", fontName="Gothic", fontSize=10, textColor=HexColor("#666666"), alignment=TA_CENTER, leading=18)))

    story.append(PageBreak())

    # ========== TABLE OF CONTENTS ==========
    story.append(Paragraph("목차", styles["section_title"]))
    story.append(Spacer(1, 4 * mm))
    toc_items = [
        "1. 채널 현황 분석",
        "2. 현재 채널이 개선해야 할 점",
        "3. 제목 SEO 전면 재설계",
        "4. PLAYLIST 핵심 성장 엔진 전략",
        "5. Shorts 전략 전면 재설계",
        "6. 썸네일 리디자인",
        "7. 영상 설명(Description) 최적화",
        "8. 업로드 스케줄 최적화",
        "9. 수익 다각화 전략",
        "10. 커뮤니티 & 외부 채널 연계",
        "11. 실행 우선순위 요약",
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles["toc_item"]))
    story.append(PageBreak())

    # ========== 1. 채널 현황 ==========
    story.append(Paragraph("1. 채널 현황 분석", styles["section_title"]))

    # Stats badges
    stats = [
        make_number_badge("3,190", "구독자", ACCENT),
        make_number_badge("258,498", "총 조회수", ACCENT2),
        make_number_badge("109", "영상 수", SUCCESS),
        make_number_badge("14개월", "운영 기간", WARNING),
    ]
    stat_cells = []
    for s in stats:
        inner_t = Table([[s[0]], [s[1]]], colWidths=[W / 4 - 4 * mm])
        inner_t.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
            ("TOPPADDING", (0, 0), (0, 0), 8),
            ("BOTTOMPADDING", (0, -1), (0, -1), 8),
        ]))
        stat_cells.append(inner_t)

    stats_table = Table([stat_cells], colWidths=[W / 4] * 4)
    stats_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 6 * mm))

    story.append(Paragraph("콘텐츠 포맷별 성과", styles["subsection"]))
    story.append(make_table(
        ["포맷", "영상 수", "평균 조회수", "성과 등급"],
        [
            ["1시간 PLAYLIST 모음", "약 7개", "5,000~45,000", "최상"],
            ["복음성가", "약 5개", "772~5,500", "상"],
            ["[다시, 찬송가] 단독 곡", "약 40개", "300~2,500", "중"],
            ["찬송가 OO장 (초기)", "약 15개", "450~4,500", "중"],
            ["[반주MR]", "약 3개", "124~182", "최하"],
            ["Shorts", "약 20개", "147~7,400", "하~중"],
        ],
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(make_highlight_box("핵심 인사이트: PLAYLIST 영상이 개별 곡 대비 10~30배 높은 조회수를 기록하고 있으나, 전체 109개 영상 중 PLAYLIST는 7개에 불과합니다. 성장 엔진을 충분히 활용하지 못하고 있습니다."))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("채널 강점", styles["subsection"]))
    strengths = [
        "한국 찬송가 편곡 전문 채널 중 구독자 기준 압도적 1위 (경쟁 채널 대비 6~160배)",
        "보컬+기타+피아노 밴드 편성, 4K 영상, 전문적 녹음의 높은 제작 퀄리티",
        "좋아요율 1.5~2.9%로 유튜브 평균 이상의 높은 인게이지먼트",
        "댓글에서 반복 등장하는 충성 시청자들의 진성 팬층 형성 중",
        '"1장부터 645장까지" 완주라는 명확하고 고유한 미션',
    ]
    for s in strengths:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {s}", styles["bullet"]))
    story.append(PageBreak())

    # ========== 2. 개선해야 할 점 ==========
    story.append(Paragraph("2. 현재 채널이 개선해야 할 점", styles["section_title"]))

    problems = [
        ("Shorts 제목이 전부 동일 (가장 심각)",
         "모든 Shorts의 제목이 동일하게 설정되어 있습니다. 유튜브 알고리즘이 개별 Shorts를 구분하지 못하고, 검색에 전혀 노출되지 않으며, 시청자가 어떤 곡인지 알 수 없어 클릭 동기가 없습니다. Shorts 조회의 74%가 비구독자에게서 발생하는데, 이 발견 경로를 완전히 낭비하고 있습니다."),
        ("제목 SEO가 심각하게 부족",
         '현재 제목의 감성적 서브타이틀("구원주를 향한 외침" 등)은 아무도 검색하지 않는 문구입니다. 사람들이 실제로 검색하는 키워드("찬송가 피아노", "새벽기도 음악", "수면 찬송가" 등)가 제목에 포함되어 있지 않습니다.'),
        ("반주MR 시리즈 저성과",
         "조회수 124~182회로 채널 평균의 1/10 수준입니다. 이 분야는 이미 전문 반주 채널이 포화 상태이고, 올댓힘의 강점(보컬+밴드 편곡)과도 맞지 않습니다."),
        ("PLAYLIST를 너무 적게 만들고 있음",
         "109개 영상 중 PLAYLIST는 7개뿐인데, 이 7개가 전체 조회수의 대부분을 차지합니다. 성장의 핵심 엔진을 가동하지 않고 있는 셈입니다."),
        ("썸네일 차별화 부족",
         "비슷한 톤의 연주 현장 사진이 반복되어 영상 간 구분이 어렵고, 텍스트가 작아 모바일(유튜브 시청의 70%)에서 읽기 어렵습니다."),
        ("외부 유입 경로 전무",
         "인스타그램/틱톡 계정 연계 없음, 네이버 블로그/카페 노출 없음, 웹 검색에서 채널이 거의 발견되지 않습니다."),
    ]
    for i, (title, desc) in enumerate(problems, 1):
        story.append(Paragraph(f"{i}. {title}", styles["subsubsection"]))
        story.append(Paragraph(desc, styles["body"]))
        story.append(Spacer(1, 2 * mm))

    story.append(PageBreak())

    # ========== 3. 제목 SEO ==========
    story.append(Paragraph("3. 제목 SEO 전면 재설계", styles["section_title"]))

    story.append(Paragraph("권장 제목 공식", styles["subsection"]))
    story.append(make_highlight_box("찬송가 {번호}장 {제목} | {스타일/악기} 편곡 | {영어 제목}"))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph("제목 변경 구체적 예시", styles["subsection"]))
    story.append(make_table(
        ["현재 제목", "개선안"],
        [
            ["[다시, 찬송가] 구원주를 향한 외침 |\n141 호산나 호산나", "찬송가 141장 호산나 호산나 |\n어쿠스틱 기타 편곡 | Hosanna"],
            ["[다시, 찬송가] 고난 중 우리의 소망 |\n338 내 주를 가까이 하게 함은", "찬송가 338장 내 주를 가까이 하게 함은 |\n보컬 편곡 | Nearer My God to Thee"],
            ["[다시, 찬송가] 1시간 PLAYLIST\n교회에서 자주 부르는...", "교회에서 자주 부르는 찬송가 모음 1시간 |\n중간광고없음 | 예배 전 묵상음악"],
        ],
        col_widths=[W * 0.48, W * 0.52],
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("활용해야 할 고검색량 키워드", styles["subsection"]))
    kw_table = make_table(
        ["카테고리", "한국어 키워드", "영어 키워드"],
        [
            ["기본", "찬송가, 찬송가 피아노, 찬송가 편곡,\n찬송가 기타", "hymn, hymn cover,\nhymn arrangement"],
            ["용도별", "새벽기도 음악, 수면 찬송가,\n잠잘 때 듣는 찬송가, 예배 반주", "worship piano, prayer music,\nrelaxing hymns for sleep"],
            ["스타일별", "찬송가 재즈, 찬송가 어쿠스틱,\n카페에서 듣기 좋은 찬송가", "jazz hymn, acoustic hymn,\nhymn instrumental"],
            ["실용", "중간광고없음, 가사포함,\n찬송가 모음, 찬양 모음", "hymn medley, hymn playlist,\nhymn piano 1 hour"],
        ],
        col_widths=[W * 0.18, W * 0.41, W * 0.41],
    )
    story.append(kw_table)
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("핵심 원칙", styles["subsubsection"]))
    principles = [
        "검색 키워드를 제목 앞부분에 배치 (유튜브는 앞부분에 가중치 부여)",
        '"찬송가 OOO장"을 반드시 포함 (번호로 검색하는 사람 많음)',
        "영어 곡명을 뒤에 병기 (글로벌 노출)",
        'PLAYLIST에는 "중간광고없음" 반드시 포함 (검색량 매우 높음)',
        "기존 109개 영상의 제목도 전부 수정 (유튜브는 제목 변경 후 재색인)",
    ]
    for p in principles:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {p}", styles["bullet"]))
    story.append(PageBreak())

    # ========== 4. PLAYLIST 전략 ==========
    story.append(Paragraph("4. PLAYLIST 핵심 성장 엔진 전략", styles["section_title"]))

    story.append(make_highlight_box("월 2회 이상 PLAYLIST 제작을 권장합니다. PLAYLIST가 채널 전체 조회수의 핵심 성장 엔진입니다."))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("제작할 PLAYLIST 목록 (검색량 기반 우선순위)", styles["subsection"]))
    story.append(make_table(
        ["주제", "예상 검색 수요", "참고 사항"],
        [
            ["잠잘 때 듣는 찬송가 3시간", "매우 높음", "김선생TV 유사 영상 61만 조회 달성"],
            ["새벽기도 배경음악 찬송가 2시간", "매우 높음", "새벽 4-5시 자동재생 수요"],
            ["카페에서 듣기 좋은 찬송가 1시간", "높음", "재즈/보사노바 편곡"],
            ["교회에서 자주 부르는 찬송가 TOP 30", "높음", "이미 4.5만회 달성한 검증된 포맷"],
            ["결혼식 찬송가 모음 1시간", "중간", "지속적 시즌 수요"],
            ["장례식/추모 찬송가 모음", "중간", "지속적 검색 수요"],
            ["부활절 찬송가 모음 2시간", "높음 (시즌)", "매년 반복 수요"],
            ["성탄절 찬송가 모음 3시간", "매우 높음 (시즌)", "12월 폭발적 검색"],
            ["어린이 찬송가 모음 1시간", "중간", "주일학교 수요"],
            ["공부할 때 듣는 찬송가 피아노 2시간", "높음", "학생 대상"],
        ],
        col_widths=[W * 0.40, W * 0.22, W * 0.38],
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("제작 팁", styles["subsubsection"]))
    tips = [
        "기존 단독 곡 영상들을 편집하여 모음집으로 재구성하면 제작 비용 최소화",
        "곡 사이에 2-3초 자연스러운 전환 삽입",
        "영상 설명에 타임스탬프 필수 (챕터 기능 활성화)",
        '"중간광고없음"을 제목과 썸네일에 명시',
    ]
    for t in tips:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {t}", styles["bullet"]))
    story.append(PageBreak())

    # ========== 5. Shorts 전략 ==========
    story.append(Paragraph("5. Shorts 전략 전면 재설계", styles["section_title"]))

    story.append(Paragraph("Shorts가 중요한 이유", styles["subsection"]))
    shorts_stats = [
        "Shorts 조회의 74%가 비구독자에게서 발생 - 최고의 채널 발견 도구",
        "Shorts + 장편 영상을 병행하는 채널이 41% 더 빠르게 성장",
        "Shorts 추천 엔진이 장편 추천과 완전 분리 - 부정적 영향 없음",
    ]
    for s in shorts_stats:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {s}", styles["bullet"]))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("주 3-5개 업로드, 각각 고유한 콘텐츠로", styles["subsection"]))
    story.append(make_table(
        ["유형", "예시", "기대 효과"],
        [
            ["편곡 하이라이트", "가장 감동적인 30초 클립", "본편 유입 유도"],
            ["비포/애프터", "원곡 vs 편곡 비교", "호기심 유발"],
            ['"이 찬송가 뭔지 아시나요?"', "멜로디만 들려주고 맞추기", "참여 유도"],
            ["연주 비하인드", "녹음/편곡 과정", "진정성 강화"],
            ["찬송가 가사 묵상", "가사 한 구절 + 연주", "감성적 공유"],
        ],
        col_widths=[W * 0.30, W * 0.38, W * 0.32],
    ))
    story.append(Spacer(1, 6 * mm))

    # ========== 6. 썸네일 ==========
    story.append(Paragraph("6. 썸네일 리디자인", styles["section_title"]))
    story.append(make_table(
        ["포맷", "권장 썸네일 스타일"],
        [
            ["PLAYLIST", '풍경/무드 배경 + 큰 텍스트 ("찬송가 30곡 모음") + 재생 시간 표시'],
            ["단독 곡", "연주자 얼굴 클로즈업 + 찬송가 번호 크게 + 한줄 가사"],
            ["Shorts", "밝은 색상 + 큰 텍스트 + 물음표/느낌표"],
        ],
        col_widths=[W * 0.22, W * 0.78],
    ))
    story.append(Spacer(1, 4 * mm))

    thumb_tips = [
        "텍스트는 모바일에서도 읽을 수 있을 만큼 크게",
        "고대비 색상 사용 (밝은 노란/주황 + 어두운 배경) - CTR 20-30% 향상",
        "감정이 담긴 얼굴이 보이는 썸네일 - CTR 20-30% 향상",
        'YouTube Studio의 "Test & Compare" 기능으로 A/B 테스트 (평균 CTR 20% 향상)',
        "PLAYLIST와 단독 곡의 썸네일 스타일을 명확히 구분",
    ]
    for t in thumb_tips:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {t}", styles["bullet"]))
    story.append(PageBreak())

    # ========== 7. 영상 설명 ==========
    story.append(Paragraph("7. 영상 설명(Description) 최적화", styles["section_title"]))

    story.append(Paragraph("권장 설명 템플릿", styles["subsection"]))
    desc_template = """찬송가 338장 "내 주를 가까이 하게 함은"을 어쿠스틱 기타와 보컬로 편곡하여 연주했습니다.

이 찬송가는 1856년 사라 애덤스가 작사한 곡으로... (곡에 대한 2-3줄 소개)

[가사 전문 포함 - 검색 노출에 매우 효과적]

더 많은 찬송가 편곡:
- 교회에서 자주 부르는 찬송가 모음: [링크]
- 새벽기도 찬송가 PLAYLIST: [링크]

악보 구매: [링크]
음원 스트리밍: [링크]

#찬송가 #찬송가338장 #내주를가까이하게함은 #NearerMyGodToThee #찬송가편곡 #예배음악"""

    # Wrap in a box
    desc_p = Paragraph(desc_template.replace("\n", "<br/>"), ParagraphStyle("desc", fontName="Gothic", fontSize=8.5, textColor=HexColor("#333333"), leading=14))
    desc_box = Table([[desc_p]], colWidths=[W - 10 * mm])
    desc_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ]))
    story.append(desc_box)
    story.append(Spacer(1, 4 * mm))

    desc_tips = [
        "첫 2줄에 핵심 키워드 포함 (검색 미리보기에 노출됨)",
        "가사 전문 포함 (가사로 검색하는 사람 유입)",
        "관련 PLAYLIST 링크 포함 (세션 시청 시간 증가)",
        "해시태그 10-15개 (한국어+영어 병기)",
    ]
    for t in desc_tips:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {t}", styles["bullet"]))
    story.append(Spacer(1, 6 * mm))

    # ========== 8. 업로드 스케줄 ==========
    story.append(Paragraph("8. 업로드 스케줄 최적화", styles["section_title"]))

    story.append(Paragraph("권장 주간 스케줄", styles["subsection"]))
    story.append(make_table(
        ["요일", "콘텐츠", "비고"],
        [
            ["월요일", "Shorts 1개", "지난주 영상 하이라이트"],
            ["수요일", "Shorts 1개", "비하인드 / 참여형"],
            ["금요일", "단독 곡 본편", "주력 콘텐츠 (오후 3-5시 업로드)"],
            ["토요일", "Shorts 1개", "주일 예배 전 관련 콘텐츠"],
        ],
        col_widths=[W * 0.18, W * 0.32, W * 0.50],
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("월간 추가 콘텐츠", styles["subsubsection"]))
    monthly = [
        "월 2회 1시간 PLAYLIST (1째 주, 3째 주)",
        "교회력 시즌에 맞춘 특별 PLAYLIST (사순절, 부활절, 성탄절 등)",
    ]
    for m in monthly:
        story.append(Paragraph(f"<bullet>&bull;</bullet> {m}", styles["bullet"]))
    story.append(PageBreak())

    # ========== 9. 수익 다각화 ==========
    story.append(Paragraph("9. 수익 다각화 전략", styles["section_title"]))

    story.append(Paragraph("유튜브 파트너 프로그램(YPP) 현황", styles["subsection"]))
    story.append(make_table(
        ["Tier", "조건", "현재 달성 여부"],
        [
            ["Tier 1\n(팬 펀딩)", "구독자 500명 +\n시청시간 3,000시간 또는 Shorts 300만", "구독자 충족\n(시청시간 확인 필요)"],
            ["Tier 2\n(전체 광고)", "구독자 1,000명 +\n시청시간 4,000시간 또는 Shorts 1,000만", "구독자 충족\n(시청시간 확인 필요)"],
        ],
        col_widths=[W * 0.18, W * 0.44, W * 0.38],
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("추가 수익원", styles["subsection"]))
    story.append(make_table(
        ["수익원", "방법", "예상 수익"],
        [
            ["악보 판매", "자체 편곡 악보 PDF\n(스마트스토어/크몽)", "곡당 3,000~10,000원"],
            ["음원 배포", "DistroKid로 Spotify/\nApple Music 등록", "누적 소액이지만 장기 자산"],
            ["후원", "투네이션/카카오 후원", "월 수만~수십만 원"],
            ["교회 맞춤 편곡", "결혼식/세례식/특별예배용", "건당 10만~50만 원"],
            ["교회 반주 구독", "소규모 교회 대상 월정액", "월 1만~3만 원/교회"],
        ],
        col_widths=[W * 0.22, W * 0.42, W * 0.36],
    ))
    story.append(Spacer(1, 6 * mm))

    # ========== 10. 커뮤니티 ==========
    story.append(Paragraph("10. 커뮤니티 & 외부 채널 연계", styles["section_title"]))

    story.append(make_table(
        ["시기", "액션", "상세 내용"],
        [
            ["즉시", "유튜브 커뮤니티 탭", '투표("다음 편곡할 찬송가?"), 기도 나눔'],
            ["즉시", "댓글 전부 답글", "답글하는 채널의 시청자 유지율 67% 향상"],
            ["단기\n(1-3개월)", "인스타그램 계정", "릴스로 Shorts 교차 게시, 비하인드 스토리"],
            ["단기", "네이버 블로그", "찬송가 편곡 이야기 + 유튜브 임베드"],
            ["중기\n(3-6개월)", "크리에이터 콜라보", "목사, 찬양 사역자, 다른 악기 연주자와 협업"],
            ["중기", "교회/기독교 단체 협업", "부흥회 특송, 기독교 행사 참여"],
        ],
        col_widths=[W * 0.15, W * 0.28, W * 0.57],
    ))
    story.append(PageBreak())

    # ========== 11. 실행 우선순위 ==========
    story.append(Paragraph("11. 실행 우선순위 요약", styles["section_title"]))

    story.append(make_highlight_box("1~3번을 이번 주 안에 실행하면, 1-2개월 내에 눈에 띄는 조회수 변화를 체감할 수 있습니다."))
    story.append(Spacer(1, 4 * mm))

    story.append(make_table(
        ["순위", "액션", "난이도", "예상 효과", "소요 시간"],
        [
            ["1", "Shorts 제목 전부 개별화", "쉬움", "높음", "1-2시간"],
            ["2", "기존 109개 영상 제목/설명/태그\nSEO 재최적화", "중간", "매우 높음", "1-2일"],
            ["3", "월 2회 1시간 PLAYLIST\n제작 시작", "중간", "매우 높음", "기존 영상 편집"],
            ["4", "썸네일 리디자인\n(최소 상위 20개)", "중간", "높음", "2-3일"],
            ["5", "Shorts 주 3-5회\n정기 업로드 시작", "쉬움", "높음", "편곡당 10분"],
            ["6", "영상 설명 템플릿 적용\n+ 가사 추가", "쉬움", "중간", "영상당 5분"],
            ["7", "반주MR 시리즈 중단", "즉시", "리소스 절약", "-"],
            ["8", "2-3시간 대형 PLAYLIST 제작", "높음", "매우 높음", "1주"],
        ],
        col_widths=[W * 0.07, W * 0.33, W * 0.13, W * 0.20, W * 0.27],
    ))
    story.append(PageBreak())

    # Footer
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("본 보고서는 2026년 3월 22일 기준으로 작성되었습니다.", styles["caption"]))
    story.append(Paragraph("유튜브 정책은 지속적으로 변경될 수 있으므로 정기적인 업데이트가 필요합니다.", styles["caption"]))

    # Build
    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=add_page_number)
    print(f"PDF 생성 완료: {output_path}")

if __name__ == "__main__":
    build_report()
