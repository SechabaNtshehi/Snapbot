import requests



class Querier:
    def __init__(self):
        self.api_url = "http://localhost:8080"

    def query_image_coordinates(self):
        api_image_coordinates = self.api_url + "/image-coordinates"
        response = requests.get(api_image_coordinates)
        response = response.json()
        print(response)
        return response

    def set_next_location(self, _location):
        api_new_location = self.api_url + "/toggle-location"
        location = {"location" : _location}
        response = requests.put(api_new_location, params = location)
        response = response.json()
        print(response)
        return response

    def add_location(self, new_location):
        new_location = self.api_url + "/add-location"
        response = requests.post(new_location, json = new_location)
        print(response)
        return response

    def delete_location(self, _location):
        location = {"location" : _location}
        delete_endpoint = self.api_url + "/remove-location"
        response = requests.delete(delete_endpoint, params = location)
        response = response.json()
        print(response)
        return

    def query_location_name(self, index):
        get_location = self.api_url + "/get-location"+str(index)
        response = requests.get(get_location)
        response = response.json()
        print(response)
        return response

    def query_number_of_locations(self):
        get_number_of_location = self.api_url + "/get-number-of-locations"
        response = requests.get(get_number_of_location)
        response = response.json()
        print(response)
        return response


