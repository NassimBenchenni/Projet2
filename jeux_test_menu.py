import pyxel, random, sqlite3, pygame, sys



# taille de la fenetre 128x128 pixels
# ne pas modifier


# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 60
vaisseau_y = 60

# vies
vies = 4

# initialisation des tirss
tirs_liste = []

# initialisation des ennemis
ennemis_liste = []

# initialisation des explosions
explosions_liste = []  

# Initialisation du compteur d'ennemis
compteur_ennemie = 10

compteur_niveau = 10

text_potion = "Speed boost!"

niveau = 1

speed = 1

deaths = 0

score = 0

nombre_ennemie = 0

level = 0

boost_vitesse = False

boost_text_counter = 0

random_target_position = [random.randint(0, 120), random.randint(95, 120)]







def vaisseau_deplacement(x, y):
    """Déplacement avec les touches de directions, en fonction de la vitesse et du niveau"""
    global random_target_position, speed, niveau, boost_vitesse, boost_text_counter

    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 120):
            x = x + speed
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 0):
            x = x - speed
    if pyxel.btn(pyxel.KEY_DOWN):
        if (y < 120):
            y = y + speed
    if pyxel.btn(pyxel.KEY_UP):
        if (y > 0):
            y = y - speed 
     # Vérification si le vaisseau atteint la case spécifique pour le prochain niveau
    if niveau > 0 and niveau % 2 == 0:  # Changer cette condition selon le niveau que vous ciblez
        if x <= random_target_position[0] + 5 and x >= random_target_position[0] - 5  and y <= random_target_position[1] + 5 and y >= random_target_position[1] - 5 :
            niveau += 1
            speed += 1
            augmenter_score(15)
            random_target_position = [random.randint(0, 120), random.randint(95, 120)]
     # Active le boost_vitesse
            boost_vitesse = True

    # Initialise le compteur pour afficher le texte "Speed boost!"
    if boost_vitesse:
        boost_text_counter = 30 
        boost_vitesse = False
    return x, y 
    

def tirs_creation(x, y, tirs_liste):
    """création d'un tir avec la barre d'espace"""

    # btnr pour eviter les tirs multiples
    if pyxel.btnr(pyxel.KEY_SPACE):
        tirs_liste.append([x+4, y-4])
    return tirs_liste


def tirs_deplacement(tirs_liste):
    """déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""

    for tir in tirs_liste:
        tir[1] -= 2
        if  tir[1]<-8:
            tirs_liste.remove(tir)
    return tirs_liste


def ennemis_creation(ennemis_liste):
    """création aléatoire des ennemis"""
    global nombre_ennemie

    # un ennemi par seconde
    if (pyxel.frame_count % 30 == 0):
        ennemis_liste.append([random.randint(0, 120), random.randint(0, 25)])
        nombre_ennemie += 1
        if nombre_ennemie % 2 == 0 :
            for i in range(niveau):
                ennemis_liste.append([random.randint(0, 120), random.randint(0, 25)])            
    return ennemis_liste


def ennemis_deplacement(ennemis_liste):
    """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

    for ennemi in ennemis_liste:
        ennemi[1] += niveau
        if  ennemi[1]>128:
            ennemis_liste.remove(ennemi)
    return ennemis_liste

def vaisseau_suppression(vies):
    """disparition du vaisseau et d'un ennemi si contact"""
    global deaths

    for ennemi in ennemis_liste:
        if ennemi[0] <= vaisseau_x+8 and ennemi[1] <= vaisseau_y+8 and ennemi[0]+8 >= vaisseau_x and ennemi[1]+8 >= vaisseau_y:
            ennemis_liste.remove(ennemi)
            vies -= 1
            deaths = get_deaths(username) + 1
            # on ajoute l'explosion
            explosions_creation(vaisseau_x, vaisseau_y)
            update_deaths(username, deaths)
    return vies

def incrementer_compteur():
    global compteur_ennemie, compteur_niveau, niveau

    niveau += 1
    compteur_niveau += 5
    compteur_ennemie = compteur_niveau
    return niveau


# Fonction pour augmenter le score lorsqu'un ennemi est éliminé
def augmenter_score(points):
    global score, score2
    score += points
    score2 = get_score(username)
    score2 += score
    update_score(username, score2)
    

def ennemis_suppression():
    """disparition d'un ennemi et d'un tir si contact"""
    global compteur_ennemie, compteur_niveau, niveau

    for ennemi in ennemis_liste:
        for tir in tirs_liste:
            if ennemi[0] <= tir[0]+1 and ennemi[0]+8 >= tir[0] and ennemi[1]+8 >= tir[1]:
                ennemis_liste.remove(ennemi)
                compteur_ennemie -= 1
                if compteur_ennemie == 0:
                    incrementer_compteur()     
                tirs_liste.remove(tir)
                # Appeler la fonction pour augmenter le score
                augmenter_score(5)
                # on ajoute l'explosion
                explosions_creation(ennemi[0], ennemi[1])

    

def explosions_creation(x, y):
    """explosions aux points de collision entre deux objets"""
    explosions_liste.append([x, y, 0])


