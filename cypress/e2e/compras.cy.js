describe('Pruebas E2E del Carrito de Pizzas', () => {
  
  beforeEach(() => {
    cy.visit('http://127.0.0.1:5000/');
    cy.get('.card').should('have.length.at.least', 5);
  });

  it('Test 1: Agregar 1 pizza al carrito y validar total', () => {
    cy.get('#agregar-pizza-1').click();

    cy.get('#agregar-pizza-1').should('contain', '¡Añadido!');

    cy.get('#carrito').click();

    cy.get('#total-carrito').should('contain', '$8000.00 ARS');

    cy.get('#cerrar-carrito').click();
  });

  it('Test 2: Agregar otra pizza mas al carrito y validar total sumado', () => {

    cy.get('#agregar-pizza-3').click();

    cy.get('#agregar-pizza-3').should('contain', '¡Añadido!');

    cy.get('#carrito').click();

    cy.get('#total-carrito').should('contain', '$18000.00 ARS');

    cy.get('#cerrar-carrito').click();
  });

  it('Test 3: Agregar 1 pizza mas, validar total, eliminar 1, y re-validar total', () => {

    cy.get('#agregar-pizza-5').click();

    cy.get('#agregar-pizza-5').should('contain', '¡Añadido!');

    cy.get('#carrito').click();

    cy.get('#total-carrito').should('contain', '$29000.00 ARS');

    cy.get('#eliminar-pizza-1').click();

    cy.get('#eliminar-pizza-1').should('not.exist');

    cy.get('#total-carrito').should('contain', '$21000.00 ARS');
  });;
});