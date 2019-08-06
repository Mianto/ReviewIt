# ReviewIt
Analyzes reviews gatherrd by clients for their products

# Install Dependencies
```
	virutualenv myenv && pip install -r requirements.txt
```

# Run Server

```
	python run.py runserver
```

# Database Initialization

```
	python run.py db init
```

# Database Generate Migration

```
	python run.py db migrate
```

# Database Generate Upgrade

```
	python run.py db upgrade
```

Read [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/), [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) for more details

Also checkout ```config.py``` for configuration details