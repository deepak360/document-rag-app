# create postgres db from terminal

```bash
show psql query editor = sudo -u postgres psql
Create DB = create database online_course;
CREATE USER newuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE "ragdb" to newuser;
GRANT CREATE ON SCHEMA public TO newuser;
GRANT USAGE ON SCHEMA public TO newuser;
ALTER SCHEMA public OWNER TO newuser;
ALTER SCHEMA public OWNER TO newuser;
ALTER DATABASE ragdb OWNER TO newuser;
```


##  Commands to play with postgres
```bash
List All database = \l
Use database = \c online_course
Show All Tables = \d
List of all tables = \dt
Describe Table = \d table_name or \d+ table_name
Quit from query = \q
Help commands = \?
```
##  Insert Queries
```bash
INSERT INTO api_category(name,slug,is_active,created_at,updated_at)values
('Uncategorized','uncategorized',True,now(),now());
select * from api_category limit 1;
truncate table api_category;
truncate table api_category cascade; //related table
truncate table api_posts_post_categories restart identity;//index start from 1
truncate table api_category restart identity cascade;
```

##  PgAdmin Query
```bash
SELECT *
FROM information_schema.columns
WHERE table_name = 'api_category';
INSERT INTO api_category(name,slug,is_active,created_at,updated_at)values
('Uncategorized','uncategorized',True,now(),now());
select * from api_category limit 1;
```

##  Error 1
```bash
Error: django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 or psycopg module
Solution: pip3 install psycopg2-binary
```

##  Error 2
```bash
Error-: Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5432 -> 0.0.0.0:0: listen tcp 0.0.0.0:5432: bind: address already in use

Solution:-
sudo lsof -i :5432
sudo netstat -tuln | grep 5432
sudo systemctl stop postgresql
```