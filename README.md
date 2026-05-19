*This project has been created as part of the 42 curriculum by maroard, almanier.*

# A-Maze-ing

## Description

A-Maze-ing est un générateur de maze en Python réalisé dans le cadre du
cursus 42. Le programme lit un fichier de configuration texte, génère un maze
valide, écrit le résultat dans un fichier de sortie en hexadécimal, puis affiche
une représentation du maze avec UI interactive dans le terminal.

Le maze est composé de cellules avec quatre murs possibles: nord, est, sud et
ouest. Les données générées gardent les murs voisins cohérents, permettent de
reproduire une génération avec une seed, et peuvent produire soit un maze
parfait, soit un maze avec plusieurs solutions. L'interface terminal
permet aussi de régénérer le maze, d'afficher ou cacher le plus court chemin,
de changer les couleurs, et d'afficher le pattern 42 demandé quand la taille du
maze le permet.

Le projet fournit aussi un package Python réutilisable nommé
`mazegen-maroard-almanier`, qui contient les logiques de génération et solution sans la couche
application terminal.

## Instructions

Installer les dépendances de développement:

```bash
make install
```

Lancer l'application avec le fichier de configuration par défaut:

```bash
make run
```

La lancer manuellement depuis `src/`:

```bash
cd src
python3 a_maze_ing.py ../config.txt
```

Lancer le debugger:

```bash
make debug
```

Lancer les checks de lint obligatoires:

```bash
make lint
```

Lancer les checks stricts optionnels:

```bash
make lint-strict
```

Nettoyer les fichiers générés et les caches:

```bash
make clean
make fclean
```

Construire le package réutilisable:

```bash
make build
```

## Fichier de configuration

Le programme attend une paire `KEY=VALUE` par ligne. Les lignes vides et les
lignes qui commencent par `#` sont ignorées.

Clés obligatoires:

- `WIDTH`: largeur du maze en cellules, sous forme d'entier.
- `HEIGHT`: hauteur du maze en cellules, sous forme d'entier.
- `ENTRY`: coordonnées d'entrée au format `x,y`.
- `EXIT`: coordonnées de sortie au format `x,y`.
- `OUTPUT_FILE`: chemin de sortie qui finit par `.txt`.
- `PERFECT`: `True`, `False`, `1`, ou `0`.

Clé optionnelle:

- `SEED`: entier utilisé pour reproduire le même maze.

Exemple par défaut:

```text
#Largeur du maze (nombre de cellules)
WIDTH=15
#Hauteur du maze
HEIGHT=15
#Coordonnées d'entrée (x,y)
ENTRY=0,0
#Coordonnées de sortie (x,y)
EXIT=13,13
#Fichier de sortie
OUTPUT_FILE=../maze.txt
#Le maze est-il parfait?
PERFECT=True
#Seed
SEED=42
```

Les coordonnées commencent en haut à gauche. `x` augmente vers la droite et
`y` augmente vers le bas.

## Interface terminal

L'application affiche le maze et un menu interactif directement dans le
terminal. Les choix se font en tapant le numéro de l'action, puis `Entrée`.
Dans les sous-menus, `0` permet de revenir au menu précédent ou de quitter
depuis le menu principal.

Commandes de caméra disponibles dans tous les menus:

- `C`: recentrer la caméra sur le maze.
- `W`: déplacer la caméra vers le haut.
- `A`: déplacer la caméra vers la gauche.
- `S`: déplacer la caméra vers le bas.
- `D`: déplacer la caméra vers la droite.

Actions du menu principal:

- `1. Generate a new Maze`: régénère un nouveau maze avec la configuration et
  les options de génération actuelles.
- `2. Show/Hide path from entry to exit`: affiche ou cache le plus court chemin
  entre l'entrée et la sortie.
- `3. Options`: ouvre les sous-menus de configuration, génération, couleurs et
  pattern.
- `4. Infos`: affiche un rappel des commandes de caméra.
- `5. Credits`: affiche les crédits du projet.
- `0. Quit`: quitte l'application.

Le menu `Options` donne accès à plusieurs sous-menus:

