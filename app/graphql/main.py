from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .schema import schema_graphql  

app = FastAPI()
# Create a GraphQL router instance using our schema
graphql_app = GraphQLRouter(schema_graphql)
app.include_router(graphql_app, prefix="/graphql")
