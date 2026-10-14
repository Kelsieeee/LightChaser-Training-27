# -*- coding: utf-8 -*-
"""
《我的特长介绍》3 页 PPT 生成脚本
设计系统：tokens（色/字/间距） -> primitives（文本/线条/形状/短令牌） -> compositions（封面/证据网格/结束页）
风格：明亮、自信、清爽；青春有活力，但结构严谨可信。
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------------------------------------------------------------- tokens
BG       = RGBColor(0xFA, 0xF7, 0xF2)  # 暖纸背景
CARD     = RGBColor(0xFD, 0xFB, 0xF7)  # 卡片表面
HAIRLINE = RGBColor(0xDC, 0xD4, 0xC4)  # 细分隔线
INK      = RGBColor(0x23, 0x27, 0x2F)  # 主文字
BODY     = RGBColor(0x3A, 0x3D, 0x44)  # 正文
MUTED    = RGBColor(0x70, 0x68, 0x5E)  # 次要文字
ACCENT   = RGBColor(0xDF, 0x55, 0x3A)  # 朱砂红（主强调）
ACCENT_D = RGBColor(0xC2, 0x41, 0x2A)  # 深朱砂
ACCENT_T = RGBColor(0xF7, 0xEA, 0xE5)  # 浅朱砂底
TEAL     = RGBColor(0x1C, 0x64, 0x5E)  # 黛青（辅助色）
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)

FONT_CN = "微软雅黑"
FONT_EN = "Arial"

MARGIN = 0.9          # 外边距
FOOT_Y = 6.82         # 页脚线位置

# ------------------------------------------------------------- primitives
def add_shape(slide, kind, x, y, w, h, fill=None, line=None, line_w=1.0, radius=None):
    sh = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(line_w)
    sh.shadow.inherit = False
    if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sh.adjustments[0] = radius
        except Exception:
            pass
    return sh


def add_rect(slide, x, y, w, h, fill):
    return add_shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=fill)


def add_rule(slide, x, y, w, color=HAIRLINE, weight=0.014):
    add_rect(slide, x, y, w, weight, color)


def _style_run(r, st):
    f = r.font
    f.name = st.get("font", FONT_CN)
    f.size = Pt(st["size"])
    f.bold = st.get("bold", False)
    f.italic = st.get("italic", False)
    f.color.rgb = st.get("color", INK)
    rPr = r._r.get_or_add_rPr()
    ea = rPr.makeelement(qn("a:ea"), {"typeface": st.get("ea", FONT_CN)})
    rPr.append(ea)
    if st.get("spc"):
        rPr.set("spc", str(int(st["spc"] * 100)))  # 字距，1/100 pt


def add_text(slide, x, y, w, h, paras, *, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.0, wrap=True):
    """paras: [[(text, style), ...], ...] 每个子列表是一段"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        for text, st in para:
            r = p.add_run()
            r.text = text
            _style_run(r, st)
    return tb


def add_token(slide, text, x, y, w, h, *, size, color=ACCENT, bold=True,
              font=FONT_EN, align=PP_ALIGN.CENTER):
    """短令牌（序号/页码）：零边距、禁止自动换行，防止被排成竖排"""
    return add_text(
        slide, x, y, w, h,
        [[(text, {"size": size, "color": color, "bold": bold, "font": font})]],
        align=align, anchor=MSO_ANCHOR.MIDDLE, wrap=False,
    )


def section_label(slide, num, cn, en):
    add_rect(slide, MARGIN, 0.605, 0.12, 0.12, ACCENT)
    add_text(slide, MARGIN + 0.22, 0.52, 8.0, 0.3,
             [[(f"{num}　", {"size": 11, "color": ACCENT, "bold": True, "font": FONT_EN}),
               (cn, {"size": 11, "color": TEAL, "bold": True}),
               (f"　{en}", {"size": 10, "color": TEAL, "bold": True,
                            "font": FONT_EN, "spc": 1.2})]],
             anchor=MSO_ANCHOR.MIDDLE)


def claim_title(slide, text):
    add_text(slide, MARGIN, 0.9, 11.6, 0.68,
             [[(text, {"size": 27, "bold": True, "color": INK})]],
             anchor=MSO_ANCHOR.MIDDLE)


