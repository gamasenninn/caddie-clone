/* -------- 請求書データ　------*/
h = {
    numberLabel: "請求番号:",
    customerName: "テスト商店",
    applyNumber: "00000001",
    myCompanyName: "テスト会社",
    category: "請求書",
    dueDate: "2021-08-22",
    person: "小野",
    memo: "とりあえずメモ",
    tax: "税込",
    myCompanyName: "株式会社 テストコム",
    myAddress1: "栃木県鹿沼市板荷000-99",
    myTel1: "000-999-1111",
    myFax1: "000-888-2222",
    myAddress2: "栃木県鹿沼市千渡000-99",
    myTel2: "000-999-7777",
};
sum = {
    amountLabel: "小計",
    amount: 0,
    taxLabel: "うち消費税",
    tax: 0,
    totalLabel: "合計金額",
    total: 0
};
function getPdfData() {
    return {
        "defPdf": {
            "attr": {
                "name": "def_invoice",
                "name_jp": "請求書",
                "page_size": "A4",
                "page_type": "portrait",
                "top_mergin": 15,
                "footter_size": 50
            },
            "file": {
                "outDir": "./static/pdf",
                "file_name": "test.pdf"
            },
            "header": {
                "title": ["P", h.category, "big_center"],
                "title_after": ["E", "Spacer(0,15*mm)"],
                "table_infos": [
                    {
                        "table": [
                            [["P", h.customerName, "client"], ["P", h.numberLabel + h.applyNumber, "sm_r"]],
                            ["", ""],
                            ["", ["P", h.myCompanyName, "md_l_b"]],
                            ["", ""],
                            ["", ["P", '鹿沼店:' + h.myAddress1, "sm_r"]],
                            ["", ["P", 'TEL: ' + h.myTel1, "sm_r"]],
                            ["", ["P", 'FAX: ' + h.myFax1, "sm_r"]],
                            ["", ["P", '千渡店:' + h.myAddress2, "sm_r"]],
                            ["", ["P", 'TEL: ' + h.myTel2, "sm_r"]],
                            ["", ["P", '担当者: ' + h.person, "sm_l"]]
                        ],
                        "col_widths": ["E", "[110*mm, 70*mm]"],
                        "table_style": [
                            ["NOP", "('GRID',(0,0),(-1,-1),0.15,colors.black)"],
                            ["E", "('SPAN',(0,7),(0,8))"]
                        ],
                        "after": ["E", "Spacer(10*mm,5*mm)"]
                    }
                ],
                "drawImages": [
                    ["('./static/asset/logo2.jpg', 495,675,50,50,mask='auto')"]
                ]
            },
            "body": {
                "detail": {
                    "row_max": 15,
                    "label_style": "sm_c",
                    "fields": [
                        { "key": "num", "label": "No.", "width": 20, "p_style": "sm_r", "eval": "_ROWNUM+1" },
                        { "key": "itemName", "label": "商品名", "width": 90, "p_style": "sm_l" },
                        { "key": "count", "label": "数量", "width": 15, "p_style": "sm_r", "format": "{:,}" },
                        { "key": "unit", "label": "単位", "width": 15, "p_style": "sm_r" },
                        { "key": "price", "label": "単価", "width": 25, "p_style": "sm_r", "format": "{:,}" },
                        { "key": "calcPrice", "label": "金額", "width": 25, "p_style": "sm_r", "format": "{:,}" }
                    ],
                    "styles": [
                        ["E", "('FONT', (0, 0), (-1, -1), 'IPAexGothic', 11)"],
                        ["E", "('GRID', (0, 0), (-1,-1), 0.25, colors.black)"],
                        ["E", "('ALIGN', (0, 0), (-1, 0), 'CENTER')"],
                        ["E", "('BACKGROUND', (0, 0), (6, 0), colors.lightgrey)"]
                    ],
                    "stripe_backcrounds": ["colors.lightblue", "colors.white"]
                },
                "detail_after": {
                    "table_info": {
                        "table": [
                            ["", ["PF", sum.amountLabel, "sm_l", "{:}"], ["PF", sum.amount, "sm_r", "{:,}"]],
                            ["", ["PF", sum.taxLabel, "sm_l", "{:}"], ["PF", sum.tax, "sm_r", "{:,}"]],
                            ["", ["PF", sum.totalLabel, "sm_l", "{:}"], ["PF", sum.total, "sm_r", "{:,}"]]
                        ],
                        "col_widths": ["E", "(65*mm, 75*mm, 50*mm)"],
                        "table_style": [
                            ["E", "('LINEBEFORE', (0, 0), (0, -1), 0.15, colors.black)"],
                            ["E", "('LINEABOVE', (0, 0), (-1, -1), 0.15, colors.black)"],
                            ["E", "('LINEBELOW', (0, 0), (-1, -1), 0.15, colors.black)"],
                            ["E", "('GRID',(2,0),(-1,-1),0.15,colors.black)"]
                        ]
                    }
                }
            },
            "footer": {
                "pos_xy": ["E", "(15*mm,10*mm)"],
                "table_infos": [
                    {
                        "table": [
                            ["摘要", "", "", ""],
                            [["P", h.memo, "sm_l"], "", "", ""]
                        ],
                        "col_widths": ["E", "(110*mm,10*mm,30*mm,30*mm)"],
                        "row_heights": ["E", "(8*mm,30*mm)"],
                        "table_style": [
                            ["E", "('FONT', (0, 0), (-1, -1), 'IPAexGothic', 11)"],
                            ["E", "('GRID', (0, 0), (0,1), 0.25, colors.black)"],
                            ["E", "('GRID', (2, 0), (3,2), 0.25, colors.black)"],
                            ["E", "('VALIGN',(0,1),(0,-1),'TOP')"],
                            ["E", "('ALIGN',(0,0),(0,-1),'CENTER')"]
                        ]
                    }
                ],
                "drawImages": [
                    ["('./static/asset/inkan.png', 400,50,50,50,mask='auto')"],
                    ["('./static/asset/inkan.png', 490,50,50,50,mask='auto')"]
                ]
            }
        },
        data: {
            "bdata": [
                {
                    "itemNum": 1, "itemName": "",
                    "count": 1, "price": 0, "calcPrice": 0
                },
            ]
        },
        "style": {
            "sm_r": { "name": "Normal", "alignment": 2, "fontName": "IPAexGothic", "fontSize": 11 },
            "sm_l": { "name": "Normal", "alignment": 0, "fontName": "IPAexGothic", "fontSize": 11 },
            "sm_c": { "name": "Normal", "alignment": 1, "fontName": "IPAexGothic", "fontSize": 11 },
            "md_l_b": { "name": "Normal", "alignment": 0, "fontName": "IPAexGothic", "fontSize": 15 },
            "big_center": {
                "name": "Normal",
                "alignment": 1,
                "fontName": "IPAexGothic",
                "fontSize": 20,
                "underlineWidth": 0.5,
                "underlineGap": 0,
                "underlineOffset": -5.0,
                "strikeWidth": 0.5,
                "strikeGap": 0,
                "strikeOffset": -3.0,
                "leading": 2
            },
            "client": {
                "name": "Normal",
                "alignment": 0,
                "fontName": "IPAexGothic",
                "fontSize": 18,
                "underlineWidth": 1,
                "underlineGap": 1,
                "underlineOffset": -3.0,
                "textColor": "#000000"
            }
        },
    }
}
/* -------  領収書　----------*/
hr = {
    customerName: "テスト商店",
    category: "領収書",
    amount: 3456789,
    forPaymentOf: "PCサポートとして",
    dueDate: "2021-08-22",
    myCompanyName: "株式会社 テストコム",
    myAddress1: "栃木県鹿沼市板荷000-99",
    myTel1: "000-999-1111",
    jobTitle: "代表取締役",
    ceoName: "テスト太郎",
    applyNumber: "220001",
};

