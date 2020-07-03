@echo off
pipenv run invoke preview
git fetch
git pull
git submodule update
git push --recurse-submodules=on-demand