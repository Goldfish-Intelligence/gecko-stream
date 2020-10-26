#!/bin/bash
cp out/* ../gh-page/
cd ../gh-page/
git add *
git commit -m "Update website by Kamerakind"
git push --force