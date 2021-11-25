from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Spacer



#----------　フォント定義------------
pdfmetrics.registerFont(TTFont('IPAexGothic','./ipaexg.ttf'))
pdfmetrics.registerFont(TTFont('IPAexMincho','./ipaexm.ttf'))


#----------　スタイル定義------------
style_small_right={
    "name":         "Normal",
    "alignment":    2,
    "fontName":     "IPAexGothic",
    "fontSize":     11
}

style_small_left={
    "name":         "Normal",
    "alignment":    0,
    "fontName":     "IPAexGothic",
    "fontSize":     11
}

style_small_left_bold ={
    "name":         "Normal",
    "alignment":    0,
    "fontName":     "IPAexGothic",
    "fontSize":     12
}

style_midium_left_bold = {
    "name":         "Normal",
    "alignment":    0,
    "fontName":     "IPAexGothic",
    "fontSize":     15
}

style_big_center = {
    "name":         "Normal",
    "alignment":    1,
    "fontName":     "IPAexGothic",
    "fontSize":     20,
    "underlineWidth":   0.5,
    "underlineGap":     0,
    "underlineOffset": -5.0,
    "strikeWidth":   0.5,
    "strikeGap" : 0,
    "strikeOffset" : -3.0,
    "leading":2,
}


style_client = {
    "name":         "Normal",
    "alignment":    0,
    "fontName":     "IPAexGothic",
    "fontSize":     18,
    "underlineWidth":   1,
    "underlineGap":     1,
    "underlineOffset": -3.0,
    "textColor": '#000000',
}


#----------　変数定義 ------------

ntext_sub = "'毎度お買い上げいただき誠にありがとうございます。<br/>下記の通り納品いたしましたのでご査収ください。'"
#ntext_sub = "''"

h_client = "'<u>'+_HEAD['client_name'] + '&nbsp;&nbsp御中</u>' if _HEAD['client_class'] =='法人' else '<u>'+_HEAD['client_name'] + '&nbsp;&nbsp様</u>'"

fmt_date =  "'{0[0]}年 {0[1]}月 {0[2]}日'.format(_HEAD['apply_date'].split('-')) if _HEAD['apply_date'] else '0000年00月00日'"
h_date =  "'請求日：'"+ fmt_date

tantou = "'<u>'+'担当:&nbsp;&nbsp;'+_HEAD['person']+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>'"



p_price = "_ROW['p_price'] if _ROW['p_price'] != 0 else ''"
p_qty = "_ROW['p_qty'] if _ROW['p_qty'] != 0 else ''"

compute_price = "_ROW['p_qty']*_ROW['p_price'] if _ROW['p_qty'] != 0 else ''"
compute_sum = "sum([row['p_qty']*row['p_price'] for row in _ROWS])"
compute_tax = "int(sum([row['p_qty']*row['p_price'] for row in _ROWS])*0.1) if _HEAD['tax'] == '税込' else int(sum([row['p_qty']*row['p_price']*0.1 for row in _ROWS]))"




compute_total = "(int(sum([row['p_qty']*row['p_price'] for row in _ROWS])) if _HEAD['tax'] == '税込' else int(sum([row['p_qty']*row['p_price']*1.1 for row in _ROWS])))  -(int(_HEAD['discount']) if _HEAD['discount']  else 0)"

compute_discount ="_HEAD['discount']"

replace_crlf_pname = "_ROW['p_name'].replace('\\n','<br/>')"

#nebiki_row =  ['',Paragraph('値引き額',PS(**style_small_left)), ['evalParagraph',compute_discount,style_small_right,"▲{:,}" ]]
nebiki_row =  ['',['evalParagraph',"'出精値引' if _HEAD['discount'] else ''",style_small_left], ['evalParagraph',compute_discount,style_small_right,"▲{:,}" ]]


#----------　詳細定義 ------------

