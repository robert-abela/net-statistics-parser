# net-statistics-parser
A parser for the output of `netstat -es` (on Linux) a sample of which can be found in netstat.txt.
This parser will look for specific numeric values in the output and export them to CSV.

Sample usage:

`my_list = ValueList()`

`my_list.add_value_to_parse('TPR.log', NP + ' total packets received', 'Ip:')`
`my_list.add_value_to_parse('DU.log', 'destination unreachable: ' + NP, 'Icmp:', 'ICMP input histogram:')`

`my_list.write_csv()`
