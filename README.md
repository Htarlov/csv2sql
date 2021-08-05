# csv2sql

This script reads a CSV file and converts it to a SQL file.
Currently only MySQL syntax is supported.
It is simple script and does not support fancy things like dates conversion etc.
It needs proper column names in the first line.

### Usage:

```text
  csv2sql.py [-h] --input INPUTNAME [--output OUTPUTNAME] [--table TABLE]
             [--delimiter DELIMITER] [--per-line PERLINE] [--ignore]
             [--no-escape]

Converts CSV to SQL

optional arguments:
  -h, --help            show this help message and exit
  --input INPUTNAME, -i INPUTNAME
                        Input filename
  --output OUTPUTNAME, -o OUTPUTNAME
                        Output filename. Will be based on file name if not
                        set.
  --table TABLE, -t TABLE
                        Table name. Will be taken from file name if not set.
  --delimiter DELIMITER, -d DELIMITER
                        CSV delimiter. Default: semicolon (;)
  --per-line PERLINE, -pl PERLINE
                        Number of entries per line. Default: 100.
  --ignore, -ig         If present it will create INSERT IGNORE statements.
  --no-escape, -ne      If present it will NOT escape values. 
                        Use with caution.
````

### Needs:

* Python 3.6+
* MySQLdb library for MySQL escape.

### Not yet done:

* verbosity
* support for syntax for other databases
* support for column names mapping
* support for dates conversion
