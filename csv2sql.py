import csv
import argparse
import importlib
import os

# Lazy imports:
# - MySQLdb for MySQL value escape

# This script reads a CSV file and converts it to a SQL file
# Currently only MySQL syntax is supported.
# It is simple script and does not support fancy things like dates conversion etc.
# It needs proper column names in the first line.

# Basic usage: python3 csv2sql.py -i file.csv -d ','
# Help: python3 csv2sql.py -h
# Python version: 3.6+
# Author: Zbyszek Matuszewski
# License: Unlicense (https://unlicense.org/)

# TODO: implement verbosity
# TODO: implement support for syntax for other databases

# Parses arguments from command line or shows help and exists if proper parameters are not present.
def parse_args():
    parser = argparse.ArgumentParser(description='Converts CSV to SQL')
    parser.add_argument('--input', '-i', dest='inputname', help='Input filename', required=True)
    parser.add_argument('--output', '-o', dest='outputname', help='Output filename. Will be based on file name if not set.', default=None)
    parser.add_argument('--table', '-t', dest='table', help='Table name. Will be taken from file name if not set.', default=None)
    parser.add_argument('--delimiter', '-d', dest='delimiter', help='CSV delimiter. Default: semicolon (;)', default=';')
    parser.add_argument('--per-line', '-pl', dest='perline', type=int, help='Number of entries per line. Default: 100.', default=100)
    parser.add_argument('--ignore', '-ig', dest='ignore', action='store_true', help='If present it will create INSERT IGNORE statements.')
    parser.add_argument('--no-escape', '-ne', dest='escape', action='store_false', help='If present it will NOT escape values. Use with caution.')

    # parser.add_argument('--database', 'db', dest='database', choices=['mysql', 'postgres', 'mssql'], help='Database engine for format and escaping.', default='mysql')

    args = parser.parse_args()
    input_fname = args.inputname
    if args.outputname is None:
        output_fname = input_fname + '.sql'
    else:
        output_fname = str(args.outputname)
    if args.table is None:
        table_name = os.path.basename(str(args.inputname)).split('.', 1)[0]
    else:
        table_name = str(args.table)

    return (input_fname, output_fname, args.delimiter, table_name, args.perline, args.ignore, args.escape, 'mysql')

# Escape string for mysql database SQL query
def mysql_escape(value):
    import MySQLdb # lazy import
    escaped = MySQLdb.escape_string(value)
    return escaped.decode()

# Create start of insert query for mysql database
def mysql_create_sql_insert_values_part (values):
    return '("'+'", "'.join(values)+'")'

# Create values section of insert query for mysql database
def mysql_begin_sql_insert_query (ignore, table_name, column_names):
    sql =  'INSERT ' + ('IGNORE' if ignore else '') + 'INTO '
    sql += table_name+' ('+', '.join(column_names)+') ' + 'VALUES '
    return sql

# Escape string for database SQL query
def db_escape(value, database):
    # only mysql supported currently, database is ignored
    return mysql_escape(value)

# Create start of insert query
def create_sql_insert_values_part (values, database):
    # only mysql supported currently, database is ignored
    return mysql_create_sql_insert_values_part (values)

# Create start of insert query
def begin_sql_insert_query (ignore, table_name, column_names, database):
    # only mysql supported currently, database is ignored
    return mysql_begin_sql_insert_query (ignore, table_name, column_names)

# Preprocess values including escaping them for SQL query
def preprocess_values (values, escape = True):
    if not escape:
        return values
    # only mysql supported currently
    return [mysql_escape(val) for val in values]

# Main method
def main():
    input_fname, output_fname, delimiter, table_name, per_line, ignore, escape, database = parse_args()
    with open(input_fname,'r') as file_reader, open(output_fname,'w') as file_writer:
        csv_reader = csv.reader(file_reader,delimiter=delimiter)
        num = 0
        added_counter = None
        sql = None
        for row in csv_reader:
            num += 1
            if num == 1:
                # get column names from the first line
                column_names = row
                continue
            values = preprocess_values(row, database)
            if added_counter is None or added_counter >= per_line:
                if not sql is None:
                    # write previously started query
                    file_writer.write(sql+';\n')
                # start query on second line or when batch of values for one line is full and was written
                sql = begin_sql_insert_query (ignore, table_name, column_names, database)
                sql += create_sql_insert_values_part (values, database)
                added_counter = 1
            else:
                sql += ', ' + create_sql_insert_values_part (values, database)
                added_counter += 1
        # write last query
        file_writer.write(sql+';\n')

if __name__ == "__main__":
    main()