function getPdfDataRcpt() {
    return {
        "defPdf":{
            "attr":{
                "name": "def_invoice",
                "name_jp":"領収書",
                "page_size": "A5",
                "page_type": "landscape",
                "top_mergin": 10,
                "footter_size": 0
            },
            "file":{
                "outDir": "./static/pdf", 
                "file_name": "test_n_table.pdf"
            },
            "header":{
                "table_infos":[
                    {
                        "table":[
                            [["P",hr.category,"big_center"],"","","","",""],
                            [["EP","'入金先'","sm_l"],["P",hr.customerName,"big_left"],"","","",["P","No:"+hr.applyNumber,"sm_l"]],
                            ["",["PF",hr.amount,"big_price","￥{:,}-"],"","","",""],
                            ["",["EP","'但'","sm_l"],["P",hr.forPaymentOf,"md_l"],"","",""],
                            ["",["EP","'入金日'","sm_l"],["P",hr.dueDate,"md_l"],"","",""],
                            ["","",["P",hr.myCompanyName+'<br/><font size=-3>'+hr.myAddress1+'<br/>'+hr.myTel1+'</font>',"md_l"],"","",""],
                            ["","","","","",""],
                            ["","",["P",'<font size=-3>'+hr.jobTitle +'</font>　' +hr.ceoName,"md_c"],"","",""]
                        ],
                        "col_widths": ["E","[30*mm, 30*mm, 30*mm,30*mm,30*mm]"],
                        "row_heights": ["E","(20*mm,20*mm,15*mm,10*mm,10*mm,10*mm,10*mm,10*mm)"],
                        "table_style":[
                            ["NOP","('GRID',(0,0),(-1,-1),0.15,colors.black)"],
                            ["E","('VALIGN',(0,0),(-1,-1),'TOP')"],
                            ["E","('SPAN',(0,0),(5,0))"],
                            ["E","('SPAN',(1,1),(4,1))"],
                            ["E","('SPAN',(1,2),(4,2))"],
                            ["E","('VALIGN',(1,2),(4,2),'CENTER')"],
                            ["E","('BACKGROUND',(1,2),(4,2),colors.aliceblue)"],
                            ["E","('SPAN',(2,3),(5,3))"],
                            ["E","('SPAN',(2,4),(5,4))"],
                            ["E","('SPAN',(2,5),(5,6))"],
                            ["E","('SPAN',(2,7),(5,7))"]
                        ],
                        "after": ["E","Spacer(10*mm,5*mm)"]
                    }
                ],
                "drawImages": [
                    ["('./static/asset/logo2.jpg', 0,350,50,50,mask='auto')"]
                ]

            },
            "footer": {
                "pos_xy": ["E", "(170*mm,40*mm)"],
                "table_infos": [
                    {
                        "table": [
                            [["P", "収入<br/>印紙", "sm_c"]]
                        ],
                        "col_widths": ["E", "(20*mm)"],
                        "row_heights": ["E", "(20*mm)"],
                        "table_style": [
                            ["E", "('FONT', (0, 0), (-1, -1), 'IPAexGothic', 11)"],
                            ["E", "('GRID', (0, 0), (0,0), 0.1, colors.black, None, (3,3,3,3))"],
                            ["E", "('VALIGN', (0, 0), (0,0), 'CENTER')"]
                        ]
                    }
                ],
                "drawImages": [
                    ["('./static/asset/inkan.png', 420,100,50,50,mask='auto')"]
                ]
            }
        },
        "data": {
            "hdata": {
            }
        },
        "style":{
            "sm_r":{
                "name": "Normal",
                "alignment":    2,
                "fontName":     "IPAexGothic",
                "fontSize":     10
            },
    
            "sm_l":{
                "name": "Normal",
                "alignment":    0,
                "fontName":     "IPAexGothic",
                "fontSize":     10
            },
            "sm_c":{
                "name": "Normal",
                "alignment":    1,
                "fontName":     "IPAexGothic",
                "fontSize":     10
            },
    
            "sm_l_b":{
                "name": "Normal",
                "alignment":    0,
                "fontName":     "IPAexGothic",
                "fontSize":     9
            },
            "md_l":{
                "name": "Normal",
                "alignment":    0,
                "fontName":     "IPAexGothic",
                "fontSize":     15,
                "strikeWidth":   0.5,
                "strikeGap" : 2,
                "strikeOffset" : 1.0,
                "leading":20
            },
            "md_c":{
                "name": "Normal",
                "alignment":    1,
                "fontName":     "IPAexGothic",
                "fontSize":     15,
                "strikeWidth":   0.5,
                "strikeGap" : 2,
                "strikeOffset" : 1.0,
                "leading":20
            },
            "big_left":{
                "name": "Normal",
                "alignment":    0,
                "fontName":     "IPAexGothic",
                "fontSize":     20,
                "underlineWidth":   0.5,
                "underlineGap":     0,
                "underlineOffset": -5.0,
                "strikeWidth":   0.5,
                "strikeGap" : 0,
                "strikeOffset" : -3.0,
                "leading": 10
            },
            "big_center":{
                "name": "Normal",
                "alignment":    1,
                "fontName":     "IPAexGothic",
                "fontSize":     20,
                "underlineWidth":   0.5,
                "underlineGap":     0,
                "underlineOffset": -5.0,
                "strikeWidth":   0.5,
                "strikeGap" : 0,
                "strikeOffset" : -3.0,
                "leading":2
            },
            "big_price":{
                "name": "Normal",
                "alignment":    1,
                "fontName":     "IPAexGothic",
                "fontSize":     20,
                "underlineWidth":   1,
                "underlineGap":     1,
                "underlineOffset": -3.0,
                "strikeWidth":   0.5,
                "strikeGap" : 5,
                "strikeOffset" : 0,
                "leading": 20
            },
            "client":{
                "name": "Normal",
                "alignment":    0,
                "fontName":     "IPAexGothic",
                "fontSize":     18,
                "underlineWidth":   1,
                "underlineGap":     1,
                "underlineOffset": -3.0,
                "textColor": "#000000"
            }  
        }
    }
}
