from pymongo import MongoClient
from neo4j import GraphDatabase
from decouple import config
import redis

def init_mongo():
    mongo_uri = config("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["talentum_demo"]
    return client, db

def init_neo4j():
    driver = GraphDatabase.driver(
        config("NEO4J_URI"),
        auth=(config("NEO4J_USER"), config("NEO4J_PASSWORD"))
    )
    return driver

def init_redis():
    redis_url = config("REDIS_URL", default="redis://localhost:6379")
    return redis.from_url(redis_url, decode_responses=True)

def close_connections(mongo_client, neo4j_driver, redis_client):
    mongo_client.close()
    neo4j_driver.close()
    redis_client.close()

mongo_client, db = init_mongo()
neo4j_driver = init_neo4j()
redis_client = init_redis()