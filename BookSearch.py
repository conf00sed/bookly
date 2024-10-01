import requests, json

key = "AIzaSyBBbSjYsW7FBpzIZmpsbw4lUVzJ8GtdPGo"
url="https://www.googleapis.com/books/v1/volumes"



def searchBook(title):
    resp = []

    title=title
    query= f"q={title}"

    response = requests.get(url, params=query).json()

    # Ideal Book Parameters
    parameters = ['title', 'authors', 'pageCount']
    for book in response["items"]:
        bookProperties = {}

        for parameter in parameters:
            try:
                bookProperties[parameter] = book['volumeInfo'][parameter]

            except: pass

        try:
            bookProperties['description'] = book['volumeInfo']['description'][0:750]
            bookProperties['img'] = book['volumeInfo']['imageLinks']['thumbnail']

        except: pass

        # Append Succesful Parameters
        resp.append(bookProperties)
    
    # Return Collected Book Data
    return resp


