# Problem

Hola Alberto

La prueba trata de hacer un API en Flask (microframework de python). Como base de datos se utilizará MongodB. Los endpoints serán los siguientes:

    GET /words/ -> Devuelve un listado de palabras ordenadas. Ojo, que el orden no es orden alfabético, sino el orden en el que están guardadas.

    POST /words/ -> añade una palabra. El payload será la palabra en sí y la posición. 

    PATCH /words/<palabra> -> Obtiene "position" del payload y pone esa palabra en la posición indicada
    GET /words/<palabra>/anagrams -> Devuelve los anagramas de una palabra. La palabra no tiene por qué formar parte del conjunto de palabras.
    DELETE /words/<palabra> -> Borra la palabra

Ejemplos:
1 - GET /words
code: 200
resp:
{data: [
"cosa",
"caso",
"paco",
"pepe",
"Málaga"]
}

2 - POST /words {"word": "calle", "position": 3}
code: 201
resp:
{"word": "calle", "position": 3}

3 - GET /words
code: 200
resp:
{data: [
"cosa",
"caso",
"calle",
"paco",
"pepe",
"Málaga"]
}

4 - PATCH /words/calle {"position": 5}
code: 200
resp:
{"word": "calle", "position": 5}

5 - GET /words
code: 200
resp:
{data: [
"cosa",
"caso",
"paco",
"pepe",
"calle",
"Málaga"]
}

6- GET /words/asco/anagrams
code: 200
resp:
{data: [
"cosa",
"caso"]
}

7- DELETE /words/calle
code: 204

8 - GET /words
code: 200
resp:
{data: [
"cosa",
"caso",
"paco",
"pepe",
"Málaga"]
}

¿Qué se valora de la prueba?
Resolución a los problemas de ordenación y anagramas
Organización/estructuración del código

Fecha de entrega: alrededor de 2 semanas.


Un saludo,
Pedro.