defPdf = {
    "attr":{
        "name": "def_invoice",
        "name_jp":"請求書",
        "page_size": "A4",
        "page_type": "portrait",  #portrait/landscape
        "top_mergin": 15*mm,
        "footter_size": 40*mm,

    },
    "file":{
        "outDir": "f'./pdf'", #eval
        "file_name": "f'{_ATTR_NAME}_out_{_KEY}.pdf'",  #eval
    },
    "DB":{
        "database": "./rem_hikousen.db",
        "table_head": "doc_header",
        "table_body":   "doc_body",
        "link_key": "h_id",
    },
    "default":{
        "param":{
            "key": 691,
        },
    },
    "header":{
        "title": Paragraph("<u>&nbsp;&nbsp;請&nbsp;&nbsp;&nbsp;求&nbsp;&nbsp;&nbsp;書&nbsp;&nbsp;</u>",PS(**style_big_center)),
        "title_after": Spacer(0,15*mm),
        "table_info":{
            "table":[
                [ ['EP' ,h_client,style_client],['EP' ,h_date,style_small_right]],
                ['',''],
                ['',['EP2',"'株式会社　テストコム'","md_l_b"] ],
                ['',''],
                ['', ['EP2',"'鹿沼店:栃木県鹿沼市板荷0000－99'","sm_r"]],
                ['', ['EP2',"'TEL: 0289-000-0000'","sm_r"]],
                ['', ['EP2',"'FAX: 0289-000-0001'","sm_r"]],
                ['', ['EP2',"'宇都宮店:栃木県宇都宮市鶴田0-00-0'","sm_r"]],
                ['', ['EP2',"'TEL: 028-000-0000'","sm_r"]],
                ['', ['EP2' ,tantou,"sm_l"]],
            ],
            "col_widths":(110*mm, 70*mm),
            "table_style":[
#                ('GRID',(0,0),(-1,-1),0.15,colors.black),
                ('SPAN',(0,7),(0,8))
            ],
        },
        "table_after": Spacer(10*mm,5*mm)
    },
    "body":{
        "num_key": 'item_num',
        "num_field": "num",
        "row_max": 12,
        "fields":[
            {  "key": "num"        ,"label": "No." ,  "width": 10*mm , 'p_style':style_small_right,'eval':"_ROWNUM+1" },
            {  "key": "p_name"      ,"label": "商品名", "width": 95*mm, 'p_style':style_small_left ,'eval':replace_crlf_pname },
            {  "key": "p_qty"       ,"label": "数量",   "width": 15*mm , 'p_style':style_small_right,'eval':p_qty,   "format": "{:,}"   },
            {  "key": "p_price"     ,"label": "単価",   "width": 25*mm , 'p_style':style_small_right,'eval':p_price, "format": "{:,}"},
            {  "key": "p_calc_price","label": "金額",   "width": 25*mm , 'p_style':style_small_right,'eval':compute_price , "format": "{:,}" },
        ],
        "title_style":[
            ('FONT', (0, 0), (-1, -1), "IPAexGothic", 11),
            ('GRID', (0, 0), (-1,-1), 0.25, colors.black),
	    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
	    ('BACKGROUND', (0, 0), (6, 0), colors.lightgrey)
#	    ('BACKGROUND', (0, 0), (6, 0), colors.blue)
        ],
        "after_table":{
            "table":[
                #['',Paragraph('小計',PS(**style_small_left)), ['evalParagraph',compute_sum, style_small_right,"{:,}"]],
                ['',['evalParagraph',"'小計(税込)' if _HEAD['tax'] == '税込' else '小計'",style_small_left,"{:}"], ['evalParagraph',compute_sum, style_small_right,"{:,}"]],
                ['',['evalParagraph',"'うち消費税分' if _HEAD['tax'] == '税込' else '消費税分'",style_small_left,"{:}"], ['evalParagraph',compute_tax,style_small_right,"{:,}" ]],
                nebiki_row,
                #['',Paragraph('値引き額',PS(**style_small_left)), ['evalParagraph',compute_discount,style_small_right,"▲{:,}" ]],
                ['',Paragraph('合計金額',PS(**style_small_left)), ['evalParagraph',compute_total,style_small_right,"{:,}" ]],
            ],
            "col_widths":(55*mm, 75*mm, 40*mm),
            "table_style":[
                ('LINEBEFORE', (0, 0), (0, -1), 0.15, colors.black),#左
                ('LINEABOVE', (0, 0), (-1, -1), 0.15, colors.black),#上
                ('LINEBELOW', (0, 0), (-1, -1), 0.15, colors.black),#下
                ('GRID',(2,0),(-1,-1),0.15,colors.black),
                #('SPAN',(0,0),(1,0)),
            ]
        }
    },
    "footer":{
        "pos_xy": (15*mm,10*mm),
        "table_info":{
            "table":[
                ['摘要', '', '', ''],
                ['','', '', '']
            ],
            "col_widths":(110*mm,10*mm,30*mm,30*mm),
            "row_Heights": (8*mm,30*mm),
            "table_style":[
                ('FONT', (0, 0), (-1, -1), "IPAexGothic", 11),
                ('GRID', (0, 0), (0,1), 0.25, colors.black),
                ('GRID', (2, 0), (3,2), 0.25, colors.black),
                ('VALIGN',(0,1),(0,-1),'TOP'),
                ('ALIGN',(0,0),(0,-1),'CENTER'),
            ],
        },
        "hanko": "canvas.drawImage('./inkan.png', 490,525,50,50,mask='auto')",
        "logo": "canvas.drawImage('./logo2.jpg', 490,675,50,50,mask='auto')",

    },
    "style":{
        "sm_r":{
            "name":         "Normal",
            "alignment":    2,
            "fontName":     "IPAexGothic",
            "fontSize":     11
        },

        "sm_l":{
            "name":         "Normal",
            "alignment":    0,
            "fontName":     "IPAexGothic",
            "fontSize":     11
        },

        "sm_l_b":{
            "name":         "Normal",
            "alignment":    0,
            "fontName":     "IPAexGothic",
            "fontSize":     12
        },

        "md_l_b":{
            "name":         "Normal",
            "alignment":    0,
            "fontName":     "IPAexGothic",
            "fontSize":     15
        },

        "big_center":{
            "name":         "Normal",
            "alignment":    1,
            "fontName":     "IPAexGothic",
            "fontSize":     20,
            "underlineWidth":   0.5,
            "underlineGap":     0,
            "underlineOffset": -5.0,
            "strikeWidth":   0.5,
            "strikeGap" : 0,
            "strikeOffset" : -3.0,
            "leading":2,
        },
        "client":{
            "name":         "Normal",
            "alignment":    0,
            "fontName":     "IPAexGothic",
            "fontSize":     18,
            "underlineWidth":   1,
            "underlineGap":     1,
            "underlineOffset": -3.0,
            "textColor": '#000000',
        }
        
    }

}