def footer(slide, folio):
    add_rule(slide, MARGIN, FOOT_Y, 13.333 - 2 * MARGIN)
    add_text(slide, MARGIN, FOOT_Y + 0.1, 4, 0.26,
             [[("我的特长介绍", {"size": 10, "color": MUTED})]],
             anchor=MSO_ANCHOR.MIDDLE)
    add_token(slide, folio, 11.63, FOOT_Y + 0.08, 0.8, 0.3,
              size=10.5, color=MUTED, align=PP_ALIGN.RIGHT)


# ---------------------------------------------------------- compositions
def build_cover(slide):
    # 背景身份层：朱砂圆环 + 黛青细线环 + 点状呼应 + 圆形“印章”
    add_shape(slide, MSO_SHAPE.OVAL, 9.35, 1.32, 3.92, 3.92,
              line=ACCENT, line_w=2.4)
    add_shape(slide, MSO_SHAPE.OVAL, 10.98, 1.02, 1.42, 1.42,
              line=HAIRLINE, line_w=1.0)
    add_shape(slide, MSO_SHAPE.OVAL, 12.5, 1.66, 0.15, 0.15, fill=TEAL)
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 9.28, 4.32, 1.28, 1.28,
              fill=ACCENT, radius=0.16)
    add_text(slide, 9.28, 4.32, 1.28, 1.28,
             [[("特", {"size": 25, "bold": True, "color": WHITE})],
              [("长", {"size": 25, "bold": True, "color": WHITE})]],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             line_spacing=1.05)

    # 眉标
    add_rect(slide, MARGIN, 1.72, 0.13, 0.13, TEAL)
    add_text(slide, MARGIN + 0.23, 1.62, 6.5, 0.32,
             [[("个人特长展示", {"size": 12, "bold": True, "color": TEAL}),
               ("　PERSONAL PROFILE", {"size": 10.5, "bold": True,
                "color": TEAL, "font": FONT_EN, "spc": 1.6})]],
             anchor=MSO_ANCHOR.MIDDLE)

    # 主标题
    add_text(slide, MARGIN - 0.04, 2.34, 8.2, 1.12,
             [[("我的特长介绍", {"size": 53, "bold": True, "color": INK})]],
             anchor=MSO_ANCHOR.MIDDLE)
    add_rect(slide, MARGIN, 3.62, 0.88, 0.075, ACCENT)
    add_text(slide, MARGIN, 3.92, 7.6, 0.42,
             [[("三项拿得出手的特长，与背后长期的练习",
                {"size": 17, "color": MUTED})]])

    # 底部信息
    add_rule(slide, MARGIN, 6.3, 7.2)
    add_text(slide, MARGIN, 6.42, 8.0, 0.3,
             [[("汇报人：XXX", {"size": 12, "color": MUTED}),
               ("　｜　班级：XX 班", {"size": 12, "color": MUTED}),
               ("　｜　2026 年", {"size": 12, "color": MUTED,
                                  "font": FONT_EN})]])
    add_token(slide, "01 / 03", 11.55, 6.4, 0.9, 0.3,
              size=11, color=MUTED, align=PP_ALIGN.RIGHT)


CARDS = [
    ("01", "公众表达", "表达力", [
        "校级演讲比赛一等奖",
        "主持校园活动 10 余场",
        "能把复杂的事情讲清楚",
    ]),
    ("02", "编程与逻辑", "逻辑力", [
        "掌握 Python、C++ 两门语言",
        "信息学竞赛获省级二等奖",
        "独立完成 3 个实用小工具",
    ]),
    ("03", "硬笔书法", "专注力", [
        "书法水平考级玖级",
        "作品入选校园文化展",
        "坚持每日临帖 30 分钟",
    ]),
]