- `Generation settings`: active ou désactive l'utilisation de la seed, change
  l'algorithme de génération entre DFS et Prim, active ou désactive l'animation
  de génération, et permet de régler sa vitesse quand elle est activée.
- `Pattern settings`: change le style du pattern 42 entre dotted et solid, et
  permet de choisir sa position quand le pattern peut être placé dans le maze.
- `Customize colors`: applique un thème prédéfini ou change séparément les
  couleurs des murs, du vide, de l'entrée, de la sortie, du pattern et du
  chemin.
- `Configuration`: modifie la largeur, la hauteur, l'entrée, la sortie, le
  fichier de sortie, le mode perfect et la seed, puis régénère le maze avec les
  nouvelles valeurs.

## Format de sortie

Le maze généré est écrit avec un caractère hexadécimal par cellule et une ligne
par rangée. Chaque valeur hexadécimale stocke les murs fermés de la cellule:

- bit `0`: mur nord.
- bit `1`: mur est.
- bit `2`: mur sud.
- bit `3`: mur ouest.

Après une ligne vide, le fichier contient aussi les coordonnées d'entrée, les
coordonnées de sortie, et le plus court chemin entre l'entrée et la sortie avec
les lettres `N`, `E`, `S` et `W`.

## Algorithme de génération

L'application principale utilise par défaut une recherche en profondeur
randomisée, aussi appelée depth-first search (DFS) backtracker. Elle part de la
cellule d'entrée, choisit à chaque étape un voisin non visité au hasard, ouvre
le mur entre les deux cellules, puis revient en arrière quand elle arrive dans
une impasse.

Cet algorithme a été choisi parce qu'il est extrêmement simple et crée
naturellement un maze parfait et entièrement connecté: chaque cellule est
atteinte une fois, et chaque nouveau passage connecte une nouvelle cellule au
maze existant. Il correspond donc bien au besoin de `PERFECT=True`.

Le générateur contient aussi une implémentation de Prim randomisé comme
algorithme alternatif. Cet algorithme part lui aussi de la cellule d'entrée,
mais il garde une liste de cellules frontières autour du maze en construction.
À chaque étape, il choisit une cellule frontière au hasard, la relie à une
cellule voisine déjà visitée, puis ajoute ses voisins non visités dans la liste
des frontières. Cette approche construit aussi un maze connecté et parfait, mais
avec un style de génération différent de DFS: elle étend progressivement une
zone de cellules visitées au lieu de suivre un long chemin puis de backtracker.

Quand `PERFECT=False`, le générateur ouvre des murs supplémentaires
après la génération initiale du maze parfait pour créer plusieurs chemins
possibles, puis l'application principale corrige les grandes zones ouvertes
interdites.

Le plus court chemin entre l'entrée et la sortie est trouvé avec une recherche
en largeur, ou breadth-first search (BFS). L'algorithme part de l'entrée et
explore d'abord toutes les cellules accessibles en un déplacement, puis toutes
celles accessibles en deux déplacements, et ainsi de suite jusqu'à atteindre la
sortie. Il garde une file de cellules à visiter, un ensemble de cellules déjà
visitées pour éviter les boucles, et une table de parents pour retenir par où
chaque cellule a été atteinte.

Quand la sortie est trouvée, le chemin est reconstruit en remontant cette table
de parents depuis la sortie jusqu'à l'entrée, puis il est inversé pour obtenir
les directions dans le bon ordre. BFS convient bien ici parce que chaque
déplacement entre deux cellules a le même coût: la première fois que la sortie
est atteinte, le chemin trouvé est donc le plus court.

## Package réutilisable

Le package buildable du projet est `mazegen-maroard-almanier`.
Le module Python à importer est `mazegen_maroard_almanier`.

Ce module contient seulement la logique utile pour celui qui devra le réutiliser
pour le projet Pac-Man:

- création d'un maze
- cellules et murs
- directions cardinales
- génération DFS backtracker ou Prim
- seed pour reproduire le même maze
- option `perfect`
- pathfinding BFS entre `entry` et `exit`
- export simple du maze en hexadécimal avec `str(maze)`

Le module ne contient pas la terminal UI, les menus, les couleurs, le pattern
42, le parser de config ou le rendu ANSI de l'application principale.

