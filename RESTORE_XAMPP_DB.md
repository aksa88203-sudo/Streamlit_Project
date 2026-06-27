# XAMPP / phpMyAdmin Restore

Project ki database config abhi yeh expect karti hai:

- Database: `inventory_db`
- MySQL user: `app_user`
- MySQL password: `3910e6ab912647bfa50e82712088bf6e`

## Option 1: phpMyAdmin se restore

1. XAMPP me `Apache` aur `MySQL` start karein.
2. `http://localhost/phpmyadmin` kholen.
3. `Import` tab me jaa kar pehle [restore_inventory_db_schema.sql](./restore_inventory_db_schema.sql) import karein.
4. Agar app ko demo products aur demo sales bhi chahiye hon, to uske baad [restore_inventory_db_demo_data.sql](./restore_inventory_db_demo_data.sql) import karein.

## Option 2: sirf database/user banao, baqi backend khud bana dega

Is project me backend startup par `AUTO_CREATE_TABLES=True` hai aur `admin/admin` user auto-create hota hai.

1. phpMyAdmin ke SQL tab me schema file ka sirf database/user wala hissa run karein.
2. Backend start karein.
3. Backend `users`, `products`, `sales`, aur `items` tables khud create kar dega.

## Important

- Project me koi original `.sql` backup file nahi mili.
- `restore_inventory_db_demo_data.sql` original lost data nahi hai; yeh project ke demo UI ke liye recreated sample data hai.
- Agar aap ke paas purana `xampp/mysql/data/inventory_db` folder ya koi `.sql` export kahin aur saved ho, to wahi aapka real data restore karega.
