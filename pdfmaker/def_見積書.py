from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Spacer

from def_base import *

defPdf['attr']['name'] = "estimate"
defPdf['attr']['name_jp'] = "見積書"

defPdf['file']['file_name'] = "f'def_見積書_{_KEY}.pdf'"  #eval

h_date =  "'見積日： '"+ fmt_date

tekiyou = "_HEAD['doc_descript']"

limit_date = "'<u><font size=12> 本見積書有効期限&nbsp;&nbsp;　見積日より2週間以内</font></u>'"
ntext_sub = "'下記の通りお見積りさせていただきます。<br/>ご検討のほど、よろしくお願いいたします。<br/><br/>'"

defPdf['header']['title'] = Paragraph("<u><strike>&nbsp;&nbsp;見&nbsp;&nbsp;&nbsp;積&nbsp;&nbsp;&nbsp;書&nbsp;&nbsp;</strike></u>",PS(**style_big_center))

defPdf['header']['table_info']['table'][0][1] = ['evalParagraph' ,h_date,style_small_right]
defPdf['header']['table_info']['table'][7][0] =['evalParagraph',ntext_sub,style_small_left ]
defPdf['header']['table_info']['table'] += [
    [['evalParagraph' ,limit_date, style_small_left],'']
]


defPdf['footer']['table_info']['table'][1][0] = ['evalParagraph' ,tekiyou,style_small_left]
defPdf['footer']['hanko'] = "canvas.drawImage('./inkan.png', 450,500,100,100,mask='auto')"
