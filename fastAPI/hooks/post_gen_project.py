import os
import shutil

database_choice = '{{ cookiecutter.database }}'
package_slug = '{{ cookiecutter.package_slug }}'

db_mongodb_path = os.path.join('src', package_slug, 'data', 'db_mongodb.py')
db_supabase_path = os.path.join('src', package_slug, 'data', 'db_supabase.py')
database_path = os.path.join('src', package_slug, 'data', 'database.py')

if database_choice == 'mongodb':
    if os.path.exists(db_mongodb_path):
        os.rename(db_mongodb_path, database_path)
    if os.path.exists(db_supabase_path):
        os.remove(db_supabase_path)
elif database_choice == 'supabase':
    if os.path.exists(db_supabase_path):
        os.rename(db_supabase_path, database_path)
    if os.path.exists(db_mongodb_path):
        os.remove(db_mongodb_path)

print(f"Project generated with {database_choice} database setup.")
