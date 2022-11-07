# Outfit-Forecast

An app to generate outfit predictions based on one's wardrobe and current weather.

Current class diagram
![Class Diagram](class-diagrams/updatedClassDiagram2.png)

Test suites used:

- FRONT END: Jest (https://jestjs.io/)
- BACK END: unittest (https://docs.python.org/3/library/unittest.html)

Testing files:

- frontend_functions_tests.js -- for functions associated with the front end
- backend_functions_tests.py -- for functions associated with the back end

Test changes for Milestone 3.b:
- test_username for User class has some changes due to changing parameters of what is allowed. 
  Old parameters: length at most 32, cannot be empty, alphanmeric but must have at least one letter and one digit, no special characters, first char cannot be a digit
  New parameters: length at most 32, cannot be empty, alphanumeric but must have at least one letter, no special characters, no whitespaces, first char cannot be a digit 
