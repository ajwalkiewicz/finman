.PHONY: publish

publish: scripts/publish.sh
	@echo "publishing changes..."
	./scripts/publish.sh