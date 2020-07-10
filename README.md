Basic app to store your favourite music. Built in VueJS for the frontend and Django as the backend restful API.

Steps to use

1. Clone the project
2. In the `jazz` directory, create a `local_settings.py` and add settings for DEBUG, DATABASES, and a SECRET_KEY.
3. In the `frontend` directory, run `npm install` and `npm run dev` from a terminal window to start the VueJS frontend.
4. In another terminal, run `python manage.py runserver` to start the Django API webserver.
5. Go to http://localhost:8080/#/music in your browser to start the app.