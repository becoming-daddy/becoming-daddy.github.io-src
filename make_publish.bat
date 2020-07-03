@echo off
pipenv run invoke gh_pages
git fetch
git pull
git submodule update
git push --recurse-submodules=on-demand