
#vars
VERSION=$(shell ./version.py)

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

clean: ## Clean all dev data
	@echo "Removing dev and distribution data..."
	@rm -rf dist/* build/* src/scanoss*.egg-info src/*.so

dev_setup:  ## Setup Python dev env for the current user
	@echo "Setting up dev env for the current user..."
	pip3 install -e .

dev_uninstall:  ## Uninstall Python dev setup for the current user
	@echo "Uninstalling dev env..."
	pip3 uninstall -y scanoss_winnowing
	@rm -rf src/scanoss*.egg-info

src_dist: clean dev_uninstall  ## Build the source distribution
	@echo "Build source package for distribution $(VERSION)..."
	python3 -m build --sdist

dist: clean dev_uninstall  ## Prepare Python package into a distribution
	@echo "Build deployable package for distribution $(VERSION)..."
	python3 -m build
	twine check dist/*

publish_test:  ## Publish the Python package to TestPyPI
	@echo "Publishing package to TestPyPI..."
	twine upload --repository testpypi dist/*

publish:  ## Publish Python package to PyPI
	@echo "Publishing package to PyPI..."
	twine upload dist/*

package_all: dist publish  ## Build & Publish Python package to PyPI