def explosions_animation():
    """animation des explosions"""
    for explosion in explosions_liste:
        explosion[2] +=1
        if explosion[2] == 14:
            explosions_liste.remove(explosion)                

# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global vaisseau_x, vaisseau_y, tirs_liste, ennemis_liste, vies, explosions_liste, compteur_ennemie, compteur_niveau

    # mise à jour de la position du vaisseau
    vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)

    # creation des tirs en fonction de la position du vaisseau
    tirs_liste = tirs_creation(vaisseau_x, vaisseau_y, tirs_liste)

    # mise a jour des positions des tirs
    tirs_liste = tirs_deplacement(tirs_liste)

    # creation des ennemis
    ennemis_liste = ennemis_creation(ennemis_liste)

    # mise a jour des positions des ennemis
    ennemis_liste = ennemis_deplacement(ennemis_liste)

    # suppression des ennemis et tirs si contact
    ennemis_suppression()

    # suppression du vaisseau et ennemi si contact
    vies = vaisseau_suppression(vies)
    
    # evolution de l'animation des explosions
    explosions_animation()    

# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""
    global boost_text_counter

    # vide la fenetre
    pyxel.cls(0)

    # si le vaisseau possede des vies le jeu continue
    if vies > 0:

        # affichage des vies            
        pyxel.text(5,5, 'VIES:'+ str(vies), 7)
        
        pyxel.text(85,5, 'Ennemies:' + str(compteur_ennemie), 8)
        
        pyxel.text(40,5, 'Niveau:' + str(niveau), 5)

        # vaisseau (carre 8x8)
        pyxel.rect(vaisseau_x, vaisseau_y, 8, 8, 1)

        # tirs
        for tir in tirs_liste:
            pyxel.rect(tir[0], tir[1], 1, 4, 10)
        
        # Affiche quand le joueur prend un boost de vitesse    
        if boost_text_counter > 0:
            pyxel.text(45, 50, text_potion, 3)
            boost_text_counter -= 1  # Diminue le compteur

        # Afficher le score
        pyxel.text(5, 115, 'Score:' + str(score), 9)
        
        # Dessine le marqueur de la case pour changer la vitesse
        if niveau > 0 and niveau % 2 == 0:
            pyxel.rect(random_target_position[0], random_target_position[1], 8, 8, 6)
        
        # ennemis
        for ennemi in ennemis_liste:
            pyxel.rect(ennemi[0], ennemi[1], 8, 8, 8)

        # explosions (cercles de plus en plus grands)
        for explosion in explosions_liste:
            pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)            

    # sinon: GAME OVER
    else:

        pyxel.text(50,64, 'GAME OVER', 7)
  

conn = sqlite3.connect('data.db')
cur = conn.cursor()

username = input("username:")

def supprimer_utilisateur(username):
    cur.execute("DELETE FROM Players WHERE username = ?", (username,))
    conn.commit()

def drop_table():
    cur.execute("DROP TABLE IF EXISTS Players;")

def creer_table():
    cur.execute("""
    CREATE TABLE if not exists Players(
        ID INTEGER PRIMARY KEY,
        username Varchar(20),
        deaths INTEGER,
        score INTEGER
    );
    """)

def insert():
    cur.execute("SELECT * FROM Players")
    result = cur.fetchall()
    if len(result) == 0:
        cur.execute("INSERT INTO Players (username, deaths, score) VALUES (?, 0, 0)", (username,))
        conn.commit()
    else:
        cur.execute("SELECT * FROM Players WHERE username = ?", (username,))
        result = cur.fetchone()
        if result is None:
            cur.execute("INSERT INTO Players (username, deaths, score) VALUES (?, 0, 0)", (username,))
            conn.commit()


    
def update_deaths(username, deaths):
    cur.execute("UPDATE Players SET deaths = ? WHERE username = ?", (deaths, username))
    conn.commit()

def get_deaths(username):
    cur.execute("SELECT deaths FROM Players WHERE username = ?", (username,))
    result = cur.fetchone()
    return result[0] if result else 0

def get_score(username):
    cur.execute("SELECT score FROM Players WHERE username = ?", (username,))
    result = cur.fetchone()
    return result[0] if result else 0

def update_score(username, score2):
    cur.execute("UPDATE Players set score = ? where username = ?", (score2, username))
    conn.commit()


creer_table()
insert()  

def menu():
    while True:
        print("1. Jouer")
        print("2. Voir les scores")
        print("3. Quitter")
        choix = input("Choisissez une option : ")
        if choix == "1":
            # Insérez ici le code pour démarrer le jeu
            pyxel.init(128, 128, title="Space_invaders")
            pyxel.run(update, draw)
        elif choix == "2":
            # Insérez ici le code pour afficher les scores
            print("Score:" + str(get_score(username)))
            print("Deaths:" + str(get_deaths(username)))
        elif choix == "3":
            pyxel.quit()
        else:
            print("Choix invalide. Veuillez réessayer.")

# Appeler la fonction menu pour afficher le menu
menu()

