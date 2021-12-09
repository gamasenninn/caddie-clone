#!/usr/local/bin/python3.8


from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus import BaseDocTemplate,Frame,PageTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle as PS

from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

from reportlab.platypus.flowables import Spacer

from reportlab.pdfgen import canvas


import json
import sys
import re
#import cStringIO
from importlib import import_module
import json

import pprint


#----------　フォント定義------------
pdfmetrics.registerFont(TTFont('IPAexGothic','./ipaexg.ttf'))
pdfmetrics.registerFont(TTFont('IPAexMincho','./ipaexm.ttf'))


psize ={
    "A3":{ "short": 297, "long": 420},
    "A4":{ "short": 210, "long": 297},
    "A5":{ "short": 148, "long": 210},
    "A6":{ "short": 105, "long": 148},
    "B4":{ "short": 257, "long": 364},
    "B5":{ "short": 182, "long": 257},
    "B6":{ "short": 128, "long": 182},
}



class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        if page_count > 1 :
            self.drawRightString(200*mm, 5*mm,
                "Page %d of %d" % (self._pageNumber, page_count))

def make_table(table_info):

    t_data = table_info['table']

    for i,row in enumerate(t_data):
        for j,col in enumerate( row ):
            if type(col) is list:
                col_val = cv(col)          
            else:
                col_val  = col
            t_data[i][j] = col_val

    if 'row_Heights' in table_info:
        ht=Table(t_data,colWidths=cv(table_info['col_widths']),rowHeights=cv(table_info['row_Heights']))
    else:    
        ht=Table(t_data,colWidths=cv(table_info['col_widths']))

    t_styles = []
    for t_style in table_info['table_style']:
        cv_style = cv(t_style)
        if cv_style : t_styles.append(cv_style)

    ht.setStyle(TableStyle(t_styles))
    print(t_styles)

    return ht


def make_row(fields,bdata):
    _ROWNUM = 0

    vals_l =[]

    for b_row in bdata:
        vals = []
        col_width = 0
        for f in fields:
            k = f['key']
            val = b_row.get(k) #値の取得

            if 'eval' in f:
                val = eval(str(f.get('eval')))
            if 'format' in f:
                if val:
                    fmt = f.get('format')
                    if fmt: val = fmt.format(val)
            val = Paragraph(str(val),PS(**styles[f.get('p_style')]))
            vals.append(val)
        #print(vals)
        _ROWNUM += 1
        vals_l.append(vals)

    return vals_l

def make_detail(detail,bdata):

    th_style = detail.get('label_style')
    labels = [Paragraph(f.get('label'),PS(**styles[th_style])) for f in detail['fields']]
    vals_l = make_row(detail['fields'],bdata)
    vals_l.insert(0,labels)
    col_width_l = [int(f.get('width'))*mm for f in detail['fields']]
    bt=Table(vals_l,colWidths=col_width_l)

    t_styles = []
    for t_style in detail['styles']:
        cv_style = cv(t_style)
        if cv_style : t_styles.append(cv_style)

    bt.setStyle(TableStyle(t_styles))



    return bt


def footer(canvas, doc):
    canvas.saveState()

    ft = make_table(defPdf['footer']['table_info'])

    x,y =cv(defPdf['footer']['pos_xy'])
    #print("xy:",type(x),x)
    #print("xy:",type(y),y)

    ft.wrapOn(canvas, x, y)
    ft.drawOn(canvas, x, y)


    #canvas.drawImage('./inkan.png', 300,300,50,50,mask='auto')

#    for di in defPdf['footer']['DrawImage']:
#        print(di[1])
        #canvas.drawImage(di[1])


    canvas.restoreState()


def monitor(type,val):
    print(type,val)

def page_break(pageno):

    print(f"-----------Page Break {pageno}------------------------")


def cv(src_l):
    #print("srcl:",src_l)
    #return Paragraph(src_l[1],PS(**styles[src_l[2]]))
    if src_l[0] == "P": 
        return Paragraph(src_l[1],PS(**styles[src_l[2]]))
    elif  src_l[0] == "E":
        return eval(src_l[1])
    elif  src_l[0] == "EP":
        return Paragraph(eval(src_l[1]),PS(**styles[src_l[2]]))
    elif  src_l[0] == "EPF":
        print("EPF:",src_l[1])
        val = src_l[3].format(eval(src_l[1]))
        return Paragraph(val,PS(**styles[src_l[2]]))
    elif  src_l[0] == "NOP":
        return 


    #if src_l[0] == "P": return Paragraph(src_l[1],PS(**styles[src_l[2]]))

    return Paragraph("error",PS(**styles['sm_l']))


#------- initial ---------


args = sys.argv
if len(args) == 1 :
    hkey = ''
    mod_name = 'def_base'
elif len(args) ==2:
    hkey = int(args[1])
    mod_name = 'def_base'
elif len(args) == 3:
    mod_name = args[1]
    hkey = int(args[2])
else:
    print("パラメータエラー\n")
    sys.exit()
    

