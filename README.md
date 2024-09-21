# Coding-Assignment-DLO
Job interview coding assignment "DLO"

The application runs in a Docker container. To get started, you need to place
a file containing the secret shared key (that you provided to me via email) next to
the Docker files. The filename must be *shared_key_secret.env*:
```
coding-assigment-dlo/
├── Dockerfile
├── docker-compose.yaml
├── shared_key_secret.env # Place file here 
```

The containers can now be run. There are two modes available: one to run
the application and one to run all tests in the container:
- Run the Django application: ```docker compose up django```
- Run all tests in docker: ```docker compose up pytest```

Some of the tests can also be run locally in a virtualenv, but since
the secret is not available there, the network-based tests will fail.

When the Django container is running, its interface can be accessed at
[http://127.0.0.1:8000](http://127.0.0.1:8000).

On the interface you will find buttons showcasing the implementation.
