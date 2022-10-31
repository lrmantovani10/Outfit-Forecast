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
// Here, we use Jet's "test" function
test("sendSurveyResponses", () => {
    for (const testCase of surveyTests) {
        expect(user_x.sendSurveyResponses(testCase[0])).toEqual(testCase[1])
    }
})

// getWeather test //
// the format of the OpenWeather API's response can be seen here:
// https://rapidapi.com/blog/openweathermap-api-overview/javascript/

/*
    getWeather's response should be an object containing the 
    following keys (example):

    {
            "temp_min" : 50,
            "temp_max" : 65,
            "feels_like": 62,
            "atmosphere": "sunny"
    }
*/
var response = envData.getWeather()
// Check that all the keys neeed for the app to generate predictions are in the
// API's response. This is not a value test like the one above, but a check of
// the response's format, since the actual response will differ by day
let necessaryKeys = new Set(["temp_min", "temp_max", "feels_like", "atmosphere"])

Object.keys(response).forEach(function (key) {
    if (necessaryKeys.has(key)) {
        try {
            if (typeof (response[key]["temp_min"]) != "number" ||
                typeof (response[key]["temp_max"]) != "number" ||
                typeof (response[key]["feels_like"]) != "number") {
                throw "Value associated with key " + key + " in getWeather's response is not a number!"
            }
        }
        catch {
            throw "getWeather's response missing " + key + " key"
        }
        necessaryKeys.delete(key)
    }
})

// If there are important keys not found in the API's response, throw error
if (necessaryKeys.size != 0) {
    throw "The following keys were not found in the weather API's response: " +
    necessaryKeys.toString()
}

// dailyRecommender tests //
// Generate outfit predictions based on weather, sensitivity, and wardrobe

// adding a wardrobe to the user for testing. Each key in the wardrobe's
// nested objects is mapped to an array containing the lower and upper bounds in
// which the user would wear that piece of clothing
user_x.wardrobe = {
    "lowerBody": {
        "pants": [40, 85],
        "shorts": [80, 110]
    },
    "upperBody": {
        "tShirt": [60, 110],
        "longSleeve": [20, 60],
    },
    "jacket": {
        "leather": [-10, 40],
        "polyester": [41, 80]
    }
}

// Each element in "outfitTests" contains an input and an expected
// combination of lower body, upper body, and jacket selections.
// Each input is the current weather (which in the actual function's code
// will be envData.weather instead of a manually-entered JSON object)
// and the user's wardrobe object, declared above

// For the recommendations, we should determine what outfit to generate
// based on the "feels_like" parameter, but "temp_min" and "temp_max"
// are also used as tie-breakers in case a certain outfit has been \
// suggested before and we want to avoid repetition.
var outfitTests = [
    [[
        
        // "pants" is the only lowerBody item whose range contains the current
        // temperature, and so is "tShirt" for the upperBody. There is no 
        // ambiguity here. 
        {
            "temp_min" : 50,
            "temp_max" : 65,
            "feels_like": 62,
            "atmosphere": "cloudy"
        },
        user_x.wardrobe,
    ], ["pants", "tShirt", "polyester"]],

    // Again, there is no ambiguity here. Notice how no jacket falls within the
    // constraints, so we output NULL for it.
    [[
        {
            "temp_min" : 90,
            "temp_max" : 100,
            "feels_like": 105,
            "atmosphere": "sunny"
        }
    ], ["shorts", "tShirt", NULL]],

    // Here, there is ambiguity between "tShirt" and "longSleeve", both of
    // which include 60F in their ranges. Since we already predicted 
    // tSHirt, we will no predict longSleeve. If we had many, many different
    // conflicting temperature ranges for different pieces of clothing, we 
    // would need to select the one that had been predicted the less, as long
    // as it fell within the temp_min / temp_max range. If not, we just
    // repeat one that did fall in that range or output NULL if none fall in that
    // range. Here, "polyester" is being repeated, but it is the only one that
    // falls within our range, so select it
    [[
        {
            "temp_min" : 40,
            "temp_max" : 70,
            "feels_like": 60,
            "atmosphere": "cloudy"
        }
    ], ["pants", "longSleeve", "polyester"]],

    // Here, only the jacket falls within the constraints, so we output
    // NULL for the other ones -- the user needs to go shopping or change their
    // preferences! This is fine -- we could even have all three NULL
    [[
        {
            "temp_min" : 0,
            "temp_max" : 10,
            "feels_like": 5,
            "atmosphere": "snowy"
        }
    ], [NULL, NULL, "leather"]]

]

// iterate over the input / output pairs and check if we obtain what is expected
test("dailyRecommender", () => {
    for (const testCase of outfitTests) {
        expect(envData.dailyReccomender(testCase[0])).toEqual(testCase[1])
    }
})
