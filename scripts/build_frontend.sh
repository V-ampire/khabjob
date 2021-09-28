#!/bin/bash

cd frontend
npm run build
sudo service nginx restart