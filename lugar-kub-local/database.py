from orator import DatabaseManager
config = {
    'pgsql': {
        'driver': 'pgsql',
        'host': 'localhost',
        'database': 'homestead',
        'user': 'homestead',
        'password': 'secret',
        'prefix': '',
        'port': '5432'
    }
}
db = DatabaseManager(config)
