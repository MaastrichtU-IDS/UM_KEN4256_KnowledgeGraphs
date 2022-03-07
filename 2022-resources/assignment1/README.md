# Solution for 2022 BMKG assignment 1

Requirements: Java 11 or later, accessible from the terminal.

## Part 1 - RML

### Task 1

There is a lot of possibilities for task one. The answer is good if:

* There is at least one class for Recipe and for Ingredient, it is possible to have Nutrition Information as a class separated from Ingredient, or directly define the informations on the Ingredient class, the 2 are good
* To define the nutrition informations 2 options are possible:
  * Use different predicates that points to the nutrition value. They need to define which unit to use in the vocabulary. e.g. `schema:cholesterolContent`
  * It is possible to use the same predicate to indicate a nutritional information, with different class that contains the value and the unit. ⚠️ With this option the unit is defined at the data level, not in the vocabulary (it needs to be added for each nutritional information)
* There is a predicate that indicates that Recipes contains Ingredients.

### Task 3 - Generate RDF with RML

Download the RML mapper from https://github.com/RMLio/rmlmapper-java/releases

```bash
wget -O rmlmapper.jar https://github.com/RMLio/rmlmapper-java/releases/download/v4.15.0/rmlmapper-4.15.0-r361-all.jar
```

Run the RML mapper with Java to generate the RDF from the mapping file:

```bash
java -jar rmlmapper.jar -m task3-StructuredSource_Food/nutrition-info-mappings.rml.ttl -o task3-StructuredSource_Food/nutrition-info.ttl
```

### Task 4 - Interlinking with LIMES

Download LIMES from https://github.com/dice-group/LIMES/releases/download/1.7.5/limes.jar

```bash
wget -O limes.jar https://github.com/dice-group/LIMES/releases/download/1.7.5/limes.jar
```

Run LIMES with Java using the config file to interlink the 2  RDF datasets:

```bash
java -jar limes.jar task4-Linking_KGs/interlink-recipe-nutrition.xml
```

> Output in `task4-Linking_KGs/accepted.nt` and `reviewme.nt`

## Part 2 - SPARQL

Install the `rdflib-endpoint` Python package with `pip`:

```bash
pip install "rdflib-endpoint==0.1.6"
```

Start a SPARQL endpoint on http://localhost:8000

```bash
rdflib-endpoint serve task2-UnstructuredSource_Recipe/recipe-ingredients.ttl task3-StructuredSource_Food/nutrition-info.ttl task4-Linking_KGs/vincent-accepted.nt
```

Review the LIMES results easily:

```SPARQL
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?recipeLabel ?nutrititionLabel ?nutritionIngredient ?file WHERE {
    GRAPH ?file {
        ?recipeIngredient owl:sameAs ?nutritionIngredient .
    }
  	?nutritionIngredient rdfs:label ?nutrititionLabel .
    ?recipeIngredient rdfs:label ?recipeLabel .
    FILTER contains(str(?file), "reviewme")
}
```

1. How much vitamin C is in  "Caprese Stuffed Portobello Mushrooms"?

```SPARQL
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX schema: <https://schema.org/>
PREFIX foodinfo: <https://w3id.org/foodinfo/>
PREFIX recipe: <https://w3id.org/recipe-nutrition/>
PREFIX ingredient: <https://w3id.org/recipe-nutrition/ingredient/>

SELECT ((SUM(?vitaminC)) AS ?vitC) WHERE {
  	?recipe rdfs:label "Caprese Stuffed Portobello Mushrooms" ;
           schema:recipeIngredient ?recipeIngredients .
  	?recipeIngredients owl:sameAs ?ingredients .
  	?ingredients schema:nutrition ?nutritionInfo .
  	?nutritionInfo schema:additionalProperty ?vitaminCProp .
    ?vitaminCProp rdfs:label ?vitCLabel ;
    	schema:value ?vitaminC .
    FILTER contains(str(?vitCLabel), "Vitamin C")
}
```

2. Which Mediterranean meals do not include meat?

```SPARQL
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX schema: <https://schema.org/>
PREFIX foodinfo: <https://w3id.org/foodinfo/>
PREFIX recipe: <https://w3id.org/recipe-nutrition/>
PREFIX ingredient: <https://w3id.org/recipe-nutrition/ingredient/>

SELECT ?recipe ?suitableForDiet WHERE {
  	?recipe a schema:Recipe ;
  		schema:suitableForDiet ?suitableForDiet .
  	FILTER(?suitableForDiet = "Vegan" || ?suitableForDiet = "Vegetarian")
}
```

3. Which vegetarian meals are rich in fiber?

```SPARQL
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX schema: <https://schema.org/>

SELECT ?recipe ((SUM(?fiberContent)) AS ?fiber) WHERE {
  	?recipe a schema:Recipe ;
		schema:recipeIngredient ?recipeIngredients ;
  		schema:suitableForDiet ?suitableForDiet .
  	FILTER(?suitableForDiet = "Vegan" || ?suitableForDiet = "Vegetarian")
  	
  ?recipeIngredients owl:sameAs ?ingredients .
  	?ingredients schema:nutrition ?nutritionInfo .
  	?nutritionInfo schema:fiberContent ?fiberContent .
} GROUP BY ?recipe ORDER BY DESC(?fiber)
```

4. List the 10 most frequently used ingredients

```SPARQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX schema: <https://schema.org/>

SELECT ?recipeIngredients (count(?recipeIngredients) AS ?count)
WHERE {
    ?recipe a schema:Recipe ;
		schema:recipeIngredient ?recipeIngredients .
} 
GROUP BY ?recipeIngredients
ORDER BY DESC(?count)
LIMIT 10
```

5. Simply list the most frequently used ingredients per diet:

```SPARQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX schema: <https://schema.org/>

SELECT ?diet ?ingredient (count(?ingredient) AS ?countPerDiet)
WHERE {
    ?recipe a schema:Recipe ;
		schema:recipeIngredient ?ingredient ;
        schema:suitableForDiet ?diet .
} 
GROUP BY ?diet ?ingredient ORDER BY ?diet DESC(?countPerDiet)
```

It could also be done more precisely for the 5 most used ingredients per diet:

```SPARQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <https://schema.org/>
SELECT ?diet ?ingredientName (count(?ingredientName) AS ?countPerDiet) 
WHERE { 
    ?recipe rdf:type schema:Recipe ;
            rdfs:label ?recipeName ;
            schema:suitableForDiet ?diet;
            schema:recipeIngredient ?ingredient .
    ?ingredient rdfs:label ?ingredientName .
    {
        SELECT ?ingredient (count(?ingredient) AS ?ingredientCount)
        WHERE {
                ?recipe rdf:type schema:Recipe ;
                rdfs:label ?recipeName ;
                schema:recipeIngredient ?ingredient .
        } GROUP BY ?ingredient ORDER BY DESC(?ingredientCount) LIMIT 5
    }
} GROUP BY ?ingredientName ?diet ORDER BY ?diet DESC(?countPerDiet)
```


6. Find recipes that you should avoid if you are allergic to peanuts

```SPARQL
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX schema: <https://schema.org/>

SELECT DISTINCT ?recipe
WHERE {
    ?recipe a schema:Recipe ;
		schema:recipeIngredient ?recipeIngredients .
  FILTER NOT EXISTS { ?recipe schema:recipeIngredient <https://w3id.org/recipe-nutrition/pistachio> }
} 
```
