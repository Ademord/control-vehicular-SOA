from orator import DatabaseManager
import os
config = {
    'pgsql': {
        'driver': 'pgsql',
        'host': os.environ.get('DATABASE_HOST', 'homestead'),
        'database': os.environ.get('DATABASE_NAME', 'homestead'),
        'user': os.environ.get('DATABASE_USER', 'homestead'),
        'password': os.environ.get('DATABASE_PASSWORD', 'secret'),
        'prefix': '',
        'port': os.environ.get('DATABASE_PORT', '5432')
    }
}
db = DatabaseManager(config)