def build_grid(slide):
    section_label(slide, "02", "特长一览", "MY STRENGTHS")
    claim_title(slide, "三项特长，每项都有看得见的成果")
    add_rule(slide, MARGIN, 1.66, 13.333 - 2 * MARGIN)

    gap = 0.33
    card_w = (13.333 - 2 * MARGIN - 2 * gap) / 3
    x0, y0, ch = MARGIN, 1.95, 4.55

    for i, (num, name, tag, items) in enumerate(CARDS):
        x = x0 + i * (card_w + gap)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y0, card_w, ch,
                  fill=CARD, line=HAIRLINE, line_w=0.75, radius=0.035)
        add_rect(slide, x + 0.34, 2.30, 0.5, 0.075, ACCENT)
        add_token(slide, num, x + 0.3, 2.46, 1.25, 0.62,
                  size=33, color=ACCENT, align=PP_ALIGN.LEFT)
        add_text(slide, x + 0.34, 3.12, card_w - 0.6, 0.42,
                 [[(name, {"size": 21, "bold": True, "color": INK})]])
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE,
                  x + 0.34, 3.7, 1.02, 0.34,
                  fill=ACCENT_T, radius=0.5)
        add_text(slide, x + 0.34, 3.7, 1.02, 0.34,
                 [[(tag, {"size": 10.5, "bold": True, "color": ACCENT_D})]],
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_rule(slide, x + 0.34, 4.3, card_w - 0.68)
        for j, item in enumerate(items):
            ry = 4.52 + j * 0.58
            add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE,
                      x + 0.35, ry + 0.075, 0.09, 0.09,
                      fill=ACCENT, radius=0.25)
            add_text(slide, x + 0.56, ry, card_w - 0.86, 0.42,
                     [[(item, {"size": 12.5, "color": BODY})]],
                     anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)

    footer(slide, "02 / 03")


HABITS = [
    ("01", "刻意练习", "拆解薄弱环节，每周只盯住一个点反复打磨"),
    ("02", "输出作品", "用比赛、展览和项目检验自己的真实水平"),
    ("03", "主动求反馈", "请老师和同伴挑错，把批评当作改进的路标"),
]


def build_closing(slide):
    section_label(slide, "03", "持续精进", "KEEP GROWING")
    claim_title(slide, "每天 30 分钟，让特长持续生长")
    add_rule(slide, MARGIN, 1.66, 13.333 - 2 * MARGIN)

    # 三条习惯行
    top, rh = 2.0, 1.06
    add_rule(slide, MARGIN, top, 13.333 - 2 * MARGIN)
    for i, (num, title, desc) in enumerate(HABITS):
        y = top + i * rh
        cy = y + 0.17
        add_shape(slide, MSO_SHAPE.OVAL, MARGIN, cy, 0.62, 0.62,
                  line=ACCENT, line_w=1.4)
        add_token(slide, num, MARGIN, cy, 0.62, 0.62, size=15, color=ACCENT)
        add_text(slide, 1.82, y + 0.12, 2.0, 0.72,
                 [[(title, {"size": 17, "bold": True, "color": INK})]],
                 anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, 3.98, y + 0.12, 7.2, 0.72,
                 [[(desc, {"size": 13.5, "color": MUTED})]],
                 anchor=MSO_ANCHOR.MIDDLE)
        if i < len(HABITS) - 1:  # 末行下方由色带边缘收束，避免双线挤压
            add_rule(slide, MARGIN, y + rh, 13.333 - 2 * MARGIN)

    # 结束色带（满幅朱砂）
    band_y = 5.3
    add_rect(slide, 0, band_y, 13.333, 7.5 - band_y, ACCENT)
    add_text(slide, MARGIN, 5.78, 7.2, 0.9,
             [[("谢谢观看", {"size": 40, "bold": True, "color": WHITE})]])
    add_text(slide, MARGIN + 0.03, 6.68, 7.0, 0.3,
             [[("THANK YOU FOR WATCHING", {"size": 11, "bold": True,
                "color": WHITE, "font": FONT_EN, "spc": 1.8}),
               ("　·　期待与你交流", {"size": 11.5, "color": WHITE})]])
    add_text(slide, 8.1, 7.02, 3.15, 0.3,
             [[("汇报人：XXX　|　2026", {"size": 10.5, "color": WHITE})]],
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    add_shape(slide, MSO_SHAPE.OVAL, 11.42, 5.46, 1.72, 1.72,
              line=WHITE, line_w=1.4)
    add_shape(slide, MSO_SHAPE.OVAL, 11.84, 5.88, 0.88, 0.88,
              line=WHITE, line_w=0.9)


# ----------------------------------------------------------------- build
def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    for builder in (build_cover, build_grid, build_closing):
        slide = prs.slides.add_slide(blank)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = BG
        builder(slide)

    prs.core_properties.title = "我的特长介绍"
    prs.core_properties.author = "XXX"

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "我的特长介绍.pptx")
    prs.save(out)
    print("saved:", out)


if __name__ == "__main__":
    main()
