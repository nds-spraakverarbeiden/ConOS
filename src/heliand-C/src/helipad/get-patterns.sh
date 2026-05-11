curl --data-urlencode "query@get-patterns.sparql" http://localhost:9999/bigdata/sparql | \
grep literal | sed -e s/'^\s*'//g -e s/'<[^>]*>'//g | sort | uniq -c | sort -n | sed -e s/'^\s*'//g -e s/' '/'\t'/ -e s/'^\([^A-Z]*\)\([A-Z][^ \t]*\)'/'\2\t\1\2'/g 
