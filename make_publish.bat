@echo off
git fetch
git pull
git submodule update
pipenv run invoke preview
git push --recurse-submodules=on-demand