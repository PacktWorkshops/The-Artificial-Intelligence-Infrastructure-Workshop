#!/bin/bash

# exit immediately if a command exits with a non-zero exit status
set -e

# check our RDS instances
echo "Amazon RDS instances:"
aws rds describe-db-instances

# use client to talk to your MySQL instance
mysql --host ${Endpoint.Address} --port ${Endpoint.Port} -u ${MasterUsername} -p

# show databases
show databases;

# use our database "chapter10"
use chapter10;

# show tables;
show tables;

# exit
exit