# Simple Django Web Application(Wise)

`Docker` `Nginx` `PostgreSQL` `Gunicorn` `Django 4.2`

## Overview

This is a simple Django web application that allows users to:

- Register an account.
- Explore text-based posts created by other users.
- Add posts to their favorites.
- Write and manage their own posts.

# Run

1. Set corect path to volume with static files in compose file for web and nginx container.
2. Navigate to the project root folder.
3. Execute: `docker compose up --build`
4. Open `0.0.0.0:8001` in browser.