## Construction du package

Depuis la racine du repo:

```bash
python3 -m pip install build
python3 -m build
```

Avec le `Makefile`:

```bash
make install
make build
```

`make build` génère le `.whl` et le `.tar.gz` dans `dist/`.

## Installation locale

Depuis la racine du repo:

```bash
python3 -m pip install .
```

Ou en mode éditable pendant le développement:

```bash
python3 -m pip install -e .
```

## API principale

```python
from mazegen_maroard_almanier import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    seed=42,
    perfect=True,
    algorithm="dfs",
)
```

Paramètres de `MazeGenerator`:

- `width`: largeur du maze, en nombre de cellules.
- `height`: hauteur du maze, en nombre de cellules.
- `entry`: coordonnées d'entrée sous forme `(x, y)`.
- `exit`: coordonnées de sortie sous forme `(x, y)`.
- `seed`: entier optionnel pour générer le même maze plusieurs fois.
- `perfect`: `True` pour un maze parfait, `False` pour ajouter des passages.
- `algorithm`: `"dfs"` par défaut, ou `"prim"`.

Les coordonnées commencent en haut à gauche:

- `x` augmente vers la droite ;
- `y` augmente vers le bas ;
- la cellule `(0, 0)` est en haut à gauche.

## Structure du maze

`generate()` renvoie un objet `Maze`.

```python
maze = generator.generate()

print(maze.width)
print(maze.height)
print(maze.entry)
print(maze.exit)
```

La grille est stockée dans `maze.grid`, sous forme de lignes:

```python
cell = maze.grid[y][x]
```

Il est conseillé d'utiliser `get_cell()`:

```python
cell = maze.get_cell(4, 2)
```

## Lire les murs

Chaque cellule possède quatre murs. Les directions sont données par `Side`.

```python
from mazegen_maroard_almanier import Side

cell = maze.get_cell(4, 2)

if cell.is_closed(Side.NORTH):
    print("Il y a un mur au nord.")

if not cell.is_closed(Side.EAST):
    print("On peut aller à droite.")
```

Valeurs disponibles:

```python
Side.NORTH
Side.EAST
Side.SOUTH
Side.WEST
```

Chaque `Side` donne aussi des helpers:

```python
dx, dy = Side.EAST.delta()
opposite = Side.EAST.opposite()
letter = Side.EAST.to_char()
```

## Exemple pour déplacer Pac-Man

Pour un Pac-Man, le maze peut servir de carte de collision. Avant de bouger,
on regarde si le mur dans la direction voulue est ouvert.

```python
from mazegen_maroard_almanier import MazeGenerator, Side

generator = MazeGenerator(
    width=28,
    height=31,
    entry=(0, 0),
    exit=(27, 30),
    seed=42,
    perfect=False,
)

maze = generator.generate()
pacman_x = 0
pacman_y = 0

wanted_direction = Side.EAST
current_cell = maze.get_cell(pacman_x, pacman_y)

if not current_cell.is_closed(wanted_direction):
    dx, dy = wanted_direction.delta()
    pacman_x += dx
    pacman_y += dy
```

## Trouver une solution

Le générateur peut calculer le plus court chemin entre `entry` et `exit`. Les fonctions de pathfinding ont été rajoutées dans la classe MazeGenerator car je n'avais pas fait de classe pour ces fonctions, ce n'est pas propre mais t'as une API simple à utiliser.

```python
path = generator.get_shortest_path()
path_string = generator.get_path_string(path)
path_coords = generator.get_path_coords(path)

print(path)
print(path_string)
print(path_coords)
```

`path` est une liste de `Side`.

Exemple :

```python
[Side.EAST, Side.EAST, Side.SOUTH]
```

`path_string` est une version compacte:

```text
EES
```

`path_coords` contient les coordonnées du chemin:

```python
[(0, 0), (1, 0), (2, 0), (2, 1)]
```

## Export hexadécimal

Le maze peut être converti en représentation hexadécimale avec `str(maze)` (méthode `__str__(self) -> str` built-in pour renvoyer l'instance d'une classe (ici maze, instance de `Maze()`) sous forme de string).

```python
hex_maze = str(maze)
print(hex_maze)
```

