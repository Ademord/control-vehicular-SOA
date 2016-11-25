from orator import DatabaseManager
config = {
    'pgsql': {
        'driver': 'pgsql',
        'host': 'localhost',
        'database': 'homestead',
        'user': 'homestead',
        'password': 'secret',
        'prefix': '',
        'port': '54320'
    }
}
db = DatabaseManager(config)
