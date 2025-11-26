from flask import Flask, make_response, request

app = Flask(__name__)

data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]

@app.route("/")
def index():
    """
    Handles the root path of the application.

    Returns:
        str: A simple "hello world" greeting.
    """
    return "hello world"

@app.route("/no_content")
def no_content():
    """
    Handles the '/no_content' path, demonstrating a 204 No Content response.

    This endpoint returns a JSON-like body along with a 204 status code.
    While a 204 response typically should not have a body, some frameworks
    allow it, or it may be used to illustrate returning an empty response.

    Returns:
        tuple[dict, int]: A tuple containing a dictionary (the response body,
                         though it's typically ignored by clients for a 204)
                         and the HTTP status code (204).
    """
    return ({"message": "No content found"}, 204)

@app.route("/exp")
def index_explicit():
    """Return 'Hello World' message with a status code of 200.
    Returns:
        response: A response object containing the message and status code 200.
    """
    resp = make_response({"message": "Hello World"})
    resp.status_code = 200
    return resp

@app.route("/data")
def get_data():
    """
    Checks the status of the 'data' list and returns a status message.

    Returns:
        tuple[dict, int]: A tuple of a JSON message and an HTTP status code.
                          - 200: Data found, message includes its length.
                          - 500: Data list is empty.
                          - 404: 'data' variable is not defined (NameError).
    """
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}

        return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

@app.route("/name_search")
def name_search():
    """
    Searches the 'data' list for a person whose first name contains the query string.

    The search is case-insensitive.

    Query Parameters:
        q (str): The search query string for a first name.

    Returns:
        tuple[dict, int]: A tuple of a JSON response body and an HTTP status code:
                          - 200: Found person dictionary.
                          - 400: Query parameter 'q' is missing.
                          - 422: Invalid input (empty string or only digits).
                          - 404: Person not found.
    """
    query = request.args.get("q")

    if query is None:
        return {"message": "Query parameter 'q' is missing"}, 400

    if query.strip() == "" or query.isdigit():
        return {"message": "Invalid input parameter"}, 422

    for person in data:
        if query.lower() in person["first_name"].lower():
            return person, 200
    return {"message": "Person not found"}, 404

@app.route("/count")
def count():
    """
    Returns the total number of items in the 'data' list.

    Returns:
        tuple[dict, int]: A tuple of a JSON response and an HTTP status code:
                          - 200: Successful count.
                          - 500: 'data' variable is not defined (NameError).
    """
    try:
        return {"data count": len(data)}, 200
    except NameError:
        return {"message": "data not defined"}, 500

@app.route("/person/<var_name>")
def find_by_uuid(var_name):
    """
    Finds a person in the 'data' list by their UUID (ID).

    Path Parameters:
        var_name (str): The UUID (ID) of the person to find.

    Returns:
        tuple[dict, int]: A tuple of a JSON response and an HTTP status code:
                          - 200: Found person dictionary.
                          - 404: Person not found.
    """
    for person in data:
        if person["id"] == str(var_name):
            return person
    return {"message": "Person not found"}, 404

@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):
    """
    Deletes a person from the 'data' list by their UUID (ID).

    Path Parameters:
        id (uuid): The UUID (ID) of the person to delete.

    Returns:
        tuple[dict, int]: A tuple of a JSON message and an HTTP status code:
                          - 200: Successful deletion.
                          - 404: Person not found.
    """
    for person in data:
        if person["id"] == str(id):
            data.remove(person)
            return {"message": f"Person with ID {id} deleted"}, 200
    return {"message": "Person not found"}, 404

@app.route("/person", methods=['POST'])
def add_by_uuid():
    """
    Adds a new person dictionary to the 'data' list.

    The new person object is expected to be in the JSON request body.

    Returns:
        tuple[dict, int]: A tuple of a JSON response and an HTTP status code:
                          - 200: Successful addition, message contains the new person's ID.
                          - 422: Invalid input (no JSON body provided).
                          - 500: 'data' variable is not defined (NameError).
    """
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500

    return {"message": f"{new_person['id']}"}, 200

@app.errorhandler(404)
def api_not_found():
    """
    Custom error handler for 404 Not Found errors across the application.

    Args:
        error: The exception object (automatically passed by Flask).

    Returns:
        tuple[dict, int]: A tuple of a JSON error message and the 404 status code.
    """
    return {"message": "API not found"}, 404
