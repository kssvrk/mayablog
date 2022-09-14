pkill -f gunicorn
gunicorn --name=mayagram --pythonpath=~/mayaenv/bin/  --bind 0.0.0.0:8000 blog.wsgi:application --workers=4  --worker-class=gthread