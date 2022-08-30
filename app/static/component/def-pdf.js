/* -------- 請求書データ　------*/

function nvl(src_val, rep) {
    return (src_val == null) ? rep : src_val;
}

function getPdfDataInvoice(mode, invoice, setting, sumInvoice, customer, docClass = 'origin') {
    const h = {};
    const sum = {};
    if (mode == 'delivery') {
        h.category = '納品書';
        h.baseImagePath = "./static/asset/delivery_base.png";
    } else if (mode == 'receipt') {
        h.category = '領収書';
        h.baseImagePath = "./static/asset/receipt_base.png";
    } else {
        h.category = '請求書';
        h.baseImagePath = "./static/asset/invoice_base.png";
    }
    h.mode = mode;
    h.docClass = docClass;
    h.customerName = nvl(invoice.customerName, '');
    h.honorificTitle = nvl(invoice.honorificTitle, '');
    h.applyNumber = invoice.applyNumber;
    if (docClass == 'nodate') {
        h.applyDate = "&nbsp;&nbsp; 年 &nbsp;&nbsp; 月 &nbsp;&nbsp; 日";
    } else {
        h.applyDate = nvl(invoice.applyDate, '');
    }
    h.myPostNumber = nvl(setting.postNumber, '');
    h.myCompanyName = nvl(setting.companyName, '');
    h.myAddress1 = nvl(setting.address, '');
    h.myTel1 = nvl(setting.telNumber, '');
    h.myFax1 = nvl(setting.faxNumber, '');
    h.person = nvl(invoice.manager, '');
    h.title = nvl(invoice.title, '');
    h.taxrate = nvl(invoice.tax, '');
    h.customerPostNumber = nvl(customer.postNumber, '');
    h.customerAddress = nvl(customer.address, '') + nvl(customer.addressSub, '');
    h.customerDepartment = nvl(invoice.department, '');
    h.customerManager = invoice.otherPartyManager ? invoice.otherPartyManager + " 様" : "";
    h.headerTotalLabel = "請求金額";
    sum.amountLabel = "小計";
    sum.taxLabel = "消費税";
    sum.totalLabel = "合計金額";
    sum.amount = sumInvoice.sum;
    sum.tax = sumInvoice.taxAmount;
    sum.total = sumInvoice.priceIncludingTax;
    //税別集計
    sum.normalTaxAmount = sumInvoice.normalTaxAmount;
    sum.normalTax = sumInvoice.normalTax;
    sum.reducedTaxAmount = sumInvoice.reducedTaxAmount;
    sum.reducedTax = sumInvoice.reducedTax;
    h.memo = nvl(invoice.remarks, '');
    h.deadLine = invoice.deadLine ? moment(nvl(invoice.deadLine, '')).format("YYYY年MM月DD日") : "";
    h.payee = !!setting.payee ? setting.payee.replace(/\n/g, '<br />') : ''
    h.accountHolderKana = nvl(setting.accountHolderKana);
    h.accountHolder = nvl(setting.accountHolder);
    h.logoPath = setting.logoFilePath;
    h.stampPath = setting.stampFilePath;
    h.logoWidth = setting.logoWidth ? setting.logoWidth : 50;
    h.logoHeight = setting.logoHeight ? setting.logoHeight : 50;
    h.stampWidth = setting.stampWidth ? setting.stampWidth : 50;
    h.stampHeight = setting.stampHeight ? setting.stampHeight : 50;
    const pdfData = getPdfData(h, sum);
    if (mode == 'delivery') {
        if (!setting.isDisplayDeliveryLogo) pdfData.defPdf.header.drawImages = [];
        if (!setting.isDisplayDeliveryStamp) pdfData.defPdf.first_page.drawImages = [];
    } else {
        if (!setting.isDisplayInvoiceLogo) pdfData.defPdf.header.drawImages = [];
        if (!setting.isDisplayInvoiceStamp) pdfData.defPdf.first_page.drawImages = [];
    }
    if (invoice.invoice_items.length > 0) {
        pdfData.data.bdata = invoice.invoice_items;
        pdfData.data.bdata = pdfData.data.bdata.map(i => ({
            ...i,
            price: parseInt(i.price),
            count: parseInt(i.count),
            calcPrice: i.price * i.count,
            itemName: (i.itemName ? i.itemName.replace(/\n/g, '<br />') : '')
        }));
    } else {
        pdfData.data.bdata = [{}];
    }
    return pdfData;

}
function getPdfDataQuotation(quotation, setting, sumQuotation, customer) {
    const h = {};
    const sum = {};
    h.mode = 'quotation';
    h.category = '見積書';
    h.baseImagePath = "./static/asset/quotes_base.png";
    h.customerName = nvl(quotation.customerName, '');
    h.honorificTitle = nvl(quotation.honorificTitle, '');
    h.applyNumber = quotation.applyNumber;
    h.applyDate = nvl(quotation.applyDate, ' / / ');
    h.myPostNumber = nvl(setting.postNumber, '');
    h.myCompanyName = nvl(setting.companyName, '');
    h.myAddress1 = nvl(setting.address, '');
    h.myTel1 = nvl(setting.telNumber, '');
    h.myFax1 = nvl(setting.faxNumber, '');
    h.person = nvl(quotation.manager, '');
    h.title = nvl(quotation.title);
    h.customerPostNumber = nvl(customer.postNumber, '');
    h.customerAddress = nvl(customer.address, '') + nvl(customer.addressSub, '');
    h.customerDepartment = nvl(quotation.department, '');
    h.customerManager = quotation.otherPartyManager ? quotation.otherPartyManager + " 様" : "";;
    h.headerTotalLabel = "見積金額";
    sum.amountLabel = "小計(税込み)";
    sum.taxLabel = "うち消費税";
    sum.totalLabel = "合計金額";
    sum.amount = sumQuotation.sum;
    sum.tax = sumQuotation.taxAmount;
    sum.total = sumQuotation.priceIncludingTax;
    h.memo = nvl(quotation.remarks, '');
    h.expiry = nvl(quotation.expiry, '');
    h.dayOfDelivery = nvl(quotation.dayOfDelivery, '');
    h.termOfSale = nvl(quotation.termOfSale, '');

    h.logoPath = setting.logoFilePath;
    h.stampPath = setting.stampFilePath;
    h.logoWidth = setting.logoWidth ? setting.logoWidth : 50;
    h.logoHeight = setting.logoHeight ? setting.logoHeight : 50;
    h.stampWidth = setting.stampWidth ? setting.stampWidth : 50;
    h.stampHeight = setting.stampHeight ? setting.stampHeight : 50;

    const pdfData = getPdfData(h, sum);
    if (!setting.isDisplayQuotationLogo) pdfData.defPdf.header.drawImages = [];
    if (!setting.isDisplayQuotationStamp) pdfData.defPdf.first_page.drawImages = [];
    if (self.quotation.quotation_items.length > 0) {
        pdfData.data.bdata = self.quotation.quotation_items;
        pdfData.data.bdata = pdfData.data.bdata.map(i => ({
            ...i,
            price: parseInt(i.price),
            count: parseInt(i.count),
            calcPrice: i.price * i.count,
            itemName: (i.itemName ? i.itemName.replace(/\n/g, '<br />') : '')
        }));
    } else {
        pdfData.data.bdata = [{}];
    }

    return pdfData;

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
                "footter_size": 80
            },
            "file": {
                "outDir": "./static/pdf",
                "file_name": "test.pdf"
            },
            "header": {
                //"title": ["P", h.category, "big_center"],
                "title_after": ["E", "Spacer(0,100*mm)"],
                "table_infos": [],
                "drawBaseImages": [
                    ["('" + h.baseImagePath + "',0,0, 210*mm,295*mm,mask='auto')"]
                ],
                "drawImages": [
                    ["('" + h.logoPath + "', 350,760," + h.logoWidth + "," + h.logoHeight + ",mask='auto')"]
                ]
            },
            "body": {
                "detail": {
                    "row_max": 10,
                    "label_style": "sm_c_color",
                    "fields": [
                        //{ "key": "any", "label": "#", "width": 15, "p_style": "sm_l" },
                        { "key": "itemName", "label": "内容", "width": 85, "p_style": "sm_l" },
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
                        //["E", "('TEXTCOLOR', (0, 0), (-1, -1), colors.red)"],
                        ["E", "('BOX', (0, 0), (6, 0), 0.25,'#10AFC5')"],
                    ],
                    "stripe_backgrounds": ["'#EBF5FF'", "colors.white"]
                },
            },
            "first_page": {
                "table_infos": [
                    // top leftt area 
                    {
                        "pos_xy": ["E", "(20*mm,245*mm)"],
                        "table": [
                            [["P", '〒' + h.customerPostNumber + "<br/>" + h.customerAddress, "sm_l"]],
                            [["P", h.customerName + '&nbsp;&nbsp;' + h.honorificTitle, "client"]],
                            [["P", h.customerDepartment + "" + h.customerManager, "sm_l"]],
                        ],
                        "col_widths": ["E", "(86*mm)"], "row_heights": ["E", "(17*mm,10*mm,7*mm)"],
                        "table_style": [
                            ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.lightblue)"],
                            ["E", "('VALIGN', (0, 0), (-1, -1), 'TOP')"],
                        ]
                    },
                    // top right area 
                    { "pos_xy": ["E", "(175*mm,277*mm)"], "table": [[["PF", h.applyNumber, "sm_l", "{:}"]]], "col_widths": ["E", "(30*mm)"] },
                    { "pos_xy": ["E", "(175*mm,271*mm)"], "table": [[["P", h.applyDate, "sm_l"]]], "col_widths": ["E", "(30*mm)"] },
                    {
                        "pos_xy": ["E", "(120*mm,235*mm)"],
                        "table": [
                            [["P", h.myCompanyName, "my_company"]],
                            [["P", '〒' + h.myPostNumber + '<br/>' + h.myAddress1 + '<br/>TEL:' + h.myTel1 + '&nbsp; FAX:' + h.myFax1, "sm_l"]],
                        ],
                        "col_widths": ["E", "(90*mm)"], "row_heights": ["E", "(10*mm,20*mm)"],
                        "table_style": [
                            ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.lightblue)"],
                            ["E", "('VALIGN', (0, 0), (-1, -1), 'TOP')"],
                        ]
                    },
                    // copy 
                    h.docClass == 'copy' ? { "pos_xy": ["E", "(95*mm,220*mm)"], "table": [[["P", "(控え)", "md_l_b"]]], "col_widths": ["E", "(30*mm)"] } : {},
                    // total area 
                    h.mode == 'receipt' ? {} : { "pos_xy": ["E", "(40*mm,218*mm)"], "table": [[["P", h.title, "sm_l"]]], "col_widths": ["E", "(110*mm)"] },
                    h.mode == 'receipt' ? { "pos_xy": ["E", "(45*mm,209*mm)"], "table": [[["PF", sum.total, "md_c_b", "￥{:,}-"]]], "col_widths": ["E", "(50*mm)"] } :
                        { "pos_xy": ["E", "(45*mm,208*mm)"], "table": [[["PF", sum.total, "md_c_b", "￥{:,}-"]]], "col_widths": ["E", "(50*mm)"] },
                    h.mode == 'receipt' ? { "pos_xy": ["E", "(33*mm,193*mm)"], "table": [[["PF", sum.amount, "sm_r", "{:,}"]]], "col_widths": ["E", "(20*mm)"] } : {},
                    h.mode == 'receipt' ? { "pos_xy": ["E", "(70*mm,193*mm)"], "table": [[["PF", sum.tax, "sm_r", "{:,}"]]], "col_widths": ["E", "(20*mm)"] } : {},
                    h.mode == 'receipt' ? { "pos_xy": ["E", "(100*mm,193*mm)"], "table": [[["PF", h.taxrate, "sm_r", "{:}%"]]], "col_widths": ["E", "(20*mm)"] } : {},


                    // quotes area
                    h.mode == 'quotation' ? { "pos_xy": ["E", "(145*mm,217*mm)"], "table": [[["P", h.expiry, "sm_l"]]], "col_widths": ["E", "(50*mm)"] } : {},
                    h.mode == 'quotation' ? { "pos_xy": ["E", "(145*mm,211*mm)"], "table": [[["P", h.dayOfDelivery, "sm_l"]]], "col_widths": ["E", "(50*mm)"] } : {},
                    h.mode == 'quotation' ? { "pos_xy": ["E", "(145*mm,204*mm)"], "table": [[["P", h.termOfSale, "sm_l"]]], "col_widths": ["E", "(50*mm)"] } : {},

                    // left side footer
                    h.mode == 'invoice' ? { "pos_xy": ["E", "(145*mm,47*mm)"], "table": [[["P", h.deadLine, "sm_l"]]], "col_widths": ["E", "(50*mm)"] } : {},
                    h.mode == 'invoice' ? {
                        "pos_xy": ["E", "(40*mm,57*mm)"], "table": [[["P", h.payee, "sm_l"]]], "col_widths": ["E", "(85*mm)"], "row_heights": ["E", "(11*mm)"],
                        "table_style": [["E", "('VALIGN', (0, 0), (-1, -1), 'TOP')"], ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.lightblue)"],
                        ]
                    } : {},
                    h.mode == 'invoice' ? { "pos_xy": ["E", "(40*mm,52*mm)"], "table": [[["P", h.accountHolderKana, "sm_l"]]], "col_widths": ["E", "(85*mm)"] } : {},
                    h.mode == 'invoice' ? { "pos_xy": ["E", "(40*mm,47*mm)"], "table": [[["P", h.accountHolder, "sm_l"]]], "col_widths": ["E", "(85*mm)"] } : {},
                    // right side footer sum
                    h.mode != 'receipt' ? { "pos_xy": ["E", "(27*mm,194*mm)"], "table": [[["PF", sum.amount, "sm_r", "{:,}"]]], "col_widths": ["E", "(26*mm)"] } : {},
                    h.mode != 'receipt' ? { "pos_xy": ["E", "(67*mm,194*mm)"], "table": [[["PF", sum.tax, "sm_r", "{:,}"]]], "col_widths": ["E", "(24*mm)"] } : {},
                    h.mode != 'receipt' ? { "pos_xy": ["E", "(105*mm,194*mm)"], "table": [[["PF", sum.total, "sm_r", "{:,}"]]], "col_widths": ["E", "(26*mm)"] } : {},
                    // 税率別表示
                    h.mode != 'receipt' ? { 
                        "pos_xy": ["E", "(135*mm,194*mm)"], 
                        "table": [
                            [
                                ["P", "税率10%対象", "sm_l"],
                                ["PF", sum.normalTaxAmount, "sm_r", "{:,}"],
                                ["P", "税", "sm_l"],
                                ["PF", sum.normalTax, "sm_r", "{:,}"]
                            ],
                            [
                                ["P", "税率 8%対象", "sm_l"],
                                ["PF", sum.reducedTaxAmount, "sm_r", "{:,}"],
                                ["P", "税", "sm_l"],
                                ["PF", sum.reducedTax, "sm_r", "{:,}"]
                            ],
                        ], 
                        "col_widths": ["E", "(28*mm,18*mm,5*mm,15*mm)"] 
                    } : {},
                    // under side footer
                    {
                        "pos_xy": ["E", "(19*mm,13*mm)"], "table": [[["P", h.memo, "sm_l"]]],
                        "col_widths": ["E", "(172*mm)"],
                        "row_heights": ["E", "(24*mm)"],
                        "table_style": [
                            ["E", "('VALIGN', (0, 0), (-1, -1), 'TOP')"],
                            ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.black)"],
                        ]
                    },
                ],
                "drawImages": [
                    ["('" + h.stampPath + "', 510,680," + h.stampWidth + "," + h.stampHeight + ",mask='auto')"]
                ]
            },
            "footer": {},
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
            "sm_l_color": { "name": "Normal", "alignment": 0, "fontName": "IPAexMincho", "fontSize": 11, "textColor": "#10AFC5" },
            "sm_c_color": { "name": "Normal", "alignment": 1, "fontName": "IPAexMincho", "fontSize": 11, "textColor": "#10AFC5" },
            "sm_c": { "name": "Normal", "alignment": 1, "fontName": "IPAexMincho", "fontSize": 11 },
            "md_l_b": { "name": "Normal", "alignment": 0, "fontName": "IPAexMincho", "fontSize": 15 },
            "md_c_b": { "name": "Normal", "alignment": 1, "fontName": "IPAexMincho", "fontSize": 15 },
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
}
//合算請求書
function getPdfDataTotalInvoice(mode, prePdfToalInvoice, setting, docClass = 'origin') {
    const h = {};
    const sum = {};
    const invoice = prePdfToalInvoice.invoices[0];
    const invoices = prePdfToalInvoice.invoices;
    const customer = prePdfToalInvoice.invoices[0].customer;

    if (mode == 'receipt') {
        h.category = '領収書';
        h.baseImagePath = "./static/asset/receipt_base.png";
    } else {
        h.category = '請求書';
        h.baseImagePath = "./static/asset/invoice_base.png";
    }
    h.mode = mode;
    h.docClass = docClass;
    h.customerName = nvl(invoice.customerName, '');
    h.honorificTitle = nvl(invoice.honorificTitle, '');
    //h.applyNumber = invoice.applyNumber;
    h.applyNumber = prePdfToalInvoice.totalInvoiceApplyNumber; //合計請求書独自の請求番号
    if (docClass == 'nodate') {
        h.applyDate = "&nbsp;&nbsp; 年 &nbsp;&nbsp; 月 &nbsp;&nbsp; 日";
    } else {
        h.applyDate = nvl(invoice.applyDate, '');
    }
    h.myPostNumber = nvl(setting.postNumber, '');
    h.myCompanyName = nvl(setting.companyName, '');
    h.myAddress1 = nvl(setting.address, '');
    h.myTel1 = nvl(setting.telNumber, '');
    h.myFax1 = nvl(setting.faxNumber, '');
    h.person = nvl(invoice.manager, '');
    h.title = nvl(invoice.title, '');
    h.taxrate = nvl(invoice.tax, '');
    h.customerPostNumber = nvl(customer.postNumber, '');
    h.customerAddress = nvl(customer.address, '') + nvl(customer.addressSub, '');
    h.customerDepartment = nvl(invoice.department, '');
    h.customerManager = invoice.otherPartyManager ? invoice.otherPartyManager + " 様" : "";
    h.headerTotalLabel = "請求金額";
    sum.amountLabel = "小計";
    sum.taxLabel = "消費税";
    sum.totalLabel = "合計金額";

    sum.amount = prePdfToalInvoice.basePrices.reduce((a, b) => a + b, 0); //小計
    sum.tax = prePdfToalInvoice.taxies.reduce((a, b) => a + b, 0); //消費税分
    sum.total = prePdfToalInvoice.totalBillings.reduce((a, b) => a + b, 0); //全計
    //軽減税率対応
    sum.reduceAmount = prePdfToalInvoice.reduceBasePrices.reduce((a, b) => a + b, 0); //小計
    sum.reduceTax = prePdfToalInvoice.reduceTaxies.reduce((a, b) => a + b, 0); //消費税分
    sum.reduceTotal = prePdfToalInvoice.reduceTotalBillings.reduce((a, b) => a + b, 0); //全計
    h.memo = nvl(invoice.remarks, '');
    h.deadLine = invoice.deadLine ? moment(nvl(invoice.deadLine, '')).format("YYYY年MM月DD日") : "";
    h.payee = !!setting.payee ? setting.payee.replace(/\n/g, '<br />') : ''
    h.accountHolderKana = nvl(setting.accountHolderKana);
    h.accountHolder = nvl(setting.accountHolder);
    h.logoPath = setting.logoFilePath;
    h.stampPath = setting.stampFilePath;
    h.logoWidth = setting.logoWidth ? setting.logoWidth : 50;
    h.logoHeight = setting.logoHeight ? setting.logoHeight : 50;
    h.stampWidth = setting.stampWidth ? setting.stampWidth : 50;
    h.stampHeight = setting.stampHeight ? setting.stampHeight : 50;
    const pdfData = getPdfDataTotal(h, sum);
    //console.log("pdfData:",pdfData)
    if (mode == 'delivery') { //note:modeで納品書は必要ないと思われるが、領収書は存在するか？
        if (!setting.isDisplayDeliveryLogo) pdfData.defPdf.header.drawImages = [];
        if (!setting.isDisplayDeliveryStamp) pdfData.defPdf.first_page.drawImages = [];
    } else {
        if (!setting.isDisplayInvoiceLogo) pdfData.defPdf.header.drawImages = [];
        if (!setting.isDisplayInvoiceStamp) pdfData.defPdf.first_page.drawImages = [];
    }
    pdfData.data.bdata = [];
    invoices.sort((a,b)=>{ //日付でソートする
        if(a.applyDate > b.applyDate) return 1
        else if (a.applyDate < b.applyDate) return -1
        else return 0
    });
    for (let i of invoices) {
        i.invoice_items = i.invoice_items.map((j, ix) => ({
            ...j,
            applyDate: (ix ? "" : i.applyDate),
            calcPrice: j.price * j.count,
            itemName: (j.itemName ? j.itemName.replace(/\n/g, '<br />') : '')
        }));
        pdfData.data.bdata = pdfData.data.bdata.concat(i.invoice_items);
    };
    //データが空白のもは出力しない。ただし、日付ブレイクは空データでも出力する。
    pdfData.data.bdata = pdfData.data.bdata.filter(i => {
        return !!i.itemName || !!i.applyDate
    });
    console.log("bdata:", pdfData.data.bdata);
    return pdfData;

}
function getPdfDataTotal(h, sum) {
    return {
        "defPdf": {
            "attr": {
                "name": "def_invoice",
                "name_jp": "請求書",
                "page_size": "A4",
                "page_type": "portrait",
                "top_mergin": 9,
                "footter_size": 80
            },
            "file": {
                "outDir": "./static/pdf",
                "file_name": "test.pdf"
            },
            "header": {
                //"title": ["P", h.category, "big_center"],
                "title_after": ["E", "Spacer(0,100*mm)"],
                "table_infos": [],
                "drawBaseImages": [
                    ["('" + h.baseImagePath + "',0,0, 210*mm,295*mm,mask='auto')"]
                ],
                "drawImages": [
                    ["('" + h.logoPath + "', 350,760," + h.logoWidth + "," + h.logoHeight + ",mask='auto')"]
                ]
            },
            "body": {
                "detail": {
                    "row_max": 10,
                    "label_style": "sm_c_color",
                    "fields": [
                        //{ "key": "any", "label": "#", "width": 15, "p_style": "sm_l" },
                        { "key": "applyDate", "label": "日付", "width": 30, "p_style": "sm_l" },
                        { "key": "itemName", "label": "内容", "width": 55, "p_style": "sm_l" },
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
                        ["E", "('BACKGROUND', (0, 0), (7, 0), '#EBF5FF')"],
                        //["E", "('TEXTCOLOR', (0, 0), (-1, -1), colors.red)"],
                        ["E", "('BOX', (0, 0), (7, 0), 0.25,'#10AFC5')"],
                    ],
                    "stripe_backgrounds": ["'#EBF5FF'", "colors.white"]
                },
            },
            "first_page": {
                "table_infos": [
                    // top leftt area 
                    {
                        "pos_xy": ["E", "(20*mm,245*mm)"],
                        "table": [
                            [["P", '〒' + h.customerPostNumber + "<br/>" + h.customerAddress, "sm_l"]],
                            [["P", h.customerName + '&nbsp;&nbsp;' + h.honorificTitle, "client"]],
                            [["P", h.customerDepartment + "" + h.customerManager, "sm_l"]],
                        ],
                        "col_widths": ["E", "(86*mm)"], "row_heights": ["E", "(17*mm,10*mm,7*mm)"],
                        "table_style": [
                            ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.lightblue)"],
                            ["E", "('VALIGN', (0, 0), (-1, -1), 'TOP')"],
                        ]
                    },
                    // top right area 
                    { "pos_xy": ["E", "(175*mm,277*mm)"], "table": [[["PF", h.applyNumber, "sm_l", "{:}"]]], "col_widths": ["E", "(30*mm)"] },
                    { "pos_xy": ["E", "(175*mm,271*mm)"], "table": [[["P", h.applyDate, "sm_l"]]], "col_widths": ["E", "(30*mm)"] },
                    {
                        "pos_xy": ["E", "(120*mm,235*mm)"],
                        "table": [
                            [["P", h.myCompanyName, "my_company"]],
                            [["P", '〒' + h.myPostNumber + '<br/>' + h.myAddress1 + '<br/>TEL:' + h.myTel1 + '&nbsp; FAX:' + h.myFax1, "sm_l"]],
                        ],
                        "col_widths": ["E", "(90*mm)"], "row_heights": ["E", "(10*mm,20*mm)"],
                        "table_style": [
                            ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.lightblue)"],
                            ["E", "('VALIGN', (0, 0), (-1, -1), 'TOP')"],
                        ]
                    },
                    // copy 
                    h.docClass == 'copy' ? { "pos_xy": ["E", "(95*mm,220*mm)"], "table": [[["P", "(控え)", "md_l_b"]]], "col_widths": ["E", "(30*mm)"] } : {},
                    // total area 
                    h.mode == 'receipt' ? {} : { "pos_xy": ["E", "(40*mm,218*mm)"], "table": [[["P", h.title, "sm_l"]]], "col_widths": ["E", "(110*mm)"] },
                    h.mode == 'receipt' ? { "pos_xy": ["E", "(45*mm,209*mm)"], "table": [[["PF", sum.total+sum.reduceTotal, "md_c_b", "￥{:,}-"]]], "col_widths": ["E", "(50*mm)"] } :
                        { "pos_xy": ["E", "(45*mm,208*mm)"], "table": [[["PF", sum.total+sum.reduceTotal, "md_c_b", "￥{:,}-"]]], "col_widths": ["E", "(50*mm)"] },
                    h.mode == 'receipt' ? { "pos_xy": ["E", "(33*mm,193*mm)"], "table": [[["PF", sum.amount, "sm_r", "{:,}"]]], "col_widths": ["E", "(20*mm)"] } : {},
                    h.mode == 'receipt' ? { "pos_xy": ["E", "(70*mm,193*mm)"], "table": [[["PF", sum.tax, "sm_r", "{:,}"]]], "col_widths": ["E", "(20*mm)"] } : {},
                    h.mode == 'receipt' ? { "pos_xy": ["E", "(100*mm,193*mm)"], "table": [[["PF", h.taxrate, "sm_r", "{:}%"]]], "col_widths": ["E", "(20*mm)"] } : {},


                    // quotes area
                    h.mode == 'quotation' ? { "pos_xy": ["E", "(145*mm,217*mm)"], "table": [[["P", h.expiry, "sm_l"]]], "col_widths": ["E", "(50*mm)"] } : {},
                    h.mode == 'quotation' ? { "pos_xy": ["E", "(145*mm,211*mm)"], "table": [[["P", h.dayOfDelivery, "sm_l"]]], "col_widths": ["E", "(50*mm)"] } : {},
                    h.mode == 'quotation' ? { "pos_xy": ["E", "(145*mm,204*mm)"], "table": [[["P", h.termOfSale, "sm_l"]]], "col_widths": ["E", "(50*mm)"] } : {},

                    // left side footer
                    h.mode == 'invoice' ? { "pos_xy": ["E", "(145*mm,47*mm)"], "table": [[["P", h.deadLine, "sm_l"]]], "col_widths": ["E", "(50*mm)"] } : {},
                    h.mode == 'invoice' ? {
                        "pos_xy": ["E", "(40*mm,57*mm)"], "table": [[["P", h.payee, "sm_l"]]], "col_widths": ["E", "(85*mm)"], "row_heights": ["E", "(11*mm)"],
                        "table_style": [["E", "('VALIGN', (0, 0), (-1, -1), 'TOP')"], ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.lightblue)"],
                        ]
                    } : {},
                    h.mode == 'invoice' ? { "pos_xy": ["E", "(40*mm,52*mm)"], "table": [[["P", h.accountHolderKana, "sm_l"]]], "col_widths": ["E", "(85*mm)"] } : {},
                    h.mode == 'invoice' ? { "pos_xy": ["E", "(40*mm,47*mm)"], "table": [[["P", h.accountHolder, "sm_l"]]], "col_widths": ["E", "(85*mm)"] } : {},
                    // right side footer sum
                    h.mode != 'receipt' ? { "pos_xy": ["E", "(27*mm,194*mm)"], "table": [[["PF", sum.amount, "sm_r", "{:,}"]]], "col_widths": ["E", "(26*mm)"] } : {},
                    h.mode != 'receipt' ? { "pos_xy": ["E", "(67*mm,194*mm)"], "table": [[["PF", sum.tax, "sm_r", "{:,}"]]], "col_widths": ["E", "(24*mm)"] } : {},
                    h.mode != 'receipt' ? { "pos_xy": ["E", "(105*mm,194*mm)"], "table": [[["PF", sum.total, "sm_r", "{:,}"]]], "col_widths": ["E", "(26*mm)"] } : {},
                    //軽減税率対応出力
                    h.mode != 'receipt' ? { "pos_xy": ["E", "(27*mm,187*mm)"], "table": [[["PF", sum.reduceAmount, "sm_r", "{:,}"]]], "col_widths": ["E", "(26*mm)"] } : {},
                    h.mode != 'receipt' ? { "pos_xy": ["E", "(67*mm,187*mm)"], "table": [[["PF", sum.reduceTax, "sm_r", "{:,}"]]], "col_widths": ["E", "(24*mm)"] } : {},
                    h.mode != 'receipt' ? { "pos_xy": ["E", "(105*mm,187*mm)"], "table": [[["PF", sum.reduceTotal, "sm_r", "{:,}"]]], "col_widths": ["E", "(26*mm)"] } : {},
                    //
                    // under side footer
                    {
                        "pos_xy": ["E", "(19*mm,13*mm)"], "table": [[["P", h.memo, "sm_l"]]],
                        "col_widths": ["E", "(172*mm)"],
                        "row_heights": ["E", "(24*mm)"],
                        "table_style": [
                            ["E", "('VALIGN', (0, 0), (-1, -1), 'TOP')"],
                            ["NOP", "('GRID', (0, 0), (-1,-1), 0.25, colors.black)"],
                        ]
                    },
                ],
                "drawImages": [
                    ["('" + h.stampPath + "', 510,680," + h.stampWidth + "," + h.stampHeight + ",mask='auto')"]
                ]
            },
            "footer": {},
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
            "sm_l_color": { "name": "Normal", "alignment": 0, "fontName": "IPAexMincho", "fontSize": 11, "textColor": "#10AFC5" },
            "sm_c_color": { "name": "Normal", "alignment": 1, "fontName": "IPAexMincho", "fontSize": 11, "textColor": "#10AFC5" },
            "sm_c": { "name": "Normal", "alignment": 1, "fontName": "IPAexMincho", "fontSize": 11 },
            "md_l_b": { "name": "Normal", "alignment": 0, "fontName": "IPAexMincho", "fontSize": 15 },
            "md_c_b": { "name": "Normal", "alignment": 1, "fontName": "IPAexMincho", "fontSize": 15 },
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
}