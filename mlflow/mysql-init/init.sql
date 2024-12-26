-- Grant access to ${MYSQL_USER} from any host
GRANT ALL PRIVILEGES ON *.* TO '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';

-- Grant root access from any host (optional)
-- GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';

-- Apply changes
FLUSH PRIVILEGES;
