db.auth('mongo_user', 'mongo_password')

// Create development database and user
db = db.getSiblingDB('dev_db')
db.createUser({
  user: 'dev_user',
  pwd: 'dev_password',
  roles: [{ role: 'readWrite', db: 'dev_db' }]
})

// Create test database and user
db = db.getSiblingDB('test_db')
db.createUser({
  user: 'test_user',
  pwd: 'test_password',
  roles: [{ role: 'readWrite', db: 'test_db' }]
})
