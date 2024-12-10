# DUAN project written in django python

Goal: familiarize with django MPA application

Demo: [valeriimon.pythonanywhere.com](https://valeriimon.pythonanywhere.com/)

## Installation

1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Create an sqlite DB file with correct name in according to setting.py
```bash
touch db.sqlite3
```

3. Run migration
```bash
python manage.py migrate
```

4. Start a server
```bash
python manage.py runserver
```

## [TESTING] Fake portal content

```bash
python manage.py generate --help # Cmd to generate portal data

python manage.py userscreds --help #Cmd to see generated users credentials to go over the portal
```

## License

[MIT](https://choosealicense.com/licenses/mit/)