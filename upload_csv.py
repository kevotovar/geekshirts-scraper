import pandas
import os
from graphqlclient import GraphQLClient
from dotenv import load_dotenv

client = GraphQLClient(os.getenv("GRAPHQL_URL"))
client.inject_token("JWT {}".format(os.getenv("JWT_TOKEN")))

shirts = pandas.read_csv("aditivo-playeras-caballero.csv")
