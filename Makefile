train-core:
	python -m rasa_core.train -d domain.yml -s data/stories.md -c config.yml -o models/dialogue
run-action:
	python -m rasa_core_sdk.endpoint --actions actions
run-telegram:
	python -m rasa_core.run -d models/dialogue -u models/current/nlu  --endpoint endpoints.yml --port 5002 --credentials credentials.yml
run-debug:
	python -m rasa_core.run -d models/dialogue -u models/current/nlu  --endpoint endpoints.yml  --debug
graph:
	python -m rasa_core.visualize -d domain.yml -s data/stories.md -o graph.html -c config.yml
