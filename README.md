# Notes 

- In the [GeoNames dataset](https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs/blob/master/dataset-geonames-countryInfo.csv) you can find informations such as Area in *sq km*, the countries ISO codes, phone code, currency...
- In WorldBank dataset: yearly GDP value in *$US* of all countries (from 1980 to 2018). 2 files are available for WorldBank:
  - [dataset-worldbank-gdp.xml](https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs/blob/master/dataset-worldbank-gdp.xml) contains a the yearly GDP of a few dozens of countries: RML should be pretty fast to process it
  - [dataset-worldbank-gdp-full.xml](https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs/blob/master/dataset-worldbank-gdp-full.xml) contains the full datasets (all countries): RML can take more than 30min to process
  - We advise you to **use the [dataset-worldbank-gdp.xml](https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs/blob/master/dataset-worldbank-gdp.xml) dataset when testing**. And when you find the right configuration you can run it for the [full XML file](https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs/blob/master/dataset-worldbank-gdp-full.xml) with all countries.
- Useful links
  - Ontologies
    - [GeoNames ontology](http://www.geonames.org/ontology/documentation.html)
    - [DBpedia ontology](http://mappings.dbpedia.org/server/ontology/classes/)
  - [SPARQL specifications](https://www.w3.org/TR/sparql11-query/)
  - Find the URL for a prefix: http://prefix.cc

## Download the required files

The easiest way to download the repository is to clone it using `git`:

```bash
git clone https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs.git
cd UM_KEN4256_KnowledgeGraphs/
```

You can also [download it as a .zip file](https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs/archive/master.zip).

# Execute RML mapping files

You can test if you have Java installed by opening the the `terminal` (or `PowerShell` on Windows) and typing:

```bash
java -version
```

> If Java is not installed, you can install the version 8 from the [Java website](https://java.com/en/download/manual.jsp).

Download RML processor [rmlmapper.jar](https://github.com/RMLio/rmlmapper-java/releases/download/v4.3.1/rmlmapper.jar) and put it in the `UM_KEN4256_KnowledgeGraphs` folder to execute the example mapping file:

```shell
java -jar rmlmapper.jar -m "mapping.ttl" -o "output.nt" --duplicates 
```

* This command **should be executed in the directory** where the `rmlmapper.jar` file and RDF files are located (this repository).
* `--duplicates` allow to remove duplicates triples from the output file.
* The example [mapping.ttl file](https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs/blob/master/mapping.ttl) is available to help you start converting the first columns.

> Running the `rmlmapper` on the full DrugBank dataset can take about 40min. Let us know if your computer can't make it.

# Install GraphDB

### Download and install

* [Download GraphDB](https://www.ontotext.com/products/graphdb) (register to receive an email with the download links)

* Install from exe, dmg, deb or rpm depending on your operating system.

* Access it on <http://localhost:7200/>

### Create a repository (triplestore)

- `Setup` > `Repositories` > `Create new repository`
  - Enter the repository ID you want (only mandatory field here)
  - `Create`
  - Try out the other parameters (the Context index is recommended if you use multiple graphs)

### Users

Enabling security and user management is not necessary when using GraphDB in local. Contact us if you have issues with it.

### Explore

GraphDB offers multiple various modules that can be useful to visualize or process data, such as the [class hierarchy visualization](http://localhost:7200/hierarchy) or [OntoRefine](http://localhost:7200/ontorefine).

# Interlink datasets with LIMES

Download the [jar file for LIMES release 1.7.1](https://github.com/dice-group/LIMES/releases).

An example of LIMES config file is provided in the repository, see [limes_config.xml](https://github.com/MaastrichtU-IDS/UM_KEN4256_KnowledgeGraphs/blob/master/limes_config.xml)

```bash
java -jar limes-core-1.7.1.jar limes_config.xml
```

See the [official LIMES documentation](http://dice-group.github.io/LIMES/#/user_manual/index) for more details on its options, such as the available metrics and thresholds.

Or try out the LIMES Web UI: http://limes.aksw.org/ 

# Explore a graph using SPARQL

Be aware that the count operations can be really time consuming (depending on the dataset size), so you might want to remove it if the query is timing out.

### Count all classes in the graph

```sql
select ?Concept (count(?Concept) as ?Count) # Count the number of ?Concept in the "group by"
where {?s a ?Concept} # We take all the URIs that are types of other URIs
group by ?Concept # Uniq concepts
order by desc(?Count) # Order from the most used class to the less
```

### Get all properties for a Class

```sql
select ?Predicate (count(?Predicate) as ?Count) 
where {
	?s a <http://geonames.org/Country> .
	?s ?Predicate ?o .
} 
group by ?Predicate
order by desc(?Count)
```

### Get all instances of a Class

```sql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?instance ?label
where {
    ?instance a <http://geonames.org/Country> .
    OPTIONAL { ?instance rdfs:label ?label . } # Display the label if one
}
```

## Using other tools (optional)

Conversion can be done using various other tools and methods. You are encouraged to use different tools than RML mapper and LIMES if they fit the task. Here are some examples of other tools to convert structured data to RDF, they usually needs a bit more proficiency with programming and deploying services on your machine than RML, but are more scalable and can process gigabytes of data.

### Data2Services

Students using Linux or MacOS and who already used Docker can use the [d2s client](https://pypi.org/project/d2s/), a scalable tool to convert input datasets to a target RDF knowledge graph. It uses SPARQL queries to map the input data to the target ontology instead of RML mappings. See the [documentation](https://d2s.semanticscience.org/).

```bash
pip install d2s cwlref-runner
d2s init
```

> Client in [Python 3](https://www.python.org/downloads/), using [docker-compose](https://docs.docker.com/compose/install/) to run services and [CWL](https://commonwl.org/) to run workflows.

### RMLStreamer

A new tool for RML processing, it aims to be a scalable implementations of RML. [RMLStreamer](https://github.com/RMLio/RMLStreamer) process stream of data to RDF. 

> It will require you to [start Apache Flink to stream the data](https://github.com/RMLio/RMLStreamer/blob/master/docker/README.md#running-the-rmlstreamer-with-docker) (using Docker).

### R2RML

You could also use [R2RML](https://www.w3.org/TR/r2rml/). The RDB (Relational Database) to RDF Mapping Language is a precursor of RML, it allows you to define mappings for SQL databases (RML extends it for other files, such as XML or JSON). R2RML has much more fast and scalable [implementations](https://github.com/chrdebru/r2rml), but doesn't handle XML (you would need to convert the XML to a CSV or a RDB). R2RML doesn't support CSV natively but CSV files can be exposed as a relational database (each file being a table) using [Apache Drill](https://drill.apache.org/). 

> See [this repository](https://github.com/MaastrichtU-IDS/apache-drill) for easy deployment of Apache Drill using Docker. Start it on  your `/data/r2rml` directory:
>
> ```bash
> docker run -dit --rm --name drill -v /data/r2rml:/data:ro -p 8047:8047 -p 31010:31010 umids/apache-drill:latest
> ```

### OntoRefine

Developed from [OpenRefine](https://openrefine.org/), [OntoRefine](http://graphdb.ontotext.com/documentation/free/loading-data-using-ontorefine.html) is specialized in converting and processing data to RDF. It is included in your [GraphDB installation](http://localhost:7200/ontorefine). It allows you to load data from CSV or XML, and apply some processing before converting it to RDF. See [this tutorial](https://medium.com/wallscope/using-ontorefine-to-transform-tabular-data-into-linked-data-7277ec8c2c0f) for more informations.

### Python scripts

A common way to process data is still to pick your favorite scripting language and use it to process the data. It usually offers more possibilities and libraries can be helpful, but the mappings are not expressed clearly in a mapping language, making them harder to read, share and reuse.