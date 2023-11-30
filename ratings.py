# Allows you to get the ratings of a professor from RateMyProfessors.com
# Makes a request to the RateMyProfessors GraphQL API
# I found out that the GraphQL API is used by inspecting the network tab in the browser

import requests
from helpers import send_request

DREXEL_RMP_ID = "U2Nob29sLTE1MjE="
AUTHORIZATION_HEADER = "Basic dGVzdDp0ZXN0"


def search_professors(professor_name):
    query = """query searchProf($query: TeacherSearchQuery!){
        newSearch {
            teachers(query: $query) {
                edges {
                    node {
                        id
                        firstName
                        lastName
                        department
                    }
                }
            }
        }
    }"""

    variables = {
        "query": {
            "text": professor_name,
            "schoolID": DREXEL_RMP_ID
        }
    }

    response = send_request(
        requests.Session(),
        "https://www.ratemyprofessors.com/graphql",
        "POST",
        json={"query": query, "variables": variables},
        headers={
            "Authorization": AUTHORIZATION_HEADER
        })

    return response.json()["data"]["newSearch"]["teachers"]["edges"]


def get_ratings(id):
    query = """query TeacherRatingsPageQuery($id: ID!){
        node(id: $id) {
            __typename
            ... on Teacher {
                avgRating
                avgDifficulty
                numRatings
                legacyId
            }
        }
    }"""

    variables = {
        "id": id
    }

    response = send_request(
        requests.Session(),
        "https://www.ratemyprofessors.com/graphql",
        "POST",
        json={"query": query, "variables": variables},
        headers={
            "Authorization": AUTHORIZATION_HEADER
        })
    
    return response.json()["data"]["node"]


def rating(professor_name):
    professor = search_professors(professor_name)

    if len(professor) == 0:
        return None

    professor_id = professor[0]["node"]["id"]

    ratings = get_ratings(professor_id)

    if ratings is None:
        return None

    del ratings["__typename"]

    if ratings["numRatings"] == 0:
        return None

    return ratings


if __name__ == "__main__":
    print(rating("Galen Long"))
