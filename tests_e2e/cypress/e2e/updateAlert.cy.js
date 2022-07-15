describe('update alert test', () => {
    it('update alert test -- invoice', () => {

        cy.visit('http://localhost:5010/login')
        cy.get('#userId').type('tanaka_taro')
        cy.get('#password').type('password')
        cy.get('.btn').click()

        //to invoice page
        cy.visit('http://localhost:5010/invoice-page#/')

        //一覧で最初の明細行を選択
        cy.get(':nth-child(1) > [aria-colindex="1"] > a > .btn').click()
        //詳細入力でヘッダーの任意の項目を更新する
        cy.get('#honorificTitle').type('テストです{enter}')
        //戻るボタンをクリック
        cy.get('.col > .btn').click()
        //モーダル表示、保存しないで戻るをクリック
        cy.get('.modal-footer > .btn-danger').should('have.text', '保存しないで戻る').click()

        //一覧で最初の明細行を選択
        cy.get(':nth-child(1) > [aria-colindex="1"] > a > .btn').click()
        //詳細入力の明細行1行目を更新
        cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(3).type('{selectall}{backspace}AA') //free item
        cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(4).type('{selectall}{backspace}ノートPC') //contents
        cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(5).type('{selectall}{backspace}05') //qty
        cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(6).find('select').select('台') // 
        cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(7).clear().type('{selectall}{backspace}98000') //cost 
        //戻るボタンをクリック
        cy.get('.col > .btn').click()
        //モーダル表示、保存しないで戻るをクリック
        cy.get('.modal-footer > .btn-danger').should('have.text', '保存しないで戻る').click()


    })
    it('update alert test -- quotation', () => {

        cy.visit('http://localhost:5010/login')
        cy.get('#userId').type('tanaka_taro')
        cy.get('#password').type('password')
        cy.get('.btn').click()

        //to quotation page
        cy.visit('http://localhost:5010/quotation-page#/')

        //一覧で最初の明細行を選択
        cy.get(':nth-child(1) > [aria-colindex="1"] > a > .btn').click()
        //詳細入力でヘッダーの任意の項目を更新する
        cy.get('#honorificTitle').type('テストです{enter}')
        //戻るボタンをクリック
        cy.get('.col > .btn').click()
        //モーダル表示、保存しないで戻るをクリック
        cy.get('.modal-footer > .btn-danger').should('have.text', '保存しないで戻る').click()

        //一覧で最初の明細行を選択
        cy.get(':nth-child(1) > [aria-colindex="1"] > a > .btn').click()
        //詳細入力の明細行1行目を更新
        cy.get('#quotation_items_table').find('tr').eq(1).find('td').eq(3).type('{selectall}{backspace}AA') //free item
        cy.get('#quotation_items_table').find('tr').eq(1).find('td').eq(4).type('{selectall}{backspace}ノートPC') //contents
        cy.get('#quotation_items_table').find('tr').eq(1).find('td').eq(5).type('{selectall}{backspace}05') //qty
        cy.get('#quotation_items_table').find('tr').eq(1).find('td').eq(6).find('select').select('台') // 
        cy.get('#quotation_items_table').find('tr').eq(1).find('td').eq(7).clear().type('{selectall}{backspace}98000') //cost 
        //戻るボタンをクリック
        cy.get('.col > .btn').click()
        //モーダル表示、保存しないで戻るをクリック
        cy.get('.modal-footer > .btn-danger').should('have.text', '保存しないで戻る').click()


    })
})
