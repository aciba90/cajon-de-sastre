# Words API

Solution to the Plytix problem. This API stores a list of words with position
and is able to retrieve anagrams of seen or not seen word.

We use a Ports and Adapters architecture to isolate the core/domain, data,
entrypoints and service layers. By assuming this complexity we gain maintainability, extensibility and testability.

## Execution

Install docker, docker-compose and make. Run

```sh
make up
```

and go to [http://localhost:5000](http://localhost:5000).

## Development

Use the make targets to execute different tools as the formater, linters, tests within
your virtual env or within a docker container:

```sh
docker-compose run api bash
# or
source ./venv/bin/activate

make format
make format_check lint d_test
```

* Black and isort for code formatting.
* Flake8 and Pylint for style, documenation, complexity and
simple coding errors checks.
* Mypy for static type analysis.

## Things to improve

* Atm the e2e tests run againts the development db (droping it). Make this injectable
and use a different one for testing.

* More tests per layer (core, service, adapters)

* Production stuff (Gunicorn, etc)

* CI / CD

* For the shake of simplicity we implementd a collection array to store the
words and a hand made optimistic loking solution to avoid concurrent updates.
We could improve this by using
  * The multidocument transaction feature of Mongo
  * Or by laying out the data with in a single document in a collection with an embedded
  array containing the words and using the transaction Mongo feature
  * With both previous approaches we could implement an Aggregate Entity in our core
  layer to handle updates of the words as a whole.

* If the domain becomes very complex or if this API is going to be hooked into
a microservice context we could refactor the service layer to an architecture driven by
commands, events and a message bus.
  * The entrypoints (only Flask atm) instead of consuming
  the service layer, would inject commnads in an internal message bus. The message bus
  would execute those commands with command handlers. Those command handlers could create
  an publish events to external message brokers and other microservices could subscribe
  themselves to those events.
  * Conversely, this service could subscribe itself to other external events and
  react to them by injecting subsecuent commands to the bus (This would be another
  entrypoint).
