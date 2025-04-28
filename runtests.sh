#!/bin/bash

# Run tests with coverage
coverage run manage.py test

# Generate coverage report
coverage report

# Generate HTML report (optional)
# coverage html

echo "Test run complete!"