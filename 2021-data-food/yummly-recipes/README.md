## Get those files

Clone this repository containing the mappings and data files:

```bash
git clone https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs
cd UM_KEN4256_KnowledgeGraphs/2021-data-food/yummly-recipes
```

> You can also [download the files as a zip file](https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs/archive/master.zip)

Note that you can use this web UI to convert YARRRML mappings to RML: https://rml.io/yarrrml/matey 

## Get the rmlmapper

Download the rmlmapper from their GitHub releases at https://github.com/RMLio/rmlmapper-java/releases

Rename it to `rmlmapper.jar`, and place it in the same folder as the mappings

Students using bash (Linux, MacOS, WSL) can download the latest version in one line:

```bash
curl -s https://api.github.com/repos/RMLio/rmlmapper-java/releases/latest \
    | grep "/rmlmapper-.*.jar" \
    | cut -d : -f 2,3 \
    | tr -d \" \
    | wget -O rmlmapper.jar -qi -
```

## Run the RML mapper

In your terminal go to the folder containing the mappings, and run the following to generate a RDF file for Yummly recipes.

```bash
java -jar rmlmapper.jar -m yummly-mappings.rml.ttl -o yummly-recipes.ttl -s turtle
```
