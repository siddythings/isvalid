from api.settings.mongo import users_collection, wallets_collection
from datetime import datetime
from pytz import utc


class Users:
    @staticmethod
    def get_user_by_username_v2(username):
        """Retrieve a user by their username from MongoDB."""
        user = users_collection.find_one({
            "username": username
        }, {'_id': 0, 'password': 0})
        return user

    @staticmethod
    def get_user_by_user_id(user_id):
        """Retrieve a user by their username from MongoDB."""
        user = users_collection.find_one({
            "id": user_id
        }, {'_id': 0, 'password': 0})
        return user

    @staticmethod
    def get_user_by_username(user_id, username):
        """Retrieve a user by their username from MongoDB."""
        user = users_collection.find_one({
            "id": user_id,
            "username": username
        }, {'_id': 0, 'password': 0})
        return user

    @staticmethod
    def get_user_by_email(email):
        """Retrieve a user by their username from MongoDB."""
        user = users_collection.find_one(
            {"email": email}, {'_id': 0, 'password': 0})
        return user

    @staticmethod
    def update_username(user_id, old_username, new_username):
        """Update the username of a user in MongoDB."""
        result = users_collection.update_one(
            {
                "id": user_id,
                "username": old_username
            },  # Find user with old username
            {
                "$set": {
                    "username": new_username,
                    "updated_at": datetime.now(utc).isoformat()
                }}  # Update with new username
        )
        # Return True if a document was modified
        return result.modified_count > 0

    @staticmethod
    def insert_user(user_object):
        """Insert a new user into the MongoDB collection."""
        user_object.update({
            "created_at": datetime.now(utc).isoformat(),
            "updated_at": datetime.now(utc).isoformat()
        })
        result = users_collection.insert_one(user_object)
        wallet_data = {
            "user_id": user_object.get("id"),
            "balance": 0.0,
            "earnings": 0.0,
            "withdraw": 0.0,
            "created_at": datetime.now(utc).isoformat(),
            "updated_at": datetime.now(utc).isoformat(),
        }
        result = wallets_collection.insert_one(wallet_data)
        # Return the inserted_id of the new user
        return result.inserted_id

    @staticmethod
    def update_user_by_email(email, user_object):
        """Update user into the MongoDB collection."""
        user_object.update({
            "updated_at": datetime.now(utc).isoformat()
        })
        result = users_collection.update_one(
            {"email": email},
            {"$set": user_object}
        )
        # Return True if a document was modified
        return result.modified_count > 0

    @staticmethod
    def update_user_by_username(username, user_object):
        """Update user into the MongoDB collection."""
        user_object.update({
            "updated_at": datetime.now(utc).isoformat()
        })
        result = users_collection.update_one(
            {"username": username},
            {"$set": user_object}
        )
        # Return True if a document was modified
        return result.modified_count > 0

    @staticmethod
    def get_profile_from_username(username):
        result = users_collection.aggregate([
            {
                "$match": {
                    "username": username
                }
            },
            {
                "$lookup": {
                    "from": "products",
                    "let": {"userId": "$id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$eq": ["$user_id", "$$userId"]},
                                        {"$eq": ["$is_deleted", False]},
                                        {"$eq": ["$is_published", True]}
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "products"
                }
            },
            {
                "$lookup": {
                    "from": "links",
                    "localField": "id",
                    "foreignField": "user_id",
                    "as": "links"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "password": 0,
                    "products._id": 0,
                    "links._id": 0
                }
            }
        ]
        )

        results = list(result)[0]
        for product in results.get("products"):
            product['currency'] = results.get("currency")
        return results
