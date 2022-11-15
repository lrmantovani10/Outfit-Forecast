# Outfit-Forecast

An app to generate outfit predictions based on one's wardrobe and current weather.

Current class diagram
![Class Diagram](class-diagrams/updatedClassDiagram4.png)

<ins>Test suite used:</ins> unittest (https://docs.python.org/3/library/unittest.html)

<ins>Directory Structure:<ins>

For milestones 4a and 4b, our new code will be in the directory 4ab

<ins>How to compile:</ins> No need to compile!

<ins>How to run code:</ins>

cd 4ab

python3 backend_functions.py

<ins>How to run the unit test cases:</ins>

run 'make setup' to download the requirements needed

run 'make tests' to run tests

<ins>Plan for 2nd iteration (backend only):<ins>

- Implement prevention of outfit repetition --> in dailyRecommender() it will look at thhe 3 most recent outfits in clothingHistory list and make sure not to output them
- Allowing user to accept/decline an outfit --> we are creating a rejected outfits list as part of the User class, if the user has rejected an outfit, dailyRecommender will rerun and add that outfit to the rejected list and create a new outfit to output
- Improve classifyNew() --> improve the way classifyNew() classifies images, including using object detection in addition to label detection. Object detection will be used for classification (it seems to have less margin of error in classifying correctly), and label detection is more specific so it will be used for the objectName

<ins>What we are not implementing and why:<ins>

"Stop making suggestions that user has denied for certain weather" --> Originally our plan was if a user rejects an outfit on a certain weather, in the future when that weather comes up again, we would weigh that outfit less (the probability of recommending that outfit is lower than other outfits). We decided not to implement this because if a user declines an outfit, it could be because of multiple reasons not due to the weather (they didn't feel like wearing that outfit that day, etc).

<ins>Work division:<ins>

Gautam and Perene: improving classifyNew(), work with frontend to make sure endpoints are being called correctly, writing tests for classifyNew() and dailyRecommender()

Leo and Daniel: 




