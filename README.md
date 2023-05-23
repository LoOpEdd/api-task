# Overview

The goal of this task is to create a reliable python HTTP-based API client. The API endpoint given in the task is taken from the OpenAPI database and offers data that is not significant to Kaufland, but includes the same general requirements used in any proprietary API endpoint and therefore is a good sandbox for client application development.

# Task description

1. The Star Wars open API database (documentation available at https://swapi.dev/documentation) contains records on planets, pilots and ships in the Star Wars universe. Assuming for the purpose of this exercise that a pilot always used the same starships for their travels, write an application that shows if a starship with a given name has been to more than one planet (i.e. if their pilots have lived on more than one planet) and list the names of those planets.

2. The website https://sunrisesunset.io/api/ offers an API endpoint which gives information about sunrise and sunset times for given geo-coordinates. Write a simple API client that will allow the users to supply the name of a city (as a command-line argument or any other way) and a number denoting a year, and as a response get the difference between the earliest and the latest sunrise during that year. Since the API endpoint requires a latitude and longitude, obtain those by querying the API available at https://developers.teleport.org/api/.

# Special requirements:

Create a HTTPConnection class that will encapsulate all functionalities required by the caller (different HTTP methods, supplying additional headers or query parameters if needed etc.). Use any HTTP library you prefer.

Some API endpoints may have rate limits on the number of requests per second or other similar limitations. Regardless of the additional constraints, the solution needs to be able to respond to HTTP 429 errors (Too many requests) and implement a retry handler that resends the request after a backoff period. The initial backoff period is 30 seconds, but it needs to grow if the next request hits the same error again using the formula 30*2n (where n is the current attempt number). If there is at least one successful attempt between two errors, the backoff timer starts from the beginning.


# Notes:

The application should be as simple as possible

Wherever it makes sense, try using an efficient approach (example: try not to scrape the entire destination API endpoint and keep the content in local memory if that is not required for the next step). Design approaches will be discussed during the task review.

In our upcoming interview you will have a chance to go through the solution step by step and discuss your design decisions with the  team. The solution should be prepared in a form where it can be executed multiple times (preferably in an IDE that can be watched through screen-sharing)