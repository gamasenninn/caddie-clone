/* -------- 請求書データ　------*/

function nvl(src_val, rep) {
    return (src_val == null) ? rep : src_val;
}

function getPdfDataInvoice(mode, invoice, setting, sumInvoice, customer) {
    const h = {};
    const sum = {};
    if (mode == 'delivery') {
        h.category = '納品書';
    } else {
        h.category = '請求書';
    }
    h.customerName = nvl(invoice.customerName, '');
    h.honorificTitle = nvl(invoice.honorificTitle, '');
    h.applyNumber = invoice.applyNumber;
    h.applyDate = nvl(invoice.applyDate, ' / / ');
    h.myCompanyName = setting.companyName;
    h.myAddress1 = setting.address;
    h.myTel1 = setting.telNumber;
    h.myFax1 = setting.faxNumber;
    h.person = invoice.manager ? invoice.manager : '';
    h.title = invoice.title;
    h.customerPostNumber = customer.postNumber;
    h.customerAddress = customer.address + customer.addressSub;
    h.customerDepartment = invoice.department;
    h.customerManager = invoice.otherPartyManager ? invoice.otherPartyManager+" 様": "";
    h.headerTotalLabel = "請求金額";
    sum.amountLabel = "小計";
    sum.taxLabel = "消費税";
    sum.totalLabel = "合計金額";
    if (invoice.isTaxExp) {
        sum.amount = sumInvoice;
        sum.tax = parseInt(sumInvoice * 0.1);
        sum.total = parseInt(sumInvoice * 1.1);
    } else {
        sum.taxLabel = "うち消費税";
        sum.amountLabel = "小計(税込み)";
        sum.amount = sumInvoice;
        sum.total = sumInvoice;
        sum.tax = parseInt(sum.total - sum.total / 1.1)
    };
    h.memo = invoice.memo;
    h.deadLine = invoice.deadLine;
    h.payee = setting.payee;
    h.accountHolderKana = setting.accountHolderKana;
    h.accountHolder = setting.accountHolder;
    h.logoPath = setting.logoFilePath;
    h.stampPath = setting.stampFilePath;
    h.logoWidth = setting.logoWidth ? setting.logoWidth:50;
    h.logoHeight = setting.logoHeight ? setting.logoHeight:50;
    h.stampWidth = setting.stampWidth ? setting.stampWidth:50;
    h.stampHeight = setting.stampHeight ? setting.stampHeight:50;
    h.baseImagePath = "./static/asset/invoice_base.png";
    return getPdfData(h, sum);
}
function getPdfDataQuotation( quotation, setting, sumQuotation, customer) {
    const h = {};
    const sum = {};
    h.category = '見積書';
    h.customerName = nvl(quotation.customerName, '');
    h.honorificTitle = nvl(quotation.honorificTitle, '');
    h.applyNumber = quotation.applyNumber;
    h.applyDate = nvl(quotation.applyDate, ' / / ');
    h.myCompanyName = setting.companyName;
    h.myAddress1 = setting.address;
    h.myTel1 = setting.telNumber;
    h.myFax1 = setting.faxNumber;
    h.person = quotation.manager ? quotation.manager : '';
    h.title = quotation.title;
    h.customerPostNumber = customer.postNumber;
    h.customerAddress = customer.address + customer.addressSub;
    h.customerDepartment = quotation.department;
    h.customerManager = quotation.otherPartyManager ? quotation.otherPartyManager+" 様": "";;
    h.headerTotalLabel = "見積金額";
    sum.amountLabel = "小計(税込み)";
    sum.taxLabel = "うち消費税";
    sum.totalLabel = "合計金額";
    if (quotation.isTaxExp) {
        sum.amount = sumQuotation;
        sum.tax = parseInt(sumQuotation * 0.1);
        sum.total = parseInt(sumQuotation * 1.1);
    } else {
        sum.amount = sumQuotation;
        sum.total = sumQuotation;
        sum.tax = parseInt(sum.total - sum.total / 1.1)
    };
    h.memo = quotation.memo;
    h.logoPath = setting.logoFilePath;
    h.stampPath = setting.stampFilePath;
    return getPdfData(h, sum);
}
function getPdfData(h, sum) {
    return {
        "defPdf": {
            "attr": {
                "name": "def_invoice",
                "name_jp": "請求書",
                "page_size": "A4",
                "page_type": "portrait",
                "top_mergin": 9,
                "footter_size": 50
            },
            "file": {
                "outDir": "./static/pdf",
                "file_name": "test.pdf"
            },
            "header": {
                //"title": ["P", h.category, "big_center"],
                //"title_after": ["E", "Spacer(0,15*mm)"],
                "table_infos": [
                    {
                        "table": [
                            ["", "", "", "", "", "",""],
                            ["", "", ["P", h.customerPostNumber + "<br/>" + h.customerAddress  , "sm_l"], "", "", "", ""],
                            ["", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", ["P", h.myCompanyName, "my_company"]],
                            ["", "", ["P", h.customerName + '&nbsp;&nbsp;' + h.honorificTitle, "client"], "", "", "", ["P", h.myAddress1, "sm_r"]],
                            ["", "", ["P",h.customerDepartment+""+h.customerManager,"sm_l"], "", "", "", ["P", 'TEL: ' + h.myTel1, "sm_r"]],
                            ["", "", "", "", "", "", ["P", 'FAX: ' + h.myFax1, "sm_r"]],
                        ],
                        "col_widths": ["E", "[5*mm,5*mm,88*mm,3*mm,9*mm,10*mm,70*mm]"],
                        "row_heights": ["E", "(5*mm,7*mm,7*mm,5*mm,7*mm,9*mm,10*mm)"],
                        //"row_heights": ["E", "(10*mm,10*mm,10*mm,10*mm,10*mm,10*mm)"],
                        "table_style": [
                            ["E", "('NOP',(0,0),(-1,-1),0.15,colors.lightblue)"],
                            ["E", "('VALIGN',(0,0),(-1,-1),'TOP')"],
                            ["NOP", "('BOX',(1,0),(2,5),0.15,colors.lightblue,None, (3,3,3,3))"],
                        ],
                        "after": ["E", "Spacer(10*mm,50*mm)"]
                    },
                ],
                "drawBaseImages": [
                    ["('" + h.baseImagePath + "',0,0, 210*mm,295*mm,mask='auto')"]
                ],
                "drawImages": [
                    //["('" + h.baseImagePath + "',0,0, 210*mm,295*mm,mask='auto')"],
                    ["('" + h.logoPath + "', 370,760," +h.logoWidth+ ","+h.logoHeight+",mask='auto')"]
                ]
            },
            "body": {
                "detail": {
                    "row_max": 14,
                    "label_style": "sm_l_color",
                    //"pos_xy": ["E", "(1*mm,190*mm)"],
                    "fields": [
                        //{ "key": "num", "label": "No.", "width": 10, "p_style": "sm_r", "eval": "_ROWNUM+1" },
                        { "key": "itemName", "label": "商品名", "width": 100, "p_style": "sm_l" },
                        { "key": "count", "label": "数量", "width": 20, "p_style": "sm_r", "format": "{:,}" },
                        { "key": "unit", "label": "単位", "width": 15, "p_style": "sm_r" },
                        { "key": "price", "label": "単価", "width": 25, "p_style": "sm_r", "format": "{:,}" },
                        { "key": "calcPrice", "label": "金額", "width": 30, "p_style": "sm_r", "format": "{:,}" }
                    ],
                    "styles": [
                        ["E", "('FONT', (0, 0), (-1, -1), 'IPAexGothic', 11)"],
                        ["E", "('VALIGN', (0, 0), (-1, -1), 'MIDDLE')"],
                        ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.lightblue)"],
                        ["E", "('LINEBEFORE', (0, 0), (-1,-1), 0.25, colors.white)"],
                        ["E", "('LINEAFTER', (0, 0), (-1,-1), 0.25, colors.white)"],
                        ["E", "('ALIGN', (0, 0), (-1, 0), 'CENTER')"],
                        ["E", "('BACKGROUND', (0, 0), (6, 0), '#EBF5FF')"],
                        ["E", "('TEXTCOLOR', (0, 0), (-1, -1), colors.red)"],
                        ["E", "('BOX', (0, 0), (6, 0), 0.25,'#10AFC5')"],
                    ],
                    "stripe_backcrounds": ["'#EBF5FF'", "colors.white"]
                },
            },
            "footer": {
                //"pos_xy": ["E", "(10*mm,5*mm)"],
                //"paras":[
                //    ["P", h.payee, "sm_l","(40*mm,50*mm)"],
                //],
                "table_infos": [
                    // top right area 
                    {   "pos_xy": ["E", "(175*mm,278*mm)"],"table": [[["P", h.applyDate, "sm_l"]]],"col_widths": ["E", "(30*mm)"] },
                    {   "pos_xy": ["E", "(175*mm,272*mm)"],"table": [[["PF", h.applyNumber, "sm_l","{:}"]]],"col_widths": ["E", "(30*mm)"] },
                    // total area 
                    {   "pos_xy": ["E", "(40*mm,208*mm)"],"table": [[["P", h.title, "sm_l"]]],"col_widths": ["E", "(70*mm)"] },
                    {   "pos_xy": ["E", "(45*mm,197*mm)"],"table": [[["PF", sum.total, "md_l_b","￥{:,}-"]]],"col_widths": ["E", "(50*mm)"] },
                    // left side footer
                    {   "pos_xy": ["E", "(40*mm,71*mm)"],"table": [[["P", h.deadLine, "sm_l"]]],"col_widths": ["E", "(50*mm)"] },
                    {   "pos_xy": ["E", "(40*mm,64*mm)"],"table": [[["P", h.payee, "sm_l"]]],"col_widths": ["E", "(70*mm)"] },
                    {   "pos_xy": ["E", "(40*mm,52*mm)"],"table": [[["P", h.accountHolderKana, "sm_l"]]],"col_widths": ["E", "(70*mm)"] },
                    {   "pos_xy": ["E", "(40*mm,46*mm)"],"table": [[["P", h.accountHolder, "sm_l"]]],"col_widths": ["E", "(70*mm)"] },
                    // right side footer sum
                    {   "pos_xy": ["E", "(140*mm,73*mm)"],"table": [[["PF", sum.amount, "sm_r","{:,}"]]],"col_widths": ["E", "(50*mm)"] },
                    {   "pos_xy": ["E", "(140*mm,64*mm)"],"table": [[["PF", sum.tax, "sm_r","{:,}"]]],"col_widths": ["E", "(50*mm)"] },
                    {   "pos_xy": ["E", "(140*mm,57*mm)"],"table": [[["PF", sum.total, "sm_r","{:,}"]]],"col_widths": ["E", "(50*mm)"] },
                    // under side footer
                    {   "pos_xy": ["E", "(19*mm,13*mm)"],"table": [[["P", h.memo, "sm_l"]]],
                        "col_widths":   ["E", "(172*mm)"], 
                        "row_heights":  ["E", "(24*mm)"],
                        "table_style": [
                            ["E", "('VALIGN', (0, 0), (-1, -1), 'TOP')"],
                            ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.black)"],    
                        ]
                    },
                ],
                "drawImages": [
                    ["('" + h.stampPath + "', 510,720,"+h.stampWidth+ ","+h.stampHeight+",mask='auto')"]
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
            "sm_r": { "name": "Normal", "alignment": 2, "fontName": "IPAexMincho", "fontSize": 11 },
            "sm_l": { "name": "Normal", "alignment": 0, "fontName": "IPAexMincho", "fontSize": 11 },
            "sm_l_color": { "name": "Normal", "alignment": 0, "fontName": "IPAexMincho", "fontSize": 11,"textColor": "#10AFC5" },
            "sm_c": { "name": "Normal", "alignment": 1, "fontName": "IPAexMincho", "fontSize": 11 },
            "md_l_b": { "name": "Normal", "alignment": 0, "fontName": "IPAexMincho", "fontSize": 15 },
            "taxsm_l": { "name": "Normal", "alignment": 2, "fontName": "IPAexMincho", "fontSize": 9 },
            "taxsm_c": { "name": "Normal", "alignment": 1, "fontName": "IPAexMincho", "fontSize": 9 },
            "h_total": { "name": "Normal", "alignment": 1, "fontName": "IPAexMincho", "fontSize": 15 },
            "my_company": { "name": "Normal", "alignment": 0, "fontName": "IPAexGothic", "fontSize": 15 },
            "memo": { "name": "Normal", "alignment": 0, "fontName": "IPAexGothic", "fontSize": 11 },
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
                "fontName": "IPAexMincho",
                "fontSize": 15,
                "underlineWidth": 1,
                "underlineGap": 1,
                "underlineOffset": -3.0,
                "textColor": "#000000"
            }
        },
    }
};
/* -------  領収書　----------*/

