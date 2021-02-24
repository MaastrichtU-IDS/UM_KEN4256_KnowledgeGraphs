
Download the rmlmapper from their GitHub releases at https://github.com/RMLio/rmlmapper-java/releases

Rename it to `rmlmapper.jar`, and place it in the same folder as the mappings

In your terminal go to the folder containing the mappings, and run the following to generate a RDF file for Yummly recipes.

```bash
java -jar rmlmapper.jar -m yummly-mappings.rml.ttl -o yummly-recipes.ttl -s turtle
```

You can use this web UI to convert YARRRML mappings to RML: https://rml.io/yarrrml/matey 