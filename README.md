# A-Maze-ing

## Package reutilisable

Le package buildable du projet est `mazegen-maroard-almanier`.
Le module Python a importer est `mazegen_maroard_almanier`.

Ce module contient seulement la logique utile pour celui qui devra le reutiliser pour le projet Pac-Man:

- creation d'un maze
- cellules et murs
- directions cardinales
- generation DFS backtracker ou Prim
- seed pour reproduire le meme maze
- option `perfect`
- pathfinding BFS entre `entry` et `exit`
- export simple du maze en hexadecimal avec `str(maze)`

Le module ne contient pas la terminal UI, les menus, les couleurs, le pattern
42, le parser de config ou le rendu ANSI de l'application principale.

## Build

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

`make build` genere le `.whl` et le `.tar.gz` dans `dist/`, puis les copie
aussi a la racine du projet.

## Installation locale

Depuis la racine du repo:

```bash
python3 -m pip install .
```

Ou en mode editable pendant le developpement:

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

Parametres de `MazeGenerator`:

- `width`: largeur du maze, en nombre de cellules.
- `height`: hauteur du maze, en nombre de cellules.
- `entry`: coordonnees d'entree sous forme `(x, y)`.
- `exit`: coordonnees de sortie sous forme `(x, y)`.
- `seed`: entier optionnel pour generer le meme maze plusieurs fois.
- `perfect`: `True` pour un maze parfait, `False` pour ajouter des passages.
- `algorithm`: `"dfs"` par defaut, ou `"prim"`.

Les coordonnees commencent en haut a gauche:

- `x` augmente vers la droite ;
- `y` augmente vers le bas ;
- la cellule `(0, 0)` est en haut a gauche.

## Structure du maze

`generate()` renvoie un objet `Maze`.

```python
maze = generator.generate()

print(maze.width)
print(maze.height)
print(maze.entry)
print(maze.exit)
```

La grille est stockee dans `maze.grid`, sous forme de lignes:

```python
cell = maze.grid[y][x]
```

Il est conseille d'utiliser `get_cell()`:

```python
cell = maze.get_cell(4, 2)
```

## Lire les murs

Chaque cellule possede quatre murs. Les directions sont donnees par `Side`.

```python
from mazegen_maroard_almanier import Side

cell = maze.get_cell(4, 2)

if cell.is_closed(Side.NORTH):
    print("Il y a un mur au nord.")

if not cell.is_closed(Side.EAST):
    print("On peut aller a droite.")
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

## Exemple pour deplacer Pac-Man

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

Le generateur peut calculer le plus court chemin entre `entry` et `exit`.

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

`path_coords` contient les coordonnees du chemin:

```python
[(0, 0), (1, 0), (2, 0), (2, 1)]
```

## Export hexadecimal

Le maze peut etre converti en representation hexadecimale avec `str(maze)`.

```python
hex_maze = str(maze)
print(hex_maze)
```

Pour obtenir les lignes separement :

```python
hex_lines = str(maze).splitlines()
```

Chaque caractere hexadecimal represente les murs d'une cellule.

## Erreurs

Le module ne fait aucun `print` et ne demande aucun `input`.
En cas de probleme, il leve des exceptions.

Exceptions exportees:

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

L'application qui utilise le package decide comment afficher l'erreur.
