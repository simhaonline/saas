/**
 * create application user
 * run as user with superuser privilege
 */
create role saas_app_usr login password 'saas_app_pw';

grant select, insert, update, delete on all tables in schema iam to saas_app_usr;
grant all privileges on database saas to saas_app_usr;
grant all privileges on all tables in schema iam to saas_app_usr;
grant execute on all functions in schema iam to saas_app_usr;