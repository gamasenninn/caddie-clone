describe('soho caddie basic test', () => {
  it('passes', () => {
    cy.visit('http://localhost:5010')
    cy.get('#userId').type('tanaka_taro')
    cy.get('#password').type('password')
    cy.get('.btn').click()
    //to invoice page
    cy.visit('http://localhost:5010/invoice-page#/')
    cy.get('#new-button').click()

    cy.get('.text-left > .btn').click()
    cy.get('#customer-table > tbody > :nth-child(1) > [aria-colindex="1"]').click()
    //cy.get('#customer-modal___BV_modal_footer_ > .btn-primary').click()

    cy.get('#honorificTitle').type('様')
    cy.get('#applyDate').type('2022-07-01')
    cy.get('#department').type('営業部')
    cy.get('#deadLine').type('2022-07-31')
    cy.get('#manager').type('小野')
    cy.get('#otherPartyManager').type('佐藤')
    cy.get('#title').type('Aシステム構築の件')
    cy.get('textarea').first().type('テストメモ')

    
    cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(3).type('AA') //free item
    cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(4).type('ノートPC') //contents
    cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(5).type(5) //qty
    cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(6).find('select').select('台') // 
    cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(7).type(98000) //cost 

    cy.get('#remarks').type('これは備考です')
    cy.get('#invoice_items_table').find('tr').eq(1).find('td').eq(8).should('contain','490,000')
    //保存
    cy.get('.text-right > .btn-primary').click()
    cy.get('.close').click()
    // 合計金額を評価
    cy.get('table:nth-child(1) tr ').eq(0).find('td').eq(1).should('contain','490,000')
    cy.get('table:nth-child(1) tr ').eq(1).find('td').eq(1).should('contain','49,000')
    cy.get('table:nth-child(1) tr ').eq(2).find('td').eq(1).should('contain','539,000')
  //削除
    cy.get('.text-right > .btn-danger > .fas').click()
    cy.get('.router-link-active > .btn').click()
  })
})