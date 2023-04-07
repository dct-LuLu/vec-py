Nom: ça balance pas mal (temporaire)

### Objectifs :
-   Écrire un programme en Python pour créer un moteur de physique avec des objets géométriques de base tels que des cercles et des carrés, ainsi que des objets personnalisés dessinés par l'utilisateur, soumis à des lois de physique et à des collisions avec des pertes d'énergie. Le programme doit utiliser la librairie Pyglet pour afficher des graphismes.
-   Utiliser un quadtree pour optimiser la détection de collisions et améliorer les performances.
-   Permettre aux utilisateurs de zoomer et dézoomer facilement et efficacement pour faciliter la manipulation des objets.
-   Implémenter un menu utilisateur pour créer des formes, choisir leurs propriétés (movable, draggable), leur couleur, etc. pour permettre une personnalisation aisée des objets.
-   Créer un menu pour choisir entre un mode sandbox et un mode jeu, avec plusieurs niveaux préconfigurés dans le mode jeu.
-   Ajouter des interactions amusantes telles que des aimants, du feu, des explosions, des objets qui se cassent en morceaux, du verre, des lasers, de l'eau, des ventilateurs avec du vent pour améliorer l'expérience utilisateur.
-   Utiliser l'API OpenGL de Pyglet pour ajouter des shaders pour des effets visuels avancés.
-   Ajouter des sons pour renforcer l'immersion de l'utilisateur lors des contacts entre les objets.

### Fonctionnalités :
-   Le programme doit être capable d'afficher des objets géométriques de base tels que des cercles et des carrés.
-   Les utilisateurs doivent être en mesure de créer des objets personnalisés dessinés à la main.
-   Le programme doit respecter les lois de la physique et des collisions avec des pertes d'énergie pour tous les objets.
-   Le quadtree doit être utilisé pour détecter les collisions en avance, afin d'optimiser les performances.
-   Les utilisateurs doivent pouvoir zoomer et dézoomer facilement pour manipuler les objets avec précision.
-   Un menu utilisateur doit être disponible pour créer des formes et choisir leurs propriétés, couleurs, etc. de manière personnalisée.
-   Le mode sandbox permettra aux utilisateurs de s'entraîner et de se familiariser avec les interactions du programme, tandis que le mode jeu comportera plusieurs niveaux préconfigurés.
-   Des interactions amusantes, telles que des aimants, du feu, des explosions, des objets qui se cassent en morceaux, du verre, des lasers, de l'eau, des ventilateurs avec du vent, doivent être implémentées pour offrir une expérience utilisateur plus immersive.
-   L'utilisation de l'API OpenGL de Pyglet doit être faite pour ajouter des shaders et des effets visuels avancés.
-   Des sons doivent être ajoutés pour renforcer l'immersion de l'utilisateur lors des contacts entre les objets.

### Contraintes :
-   Le programme doit être écrit en Python.
-   Les interactions supplémentaires doivent être implémentées pour améliorer l'expérience utilisateur.
-   L'API OpenGL de Pyglet doit être utilisée pour ajouter des shaders et des effets visuels avancés.
-   Des sons doivent être ajoutés pour renforcer l'immersion de l'utilisateur lors des contacts entre les objets.
-   Le programme doit être facile à utiliser pour les utilisateurs de tous niveaux de compétences.
-   Le programme doit être stable et ne pas planter.
-   Le programme doit être optimisé pour des performances fluides même avec de nombreux objets.
-   Le programme doit être codé de manière à permettre une maintenance facile et des mises à jour régulières.

### Répartition:
-  La partie application et physiques sera développée et implémenté par Jaurel
-  Le Quadtree sera développé par Jaurel et implémenté dans le moteur par Flavio
-  Flavio s'occupera du son, des shaders, du dessin de polygones utilisateur, Menu choix sandbox
-  Jaurel s'occupera du zoom, des shaders, du menu utilisateur
-  Les niveaux seront développées par Flavio et Jaurel

### Livraison :
-   Le programme doit être livré sous la forme d'un fichier exécutable qui peut être installé sur Windows.
-   Une documentation détaillée doit être fournie pour permettre aux utilisateurs de comprendre les fonctionnalités et de les utiliser facilement.
-   Le code source doit être fourni pour permettre une maintenance et une mise à jour faciles du programme.
- Tout le projet ainsi que le cahier des charges sera sur un repo Github
