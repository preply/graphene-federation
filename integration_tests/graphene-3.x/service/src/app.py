import logging
import os
import sys
from fastapi import FastAPI
from importlib import import_module
from starlette.routing import Route
from starlette_graphene3 import GraphQLApp, make_graphiql_handler


logging.basicConfig(
    format="[%(asctime)s] %(levelname)-5s (%(name)s): %(message)s",
    level=logging.DEBUG
)

logger = logging.getLogger("graphene_federation")


def create_app():
    """Creates the FastAPI app
    """
    logger.info(f"Creating service application for integration tests...")
    app = FastAPI()

    schema_config = os.getenv("GRAPHENE_FEDERATION_INTEGRATION_TEST_SERVICE")
    route = get_route(schema_config)
    app.routes.append(route)
    return app


def get_route(schema_config):
    schema = load_schema(schema_config)

    if not schema:
        raise RuntimeError(f"Unable to load schema for service configuration: {schema_config}")
    logger.debug(f"GraphQL Schema Registered:\n\n{schema}")
    return Route("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))


def load_schema(schema_config):
    """
    """
    logger.info(f"Loading schema: {schema_config}")
    if not schema_config:
        raise RuntimeError(f"Schema configuration not valid.")

    schema_config_path = f"schemas.{schema_config}"
    get_schema_func = "get_schema"
    try:
        module = import_module(schema_config_path)
        
        get_schema = getattr(module, get_schema_func)
        return get_schema()
    except AttributeError as err:
        raise ImportError(f'Module "{schema_config}" does not define a "{get_schema_func}" function') from err


def dump_app(app):
    print(f"")
    print(f"========================= FASTAPI =========================")
    print(f"")
    print(f"Path       ::  {sys.path}")
    print(f"PYTHONPATH ::  {os.getenv('PYTHONPATH')}")
    print(f"SCHEMA     ::  {os.getenv('GRAPHENE_FEDERATION_INTEGRATION_TEST_SERVICE')}")
    print(f"")
    print(f"{repr(app)}")
    print(f"")


app = create_app()
dump_app(app)

@app.post("/graphql")
async def graphql():
    return {}