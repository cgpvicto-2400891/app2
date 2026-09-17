# -*- coding: utf-8 -*-
"""
Leçons Partie 1 : UI & Composants
1. layout (Column, Row, Box, Modifier)
2. card (Card Material 3)
3. scaffold (Scaffold, TopAppBar, FAB, Snackbar)
4. lazycolumn (Listes défilantes performantes)
"""

LESSONS_PART1 = {
    "layout": {
        "id": "layout",
        "title": "Fondations UI : Column, Row, Box & Modifier",
        "niveau": 2,
        "level": "beg",
        "duration": "12 min",
        "quoi": "En Jetpack Compose, l'interface n'est plus construite avec des fichiers XML : tout est décrit en fonctions Kotlin déclaratives. <b>Column</b> empile ses éléments verticalement, <b>Row</b> les aligne horizontalement, et <b>Box</b> les superpose les uns sur les autres (comme des calques). Le <b>Modifier</b> est l'objet universel qui permet de décorer, dimensionner, espacer et ajouter des interactions à n'importe quel composant.",
        "pourquoi": "Sans conteneur de disposition, Compose placerait tous les éléments au même endroit (en haut à gauche à 0,0) et ils se chevaucheraient. Maîtriser Column, Row, Box et la chaîne des Modifiers est le socle indispensable pour construire 100% des écrans d'une application Android.",
        "quand": "Absolument partout ! Dès que tu veux afficher deux textes l'un sous l'autre (Column), un bouton à côté d'une icône (Row), ou un badge de notification sur une photo de profil (Box).",
        "syntaxe": """// 1. Vertical
Column(
    modifier = Modifier.fillMaxWidth().padding(16.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp),
    horizontalAlignment = Alignment.CenterHorizontally
) { /* enfants */ }

// 2. Horizontal
Row(
    modifier = Modifier.fillMaxWidth(),
    horizontalArrangement = Arrangement.SpaceBetween,
    verticalAlignment = Alignment.CenterVertically
) { /* enfants */ }

// 3. Superposition (calques)
Box(
    modifier = Modifier.size(64.dp),
    contentAlignment = Alignment.TopEnd
) { /* enfants superposés */ }""",
        "exempleMin": """@Composable
fun ProfilBasique() {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Alice Dupont", fontWeight = FontWeight.Bold)
        Text("Développeuse Android", color = Color.Gray)
    }
}""",
        "explication": [
            ["@Composable", "Indique au compilateur Compose que cette fonction génère un morceau d'interface graphique."],
            ["Column(modifier = ...)", "Crée un conteneur vertical. Le modifier applique une marge intérieure de 16.dp tout autour."],
            ["Text(\"Alice Dupont\")", "Affiche le nom en texte brut avec une graisse grasse (Bold)."],
            ["Text(\"Développeuse...\", color = ...)", "Deuxième texte empilé automatiquement sous le premier, avec une teinte grise atténuée."]
        ],
        "exempleReel": """package com.example.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * Exemple de A à Z : Carte de Profil combinant Box (avatar + badge),
 * Column (textes verticaux) et Row (boutons d'action horizontaux).
 */
@Composable
fun CarteProfilComplete(
    nom: String = "Sarah Benali",
    role: String = "Lead Mobile Architect",
    estEnLigne: Boolean = true,
    onContacterClick: () -> Unit = {}
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // 1. BOX : Avatar avec badge "En ligne" superposé en bas à droite
            Box(contentAlignment = Alignment.BottomEnd) {
                // Avatar circulaire
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.primary),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.Person,
                        contentDescription = "Avatar",
                        tint = Color.White,
                        modifier = Modifier.size(48.dp)
                    )
                }

                // Pastille indicateur de statut
                if (estEnLigne) {
                    Box(
                        modifier = Modifier
                            .size(20.dp)
                            .clip(CircleShape)
                            .background(Color(0xFF3DDC84)) // Vert Android
                            .padding(2.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            // 2. COLUMN : Identité et titre
            Text(
                text = nom,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Text(
                text = role,
                fontSize = 14.sp,
                color = MaterialTheme.colorScheme.outline
            )

            Spacer(modifier = Modifier.height(18.dp))

            // 3. ROW : Boutons d'action alignés horizontalement
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedButton(
                    onClick = { /* Voir profil */ },
                    modifier = Modifier.weight(1f)
                ) {
                    Text("Profil")
                }

                Button(
                    onClick = onContacterClick,
                    modifier = Modifier.weight(1f)
                ) {
                    Icon(Icons.Default.Email, contentDescription = null, modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Message")
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun CarteProfilPreview() {
    MaterialTheme {
        CarteProfilComplete()
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.04.01")
    implementation(composeBom)
    androidTestImplementation(composeBom)

    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    debugImplementation("androidx.compose.ui:ui-tooling")
}""",
        "resultat": """┌─────────────────────────────────┐
│              [ 👤 ]🟢           │  ← Box (Avatar + Badge superposé)
│           Sarah Benali          │  ← Column (Textes empilés)
│       Lead Mobile Architect     │
│                                 │
│  [  Profil  ]   [ ✉ Message ]   │  ← Row (Boutons côte à côte)
└─────────────────────────────────┘""",
        "params": [
            ["horizontalAlignment", "Dans Column : aligne les enfants sur l'axe horizontal (Start, CenterHorizontally, End)."],
            ["verticalArrangement", "Dans Column : répartit l'espace vertical (Top, Center, Bottom, SpaceBetween, Arrangement.spacedBy(x.dp))."],
            ["horizontalArrangement", "Dans Row : répartit l'espace horizontal (Start, Center, End, SpaceBetween, Arrangement.spacedBy(x.dp))."],
            ["verticalAlignment", "Dans Row : aligne les enfants sur l'axe vertical (Top, CenterVertically, Bottom)."],
            ["contentAlignment", "Dans Box : positionne les enfants à l'intérieur (TopStart, Center, BottomEnd, etc.)."],
            ["Modifier.weight(1f)", "Dans Row/Column : distribue l'espace restant proportionnellement (équivalent de flexbox)."],
            ["Modifier.fillMaxWidth()", "Occupe 100% de la largeur disponible offerte par le parent."]
        ],
        "erreurs": [
            ["Ordre des Modifiers inversé : Modifier.padding(16.dp).background(Color.Red)", "L'ordre des modificateurs est strict en Compose ! Ici le padding est externe (marge), puis le fond rouge est appliqué à l'intérieur. Pour avoir un fond rouge avec marge intérieure, écris toujours : .background(Color.Red).padding(16.dp)."],
            ["Utiliser Column classique pour une liste de 500 éléments", "Un Column standard instancie TOUS ses enfants en mémoire immédiatement, ce qui provoque des saccades d'écran et des plantages OutOfMemoryError. Pour toute liste longue ou dynamique, utilise une LazyColumn !"]
        ],
        "exercice": {
            "enonce": "Crée un composant d'élément de notification : une Row avec un badge numérique circulaire à gauche (Box violette et chiffre blanc), un titre et sous-titre empilés au centre (Column avec Modifier.weight(1f)), et une flèche à droite.",
            "indice": "Utilise Row(verticalAlignment = CenterVertically) contenant Box(size=36.dp, clip=CircleShape), un Spacer(12.dp), un Column(Modifier.weight(1f)), et un Icon chevron.",
            "solution": """@Composable
fun ItemNotification(
    numero: Int = 1,
    titre: String = "Mise à jour disponible",
    description: String = "La version 2.4 apporte des nouveautés."
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Badge circulaire
        Box(
            modifier = Modifier
                .size(36.dp)
                .clip(CircleShape)
                .background(Color(0xFF7F52FF)),
            contentAlignment = Alignment.Center
        ) {
            Text(text = "$numero", color = Color.White, fontWeight = FontWeight.Bold)
        }

        Spacer(modifier = Modifier.width(12.dp))

        // Textes centraux occupant l'espace restant
        Column(modifier = Modifier.weight(1f)) {
            Text(text = titre, fontWeight = FontWeight.SemiBold, fontSize = 15.sp)
            Text(text = description, color = Color.Gray, fontSize = 13.sp)
        }

        // Flèche
        Icon(
            imageVector = Icons.Default.ChevronRight,
            contentDescription = "Voir",
            tint = Color.Gray
        )
    }
}"""
        },
        "quiz": {
            "q": "Quelle est la différence concrète entre Modifier.background(Color.Blue).padding(16.dp) et Modifier.padding(16.dp).background(Color.Blue) ?",
            "options": [
                "Le premier applique la couleur sur toute la surface y compris le padding ; le second crée une marge transparente autour du bloc bleu",
                "C'est strictement identique, Compose réorganise automatiquement l'ordre",
                "Le second provoque une erreur de compilation Kotlin",
                "Le premier est interdit en Material Design 3"
            ],
            "correct": 0,
            "exp": "En Jetpack Compose, les modificateurs s'exécutent de gauche à droite (dans l'ordre de chaînage). Background puis Padding colore la surface avant d'insérer l'espace intérieur, tandis que Padding puis Background crée un espacement externe (marge) avant de colorer la zone réduite restante."
        },
        "retenir": [
            "Column = empilement vertical ; Row = alignement horizontal ; Box = calques superposés.",
            "L'ordre des Modifiers est capital : padding avant background = marge externe ; padding après background = marge interne.",
            "Modifier.weight(1f) dans Row/Column permet d'étirer un composant pour occuper l'espace restant disponible.",
            "Arrangement gère la distribution le long de l'axe principal ; Alignment gère l'alignement sur l'axe secondaire."
        ],
        "prereq": ["Kotlin de base", "Fonctions"],
        "suite": ["card", "scaffold"]
    },

    "card": {
        "id": "card",
        "title": "Créer une Card Material 3",
        "niveau": 2,
        "level": "beg",
        "duration": "10 min",
        "quoi": "Une <b>Card</b> (Carte) Material 3 est un conteneur visuel avec coins arrondis, une surface de couleur dédiée et une légère élévation ou bordure. Elle sert à regrouper des informations liées (titre, image, prix, bouton) en une entité visuelle cohérente.",
        "pourquoi": "Sans Card, les informations flottent sur l'écran sans délimitation claire. La Card crée un repère visuel immédiat pour l'utilisateur, qui perçoit le bloc comme un objet unique cliquable ou manipulable (comme une carte à jouer physique).",
        "quand": "Pour afficher une fiche produit e-commerce, une carte de contact, un article de blog dans un flux d'actualités, ou un bloc de statistiques dans un tableau de bord.",
        "syntaxe": """// Syntaxe standard Material 3
Card(
    modifier = Modifier.fillMaxWidth().padding(8.dp),
    shape = RoundedCornerShape(16.dp),
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.surfaceVariant
    ),
    elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
    onClick = { /* Action au clic */ }
) {
    // Contenu interne (souvent une Column ou Row)
}""",
        "exempleMin": """@Composable
fun CarteSimple() {
    Card(modifier = Modifier.padding(16.dp)) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("Titre de la carte", fontWeight = FontWeight.Bold)
            Text("Description courte du contenu.")
        }
    }
}""",
        "explication": [
            ["Card(modifier = ...)", "Ouvre le conteneur de carte Material 3 avec coins arrondis et ombre portée."],
            ["Column(modifier = Modifier.padding(16.dp))", "CRITIQUE : La Card ne fournit aucune marge interne par défaut. Il faut TOUJOURS ajouter un padding sur le conteneur interne pour que le texte ne colle pas aux bords."],
            ["Text(\"Titre de la carte\")", "Affiche le titre mis en gras."],
            ["Text(\"Description...\")", "Affiche le texte secondaire en dessous."]
        ],
        "exempleReel": """package com.example.app.ui

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * Exemple de A à Z : Fiche Produit E-Commerce complète Material 3
 * Avec gestion d'un favori, calcul de promotion et bouton d'ajout au panier.
 */
@Composable
fun FicheProduitCard(
    nom: String = "Casque Bluetooth ANC",
    prixInitial: Double = 149.99,
    prixPromo: Double = 99.99,
    onAjouterAuPanier: () -> Unit = {}
) {
    var estFavori by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        shape = RoundedCornerShape(20.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // En-tête : Badge Promo + Bouton Favori
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = Color(0xFFC4453A) // Rouge remise
                ) {
                    Text(
                        text = "-33% PROMO",
                        color = Color.White,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }

                IconButton(onClick = { estFavori = !estFavori }) {
                    Icon(
                        imageVector = if (estFavori) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                        contentDescription = "Favori",
                        tint = if (estFavori) Color.Red else Color.Gray
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Titre du produit
            Text(
                text = nom,
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onSurface
            )

            Spacer(modifier = Modifier.height(4.dp))

            // Prix barré et prix promo
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "$prixPromo €",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color(0xFF1E8F72) // Vert succès
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = "$prixInitial €",
                    fontSize = 14.sp,
                    color = Color.Gray,
                    textDecoration = TextDecoration.LineThrough
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Bouton pleine largeur
            Button(
                onClick = onAjouterAuPanier,
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(12.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF7F52FF))
            ) {
                Icon(Icons.Default.ShoppingCart, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Ajouter au panier", fontWeight = FontWeight.SemiBold)
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun FicheProduitPreview() {
    MaterialTheme {
        FicheProduitCard()
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.04.01"))
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
}""",
        "resultat": """┌──────────────────────────────────────┐
│ [-33% PROMO]                    [ ♡ ]│
│                                      │
│ Casque Bluetooth ANC                 │
│ 99.99 €  ~~149.99 €~~                │
│                                      │
│ [ 🛒 Ajouter au panier             ] │
└──────────────────────────────────────┘""",
        "params": [
            ["modifier", "Contrôle les dimensions, marges extérieures (padding), clics et accessibilité."],
            ["shape", "Définit le rayon des coins : RoundedCornerShape(16.dp) ou CircleShape."],
            ["colors", "Couleurs via CardDefaults.cardColors(containerColor = ..., contentColor = ...)."],
            ["elevation", "Ombre via CardDefaults.cardElevation(defaultElevation = 4.dp, pressedElevation = 8.dp)."],
            ["border", "Bordure extérieure fine via BorderStroke(1.dp, Color.LightGray) pour une OutlinedCard."],
            ["onClick", "Rend la carte entière cliquable avec animation d'onde Material ripple."]
        ],
        "erreurs": [
            ["Le contenu touche exactement les bords extérieurs de la carte", "La Card n'applique aucune marge intérieure par défaut. Tu dois impérativement mettre Modifier.padding(...) sur la Column ou Row placée à l'intérieur."],
            ["La Card s'étend sur toute la hauteur de l'écran par erreur", "Évite de mettre Modifier.fillMaxHeight() sur une Card isolée sauf si c'est explicitement voulu (ex: carte de modal plein écran)."]
        ],
        "exercice": {
            "enonce": "Crée une carte de recette culinaire : image ou pastille en haut, titre en gras, temps de préparation ('⏱ 25 min') et niveau ('Facile') alignés dans une Row, et un bouton 'Commencer'.",
            "indice": "Compose : Card { Column(padding) { Text(Titre) ; Row { Text(Temps) ; Text(Niveau) } ; Button } }",
            "solution": """@Composable
fun CarteRecette(
    titre: String = "Pâtes Carbonara Traditionnelles",
    duree: String = "20 min",
    difficulte: String = "Facile"
) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(12.dp),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = titre, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(8.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(text = "⏱ $duree", color = Color.Gray, fontSize = 14.sp)
                Text(text = "⭐ $difficulte", color = Color(0xFFD98A1B), fontWeight = FontWeight.Medium)
            }
            Spacer(modifier = Modifier.height(14.dp))
            Button(
                onClick = { /* Lancer */ },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Commencer la recette")
            }
        }
    }
}"""
        },
        "quiz": {
            "q": "Pourquoi est-il indispensable d'ajouter un Modifier.padding() sur la Column enfant à l'intérieur d'une Card ?",
            "options": [
                "Parce que la Card Compose ne fournit aucun padding intérieur par défaut",
                "Pour rendre la Card cliquable",
                "Pour activer l'élévation de la carte",
                "C'est une obligation imposée par le compilateur Kotlin"
            ],
            "correct": 0,
            "exp": "Contrairement à certains composants d'autres frameworks, la Card de Jetpack Compose ne définit aucune marge intérieure par défaut. Sans padding explicite sur le conteneur interne, les textes et boutons touchent directement les bords arrondis de la carte."
        },
        "retenir": [
            "Card = conteneur Material 3 avec coins arrondis et élévation.",
            "Ajoute TOUJOURS un padding intérieur sur le premier enfant de la Card.",
            "CardDefaults.cardColors() et CardDefaults.cardElevation() permettent de personnaliser l'apparence.",
            "Existe en trois variantes Material 3 : Card (élévée), OutlinedCard (avec bordure), et ElevatedCard."
        ],
        "prereq": ["layout"],
        "suite": ["lazycolumn", "scaffold"]
    },

    "scaffold": {
        "id": "scaffold",
        "title": "Structure d'Écran : Scaffold & TopAppBar",
        "niveau": 3,
        "level": "beg",
        "duration": "14 min",
        "quoi": "Le <b>Scaffold</b> (échafaudage) est le composant d'architecture d'écran standard de Material Design 3. Il fournit les emplacements prédéfinis (slots) pour la barre supérieure (<b>TopAppBar</b>), la barre de navigation inférieure (<b>NavigationBar</b>), le bouton d'action flottant (<b>FloatingActionButton</b>) et la bannière d'alerte (<b>SnackbarHost</b>).",
        "pourquoi": "Sans Scaffold, tu devrais calculer manuellement les hauteurs, positionner la barre d'action au bon endroit, gérer la superposition des notifications éphémères (Snackbars) et éviter que ton contenu ne passe sous la barre de statut de l'appareil. Scaffold orchestre tout cela proprement.",
        "quand": "Sur 100% des écrans principaux d'une application Android ! C'est le composant racine de chaque écran.",
        "syntaxe": """Scaffold(
    topBar = {
        TopAppBar(title = { Text("Mon Titre") })
    },
    floatingActionButton = {
        FloatingActionButton(onClick = { }) { Icon(Icons.Default.Add, null) }
    },
    snackbarHost = { SnackbarHost(snackbarHostState) },
    bottomBar = { /* Barre de navigation */ }
) { innerPadding ->
    // ATTENTION : innerPadding doit être appliqué au contenu !
    Box(modifier = Modifier.padding(innerPadding)) {
        // Contenu principal de l'écran
    }
}""",
        "exempleMin": """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EcranBasique() {
    Scaffold(
        topBar = { TopAppBar(title = { Text("Accueil") }) }
    ) { paddingValues ->
        Text(
            text = "Bonjour tout le monde !",
            modifier = Modifier.padding(paddingValues)
        )
    }
}""",
        "explication": [
            ["Scaffold(...) { innerPadding -> ... }", "Crée la structure d'écran. La lambda fournit `innerPadding`, qui contient la hauteur exacte de la TopBar et des barres système."],
            ["topBar = { TopAppBar(...) }", "Définit la barre d'en-tête de l'écran avec le titre et éventuellement des boutons d'actions."],
            ["Modifier.padding(innerPadding)", "OBLIGATOIRE : Si tu n'appliques pas innerPadding sur ton conteneur, ton contenu se dessinera EN DESSOUS de la barre supérieure et sera masqué !"]
        ],
        "exempleReel": """package com.example.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch

/**
 * Exemple de A à Z : Écran complet avec Scaffold Material 3,
 * TopAppBar, FloatingActionButton et déclenchement d'un Snackbar asynchrone.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EcranPrincipalComplet() {
    // 1. Gestion de l'état du Snackbar et de la coroutine
    val snackbarHostState = remember { SnackbarHostState() }
    val coroutineScope = rememberCoroutineScope()
    var nombreArticles by remember { mutableStateOf(3) }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            TopAppBar(
                title = { Text("Mes Notes", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = { /* Ouvrir Drawer */ }) {
                        Icon(Icons.Default.Menu, contentDescription = "Menu")
                    }
                },
                actions = {
                    IconButton(onClick = { /* Rechercher */ }) {
                        Icon(Icons.Default.Search, contentDescription = "Rechercher")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = {
                    nombreArticles++
                    coroutineScope.launch {
                        snackbarHostState.showSnackbar(
                            message = "Nouvelle note #$nombreArticles créée !",
                            actionLabel = "OK",
                            duration = SnackbarDuration.Short
                        )
                    }
                },
                containerColor = Color(0xFF7F52FF),
                contentColor = Color.White
            ) {
                Icon(Icons.Default.Add, contentDescription = "Ajouter")
            }
        },
        floatingActionButtonPosition = FabPosition.End
    ) { innerPadding ->
        // Contenu de la page recevant impérativement innerPadding
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(
                text = "Total des notes enregistrées : $nombreArticles",
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium
            )

            repeat(nombreArticles) { index ->
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Text(
                        text = "Note numéro ${index + 1} : Rappel important",
                        modifier = Modifier.padding(16.dp)
                    )
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun EcranPrincipalPreview() {
    MaterialTheme {
        EcranPrincipalComplet()
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.04.01"))
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.0")
}""",
        "resultat": """┌──────────────────────────────────────┐
│ [≡] Mes Notes                    [🔍]│  ← TopAppBar
├──────────────────────────────────────┤
│ Total des notes enregistrées : 3     │
│ ┌──────────────────────────────────┐ │
│ │ Note numéro 1 : Rappel important │ │
│ └──────────────────────────────────┘ │
│ ┌──────────────────────────────────┐ │
│ │ Note numéro 2 : Rappel important │ │
│ └──────────────────────────────────┘ │
│                                      │
│                                [ + ] │  ← FloatingActionButton
│ ┌──────────────────────────────────┐ │
│ │ Nouvelle note #4 créée !    [OK] │ │  ← SnackbarHost
└─┴──────────────────────────────────┴─┘""",
        "params": [
            ["topBar", "Slot recevant le composant d'en-tête (généralement TopAppBar, CenterAlignedTopAppBar, LargeTopAppBar)."],
            ["bottomBar", "Slot recevant la barre de navigation basse (NavigationBar avec des NavigationBarItem)."],
            ["snackbarHost", "Composant récepteur gérant l'apparition animée des bannières Snackbar via SnackbarHostState."],
            ["floatingActionButton", "Bouton d'action proéminent (FAB) flottant au-dessus du contenu."],
            ["floatingActionButtonPosition", "Position du FAB : FabPosition.End (droite par défaut) ou FabPosition.Center."],
            ["innerPadding", "PaddingValues fournies par la lambda de Scaffold pour compenser les barres et insets système."]
        ],
        "erreurs": [
            ["Le contenu principal est masqué derrière la TopAppBar", "C'est l'erreur la plus fréquente : tu as oublié d'appliquer le paramètre `innerPadding` fourni par la lambda de Scaffold via `Modifier.padding(innerPadding)` sur le composant racine."],
            ["Calling showSnackbar outside a coroutine", "La fonction `snackbarHostState.showSnackbar()` est une `suspend fun`. Elle doit impérativement être appelée dans une Coroutine via `coroutineScope.launch { ... }`."]
        ],
        "exercice": {
            "enonce": "Ajoute une TopAppBar centrée (CenterAlignedTopAppBar) avec un titre 'Mon Profil' et une icône de cadenas verrouillé à droite.",
            "indice": "Utilise CenterAlignedTopAppBar(title = { Text('Mon Profil') }, actions = { IconButton { Icon(Icons.Default.Lock) } })",
            "solution": """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EcranProfilScaffold() {
    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("Mon Profil", fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.Default.Lock, contentDescription = "Sécurité")
                    }
                }
            )
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
            Text("Informations du compte")
        }
    }
}"""
        },
        "quiz": {
            "q": "Que se passe-t-il si l'on ignore le paramètre `innerPadding` fourni par le Scaffold ?",
            "options": [
                "Le contenu démarre au tout début de l'écran (y=0) et se retrouve caché sous la TopAppBar",
                "Le Scaffold lève une exception et fait planter l'application",
                "La TopAppBar disparaît automatiquement",
                "Les boutons du Scaffold deviennent inactifs"
            ],
            "correct": 0,
            "exp": "Scaffold superpose la TopBar et le contenu dans un conteneur Box interne. Si tu n'appliques pas `Modifier.padding(innerPadding)` sur ton contenu, celui-ci commence tout en haut de l'écran et passe derrière la TopAppBar."
        },
        "retenir": [
            "Scaffold est le squelette de tout écran Android moderne Material 3.",
            "Il regroupe : topBar, bottomBar, snackbarHost et floatingActionButton.",
            "Tu dois TOUJOURS appliquer `Modifier.padding(innerPadding)` au contenu principal.",
            "Pour afficher un Snackbar, utilise `rememberCoroutineScope` et `snackbarHostState.showSnackbar()`."
        ],
        "prereq": ["layout"],
        "suite": ["lazycolumn", "navigation"]
    },

    "lazycolumn": {
        "id": "lazycolumn",
        "title": "Listes Défilantes Performantes (LazyColumn)",
        "niveau": 3,
        "level": "beg",
        "duration": "15 min",
        "quoi": "<b>LazyColumn</b> est le composant de défilement vertical paresseux (« lazy ») de Jetpack Compose. Contrairement à un Column classique, il ne compose et ne dessine à l'écran que les éléments actuellement visibles dans la zone d'affichage du téléphone, recyclant les ressources pour garantir une fluidité parfaite à 60/120 images par seconde.",
        "pourquoi": "Si tu as une liste de 1 000 articles ou messages, un simple Column créerait 1 000 vues en mémoire dès l'ouverture de la page, bloquant le smartphone. LazyColumn est l'équivalent moderne du `RecyclerView` classique d'Android, sans aucun code boilerplate (fini les Adapters et ViewHolders !).",
        "quand": "Dès que tu affiches une collection de données de taille inconnue, dynamique ou supérieure à 10 éléments : fils de réseaux sociaux, catalogues e-commerce, boîtes de réception d'emails, résultats de recherche.",
        "syntaxe": """LazyColumn(
    modifier = Modifier.fillMaxSize(),
    contentPadding = PaddingValues(16.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    // 1. Un item unique
    item { EnTeteSection() }

    // 2. Une liste dynamique d'objets
    items(
        items = listeObjets,
        key = { it.id } // Clé stable indispensable
    ) { objet ->
        ItemVue(objet)
    }
}""",
        "exempleMin": """@Composable
fun ListeNoms(noms: List<String>) {
    LazyColumn {
        items(noms) { nom ->
            Text(text = nom, modifier = Modifier.padding(12.dp))
        }
    }
}""",
        "explication": [
            ["LazyColumn { ... }", "Initialise la liste défilante paresseuse."],
            ["items(noms) { nom -> ... }", "Itère sur la collection `noms` et génère un Composable à la volée pour chaque élément visible."],
            ["Text(text = nom)", "Affiche l'élément courant pendant le défilement."]
        ],
        "exempleReel": """package com.example.app.ui

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// 1. Modèle de données
data class Contact(val id: Int, val nom: String, val telephone: String, val groupe: String)

/**
 * Exemple de A à Z : Annuaire téléphonique avec LazyColumn,
 * en-têtes collants (stickyHeader), clés stables et suppression animée.
 */
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun AnnuaireContactsComplet() {
    var contacts by remember {
        mutableStateOf(
            listOf(
                Contact(1, "Alice Dubois", "06 12 34 56 78", "Famille"),
                Contact(2, "Antoine Martin", "07 98 76 54 32", "Famille"),
                Contact(3, "Béatrice Roux", "06 45 67 89 01", "Amis"),
                Contact(4, "Bernard Henry", "06 22 33 44 55", "Amis"),
                Contact(5, "Claire Petit", "07 11 22 33 44", "Travail"),
                Contact(6, "Damien Vallet", "06 99 88 77 66", "Travail")
            )
        )
    }

    // Regroupement par catégorie
    val contactsParGroupe = contacts.groupBy { it.groupe }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        contactsParGroupe.forEach { (groupe, listeDuGroupe) ->
            // En-tête de groupe collant lors du défilement
            stickyHeader {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.primaryContainer,
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text(
                        text = "Catégorie : $groupe (${listeDuGroupe.size})",
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
            }

            // Éléments de la liste avec clé stable obligatoire
            items(
                items = listeDuGroupe,
                key = { contact -> contact.id }
            ) { contact ->
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(14.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Default.Phone,
                            contentDescription = null,
                            tint = Color(0xFF7F52FF),
                            modifier = Modifier.size(24.dp)
                        )

                        Spacer(modifier = Modifier.width(12.dp))

                        Column(modifier = Modifier.weight(1f)) {
                            Text(text = contact.nom, fontWeight = FontWeight.SemiBold, fontSize = 15.sp)
                            Text(text = contact.telephone, color = Color.Gray, fontSize = 13.sp)
                        }

                        IconButton(onClick = {
                            contacts = contacts.filter { it.id != contact.id }
                        }) {
                            Icon(Icons.Default.Delete, contentDescription = "Supprimer", tint = Color.Red.copy(alpha = 0.7f))
                        }
                    }
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun AnnuairePreview() {
    MaterialTheme {
        AnnuaireContactsComplet()
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.04.01"))
    implementation("androidx.compose.foundation:foundation")
    implementation("androidx.compose.material3:material3")
}""",
        "resultat": """[ Catégorie : Famille (2) ]  ← stickyHeader (reste fixé)
┌──────────────────────────────────────┐
│ 📞 Alice Dubois         06 12... [🗑]│
├──────────────────────────────────────┤
│ 📞 Antoine Martin       07 98... [🗑]│
└──────────────────────────────────────┘
[ Catégorie : Amis (2) ]
┌──────────────────────────────────────┐
│ 📞 Béatrice Roux        06 45... [🗑]│
└──────────────────────────────────────┘
     ↓ (Défilement fluide de 10 000 items)""",
        "params": [
            ["items(list, key = { it.id })", "Itère sur la liste. Le paramètre `key` identifie chaque item de manière stable pour optimiser les animations et la mémoire."],
            ["item { }", "Insère un élément unique non issu d'une liste (ex: un titre de section, un bandeau publicitaire, un loader)."],
            ["contentPadding", "Applique des marges intérieures globales sans rogner le défilement sous les barres de statut."],
            ["verticalArrangement", "Définit l'espacement automatique entre items : Arrangement.spacedBy(10.dp)."],
            ["stickyHeader { }", "Crée un en-tête qui reste collé en haut de l'écran tant que ses enfants défilent."],
            ["LazyRow", "Variante pour un défilement horizontal (ex: carrousel d'histoires ou de catégories)."]
        ],
        "erreurs": [
            ["Crash : IllegalStateException: Vertically scrollable component was measured with an infinity height", "Cette erreur se produit quand tu mets une `LazyColumn` à l'intérieur d'un `Column(Modifier.verticalScroll())`. Les deux conteneurs tentent de gérer le scroll infini en même temps. SOLUTION : Supprime le `verticalScroll()` du parent !"],
            ["Oublier la clé unique `key = { it.id }`", "Sans clé, lors de la suppression d'un élément, Compose ne sait pas quel Composable recycler : l'état interne des champs ou cases à cocher sera décalé sur l'élément voisin, provoquant des bugs visuels majeurs."]
        ],
        "exercice": {
            "enonce": "Affiche une liste de 20 tâches numérotées ('Tâche #1', 'Tâche #2'...). Chaque tâche doit être une Card avec une Checkbox pour marquer si elle est faite.",
            "indice": "Crée une data class Tache(val id: Int, val titre: String, val faite: Boolean), puis items(taches, key = { it.id }) avec une Row contenant Text et Checkbox.",
            "solution": """data class TacheItem(val id: Int, val titre: String, val terminee: Boolean = false)

@Composable
fun ListeTachesDemo() {
    var taches by remember {
        mutableStateOf((1..20).map { TacheItem(it, "Tâche importante #$it") })
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(taches, key = { it.id }) { tache ->
            Card(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(tache.titre, fontWeight = FontWeight.Medium)
                    Checkbox(
                        checked = tache.terminee,
                        onCheckedChange = { isChecked ->
                            taches = taches.map { if (it.id == tache.id) it.copy(terminee = isChecked) else it }
                        }
                    )
                }
            }
        }
    }
}"""
        },
        "quiz": {
            "q": "Pourquoi est-il primordial de renseigner le paramètre `key = { it.id }` dans la fonction items() d'une LazyColumn ?",
            "options": [
                "Pour permettre à Compose de suivre avec certitude chaque élément lors des ajouts, suppressions et réorganisations",
                "Pour trier automatiquement la liste par ordre alphabétique",
                "C'est indispensable pour que le scroll fonctionne",
                "Pour crypter les données affichées à l'écran"
            ],
            "correct": 0,
            "exp": "Le paramètre `key` fournit un identifiant stable et unique. Sans lui, Compose utilise la position de l'élément (0, 1, 2...) : si tu supprimes le premier item, Compose recycle mal les vues et l'état visuel est attribué par erreur à l'élément suivant."
        },
        "retenir": [
            "LazyColumn = recyclage virtuel ultra-performant pour les listes verticales.",
            "items(liste, key = { it.id }) est la façon canonique d'afficher des données.",
            "Ne JAMAIS imbriquer une LazyColumn dans un Column avec verticalScroll.",
            "Utilise `contentPadding = PaddingValues(...)` pour ajouter des marges sans couper le scroll."
        ],
        "prereq": ["layout", "card"],
        "suite": ["state", "crud"]
    }
}

print("Partie 1 chargée avec succès (4 leçons).")
