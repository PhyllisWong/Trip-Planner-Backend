import json
from bson.objectid import ObjectId

# Thanks to http://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
class JSONEncoder(json.JSONEncoder):
    """Custom JSONEncoder that extracts the strings from MongoDB ObjectIDs."""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
