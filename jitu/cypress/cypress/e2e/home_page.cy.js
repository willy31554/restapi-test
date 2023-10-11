// login.spec.js

// Visit the login page
describe('Login Test', function () {
    it('Should login with valid credentials', function () {
        // Visit the login page
        cy.visit('/practice-test-login/'); // Replace with your login page URL

        // Enter valid username and password
        cy.get('input[name="username"]').type('student');
        cy.get('input[name="password"]').type('Password123');

        // Click the "Login" button
        cy.get('#submit').click();

        // Wait for redirection to the dashboard page (replace 'dashboard' with the actual URL or element)
        cy.url().should('include', '/logged-in-successfully/'); // Check URL
        // OR
        // cy.get('.dashboard-element').should('be.visible'); // Check for a specific element on the dashboard page

        // Capture a screenshot of the dashboard page
        cy.screenshot('dashboard');

        // Verify that the "Log out" button is displayed using the CSS selector
        cy.get('#loop-container > div > article > div.post-content > div > div > div > a').should('be.visible');

        // Click the "Log out" button
        cy.get('#loop-container > div > article > div.post-content > div > div > div > a').click();

        // Verify that the user is redirected to the login page
        cy.url().should('include', '/practice-test-login/'); // Check URL

        // Close the web browser
        //cy.visit('about:blank'); // Navigate to a blank page to close the browser
    });

    it('Should display an error message for invalid credentials', function () {
        // Visit the login page
        cy.visit('/practice-test-login/'); // Replace with your login page URL

        // Enter invalid username and password
        cy.get('input[name="username"]').type('invalid_username');
        cy.get('input[name="password"]').type('InvalidPassword123');

        // Click the "Login" button
        cy.get('#submit').click();

        // Verify that an error message is displayed
        cy.get('#error').should('be.visible'); // Replace with the actual selector for the error message

        // Verify that the user is not redirected to the dashboard page
        cy.url().should('not.include', '/logged-in-successfully/'); // Check URL

        // Close the web browser
        //cy.visit('about:blank'); // Navigate to a blank page to close the browser
    });
});
