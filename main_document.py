from mongoengine import *

from datetime import datetime
import os # To create binary password.
import json

connect("mongo-dev-db") # Connect to the db.

# Defining documents/schemas.

# The collection is whatever the name of the class you give.
class User(Document):
    username = StringField(unique=True, required=True)
    email = EmailField(unique=True)
    password = BinaryField(unique=True)
    age = IntField()
    bio = StringField(max_length=100)
    categories = ListField()
    admin = BooleanField(default=False) # Everytime we create a new doc, admin will be set to false by default.
    registered = BooleanField(default=False) # We want to explicitly tell our database if the user is registered.
    date_created = DateTimeField(default=datetime.utcnow)

    def json(self):
        user_dict = {
            "username": self.username,
            "email": self.email,
            "age": self.age,
            "bio": self.bio,
            "categories": self.categories,
            "admin": self.admin,
            "registered": self.registered
        }
        return json.dumps(user_dict)
    
    meta = {
        "indexes": ["username", "email"], # To perform faster lookups.
        "ordering": ["-date_created"] # Order in desc fasion by default.
    }
    
# Dynamic Document

class BlogPost(DynamicDocument):
    title = StringField()
    content = StringField()
    author = ReferenceField(User)
    date_created = DateTimeField(default=datetime.utcnow)

    meta = {
        "indexes": ["title"],
        "ordering": ["-date_created"]
    }

# Save a Document

user = User(
    username="JohnHammond",
    email="jhammond@gmail.com",
    password=os.urandom(16),
    age=67,
    bio="Jurassic Park!",
    admin=True
).save()

BlogPost(
    title="My First Blog Post!",
    content="MongoDB and Python is Awesome!",
    author=user,
    tags=["Python", "MongoDB", "MongoEngine"],
    category="MongoDB"
).save()

print("Done")