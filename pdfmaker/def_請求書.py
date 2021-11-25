from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Spacer

from def_base import *


defPdf['attr']['name'] = "invoice"
defPdf['attr']['name_jp'] = "請求書"


defPdf['file']['file_name'] = "f'def_請求書_{_KEY}.pdf'"  #eval

h_date =  "'請求日：'" + fmt_date

ntext_sub = "'この度はご商談いただきありがとうございます。<br/>下記のとおりご請求申し上げます。'"

defPdf['header']['title'] = Paragraph("<u><strike>&nbsp;&nbsp;請&nbsp;&nbsp;&nbsp;求&nbsp;&nbsp;&nbsp;書&nbsp;&nbsp;</strike></u>",PS(**style_big_center))
defPdf['header']['table_info']['table'][7][0] =['evalParagraph',ntext_sub,style_small_left ]
defPdf['header']['table_info']['table'] += [
    [['evalParagraph' ,compute_total,style_midium_left_bold,"<u><font size=11>合計金額(消費税等込)</font>&nbsp;&nbsp;￥{:,}</u>"],''],
]

defPdf['body']['row_max'] = 12

defPdf['footer']['table_info']['table'] = [
    ['お振込先', '', '', ''],
    [Paragraph('<br/><font size=15>PayPay銀行　すずめ支店 <br/><br/>普通5544830 &nbsp;ユ)飛行船</font><br/><br/><font size=10>※お振込み手数料はお客様の負担とさせていただきます。</FONT>'
    ,PS(**style_small_left)),'', '', '']
]


defPdf['footer']['hanko'] = "canvas.drawImage('./inkan.png', 450,510,100,100,mask='auto')"