function getPdfDataRcpt(invoice, setting, sum) {
    const hr = {};
    const sumr = {};
    hr.category = "領収書";
    hr.customerName = invoice.customerName;
    hr.honorificTitle = invoice.honorificTitle;
    hr.numberLabel = "";
    hr.applyNumber = invoice.applyNumber;
    hr.headerTotalLabel = "領収金額",
        hr.title = "下記の通り領収いたしました";
    hr.dueDate = invoice.paymentDate;
    hr.person = invoice.manager;
    hr.myCompanyName = setting.companyName;
    hr.myAddress1 = setting.address;
    hr.myTel1 = setting.telNumber;
    hr.myFax1 = setting.faxNumber;
    hr.ceoName = setting.representative;
    hr.logoPath = setting.logoFilePath;
    hr.stampPath = setting.stampFilePath;

    if (invoice.isTaxExp) {
        sumr.amount = sum
        sumr.tax = parseInt(sum * 0.1);
        sumr.total = parseInt(sum * 1.1);
    } else {
        sumr.amount = sum;
        sumr.total = sum;
        sumr.tax = parseInt(sum.total - sum.total / 1.1)
    };

    return {
        "defPdf": {
            "attr": {
                "name": "def_recept",
                "name_jp": "領収書",
                "page_size": "A4",
                "page_type": "portrait",
                "top_mergin": 10,
                "footter_size": 0
            },
            "file": {
                "outDir": "./static/pdf",
                "file_name": "test.pdf"
            },
            "header": {
                "title": ["P", hr.category, "big_center"],
                "title_after": ["E", "Spacer(0,15*mm)"],
                "table_infos": [
                    {
                        "table": [
                            [["P", hr.customerName + '&nbsp;&nbsp;' + hr.honorificTitle, "client"], "", "", "", "", ["P", "番号" + hr.applyNumber, "sm_r"]],
                            ["", "", "", "", "", ["P", "日付: &nbsp;" + hr.dueDate, "sm_r"]],
                            ["", "", "", "", "", ["P", hr.myCompanyName, "md_l_b"]],
                            ["", "", "", "", "", ""],
                            ["", "", "", "", "", ["P", hr.myAddress1, "sm_r"]],
                            ["", ["P", hr.title, "sm_l"], "", "", "", ["P", 'TEL: ' + hr.myTel1, "sm_r"]],
                            ["", "", "", "", "", ["P", 'FAX: ' + hr.myFax1, "sm_r"]],
                            ["", ["P", hr.headerTotalLabel, "sm_c"], ["PF", sumr.total, "h_total", "￥{:,}-"], "", "", ""],
                            ["", "", "", "", "", ""],
                            ["", "", "", "", "", ["P", '担当者: ' + hr.person, "sm_r"]],
                            ["", ["P", "内消費税", "sm_l"], ["PF", sumr.tax, "taxsm_r", "￥{:,}-"], "", "", ""],
                            ["", ["P", "現金", "sm_l"], "", "", "", ""],
                            ["", ["P", "小切手", "sm_l"], "", "", "", ["P", "※電子領収書につき印紙不要", "sm_l"]],
                            ["", ["P", "お振込", "sm_l"], "", "", "", ""],
                            ["", ["P", "その他", "sm_l"], "", "", "", ""]
                        ],
                        "col_widths": ["E", "[5*mm,35*mm,50*mm,20*mm,10*mm,70*mm]"],
                        "table_style": [
                            ["NOP", "('GRID',(0,0),(-1,-1),0.15,colors.black)"],
                            ["E", "('VALIGN',(0,0),(-1,-1),'MIDDLE')"],
                            ["E", "('SPAN',(0,0),(3,0))"],
                            ["E", "('GRID',(1,7),(1,8),0.15,colors.black)"],
                            ["E", "('SPAN',(1,5),(2,6))"],
                            ["E", "('SPAN',(1,7),(1,8))"],
                            ["E", "('BACKGROUND',(1,7),(1,8),colors.lightblue)"],
                            ["E", "('BOX',(2,7),(3,8),0.15,colors.black)"],
                            ["E", "('SPAN',(2,7),(3,8))"],
                            ["E", "('LINEBELOW', (1, 10), (2, 10), 0.15, colors.black)"],
                            ["E", "('LINEBELOW', (1, 11), (2, 11), 0.15, colors.black)"],
                            ["E", "('LINEBELOW', (1, 12), (2, 12), 0.15, colors.black)"],
                            ["E", "('LINEBELOW', (1, 13), (2, 13), 0.15, colors.black)"],
                            ["E", "('LINEBELOW', (1, 14), (2, 14), 0.15, colors.black)"],

                        ],
                        "after": ["E", "Spacer(10*mm,5*mm)"]
                    }
                ],
                "drawImages": [
                    ["('" + hr.logoPath + "', 10,350+860/2,50,50,mask='auto')"]
                ]
            },
            "footer": {

                "pos_xy": ["E", "(170*mm,40*mm+860/2)"],
                "table_infos": [
                    {
                        "table": [
                            //[["P", "収入<br/>印紙", "sm_c"]]
                            ["", ""]
                        ],
                        "col_widths": ["E", "(20*mm)"],
                        "row_heights": ["E", "(20*mm)"],
                        "table_style": [
                            //["E", "('FONT', (0, 0), (-1, -1), 'IPAexGothic', 11)"],
                            //["E", "('GRID', (0, 0), (0,0), 0.1, colors.black, None, (3,3,3,3))"],
                            //["E", "('VALIGN', (0, 0), (0,0), 'CENTER')"]
                        ]
                    }
                ],

                "drawImages": [
                    ["('" + hr.stampPath + "', 420,120+860/2,50,50,mask='auto')"]
                ]
            }
        },
        "data": {
            "hdata": {}
        },
        "style": {
            "sm_r": { "name": "Normal", "alignment": 2, "fontName": "IPAexGothic", "fontSize": 11 },
            "sm_l": { "name": "Normal", "alignment": 0, "fontName": "IPAexGothic", "fontSize": 11 },
            "sm_c": { "name": "Normal", "alignment": 1, "fontName": "IPAexGothic", "fontSize": 11 },
            "md_l_b": { "name": "Normal", "alignment": 0, "fontName": "IPAexGothic", "fontSize": 15 },
            "taxsm_l": { "name": "Normal", "alignment": 2, "fontName": "IPAexGothic", "fontSize": 9 },
            "taxsm_c": { "name": "Normal", "alignment": 1, "fontName": "IPAexGothic", "fontSize": 9 },
            "taxsm_r": { "name": "Normal", "alignment": 2, "fontName": "IPAexGothic", "fontSize": 9 },
            "h_total": { "name": "Normal", "alignment": 1, "fontName": "IPAexGothic", "fontSize": 15 },
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