Pour obtenir les lignes séparément :

```python
hex_lines = str(maze).splitlines()
```

Chaque caractère hexadécimal représente les murs d'une cellule.

## Erreurs

Le module ne fait aucun `print` et ne demande aucun `input`.
En cas de problème, il lève des exceptions.
L'application qui utilise le package décide comment afficher l'erreur.

Exceptions exportées:

```python
MazeGenerationError
MazeInvalidSizeError
MazeInvalidCoordinatesError
MazeSameEntryExitError
MazeNotGeneratedError
```

Exemple:

```python
from mazegen_maroard_almanier import (
    MazeGenerator,
    MazeGenerationError,
)

try:
    generator = MazeGenerator(
        width=1,
        height=1,
        entry=(0, 0),
        exit=(0, 0),
    )
    maze = generator.generate()
except MazeGenerationError as error:
    print(error)
```

## Ressources

Ressources classiques utilisées pour le projet:

- Guide du packaging Python: https://packaging.python.org/
- Documentation mypy: https://mypy.readthedocs.io/
- Wikipédia, algorithmes de génération de maze:
  https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Wikipédia, recherche en largeur:
  https://en.wikipedia.org/wiki/Breadth-first_search

L'IA a été utilisée comme outil de support pour des checks répétitifs, pour la détection des import circulaires, pour débattre concernant l'architecture du projet, la mise en place des dosctrings au-dessus de chaque fonction/méthode pour finaliser le projet et pour la structure du `README.md`

## Équipe et gestion de projet

Répartition des tâches:

- `almanier`: génération du maze et pathfinding dans `src/algorithms/`,
  modifications dans `src/config.py` et dans la classe `Maze` de
  `src/maze/maze.py` pour la gestion optionnelle de la seed, ainsi que l'ajout
  de méthodes pour la gestion des grandes zones ouvertes dans cette même classe.
- `maroard`: tout le reste du projet hors `src/algorithms/`: architecture
  générale, parsing et validation du fichier de configuration, classes `Maze`,
  `Cell` et `Side`, gestion des erreurs de configuration, format de sortie
  hexadécimal, écriture du fichier de sortie, rendu terminal ANSI, thèmes et
  couleurs, caméra, affichage du plus court chemin, menus interactifs,
  intégration de la génération dans l'interface terminal, pattern 42, package réutilisable
  `mazegen_maroard_almanier`, packaging Python, Makefile, linting mypy/flake8
  et documentation du README.

Planning initial:

- Commencer par le parsing et la validation du fichier de configuration.
- Construire ensuite le modèle de données du maze avec `Maze`, `Cell` et `Side`.
- Ajouter le rendu terminal et le format de sortie hexadécimal.
- Ajouter les algorithmes de génération et de pathfinding.
- Brancher la génération avec l'application principale et les interactions.
- Extraire un package réutilisable pour de futurs projets.
- Finaliser le packaging, le linting et la documentation.

Évolution du planning:

- L'interface terminal est devenue plus grande que prévu, car elle avait besoin
  de BEAUCOUP de menus et je voulais toujours en faire plus...
- `almanier`, arrivé un peu tard sur le projet a sû se rendre utile après avoir prit un peu de temps pour lui expliquer tout mon bordel, il a bien refactor la classe `MazeGenerator` et rajouté les features énoncées plus haut.

Ce qui a bien fonctionné:

- La cohésion d'équipe a été excellente
- L'excellente architecture que j'ai mise en place (en toute humilité) a infiniment aidé à rajouter des features facilement et à identifier des bugs.
- Le Makefile a donné un workflow simple pour lancer, linter, nettoyer et build.

Ce qui pourrait être amélioré:

- Une meilleure expérience utilisateur pour la compréhension de l'utilisation de la seed à l'intérieur de l'UI
- Du découpage supplémentaire concernant la class principale du projet `MazeTerminalApp`
- Une classe dédiée à la config
- Une classe dédiée au pathfinding

Outils utilisés:

- Python 3.10.
- flake8 pour les checks de style.
- mypy pour la vérification statique des types.
- setuptools et build pour la génération du package.
- Git pour la collaboration et le versioning.
