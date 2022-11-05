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

// *********** ImageData Tests *********** //
// imageData contains a set of pictures, which are returned using getPictures()
// we return a list of UIImage pictures using getPictures() and use this as input
// 

let pictures = frontend_functions.getPictures()

test("upload", () => {
    //this will run the upload image on the returned pictures from the Image_Data object
    //if the size of the set is not 0, uploadImage() should return true
    //if the size of the set is 0, uploadImage() should return false
    
    //below tests the above two cases, expecting true in the first case and false in the
    // second case
    if(size(pictures) > 0){ expect(frontend_functions.uploadImage(pictures)).toEqual(true) }
    else { expect(frontend_functions.uploadImage(pictures_empty)).toEqual(false) }
})


// camera tests //
// Take pictures, choose from gallery, and successfully store them for later retrieval

// imageData contains one instance of a class called userCamera.
// Within userCamera, we create an instance of React Native's "image-picker" class
let imageData_x = new frontend_functions.userCamera() 
// "image-picker" stores the current image, whether it be chosen from the gallery or
// taken by the camera, in resourcePath. This is be the initial state of that,
// which should be NULL or some null-identifying value.
let initial_state = imageData_x.userCamera.state.resourcePath.data

test("camera", () => {
    // This will actually open up the camera on the phone running this code, which
    // makes automatic testing rather difficult. The way I imagine it, when running
    // this test, the user has to take a photo, and the code will then automatically
    // test to see if that photo's data has been successfully stored.
    imageData_x.userCamera.takePicture();
    // Arbitrary nonsensical value that will only change if taking picture is successful
    let new_state = -1 
    if (imageData_x.userCamera.res.didCancel) {
        console.log('User pressed cancel button');
    } else if (imageData_x.userCamera.res.error) {
        console.log('takePicture Error: ', res.error);
    } else {
        new_state = imageData_x.userCamera.state.resourcePath.data
    }
    expect((initial_state).not.toEqual(new_state))

    // Similarly, auto-testing choosing from the gallery will be tricky because there
    // is no way around making the user actually having to choose an actual image
    // from their gallery to use the function. In this, I imagine the user selecting
    // an image, which then should be successfully stored, overwriting the last image
    imageData_x.userCamera.choosePicture();
    // Arbitrary nonsensical value that will only change if taking picture is successful
    let new_state2 = -1 
    if (imageData_x.userCamera.res.didCancel) {
        console.log('User pressed cancel button');
    } else if (imageData_x.userCamera.res.error) {
        console.log('choosePicture Error: ', res.error);
    } else {
        new_state2 = imageData_x.userCamera.state.resourcePath.data
    }
    expect((initial_state).not.toEqual(new_state2))
    expect((new_state).not.toEqual(new_state2))

    // At this point, we should assume that two images (one from taking a picture with
    // the camera, the other from choosing one from the gallery) should be added to 
    // imageData_x's 'pictures' variable. This will allow us to test it as such:

    expect((imageData_x.getPictures[0]).toEqual(new_state))
    expect((imageData_x.getPictures[1]).toEqual(new_state2))

    // Testing updateImage, which replaces a certain image in imageData's pictures field

    imageData_x.userCamera.takePicture();
    if (imageData_x.userCamera.res.didCancel) {
        console.log('User pressed cancel button');
    } else if (imageData_x.userCamera.res.error) {
        console.log('takePicture Error: ', res.error);
    } else {
        new_state3 = imageData_x.userCamera.state.resourcePath.data
    }
    imageData_x.updateImage(0, new_state3)
    expect((imageData_x.getPictures[0]).toEqual(new_state3))
})

// *********** STORE SURVEY TESTS *********** //

// Generate new dict of preferences for user
user_x.Preferences = {}

// inputs are clothing_ID, lower_bound, upper_bound
var add_prefPairs = [
    // NOTE: clothing_ID validation happens in Clothing class

    // valid
    [[0, 10, 25], true], 

    // invalid, lower bound below lowest allowed temp
    [[1, -20, 25], false],

    // invalid, upper bound above highest allowed temp
    [[2, 35, 145], false],

    // invalid, lower bound greater than upper bound
    [[3, 65, 25], false]
]

test("addPrefPairs", () => {
    for (testCase of add_prefPairs) {
        expect(user_x.Preferences.addPair(testCase[0])).toEqual(testCase[1])
    }
})

user_x.Preferences.addPair(0, 10, 25);

// inputs are clothing_ID, lower_bound, upper_bound
var update_prefPairs = [
    // NOTE: clothing_ID validation happens in Clothing class

    // valid
    [[0, 10, 35], true], 

    // invalid, lower bound below lowest allowed temp
    [[0, -20, 25], false],

    // invalid, upper bound above highest allowed temp
    [[0, 35, 145], false],

    // invalid, lower bound greater than upper bound
    [[0, 65, 25], false]
]

test("updatePrefPairs", () => {
    for (testCase of update_prefPairs) {
        expect(user_x.Preferences.updatePair(testCase[0])).toEqual(testCase[1])
    }
})




