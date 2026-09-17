# -*- coding: utf-8 -*-
"""
Leçons Partie 3 : Données Robustes, CRUD, Réseau & Navigation
9. room (SQLite, Entity, Dao, RoomDatabase, Flow)
10. crud (Create, Read, Update, Delete complet avec Dialog et confirmation)
11. api (Retrofit, REST, JSON DTO, Moshi, Coroutines, gestion d'erreurs)
12. navigation (Navigation Compose, NavHost, NavController, arguments typés)
"""

LESSONS_PART3 = {
    "room": {
        "id": "room",
        "title": "Base de Données Locale SQLite avec Room",
        "niveau": 6,
        "level": "adv",
        "duration": "20 min",
        "quoi": "<b>Room</b> est la bibliothèque officielle de persistance d'Android fournissant une couche d'abstraction puissante au-dessus de SQLite. Elle repose sur 3 piliers : les <b>Entity</b> (représentent les tables SQL sous forme de data classes Kotlin), les <b>DAO</b> (Data Access Object, interfaces déclarant les requêtes SQL), et la <b>Database</b> (la classe maîtresse gérant l'ouverture et les migrations du fichier de base de données).",
        "pourquoi": "DataStore est parfait pour de petites préférences, mais incapable de gérer des données structurées et relationnelles (tri, filtrage par date ou prix, jointures). Écrire du code SQLite brut en Android classique provoquait d'innombrables bugs découverts uniquement à l'exécution. Room **vérifie la syntaxe de vos requêtes SQL à la compilation** : si vous tapez une faute dans le nom d'une colonne, le projet refuse de compiler !",
        "quand": "Dès que l'application doit fonctionner hors-connexion (Offline-First) avec des listes d'éléments structurés : catalogue de produits, tâches, messages de chat, articles favoris, historique.",
        "syntaxe": """// 1. Entité (Table SQL)
@Entity(tableName = "produits")
data class ProduitEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val nom: String,
    val prix: Double
)

// 2. DAO (Data Access Object)
@Dao
interface ProduitDao {
    @Query("SELECT * FROM produits ORDER BY nom ASC")
    fun observerTousLesProduits(): Flow<List<ProduitEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun inserer(produit: ProduitEntity): Long

    @Delete
    suspend fun supprimer(produit: ProduitEntity)
}

// 3. Database
@Database(entities = [ProduitEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun produitDao(): ProduitDao
}""",
        "exempleMin": """@Entity
data class Tache(@PrimaryKey(autoGenerate = true) val id: Int = 0, val titre: String)

@Dao
interface TacheDao {
    @Query("SELECT * FROM Tache")
    fun getAll(): Flow<List<Tache>>

    @Insert
    suspend fun insert(tache: Tache)
}""",
        "explication": [
            ["@Entity(tableName = \"produits\")", "Marque la classe Kotlin comme schéma de table SQLite relationnelle."],
            ["@PrimaryKey(autoGenerate = true)", "Définit la clé primaire avec auto-incrémentation automatique par SQLite."],
            ["@Dao", "Interface déclarant les requêtes. Room génère tout le code d'implémentation Java/Kotlin sous le capot via KSP."],
            ["fun ...: Flow<List<Produit>>", "MAGIE RECOMPOSE : Room surveille la table en temps réel. Dès qu'un produit est ajouté ou supprimé, ce Flow émet instantanément la nouvelle liste vers l'écran !"],
            ["suspend fun inserer(...)", "Les écritures doivent impérativement être `suspend` pour s'exécuter hors du thread UI."]
        ],
        "exempleReel": """package com.example.app.data

import android.content.Context
import androidx.room.*
import kotlinx.coroutines.flow.Flow

// ══════════════════════════════════════════
// 1. ENTITÉ : Table 'articles'
// ══════════════════════════════════════════
@Entity(tableName = "articles")
data class ArticleEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val titre: String,
    val quantite: Int,
    val estAchete: Boolean = false
)

// ══════════════════════════════════════════
// 2. DAO : Requêtes SQL typées
// ══════════════════════════════════════════
@Dao
interface ArticleDao {

    @Query("SELECT * FROM articles ORDER BY estAchete ASC, id DESC")
    fun observerArticles(): Flow<List<ArticleEntity>>

    @Query("SELECT * FROM articles WHERE id = :id")
    suspend fun getArticleParId(id: Long): ArticleEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insererArticle(article: ArticleEntity): Long

    @Update
    suspend fun modifierArticle(article: ArticleEntity)

    @Delete
    suspend fun supprimerArticle(article: ArticleEntity)

    @Query("DELETE FROM articles WHERE estAchete = 1")
    suspend fun supprimerArticlesAchetes()
}

// ══════════════════════════════════════════
// 3. BASE DE DONNÉES : Singleton Room
// ══════════════════════════════════════════
@Database(entities = [ArticleEntity::class], version = 1, exportSchema = false)
abstract class InventaireDatabase : RoomDatabase() {

    abstract fun articleDao(): ArticleDao

    companion object {
        @Volatile
        private var INSTANCE: InventaireDatabase? = null

        fun getDatabase(context: Context): InventaireDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    InventaireDatabase::class.java,
                    "inventaire_courses.db"
                )
                .fallbackToDestructiveMigration() // Recrée la base si version incrémentée en dev
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}

// ══════════════════════════════════════════
// 4. REPOSITORY : Couche d'abstraction
// ══════════════════════════════════════════
class InventaireRepository(private val dao: ArticleDao) {
    val tousLesArticles: Flow<List<ArticleEntity>> = dao.observerArticles()

    suspend fun ajouter(titre: String, quantite: Int) {
        dao.insererArticle(ArticleEntity(titre = titre, quantite = quantite))
    }

    suspend fun basculerAchat(article: ArticleEntity) {
        dao.modifierArticle(article.copy(estAchete = !article.estAchete))
    }

    suspend fun supprimer(article: ArticleEntity) {
        dao.supprimerArticle(article)
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
plugins {
    id("com.google.devtools.ksp") version "1.9.23-1.0.20"
}

dependencies {
    val roomVersion = "2.6.1"
    implementation("androidx.room:room-runtime:$roomVersion")
    implementation("androidx.room:room-ktx:$roomVersion") // Support des Coroutines et Flow
    ksp("androidx.room:room-compiler:$roomVersion") // Générateur de code KSP
}""",
        "resultat": """Écran Compose (LazyColumn)
      ▲ (Recomposition automatique dès qu'une ligne change !)
      │
Flow<List<ArticleEntity>> (Room Observer)
      ▲
DAO : @Query("SELECT * FROM articles")
      ▲
Base de données locale SQLite : 'inventaire_courses.db'
(Sauvegardé définitivement sur le téléphone, 100% hors-ligne)""",
        "params": [
            ["@Entity(tableName = ...)", "Définit le nom exact de la table dans SQLite."],
            ["@PrimaryKey(autoGenerate = true)", "Active l'incrémentation automatique de la clé primaire par SQLite."],
            ["@Insert(onConflict = OnConflictStrategy.REPLACE)", "En cas de conflit sur une clé déjà existante, remplace la ligne au lieu de faire planter l'application."],
            ["Flow<List<T>>", "Transforme une requête SQL en flux réactif : toute modification dans la table déclenche un nouvel émission instantanée."],
            ["version = 1", "Numéro de version de la base, à incrémenter de 1 à chaque ajout ou modification de colonne."]
        ],
        "erreurs": [
            ["Crash : Cannot access database on the main thread since it may potentially lock the UI for a long period of time", "Cette erreur majeure survient lorsque tu appelles une requête DAO d'écriture en dehors d'une Coroutine (`suspend`). Toutes les méthodes du DAO (sauf celles qui retournent un Flow) doivent être marquées `suspend` et appelées avec `viewModelScope.launch`."],
            ["Crash : Room cannot verify the data integrity. Looks like you've changed the schema but forgot to update the builder version", "Tu as modifié un champ dans ton `@Entity` sans changer le numéro `version = 2` dans `@Database`. En phase de développement, ajoute `.fallbackToDestructiveMigration()` dans ton `Room.databaseBuilder()`."]
        ],
        "exercice": {
            "enonce": "Ajoute une requête dans le DAO pour compter le nombre total d'articles restant à acheter : fun compterArticlesRestants(): Flow<Int>.",
            "indice": "Utilise l'annotation @Query(\"SELECT COUNT(*) FROM articles WHERE estAchete = 0\").",
            "solution": """@Query("SELECT COUNT(*) FROM articles WHERE estAchete = 0")
fun compterArticlesRestants(): Flow<Int>"""
        },
        "quiz": {
            "q": "Pourquoi est-il fortement recommandé de faire renvoyer un `Flow<List<T>>` par une fonction `@Query` de Room plutôt qu'une simple `List<T>` synchrone ?",
            "options": [
                "Parce que le Flow informe automatiquement Jetpack Compose dès qu'une insertion, modification ou suppression survient dans la table",
                "Pour chiffrer les données stockées dans SQLite",
                "Parce que SQLite ne supporte pas le type List en Kotlin",
                "C'est une obligation du plugin KSP"
            ],
            "correct": 0,
            "exp": "Lorsqu'une méthode `@Query` retourne un `Flow`, Room surveille automatiquement la table SQLite. Dès qu'une modification intervient (ajout, suppression, mise à jour), Room ré-exécute la requête en arrière-plan et émet la nouvelle liste : l'interface Jetpack Compose se met à jour en temps réel sans aucun code de rafraîchissement manuel !"
        },
        "retenir": [
            "Room est le pont sécurisé et typé au-dessus de SQLite.",
            "@Entity = la table SQL ; @Dao = les requêtes ; @Database = le gestionnaire.",
            "Les requêtes retournant un Flow sont automatiquement réactives en temps réel.",
            "Les fonctions d'écriture (@Insert, @Update, @Delete) doivent TOUJOURS être `suspend`."
        ],
        "prereq": ["mvvm", "viewmodel"],
        "suite": ["crud", "api"]
    },

    "crud": {
        "id": "crud",
        "title": "Créer un CRUD Complet de A à Z",
        "niveau": 6,
        "level": "adv",
        "duration": "22 min",
        "quoi": "<b>CRUD</b> est l'acronyme universel pour les quatre opérations fondamentales de gestion de données : <b>C</b>reate (Créer), <b>R</b>ead (Lire), <b>U</b>pdate (Modifier) et <b>D</b>elete (Supprimer).",
        "pourquoi": "90% des applications mobiles (gestionnaires de tâches, carnets de contacts, fiches clients, catalogues) reposent sur ces 4 opérations. Structurer un CRUD complet et robuste de A à Z — avec dialogue de saisie, validation des données et confirmation de suppression — est le modèle d'architecture réutilisable par excellence pour réussir vos examens et projets professionnels.",
        "quand": "Dès qu'un utilisateur doit manipuler une collection d'enregistrements qu'il peut ajouter, consulter, éditer ou retirer en toute sécurité.",
        "syntaxe": """// Les 4 piliers dans le DAO
@Insert suspend fun creer(item: Item)                // CREATE
@Query("SELECT * FROM items") fun lire(): Flow<List<Item>> // READ
@Update suspend fun modifier(item: Item)              // UPDATE
@Delete suspend fun supprimer(item: Item)             // DELETE""",
        "exempleMin": """class ItemViewModel(private val dao: ItemDao) : ViewModel() {
    val items = dao.lire().stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
    fun ajouter(nom: String) = viewModelScope.launch { dao.creer(Item(nom = nom)) }
    fun supprimer(item: Item) = viewModelScope.launch { dao.supprimer(item) }
}""",
        "explication": [
            ["CREATE (Insert)", "Ajoute une nouvelle entrée en base avec un formulaire ou une boîte de dialogue."],
            ["READ (Query)", "Alimente la `LazyColumn` grâce à un `Flow` réactif qui s'actualise tout seul."],
            ["UPDATE (Update)", "Modifie les propriétés d'un enregistrement existant (ex: marquer comme payé ou changer le titre)."],
            ["DELETE (Delete)", "Retire définitivement la ligne de la base, TOUJOURS précédé d'une boîte de confirmation (`AlertDialog`) pour éviter les fausses manipulations."]
        ],
        "exempleReel": """package com.example.app.crud

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

// 1. Modèle
data class Produit(val id: Long, val nom: String, val prix: Double)

// 2. ViewModel CRUD
class CrudViewModel : ViewModel() {
    private val _produits = MutableStateFlow<List<Produit>>(
        listOf(
            Produit(1, "Clavier Mécanique RGB", 89.99),
            Produit(2, "Souris Ergonomique", 45.50),
            Produit(3, "Écran 27 pouces 144Hz", 249.00)
        )
    )
    val produits: StateFlow<List<Produit>> = _produits.asStateFlow()

    // CREATE
    fun ajouterProduit(nom: String, prix: Double) {
        val nouveau = Produit(id = System.currentTimeMillis(), nom = nom, prix = prix)
        _produits.value = _produits.value + nouveau
    }

    // UPDATE
    fun modifierProduit(produitModifie: Produit) {
        _produits.value = _produits.value.map {
            if (it.id == produitModifie.id) produitModifie else it
        }
    }

    // DELETE
    fun supprimerProduit(id: Long) {
        _produits.value = _produits.value.filter { it.id != id }
    }
}

// 3. Vue CRUD Complète avec Dialogues
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EcranCrudComplet(viewModel: CrudViewModel = remember { CrudViewModel() }) {
    val produits by viewModel.produits.collectAsStateWithLifecycle()

    // États pour les boîtes de dialogue
    var afficherDialogueAjout by remember { mutableStateOf(false) }
    var produitAEditer by remember { mutableStateOf<Produit?>(null) }
    var produitASupprimer by remember { mutableStateOf<Produit?>(null) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Gestion Produits (CRUD)", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { afficherDialogueAjout = true },
                containerColor = Color(0xFF7F52FF),
                contentColor = Color.White
            ) {
                Icon(Icons.Default.Add, contentDescription = "Ajouter")
            }
        }
    ) { padding ->
        // [READ] Liste dynamique
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(produits, key = { it.id }) { produit ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(produit.nom, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Text(String.format("%.2f €", produit.prix), color = Color(0xFF1E8F72), fontWeight = FontWeight.SemiBold)
                        }

                        // Bouton UPDATE
                        IconButton(onClick = { produitAEditer = produit }) {
                            Icon(Icons.Default.Edit, contentDescription = "Modifier", tint = Color.Gray)
                        }

                        // Bouton DELETE
                        IconButton(onClick = { produitASupprimer = produit }) {
                            Icon(Icons.Default.Delete, contentDescription = "Supprimer", tint = Color(0xFFC4453A))
                        }
                    }
                }
            }
        }

        // [CREATE] Dialogue d'Ajout
        if (afficherDialogueAjout) {
            DialogueFormulaireProduit(
                titre = "Nouveau Produit",
                nomInitial = "",
                prixInitial = "",
                onConfirmer = { nom, prix ->
                    viewModel.ajouterProduit(nom, prix)
                    afficherDialogueAjout = false
                },
                onAnnuler = { afficherDialogueAjout = false }
            )
        }

        // [UPDATE] Dialogue de Modification
        produitAEditer?.let { produit ->
            DialogueFormulaireProduit(
                titre = "Modifier le produit",
                nomInitial = produit.nom,
                prixInitial = produit.prix.toString(),
                onConfirmer = { nouveauNom, nouveauPrix ->
                    viewModel.modifierProduit(produit.copy(nom = nouveauNom, prix = nouveauPrix))
                    produitAEditer = null
                },
                onAnnuler = { produitAEditer = null }
            )
        }

        // [DELETE] Dialogue de Confirmation
        produitASupprimer?.let { produit ->
            AlertDialog(
                onDismissRequest = { produitASupprimer = null },
                title = { Text("Confirmer la suppression") },
                text = { Text("Êtes-vous sûr de vouloir supprimer définitivement « \${produit.nom} » ?") },
                confirmButton = {
                    Button(
                        onClick = {
                            viewModel.supprimerProduit(produit.id)
                            produitASupprimer = null
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                    ) {
                        Text("Supprimer")
                    }
                },
                dismissButton = {
                    OutlinedButton(onClick = { produitASupprimer = null }) { Text("Annuler") }
                }
            )
        }
    }
}

@Composable
fun DialogueFormulaireProduit(
    titre: String,
    nomInitial: String,
    prixInitial: String,
    onConfirmer: (String, Double) -> Unit,
    onAnnuler: () -> Unit
) {
    var nom by remember { mutableStateOf(nomInitial) }
    var prix by remember { mutableStateOf(prixInitial) }

    AlertDialog(
        onDismissRequest = onAnnuler,
        title = { Text(titre, fontWeight = FontWeight.Bold) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                OutlinedTextField(
                    value = nom,
                    onValueChange = { nom = it },
                    label = { Text("Nom du produit") },
                    singleLine = true
                )
                OutlinedTextField(
                    value = prix,
                    onValueChange = { prix = it },
                    label = { Text("Prix (€)") },
                    singleLine = true
                )
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val prixDouble = prix.toDoubleOrNull() ?: 0.0
                    if (nom.isNotBlank()) onConfirmer(nom, prixDouble)
                },
                enabled = nom.isNotBlank() && (prix.toDoubleOrNull() != null)
            ) {
                Text("Enregistrer")
            }
        },
        dismissButton = {
            OutlinedButton(onClick = onAnnuler) { Text("Annuler") }
        }
    )
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")
    implementation("androidx.compose.material3:material3")
}""",
        "resultat": """[ + ] Clic sur FAB  ──▶ Boîte de dialogue [CREATE] ──▶ Élément inséré !
┌───────────────────────────────────────────┐
│ Clavier Mécanique       89.99 €  [✎]  [🗑]│
├───────────────────────────────────────────┤
│ Souris Ergonomique      45.50 €  [✎]  [🗑]│
└───────────────────────────────────────────┘
   │ [✎] Clic Modifier ──▶ Dialogue prérempli [UPDATE]
   │ [🗑] Clic Poubelle  ──▶ AlertDialog "Supprimer ?" [DELETE]""",
        "params": [
            ["Create", "Saisie utilisateur -> Validation non vide -> Appel ViewModel.inserer()"],
            ["Read", "Observation du Flow continu dans la LazyColumn (zéro rafraîchissement manuel nécessaire)"],
            ["Update", "Sélection de l'objet -> Pré-remplissage du formulaire -> `copy()` et mise à jour"],
            ["Delete", "Sélection de l'id -> AlertDialog de confirmation sécurisée -> Suppression en base"]
        ],
        "erreurs": [
            ["Supprimer un élément directement sans confirmation préalable", "Un clic accidentel sur un écran tactile est fréquent. Supprimer une donnée sans afficher d'AlertDialog de confirmation est une mauvaise pratique majeure en ergonomie mobile."],
            ["Modifier directement un objet sans créer de copie .copy()", "En programmation fonctionnelle et Compose, les modèles de données doivent être immuables (val). Pour modifier une propriété, utilise toujours la méthode de copie générée : `monProduit.copy(prix = nouveauPrix)`."]
        ],
        "exercice": {
            "enonce": "Ajoute une fonctionnalité de recherche en direct au CRUD : une barre de recherche au-dessus de la liste qui filtre instantanément les produits par leur nom.",
            "indice": "Crée `var filtre by remember { mutableStateOf('') }`, puis `produits.filter { it.nom.contains(filtre, ignoreCase = true) }` avant de passer la liste à la LazyColumn.",
            "solution": """var filtre by remember { mutableStateOf("") }

OutlinedTextField(
    value = filtre,
    onValueChange = { filtre = it },
    placeholder = { Text("Rechercher un produit...") },
    modifier = Modifier.fillMaxWidth().padding(16.dp)
)

val produitsFiltres = remember(produits, filtre) {
    produits.filter { it.nom.contains(filtre, ignoreCase = true) }
}
// Afficher ensuite produitsFiltres dans items()"""
        },
        "quiz": {
            "q": "Pourquoi les data classes manipulées dans un CRUD Jetpack Compose doivent-elles avoir des champs déclarés avec 'val' plutôt que 'var' ?",
            "options": [
                "Parce que l'immuabilité garantit que Compose détecte avec certitude les changements de références d'objets pour déclencher la recomposition",
                "Parce que Kotlin interdit les 'var' dans les data classes",
                "Pour rendre les données compatibles avec SQLite",
                "Pour économiser de la mémoire vive sur le smartphone"
            ],
            "correct": 0,
            "exp": "Compose s'appuie sur la comparaison des références pour savoir s'il doit redessiner un élément. Si un objet est mutable (var) et qu'on modifie un champ interne, la référence de l'objet reste la même : Compose ne s'en rend pas compte et n'actualise pas l'écran. L'immuabilité (val + copy()) est la règle d'or."
        },
        "retenir": [
            "CRUD = Create, Read, Update, Delete.",
            "Utilise toujours des data classes immuables (`val`) et la fonction `.copy()`.",
            "Protège TOUJOURS l'opération Delete par une boîte de dialogue AlertDialog.",
            "La couche ViewModel orchestre le tout en isolant l'UI de la source de données."
        ],
        "prereq": ["room", "viewmodel"],
        "suite": ["api", "navigation"]
    },

    "api": {
        "id": "api",
        "title": "Consommer une API REST avec Retrofit & Moshi",
        "niveau": 7,
        "level": "adv",
        "duration": "20 min",
        "quoi": "<b>Retrofit</b> est le standard absolu de l'écosystème Android pour effectuer des requêtes HTTP (GET, POST, PUT, DELETE) vers un serveur web distant. Associé à un convertisseur JSON comme <b>Moshi</b> ou <b>Gson</b>, Retrofit transforme automatiquement les réponses JSON envoyées par le serveur en objets data classes Kotlin prêts à l'emploi.",
        "pourquoi": "Écrire du code réseau manuel avec HttpURLConnection nécessite des centaines de lignes de code complexe pour gérer les flux d'octets, les codes de statut HTTP, les timeouts et la sérialisation JSON. Retrofit transforme cette complexité en une simple **interface Kotlin annotée** (`@GET`, `@POST`), exécutée dans des coroutines fluides.",
        "quand": "Dès que l'application a besoin de données distantes : météo en direct, catalogue d'un site marchand, authentification utilisateur, fil d'actualités, messagerie instantanée.",
        "syntaxe": """// 1. Déclaration de l'interface Retrofit
interface ApiService {
    @GET("products")
    suspend fun getProduits(): List<ProduitDto>

    @GET("products/{id}")
    suspend fun getProduitParId(@Path("id") id: Long): ProduitDto

    @POST("products")
    suspend fun creerProduit(@Body produit: ProduitDto): ProduitDto
}

// 2. Création du client singleton
val retrofit = Retrofit.Builder()
    .baseUrl("https://api.monsite.com/v1/")
    .addConverterFactory(MoshiConverterFactory.create())
    .build()

val api = retrofit.create(ApiService::class.java)""",
        "exempleMin": """interface MeteoApi {
    @GET("weather")
    suspend fun getMeteo(@Query("city") ville: String): MeteoResponse
}

// Appel dans une coroutine
val meteo = api.getMeteo("Paris")""",
        "explication": [
            ["@GET(\"products\")", "Indique que cette fonction effectue une requête HTTP GET vers l'URL https://.../products."],
            ["suspend fun", "La requête s'exécute de manière asynchrone hors du thread UI pour ne jamais faire saccader l'écran."],
            ["MoshiConverterFactory", "Moteur qui analyse le JSON brut reçu du serveur et instancie automatiquement la data class Kotlin correspondante."],
            ["@Path(\"id\") / @Query(\"...\")", "Insère dynamiquement des variables dans le chemin ou les paramètres de l'URL (?city=Paris)."]
        ],
        "exempleReel": """package com.example.app.network

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.squareup.moshi.Json
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import retrofit2.http.GET
import java.io.IOException

// ══════════════════════════════════════════
// 1. MODÈLE DTO (Data Transfer Object)
// ══════════════════════════════════════════
data class ProduitApiDto(
    val id: Long,
    val title: String,
    val price: Double,
    @Json(name = "description") val description: String,
    val category: String
)

// ══════════════════════════════════════════
// 2. INTERFACE RETROFIT
// ══════════════════════════════════════════
interface FakeStoreApiService {
    @GET("products")
    suspend fun fetchProduits(): List<ProduitApiDto>
}

// ══════════════════════════════════════════
// 3. CLIENT SINGLETON RÉSEAU
// ══════════════════════════════════════════
object RetrofitClient {
    private const val BASE_URL = "https://fakestoreapi.com/"

    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    val apiService: FakeStoreApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(MoshiConverterFactory.create(moshi))
            .build()
            .create(FakeStoreApiService::class.java)
    }
}

// ══════════════════════════════════════════
// 4. VIEWMODEL & ÉTATS RÉSEAU ROBUSTES
// ══════════════════════════════════════════
sealed interface ApiUiState {
    object Chargement : ApiUiState
    data class Succes(val catalogue: List<ProduitApiDto>) : ApiUiState
    data class Erreur(val message: String) : ApiUiState
}

class ApiProduitsViewModel(
    private val api: FakeStoreApiService = RetrofitClient.apiService
) : ViewModel() {

    private val _uiState = MutableStateFlow<ApiUiState>(ApiUiState.Chargement)
    val uiState: StateFlow<ApiUiState> = _uiState.asStateFlow()

    init {
        chargerCatalogue()
    }

    fun chargerCatalogue() {
        viewModelScope.launch {
            _uiState.value = ApiUiState.Chargement
            try {
                // Appel réseau asynchrone non-bloquant
                val reponse = api.fetchProduits()
                _uiState.value = ApiUiState.Succes(reponse)
            } catch (e: IOException) {
                _uiState.value = ApiUiState.Erreur("Pas de connexion Internet. Vérifiez vos données mobiles.")
            } catch (e: Exception) {
                _uiState.value = ApiUiState.Erreur("Erreur serveur : \${e.localizedMessage}")
            }
        }
    }
}

// ══════════════════════════════════════════
// 5. VUE COMPOSE
// ══════════════════════════════════════════
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EcranCatalogueApi(viewModel: ApiProduitsViewModel = remember { ApiProduitsViewModel() }) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Boutique en ligne (API REST)", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentAlignment = Alignment.Center
        ) {
            when (val currentState = state) {
                is ApiUiState.Chargement -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator(color = Color(0xFF7F52FF))
                        Spacer(modifier = Modifier.height(14.dp))
                        Text("Interrogation du serveur REST...", color = Color.Gray)
                    }
                }
                is ApiUiState.Erreur -> {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier.padding(24.dp)
                    ) {
                        Text(text = "⚠️ \${currentState.message}", color = MaterialTheme.colorScheme.error)
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = { viewModel.chargerCatalogue() }) {
                            Text("Réessayer la connexion")
                        }
                    }
                }
                is ApiUiState.Succes -> {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        items(currentState.catalogue, key = { it.id }) { produit ->
                            Card(modifier = Modifier.fillMaxWidth()) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Text(produit.title, fontWeight = FontWeight.Bold, maxLines = 2)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(
                                        text = "\${produit.price} $",
                                        color = Color(0xFF1E8F72),
                                        fontWeight = FontWeight.ExtraBold,
                                        fontSize = 18.sp
                                    )
                                    Text(
                                        text = produit.category.uppercase(),
                                        style = MaterialTheme.typography.bodySmall,
                                        color = Color.Gray
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}""",
        "gradle": """// 1. AndroidManifest.xml (OBLIGATOIRE !)
// <uses-permission android:name="android.permission.INTERNET" />

// 2. build.gradle.kts (Module :app)
dependencies {
    val retrofitVersion = "2.11.0"
    val moshiVersion = "1.15.1"

    implementation("com.squareup.retrofit2:retrofit:$retrofitVersion")
    implementation("com.squareup.retrofit2:converter-moshi:$retrofitVersion")
    implementation("com.squareup.moshi:moshi-kotlin:$moshiVersion")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
}""",
        "resultat": """Smartphone Android
       │  Requête HTTP : GET https://api.monsite.com/products
       ▼
Serveur Web distant
       │  Réponse : 200 OK  [{"id":1, "title":"Laptop", "price":999.0}]
       ▼
Retrofit + Moshi
       │  Désérialisation automatique en List<ProduitApiDto>
       ▼
ViewModel ──▶ Émet ApiUiState.Succes ──▶ LazyColumn s'affiche !""",
        "params": [
            ["@GET / @POST / @PUT / @DELETE", "Verbes HTTP standard indiquant le type d'opération sur la ressource REST."],
            ["@Path(\"param\")", "Remplace un tronçon de l'URL par une valeur dynamique, ex: users/{id}."],
            ["@Query(\"param\")", "Ajoute un paramètre d'URL standard, ex: search?q=kotlin."],
            ["@Body", "Envoie un objet Kotlin sérialisé en JSON dans le corps de la requête HTTP."],
            ["@Json(name = \"champ_json\")", "Mappe un nom de clé JSON vers un nom de variable Kotlin différent."]
        ],
        "erreurs": [
            ["Crash : SecurityException: Permission denied (missing INTERNET permission)", "Tu as oublié d'ajouter la permission internet dans le fichier `app/src/main/AndroidManifest.xml`. Ajoute tout en haut : `<uses-permission android:name=\"android.permission.INTERNET\" />`."],
            ["Crash : java.net.UnknownServiceException: CLEARTEXT communication to ... not permitted by network security policy", "Depuis Android 9, les requêtes HTTP non chiffrées (`http://`) sont bloquées par défaut pour des raisons de sécurité. Utilise impérativement une adresse sécurisée `https://` !"],
            ["JsonDataException : Required value 'nom' missing at $[0]", "Le nom des champs dans votre data class ne correspond pas exactement aux clés du JSON renvoyé par le serveur. Utilise l'annotation `@Json(name = \"cle_exacte\")`."]
        ],
        "exercice": {
            "enonce": "Ajoute une méthode d'API @GET('products/category/{cat}') pour charger uniquement les articles d'une catégorie donnée (ex: 'jewelery').",
            "indice": "Déclare @GET('products/category/{categorie}') suspend fun getProduitsParCategorie(@Path('categorie') cat: String): List<ProduitApiDto>.",
            "solution": """@GET("products/category/{nomCategorie}")
suspend fun getProduitsParCategorie(
    @Path("nomCategorie") categorie: String
): List<ProduitApiDto>"""
        },
        "quiz": {
            "q": "Quelle permission indispensable doit impérativement figurer dans le fichier `AndroidManifest.xml` pour qu'une application puisse exécuter des requêtes Retrofit ?",
            "options": [
                "<uses-permission android:name=\"android.permission.INTERNET\" />",
                "<uses-permission android:name=\"android.permission.ACCESS_NETWORK_STATE\" />",
                "<uses-permission android:name=\"android.permission.FOREGROUND_SERVICE\" />",
                "Aucune permission n'est requise pour Retrofit"
            ],
            "correct": 0,
            "exp": "Sans la permission `android.permission.INTERNET` dans le manifeste Android, le système d'exploitation bloque immédiatement toute tentative d'ouverture de socket réseau et lève une `SecurityException` fatale."
        },
        "retenir": [
            "Retrofit décrit les routes HTTP via une interface Kotlin annotée.",
            "N'oublie JAMAIS la permission INTERNET dans AndroidManifest.xml.",
            "Utilise toujours `suspend fun` pour exécuter les requêtes en Coroutine.",
            "Gère toujours les 3 états : Chargement, Données reçues (Succès), et Erreur réseau."
        ],
        "prereq": ["mvvm", "viewmodel"],
        "suite": ["navigation"]
    },

    "navigation": {
        "id": "navigation",
        "title": "Navigation Multi-Écrans avec Navigation Compose",
        "niveau": 8,
        "level": "mid",
        "duration": "18 min",
        "quoi": "<b>Navigation Compose</b> est la bibliothèque officielle permettant de gérer les transitions entre différents écrans d'une application Jetpack Compose, d'ordonnancer l'historique de navigation (la pile arrière ou <b>BackStack</b>), et de passer des arguments typés d'un écran source à un écran de destination.",
        "pourquoi": "Dans l'ancien monde Android, chaque écran était une Activity ou un Fragment lourd avec un cycle de vie complexe. Avec Compose, une application moderne ne possède qu'une **seule Activity unique** (Single-Activity Architecture). Navigation Compose permet de basculer de façon ultra-légère entre des fonctions Composable comme s'il s'agissait de pages web, tout en gérant parfaitement le bouton retour physique du téléphone.",
        "quand": "Dès que l'application comporte au moins deux écrans différents : Accueil -> Détail du produit, Écran de Connexion -> Tableau de bord, Liste -> Paramètres.",
        "syntaxe": """// 1. Création du contrôleur
val navController = rememberNavController()

// 2. Définition du graphe de navigation
NavHost(navController = navController, startDestination = "accueil") {
    composable("accueil") {
        EcranAccueil(onVoirDetails = { id -> navController.navigate("details/$id") })
    }
    composable(
        route = "details/{articleId}",
        arguments = listOf(navArgument("articleId") { type = NavType.LongType })
    ) { backStackEntry ->
        val id = backStackEntry.arguments?.getLong("articleId") ?: 0L
        EcranDetails(articleId = id, onRetour = { navController.popBackStack() })
    }
}""",
        "exempleMin": """@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "page1") {
        composable("page1") {
            Button(onClick = { navController.navigate("page2") }) { Text("Aller page 2") }
        }
        composable("page2") {
            Button(onClick = { navController.popBackStack() }) { Text("Retour") }
        }
    }
}""",
        "explication": [
            ["rememberNavController()", "Instancie et conserve en mémoire le contrôleur central qui garde en mémoire la pile des écrans visités."],
            ["NavHost(..., startDestination = ...)", "Le conteneur qui remplace dynamiquement l'écran affiché en fonction de la route active."],
            ["composable(\"details/{id}\")", "Associe un Composable à une route textuelle paramétrée (similaire à une URL web)."],
            ["navController.navigate(\"...\")", "Pousse un nouvel écran sur le dessus de la pile."],
            ["navController.popBackStack()", "Dépile l'écran actuel et revient fidèlement à l'écran précédent."]
        ],
        "exempleReel": """package com.example.app.navigation

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument

// ══════════════════════════════════════════
// 1. ROUTES SÉCURISÉES (Pattern Sealing)
// ══════════════════════════════════════════
sealed class Ecran(val route: String) {
    object Catalogue : Ecran("catalogue")
    object Detail : Ecran("detail/{produitId}") {
        fun creerRoute(produitId: Int) = "detail/$produitId"
    }
}

data class ArticleDemo(val id: Int, val titre: String, val prix: Double, val description: String)

val CATALOGUE_FICTIF = listOf(
    ArticleDemo(101, "MacBook Pro M3", 1999.0, "Superbe écran Liquid Retina XDR et puce ultra puissante."),
    ArticleDemo(102, "Clavier Sans-Fil", 119.0, "Touches silencieuses et rétroéclairage intelligent."),
    ArticleDemo(103, "Moniteur 4K 32\"", 699.0, "Fidélité des couleurs exceptionnelle pour les designers.")
)

// ══════════════════════════════════════════
// 2. NAVHOST PRINCIPAL
// ══════════════════════════════════════════
@Composable
fun ApplicationNavigationComplete(
    navController: NavHostController = rememberNavController()
) {
    NavHost(
        navController = navController,
        startDestination = Ecran.Catalogue.route
    ) {
        // ÉCRAN 1 : Catalogue
        composable(route = Ecran.Catalogue.route) {
            EcranCatalogue(
                articles = CATALOGUE_FICTIF,
                onArticleSelectionne = { id ->
                    navController.navigate(Ecran.Detail.creerRoute(id))
                }
            )
        }

        // ÉCRAN 2 : Détails avec argument
        composable(
            route = Ecran.Detail.route,
            arguments = listOf(
                navArgument("produitId") {
                    type = NavType.IntType
                    nullable = false
                }
            )
        ) { backStackEntry ->
            val id = backStackEntry.arguments?.getInt("produitId") ?: 0
            val article = CATALOGUE_FICTIF.find { it.id == id }

            EcranDetailArticle(
                article = article,
                onBoutonRetour = { navController.popBackStack() }
            )
        }
    }
}

// ══════════════════════════════════════════
// 3. COMPOSABLES D'ÉCRANS
// ══════════════════════════════════════════
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EcranCatalogue(
    articles: List<ArticleDemo>,
    onArticleSelectionne: (Int) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Boutique Mobile", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(articles, key = { it.id }) { item ->
                Card(
                    modifier = Modifier.fillMaxWidth().clickable { onArticleSelectionne(item.id) }
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column {
                            Text(item.titre, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Text("\${item.prix} €", color = Color(0xFF1E8F72), fontWeight = FontWeight.SemiBold)
                        }
                        Icon(Icons.Default.ChevronRight, contentDescription = "Voir", tint = Color.Gray)
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EcranDetailArticle(
    article: ArticleDemo?,
    onBoutonRetour: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(article?.titre ?: "Détail du produit") },
                navigationIcon = {
                    IconButton(onClick = onBoutonRetour) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Retour")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.secondaryContainer)
            )
        }
    ) { padding ->
        if (article == null) {
            Box(modifier = Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("Produit introuvable")
            }
        } else {
            Column(
                modifier = Modifier.fillMaxSize().padding(padding).padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text(article.titre, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold)
                Text(
                    text = "\${article.prix} €",
                    fontSize = 22.sp,
                    color = Color(0xFF1E8F72),
                    fontWeight = FontWeight.Bold
                )
                Divider()
                Text("Description :", fontWeight = FontWeight.SemiBold)
                Text(article.description, style = MaterialTheme.typography.bodyLarge, color = Color.DarkGray)

                Spacer(modifier = Modifier.weight(1f))

                Button(
                    onClick = { /* Ajouter */ },
                    modifier = Modifier.fillMaxWidth().height(50.dp)
                ) {
                    Text("Acheter maintenant")
                }
            }
        }
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    val navVersion = "2.7.7"
    implementation("androidx.navigation:navigation-compose:$navVersion")
}""",
        "resultat": """Écran 1 : Catalogue
┌──────────────────────────────────────┐
│ Boutique Mobile                      │
├──────────────────────────────────────┤
│ MacBook Pro M3            1999 €  [›]│ ──clic──▶ navController.navigate("detail/101")
│ Clavier Sans-Fil           119 €  [›]│
└──────────────────────────────────────┘
                   │
                   ▼
Écran 2 : Détails (Reçoit l'argument id=101)
┌──────────────────────────────────────┐
│ [←] MacBook Pro M3                   │
├──────────────────────────────────────┤
│ 1999.0 €                             │
│ Superbe écran Liquid Retina XDR...   │
│                                      │
│ [ Acheter maintenant               ] │
└──────────────────────────────────────┘
    ▲ Clic flèche retour : navController.popBackStack()
    │ (Revient au Catalogue exactement à la même position de scroll !)""",
        "params": [
            ["rememberNavController()", "Instance mémorisant l'historique et orchestrant les transitions d'écrans."],
            ["NavHost", "Conteneur hôte reliant le contrôleur aux différentes routes de l'application."],
            ["composable(route, arguments)", "Enregistre une destination avec sa route textuelle et la liste de ses paramètres."],
            ["navController.navigate(\"...\")", "Navigue vers une destination en l'empilant sur la pile arrière."],
            ["navController.popBackStack()", "Revient en arrière en dépilant l'écran actif (identique au bouton retour système)."],
            ["popUpTo(\"...\") { inclusive = true }", "Nettoie la pile de navigation (essentiel après un écran de Login pour empêcher le retour en arrière)."]
        ],
        "erreurs": [
            ["Crash : IllegalArgumentException: Navigation destination that matches request ... cannot be found", "La chaîne de caractères passée à `navController.navigate(...)` ne correspond à aucun `composable(...)` déclaré dans le NavHost. Vérifie scrupuleusement l'orthographe ou utilise des classes scellées (Sealed Class) pour sécuriser tes routes."],
            ["Passer un objet complexe complet dans les arguments de route", "Il ne faut JAMAIS passer des objets entiers (ex: une instance de classe User ou Produit avec 20 champs) dans une URL de route. Passe toujours uniquement l'identifiant unique (`id: Int` ou `id: String`), et laisse le ViewModel de l'écran de destination charger l'objet correspondant depuis le Repository."]
        ],
        "exercice": {
            "enonce": "Ajoute une troisième route 'parametres' sans argument et un bouton d'icône d'engrenage dans la TopBar du catalogue pour y naviguer.",
            "indice": "Ajoute composable('parametres') { EcranParametres() } dans NavHost, puis navController.navigate('parametres').",
            "solution": """// Dans le NavHost :
composable("parametres") {
    EcranParametres(onRetour = { navController.popBackStack() })
}

// Dans la TopAppBar du Catalogue :
actions = {
    IconButton(onClick = { navController.navigate("parametres") }) {
        Icon(Icons.Default.Settings, contentDescription = "Paramètres")
    }
}"""
        },
        "quiz": {
            "q": "Quelle est la bonne pratique recommandée par Google pour transmettre des informations entre deux écrans avec Navigation Compose ?",
            "options": [
                "Transmettre uniquement un identifiant simple (ex: id: Int) dans l'URL de route et charger l'objet dans le ViewModel de destination",
                "Sérialiser un objet lourd de plusieurs méga-octets en Base64 dans la route",
                "Utiliser une variable globale statique 'var articleSelectionne: Article?'",
                "Dupliquer la base de données dans chaque écran"
            ],
            "correct": 0,
            "exp": "Passer des objets entiers par URL enfreint le principe de source unique de vérité et risque de dépasser la limite de taille des bundles Android. La bonne pratique universelle consiste à passer l'identifiant (ID) dans la route, et le ViewModel de l'écran cible récupère la donnée fraîche depuis le Repository."
        },
        "retenir": [
            "Une seule Activity : Navigation Compose remplace entièrement les Fragments.",
            "NavController orchestre l'historique et NavHost affiche l'écran courant.",
            "Ne passe que des identifiants (IDs) simples dans les arguments de route.",
            "Sécurise tes routes avec une Sealed Class (`Ecran.Home`, `Ecran.Detail`)."
        ],
        "prereq": ["scaffold", "viewmodel"],
        "suite": ["crud"]
    }
}

print("Partie 3 chargée avec succès (4 leçons).")
