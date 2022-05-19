import json #imports json library
class JSONHelper(): #creates an object
    def __init__(self, filename): #each object is a file
        self.filename = filename #saves the filename
        try:
            with open(self.filename) as self.json_file: #opens the file as self.json_file
                self.json_data = json.load(self.json_file) #converts the data to dictionary
        except (OSError, ValueError) as error:
            return error
        return

    def reload_data(self): #gets the new data
        try:
            with open(self.filename) as self.json_file: #same process as __init__()
                self.json_data = json.load(self.json_file)
        except (OSError, ValueError) as error:
            return error
        return self.json_data #returns the new data
    
    def write_data(self, data): #update JSON data
        json_string = json.dumps(data) #converts to string
        try:
            with open(self.filename, 'w') as f:
                f.write(json_string) #writes the provided data to file
                self.json_data = data
        except (OSError, ValueError) as error:
            return error
        return self.json_data

#usage
if __name__ == '__main__':
    JSONFile = JSONHelper('filename.json')
    new_data = {"This":"is", "a": "test"}
    print(JSONFile.write_data(new_data))