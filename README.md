# README.md

## Project Skeleton in Development
This is a skeleton for a Django project currently under development. Eventually, it will integrate with HTMX, Alpine.js, Bulma, Django Tables 2, and Django Filters. These integrations are not yet implemented.

This project create a base app with a working Alpine.js, HTMX, Bulma, a django table and django filter.


## Functional Development Environment
To get started, create a .env file and set the necessary environment variables. Below is an example of the required .env file.

```
# Django settings
DJANGO_SETTINGS_MODULE=project.settings.local
DEBUG=True
SECRET_KEY='your-secret-key'
ALLOWED_HOSTS='*'

# MySQL settings (production, development)
DB_NAME='your-db-name'
DB_USER='your-db-user'
DB_PASS='your-db-password'
DB_ROOT='your-root-password'
DB_HOST='db'
DB_PORT='3306'

# MySQL settings (local)
DB_LOCAL_NAME='your-local-db-name'
DB_LOCAL_USER='your-local-db-user'
DB_LOCAL_PASS='your-local-db-password'
DB_LOCAL_ROOT='your-local-root-password'
DB_LOCAL_HOST='your-local-db-host'
DB_LOCAL_PORT='3306'

# AWS
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_STORAGE_BUCKET_NAME=your-aws-s3-bucket-name
AWS_S3_REGION_NAME=your-aws-region-name
```

## Instructions for Setup
- Clone the repository.
- Create a .env file in the root directory with the necessary environment variables.
- run ./init.sh
   _take a look into this file to understand what is done: virtual environment, requirements, nginx selfisgned certs and more_
- Build and run the Docker containers using docker-compose up --build.