with open( "./data.json", mode='r', encoding='utf-8') as f:
    d = json.load(f)
    d_data = d.get('data')
    defPdf = d.get('defPdf')
    styles = d.get('style')


_HEAD = d_data['hdata'][0]
_ROWS = d_data['bdata']


#----ドキュメント本体-----

attr_name = defPdf['attr']['name']
pfile = defPdf['file']['outDir']+"/"+ defPdf['file']['file_name']
size = defPdf['attr']['page_size']
if defPdf['attr']['page_type']=="landscape":
    w = psize[size]['long']*mm
    h = psize[size]['short']*mm
else:
    w = psize[size]['short']*mm
    h = psize[size]['long']*mm
#w,h = A4
doc = BaseDocTemplate(pfile, pagesize=[w,h])
#doc = BaseDocTemplate(sys.stdout, pagesize=A4)



#top_mergin = 20*mm
top_mergin = defPdf['attr']['top_mergin']*mm
ft_size = defPdf['attr']['footter_size']*mm


frames = [
    Frame(0 * mm, ft_size, w, h-ft_size-top_mergin, showBoundary=0)
]

page_template = PageTemplate("frames", frames=frames,onPage=footer)
#page_template = PageTemplate("frames", frames=frames)
doc.addPageTemplates(page_template)

#-----タイトル表示 ------
elements = []

elements.append(cv(defPdf['header']['title']))
elements.append(cv(defPdf['header']['title_after']))

ht = make_table(defPdf['header']['table_info'])
elements.append(ht)
elements.append(cv(defPdf['header']['table_after']))


bt = make_detail(defPdf['body']['detail'],d_data.get('bdata'))
elements.append(bt)

bt = make_table(defPdf['body']['detail_after']['table_info'])
elements.append(bt)

#ft = make_table(defPdf['footer']['table_info'])
#elements.append(ft)


doc.build(elements)
sys.exit()


#--- BODY 明細部　作cls
# 成----
def make_row(row_data):
    d=[]
    _ROW = row_data
    for b_row in defPdf['body']['fields']:
        add_sw = False
        key = b_row['key']
        if key in row_data:
            val = str(row_data[key])
#            print("++++",key,val)
        else:
            val = ''
            add_sw =True
#            print("+--+",key,val)

        if 'eval' in b_row.keys() :
#            print("-eval---",val)
            if b_row['eval'] :
                val = eval(str(b_row['eval']))
                print("//////",val,type(val))
                if 'format' in b_row:
                    if val != '':
                        val = b_row['format'].format(val)
                        print("%%%%%%%",val)
        p = Paragraph(str(val),PS(**b_row['p_style']))
        d.append(p)
        if add_sw == True:
            row_data[key] = val

    return d 















#------明細表示 ------


b_data = []
b_data.append([row['label'] for row in defPdf['body']['fields']])

#---- test
_ROWNUM = 0
_STR_ROWNUM = ''
row_max = defPdf['body']['row_max']
if row_max - len(nouBs) < 0 : row_max = len(nouBs)

if 'num_key' in defPdf['body']:
    target_key = defPdf['body']['num_key']
    target_field = defPdf['body']['num_field']
    nums = [ nouB[target_key] for nouB in nouBs]
    field_count = len(defPdf['body']['fields'])
    field_list =[fld['key'] for fld in defPdf['body']['fields']]
    field_pos =  field_list.index(target_field)
    nop_field_l = ['' for i in range(field_count)]
    num_mode = True
else:
    nums = []
    key_count =0
    num_mode = False

if num_mode:
    for i in range(1,row_max+1):
        if not(i in nums):
            print(i,"...............None")
            nfl = nop_field_l.copy()
            p_style = defPdf['body']['fields'][field_pos]['p_style']
            nfl[field_pos] = Paragraph(str(i),PS(**p_style))    
            b_data.append(nfl)

        else:
            idx = nums.index(i)
            print(i,nouBs[idx])
            d = make_row(nouBs[idx])
            b_data.append(d)

        _ROWNUM += 1
        _STR_ROWNUM = str(_ROWNUM)

else:
    record_max = len(nouBs)
    for i in range(row_max):
        if i < record_max:
            print(i,nouBs[i])
            d = make_row(nouBs[i])
            b_data.append(d)
        else:
            print(i,"...............None")
            b_data.append(['','','','',''])

        _ROWNUM += 1
        _STR_ROWNUM = str(_ROWNUM)


#----        
	

widths = [row['width'] for row in defPdf['body']['fields'] ]

bt=Table(b_data,repeatRows=1,colWidths=widths)


tstyle_param = defPdf['body']['title_style']

bt.setStyle(TableStyle(tstyle_param))

elements.append(Spacer(2*mm, 2*mm))
elements.append(bt)


after_table = make_table(defPdf['body']['after_table'])
elements.append(after_table)


doc.setProgressCallBack(monitor)
doc.setPageCallBack(page_break)
    

doc.build(elements,canvasmaker=NumberedCanvas)

