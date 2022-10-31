import * as frontend_functions from './frontend_functions.js';

// Creating a user to run tests
let user_x = new frontend_functions.User("user_x")

// CReating a new EnviornmentalData class to run tests
let envData = new frontend_functions.EnvironmentalData()

// sendSurveyResponses tests //

// If each input is in the valid format, sendSurveyResponses() should return true.
// Otherwise, it should return false
var surveyTests = [
    [
    
    // Valid input
    {
        "jacket": [40, 70], "t-shirt": [70, 100],
        "jeans": [60, 80], "cap": [70, 110]
    },
        true],
    
    // "jacket" contains a temperature below -10F, which is invalid
    [{
        "jacket": [-30, 70], "t-shirt": [70, 100],
        "jeans": [60, 80], "cap": [70, 110]
    }, false],

    // "cap" contains a temperature above 120F, which is invalid
    [{
        "jacket": [40, 70], "t-shirt": [70, 100],
        "jeans": [60, 80], "cap": [70, 150]
    }, false],

    // "t-shirt" contains only one array element, which is invalid
    [{
        "jacket": [40, 70], "t-shirt": [70],
        "jeans": [60, 80], "cap": [70, 150]
    }, false],

    // "jeans" contains an empty array, which is invalid
    [{
        "jacket": [40, 70], "t-shirt": [70],
        "jeans": [], "cap": [70, 150]
    }, false],
]

// iterate over the input / output pairs and check if we obtain what is expected
let surveyError = "Error when testing function 'sendSurveyResponses': "
for (const test of surveyTests) {
    try {
        let output = user_x.sendSurveyResponses(test[0])
        if (output != test[1]) {
            throw surveyError + "input " + JSON.stringify(test[0]) +
            " does not match output " + test[1].toString()
        }
    }
    catch (e) {
        throw surveyError + e
    }
}

