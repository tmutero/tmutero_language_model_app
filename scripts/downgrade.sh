#!/bin/bash
docker-compose exec app alembic downgrade "-1"
