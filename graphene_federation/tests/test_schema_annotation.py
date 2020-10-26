from graphql import graphql

from graphene import ObjectType, ID, String, NonNull, Field

from ..entity import key
from ..extend import extend, external
from ..main import build_schema

# ------------------------
# User service
# ------------------------
users = [
    {"user_id": "1", "name": "Jane", "email": "jane@mail.com"},
    {"user_id": "2", "name": "Jack", "email": "jack@mail.com"},
    {"user_id": "3", "name": "Mary", "email": "mary@mail.com"},
]

@key("user_id")
@key("email")
class User(ObjectType):
    user_id = ID(required=True)
    email = String(required=True)
    name = String()

    def __resolve_reference(self, info, *args, **kwargs):
        if self.id:
            user = next(filter(lambda x: x["id"] == self.id, users))
        elif self.email:
            user = next(filter(lambda x: x["email"] == self.email, users))
        return User(**user)

class UserQuery(ObjectType):
    user = Field(User, user_id=ID(required=True))

    def resolve_user(self, info, user_id, *args, **kwargs):
        return User(**next(filter(lambda x: x["user_id"] == user_id, users)))

user_schema = build_schema(query=UserQuery)

# ------------------------
# Chat service
# ------------------------
chat_messages = [
    {"id": "1", "user_id": "1", "text": "Hi"},
    {"id": "2", "user_id": "1", "text": "How is the weather?"},
    {"id": "3", "user_id": "2", "text": "Who are you"},
    {"id": "4", "user_id": "3", "text": "Don't be rude Jack"},
    {"id": "5", "user_id": "3", "text": "Hi Jane"},
    {"id": "6", "user_id": "2", "text": "Sorry but weather sucks so I am upset"},
]

@extend("user_id")
class ChatUser(ObjectType):
    user_id = external(ID(required=True))

class ChatMessage(ObjectType):
    id = ID(required=True)
    text = String()
    user_id = ID()
    user = NonNull(ChatUser)

    def resolve_user(self, info, *args, **kwargs):
        return ChatUser(user_id=self.user_id)

class ChatQuery(ObjectType):
    message = Field(ChatMessage, id=ID(required=True))

    def resolve_message(self, info, id, *args, **kwargs):
        return ChatMessage(**next(filter(lambda x: x["id"] == id, chat_messages)))

chat_schema = build_schema(query=ChatQuery)

# ------------------------
# Tests
# ------------------------

def test_user_schema():
    """
    Check that the user schema has been annotated correctly
    and that a request to retrieve a user works.
    """
    assert str(user_schema) == """schema {
  query: Query
}

type Query {
  user(userId: ID!): User
  _entities(representations: [_Any]): [_Entity]
  _service: _Service
}

type User {
  userId: ID!
  email: String!
  name: String
}

scalar _Any

union _Entity = User

type _Service {
  sdl: String
}
"""
    query = """
    query {
        user(userId: "2") {
            name
        }
    }
    """
    result = graphql(user_schema, query)
    assert not result.errors
    assert result.data == {"user": {"name": "Jack"}}

def test_chat_schema():
    """
    Check that the chat schema has been annotated correctly
    and that a request to retrieve a chat message works.
    """
    assert str(chat_schema) == """schema {
  query: Query
}

type ChatMessage {
  id: ID!
  text: String
  userId: ID
  user: ChatUser!
}

type ChatUser {
  userId: ID!
}

type Query {
  message(id: ID!): ChatMessage
  _entities(representations: [_Any]): [_Entity]
  _service: _Service
}

scalar _Any

union _Entity = ChatUser

type _Service {
  sdl: String
}
"""
    query = """
    query {
        message(id: "4") {
            text
            userId
        }
    }
    """
    result = graphql(chat_schema, query)
    assert not result.errors
    assert result.data == {"message": {"text": "Don't be rude Jack", "userId": "3"}}



# Test type with external field also used in a connection
# Test type with 2 similar looking names
# test camel case situation
# test basic case for extend/external/provides

# Add unit testing
# Add linting (black, flake)
# Add typing
