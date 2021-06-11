# Integration Test

This is an integration test that have for purpose to check that the library creates schemas that are compatible between each other and can be federated in a single gateway schema.

It first try to bring up the four separate services (a, b, c, d) and check that they are brought up successfully by polling the `/graphql` url to retrieve the schema.

Once those are up and running the federation service is brought up and we check that it manages to aggregates all schemas into one.

Finally the test service is brought up and does a few requests to the few services to check they act as intended.
