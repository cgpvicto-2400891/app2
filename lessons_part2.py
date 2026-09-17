# -*- coding: utf-8 -*-
"""
Leçons Partie 2 : État, Architecture & Données Légères
5. state (remember, mutableStateOf, rememberSaveable, State Hoisting)
6. viewmodel (ViewModel, StateFlow, Coroutines viewModelScope)
7. mvvm (Architecture MVVM, UiState scellé, Repository, UDF)
8. datastore (DataStore Preferences, Flow, persistance sur disque)
"""

LESSONS_PART2 = {
    "state": {
        "id": "state",
        "title": "Gestion de l'État & Recomposition (State)",
        "niveau": 4,
        "level": "mid",
        "duration": "15 min",
        "quoi": "En Jetpack Compose, l'<b>état</b> (State) est une valeur observable qui décrit ce qui doit être affiché à l'écran à un instant T. Dès que cette valeur change, Compose déclenche automatiquement une <b>recomposition</b> : il ré-exécute les fonctions Composable concernées pour rafraîchir l'affichage instantanément.",
        "pourquoi": "Si tu déclares une simple variable Kotlin (`var compteur = 0`), Compose n'a aucun moyen d'être averti quand elle change, et lors de chaque redessin d'écran, la variable serait réinitialisée à 0 ! `remember` permet de conserver la valeur en mémoire, et `mutableStateOf` en fait un conteneur réactif qui avertit l'écran.",
        "quand": "Dès qu'une interaction utilisateur modifie un élément : champ texte qui se remplit, case cochée, compteur d'articles, visibilité d'une fenêtre de dialogue ou panier d'achat.",
        "syntaxe": """// 1. Déclaration avec délégation 'by' (recommandée)
var nom by remember { mutableStateOf("") }

// 2. Survie aux rotations d'écran (changement d'orientation)
var compteur by rememberSaveable { mutableStateOf(0) }

// 3. State Hoisting (remontée d'état vers le parent)
@Composable
fun MonChamp(valeur: String, onValeurChange: (String) -> Unit)""",
        "exempleMin": """@Composable
fun CompteurSimple() {
    var count by remember { mutableStateOf(0) }

    Button(onClick = { count++ }) {
        Text("Cliqué $count fois")
    }
}""",
        "explication": [
            ["remember { ... }", "Indique à Compose de mémoriser cette valeur entre les recompositions successives (évite qu'elle retombe à 0)."],
            ["mutableStateOf(0)", "Crée un objet réactif encapsulant la valeur 0 et écouté par Compose."],
            ["by", "Opérateur de délégation Kotlin. Il permet de manipuler `count` comme un simple Int sans devoir écrire `count.value`."],
            ["onClick = { count++ }", "Incrémente l'état. Compose détecte la mutation et recompose immédiatement le Text."]
        ],
        "exempleReel": """package com.example.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * Exemple de A à Z : Composant interactif de gestion de stock
 * avec rememberSaveable (survie à la rotation), calcul de montant
 * et application du pattern "State Hoisting" (remontée d'état).
 */
@Composable
fun GestionnaireArticleComplet() {
    // État conservé même lors d'une rotation d'écran grâce à rememberSaveable
    var quantite by rememberSaveable { mutableStateOf(1) }
    val prixUnitaire = 24.90

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "T-shirt Kotlin Developer",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = "Prix unitaire : $prixUnitaire €",
                color = Color.Gray,
                fontSize = 14.sp
            )

            Spacer(modifier = Modifier.height(20.dp))

            // Composant réutilisable sans état propre (Stateless)
            SelecteurQuantite(
                quantite = quantite,
                surAugmenter = { quantite++ },
                surDiminuer = { if (quantite > 1) quantite-- },
                surReinitialiser = { quantite = 1 }
            )

            Spacer(modifier = Modifier.height(20.dp))
            Divider()
            Spacer(modifier = Modifier.height(16.dp))

            // Calcul réactif instantané
            val total = quantite * prixUnitaire
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Total commande :", fontSize = 16.sp, fontWeight = FontWeight.Medium)
                Text(
                    text = String.format("%.2f €", total),
                    fontSize = 22.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color(0xFF1E8F72)
                )
            }
        }
    }
}

/**
 * State Hoisting : Ce composant ne contient aucun état ('remember').
 * Il reçoit sa valeur et émet des événements (Unidirectional Data Flow).
 * Il est 100% testable et réutilisable dans n'importe quel écran.
 */
@Composable
fun SelecteurQuantite(
    quantite: Int,
    surAugmenter: () -> Unit,
    surDiminuer: () -> Unit,
    surReinitialiser: () -> Unit
) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Bouton Moins
        FilledIconButton(
            onClick = surDiminuer,
            enabled = quantite > 1,
            colors = IconButtonDefaults.filledIconButtonColors(containerColor = MaterialTheme.colorScheme.primary)
        ) {
            Icon(Icons.Default.Remove, contentDescription = "Diminuer")
        }

        // Valeur courante
        Text(
            text = "$quantite",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.widthIn(min = 40.dp)
        )

        // Bouton Plus
        FilledIconButton(
            onClick = surAugmenter,
            colors = IconButtonDefaults.filledIconButtonColors(containerColor = MaterialTheme.colorScheme.primary)
        ) {
            Icon(Icons.Default.Add, contentDescription = "Augmenter")
        }

        // Bouton Reset
        IconButton(onClick = surReinitialiser) {
            Icon(Icons.Default.Refresh, contentDescription = "Réinitialiser", tint = Color.Gray)
        }
    }
}

@Preview(showBackground = true)
@Composable
fun GestionnairePreview() {
    MaterialTheme {
        GestionnaireArticleComplet()
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.04.01"))
    implementation("androidx.compose.runtime:runtime")
    implementation("androidx.compose.runtime:runtime-saveable")
    implementation("androidx.compose.material3:material3")
}""",
        "resultat": """T-shirt Kotlin Developer
Prix unitaire : 24.90 €

  [ - ]    3    [ + ]    [ ↺ ]

───────────────────────────────
Total commande :       74.70 €""",
        "params": [
            ["remember { mutableStateOf(x) }", "Garde la valeur en mémoire vive durant la recomposition. Réinitialisé en cas de rotation d'écran."],
            ["rememberSaveable { mutableStateOf(x) }", "Conserve la valeur dans le Bundle de l'Activity : survit aux rotations et à la mise en arrière-plan."],
            ["by (import runtime.getValue/setValue)", "Délégation permettant d'accéder directement au type sous-jacent (Int, String) sans `.value`."],
            ["State Hoisting (Remontée d'état)", "Bonne pratique consistant à transformer un composant avec état (Stateful) en composant pur (Stateless) recevant `value` et `onValueChange`."]
        ],
        "erreurs": [
            ["Le compteur se réinitialise à chaque rotation d'écran", "Tu as utilisé `remember` au lieu de `rememberSaveable`. Seul `rememberSaveable` survit aux changements de configuration (rotation, passage en mode sombre)."],
            ["Unresolved reference: getValue / setValue", "Les imports d'extension Kotlin manquent dans ton fichier. Ajoute impérativement : `import androidx.compose.runtime.getValue` et `import androidx.compose.runtime.setValue`."],
            ["Modifier l'état directement dans le corps du Composable sans lambda", "Écrire `compteur++` directement dans le corps d'une fonction Composable provoque une boucle infinie de recompositions et fait geler l'application. Les mutations d'état doivent TOUJOURS se faire dans des callbacks (onClick, onValueChange...)."]
        ],
        "exercice": {
            "enonce": "Crée un composant d'interrupteur avec remember : un Switch accompagné d'un texte dynamique qui affiche 'Lumière allumée' (en vert) ou 'Lumière éteinte' (en gris) selon sa valeur.",
            "indice": "Déclare `var estAllume by remember { mutableStateOf(false) }`, puis Row avec Switch(checked = estAllume, onCheckedChange = { estAllume = it }) et Text.",
            "solution": """@Composable
fun InterrupteurLumiere() {
    var estAllume by remember { mutableStateOf(false) }

    Row(
        modifier = Modifier.padding(16.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Switch(
            checked = estAllume,
            onCheckedChange = { estAllume = it }
        )
        Text(
            text = if (estAllume) "💡 Lumière allumée" else "🌙 Lumière éteinte",
            fontWeight = FontWeight.Bold,
            color = if (estAllume) Color(0xFF1E8F72) else Color.Gray,
            fontSize = 16.sp
        )
    }
}"""
        },
        "quiz": {
            "q": "Quelle est la différence fondamentale entre `remember` et `rememberSaveable` ?",
            "options": [
                "remember ne survit pas à la rotation de l'écran du téléphone, alors que rememberSaveable sauvegarde la valeur dans le Bundle de l'Activity",
                "remember est asynchrone, rememberSaveable est synchrone",
                "rememberSaveable est réservé aux types String uniquement",
                "remember est déprécié depuis Compose 1.5"
            ],
            "correct": 0,
            "exp": "`remember` conserve l'état uniquement tant que le Composable reste dans l'arbre de composition. Lorsqu'une rotation d'écran survient, l'Activity Android est détruite puis recréée : `remember` est alors réinitialisé, tandis que `rememberSaveable` persiste la valeur grâce au Bundle de sauvegarde d'état."
        },
        "retenir": [
            "Un changement d'état (State) déclenche automatiquement une recomposition de l'interface.",
            "Utilise `by remember { mutableStateOf(...) }` pour l'état local d'un Composable.",
            "Utilise `rememberSaveable` pour que l'état survive aux rotations de smartphone.",
            "Applique le State Hoisting pour rendre tes composants réutilisables et testables unitairement."
        ],
        "prereq": ["layout"],
        "suite": ["viewmodel", "mvvm"]
    },

    "viewmodel": {
        "id": "viewmodel",
        "title": "Architecture de l'État avec ViewModel & StateFlow",
        "niveau": 4,
        "level": "mid",
        "duration": "16 min",
        "quoi": "Un <b>ViewModel</b> est une classe Android dédiée à la détention et la gestion de la logique d'un écran. Il hérite de `androidx.lifecycle.ViewModel`. Sa caractéristique majeure est qu'il **survit au cycle de vie de l'écran** : quand l'utilisateur tourne son téléphone et que l'Activity est détruite et recréée, l'instance du ViewModel reste intacte en mémoire avec toutes ses données.",
        "pourquoi": "Si tu mets toute ta logique métier (appels réseau, calculs de formulaires, chronomètres) directement dans les fonctions Composable avec `remember`, le code devient illisible, impossible à tester unitairement et s'efface lors d'événements complexes. Le ViewModel sépare clairement « ce qui décide » de « ce qui affiche ».",
        "quand": "Dès qu'un écran dépasse le stade d'un simple widget visuel : formulaires d'inscription, chargement de listes depuis une base de données ou une API, gestion d'un panier.",
        "syntaxe": """// 1. Définition du ViewModel
class MonViewModel : ViewModel() {
    // Encapsulation : MutableStateFlow privé, StateFlow public en lecture seule
    private val _uiState = MutableStateFlow(ValeurInitiale)
    val uiState: StateFlow<TypeState> = _uiState.asStateFlow()

    fun declencherAction() {
        viewModelScope.launch {
            // Travail en coroutine asynchrone sécurisée
        }
    }
}

// 2. Consommation dans Compose
@Composable
fun MonEcran(viewModel: MonViewModel = viewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
}""",
        "exempleMin": """class CompteurViewModel : ViewModel() {
    var count by mutableStateOf(0)
        private set

    fun incrementer() { count++ }
}

@Composable
fun VueCompteur(vm: CompteurViewModel = viewModel()) {
    Button(onClick = { vm.incrementer() }) {
        Text("Total : \${vm.count}")
    }
}""",
        "explication": [
            ["class CompteurViewModel : ViewModel()", "Hérite de la classe officielle AndroidX. Android associe son cycle de vie à l'écran."],
            ["var count ... private set", "Expose la variable en lecture publique, mais interdit sa modification directe depuis l'UI."],
            ["fun incrementer()", "Seule porte d'entrée autorisée pour modifier la donnée (centralisation de la logique métier)."],
            ["viewModel: CompteurViewModel = viewModel()", "Fonction Compose qui injecte ou récupère l'instance unique existante du ViewModel liée à l'écran."]
        ],
        "exempleReel": """package com.example.app.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

// 1. Modèle d'état d'écran immuable (State Pattern)
data class FormulaireUiState(
    val email: String = "",
    val motDePasse: String = "",
    val estValide: Boolean = false,
    val estEnCours: Boolean = false,
    val messageConfirmation: String? = null
)

// 2. ViewModel gérant toute la logique métier
class AuthentificationViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(FormulaireUiState())
    val uiState: StateFlow<FormulaireUiState> = _uiState.asStateFlow()

    fun onEmailChange(nouveau: String) {
        val valide = nouveau.contains("@") && _uiState.value.motDePasse.length >= 6
        _uiState.value = _uiState.value.copy(email = nouveau, estValide = valide)
    }

    fun onMotDePasseChange(nouveau: String) {
        val valide = _uiState.value.email.contains("@") && nouveau.length >= 6
        _uiState.value = _uiState.value.copy(motDePasse = nouveau, estValide = valide)
    }

    fun soumettre() {
        if (!_uiState.value.estValide) return

        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(estEnCours = true, messageConfirmation = null)
            // Simulation d'une requête réseau sécurisée
            delay(1500)
            _uiState.value = _uiState.value.copy(
                estEnCours = false,
                messageConfirmation = "Bienvenue, \${_uiState.value.email} ! Connexion réussie."
            )
        }
    }
}

// 3. UI pure (Compose) qui observe l'état et relaie les clics
@Composable
fun EcranConnexion(
    viewModel: AuthentificationViewModel = viewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Connexion Sécurisée",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )

        Spacer(modifier = Modifier.height(24.dp))

        // Champ Email
        OutlinedTextField(
            value = state.email,
            onValueChange = { viewModel.onEmailChange(it) },
            label = { Text("Adresse Email") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(12.dp))

        // Champ Mot de passe
        OutlinedTextField(
            value = state.motDePasse,
            onValueChange = { viewModel.onMotDePasseChange(it) },
            label = { Text("Mot de passe (min 6 car.)") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(20.dp))

        // Bouton avec indicateur de chargement
        Button(
            onClick = { viewModel.soumettre() },
            enabled = state.estValide && !state.estEnCours,
            modifier = Modifier.fillMaxWidth().height(50.dp)
        ) {
            if (state.estEnCours) {
                CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
            } else {
                Text("Se connecter")
            }
        }

        // Message de retour
        state.messageConfirmation?.let { message ->
            Spacer(modifier = Modifier.height(20.dp))
            Surface(
                color = Color(0xFFE3F5EF),
                shape = MaterialTheme.shapes.medium
            ) {
                Text(
                    text = message,
                    color = Color(0xFF1E8F72),
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.padding(12.dp)
                )
            }
        }
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.0")
}""",
        "resultat": """Écran Compose
   │  (Saisie utilisateur / Clic)
   ↓  appelle viewModel.onEmailChange(...)
ViewModel (Survit aux rotations !)
   │  Met à jour _uiState.value
   ↓  émet via StateFlow
UI Compose se recompose automatiquement ✓""",
        "params": [
            ["viewModelScope", "Portée de Coroutine liée au cycle de vie du ViewModel. S'annule automatiquement quand l'écran est définitivement fermé."],
            ["MutableStateFlow / StateFlow", "Conteneur de données réactif moderne recommandé par Google pour exposer l'état vers Compose."],
            ["collectAsStateWithLifecycle()", "Collecte le Flow de manière sûre : arrête la collecte quand l'app passe en arrière-plan pour économiser la batterie."],
            ["asStateFlow()", "Convertit un MutableStateFlow privé en StateFlow public en lecture seule (encapsulation)."]
        ],
        "erreurs": [
            ["Passer un Context d'Activity ou une vue Compose dans le ViewModel", "C'est la pire fuite de mémoire (Memory Leak) possible sous Android ! Le ViewModel vivant plus longtemps que l'Activity, conserver une référence vers l'Activity empêche le ramasse-miettes (GC) de libérer l'écran lors d'une rotation."],
            ["Modifier l'état public directement depuis l'UI", "L'état exposé doit TOUJOURS être immuable (`StateFlow` ou `private set`). Seules des fonctions explicites du ViewModel doivent modifier les valeurs."]
        ],
        "exercice": {
            "enonce": "Crée un ChronoViewModel avec une variable 'secondes' (Int) et une fonction demarrer() qui incrémente les secondes chaque seconde dans une coroutine viewModelScope.",
            "indice": "Dans demarrer(), lance viewModelScope.launch { while(true) { delay(1000); _secondes.value++ } }",
            "solution": """class ChronoViewModel : ViewModel() {
    private val _secondes = MutableStateFlow(0)
    val secondes: StateFlow<Int> = _secondes.asStateFlow()

    private var estEnCours = false

    fun demarrer() {
        if (estEnCours) return
        estEnCours = true
        viewModelScope.launch {
            while (estEnCours) {
                delay(1000)
                _secondes.value++
            }
        }
    }

    fun reinitialiser() {
        estEnCours = false
        _secondes.value = 0
    }
}"""
        },
        "quiz": {
            "q": "Que devient une instance de ViewModel lorsque l'utilisateur effectue une rotation de son smartphone ?",
            "options": [
                "L'instance reste vivante et est automatiquement rattachée au nouvel écran sans perte de données",
                "Elle est détruite et recréée comme l'Activity",
                "Elle génère une exception OutOfMemoryError",
                "Elle est sauvegardée dans le stockage local du téléphone"
            ],
            "correct": 0,
            "exp": "Le composant ViewModel d'AndroidX a été conçu spécifiquement pour survivre aux changements de configuration (comme la rotation portrait/paysage). L'Activity est détruite et reconstruite, mais le système Android conserve le ViewModel en mémoire et le reconnecte instantanément au nouvel écran."
        },
        "retenir": [
            "Le ViewModel héberge l'état et la logique métier de l'écran.",
            "Il survit à la rotation d'écran, contrairement à remember.",
            "Ne JAMAIS passer de référence vers une Activity ou un Context UI dans un ViewModel.",
            "Utilise StateFlow + collectAsStateWithLifecycle() pour une observation réactive sans fuite mémoire."
        ],
        "prereq": ["state"],
        "suite": ["mvvm", "room"]
    },

    "mvvm": {
        "id": "mvvm",
        "title": "L'Architecture MVVM & Unidirectional Data Flow",
        "niveau": 5,
        "level": "mid",
        "duration": "15 min",
        "quoi": "L'architecture <b>MVVM</b> (Model-View-ViewModel) est la norme recommandée par Google pour concevoir des applications Android professionnelles, évolutives et maintenables. Elle organise le code en trois couches indépendantes : la <b>View</b> (interface Jetpack Compose), le <b>ViewModel</b> (logique d'écran) et le <b>Model / Repository</b> (sources de données locales et distantes).",
        "pourquoi": "Sans architecture, on a tendance à mettre les appels API, le stockage en base et la logique de calcul au milieu de l'interface graphique Compose. Le code devient un plat de spaghettis illisible, impossible à tester et qui plante dès que le réseau ralentit. MVVM garantit le principe de responsabilité unique (SRP).",
        "quand": "Sur la totalité de vos projets d'applications Android. C'est l'architecture standard du cours et des entreprises.",
        "syntaxe": """// Flux Unidirectionnel des Données (UDF)
// [ UI ] ──(Events : clics)──▶ [ ViewModel ] ──(Requête)──▶ [ Repository ]
// [ UI ] ◀──(UiState : données)── [ ViewModel ] ◀──(Données)── [ Repository ]

// 1. Modèle d'état scellé (Sealed Interface)
sealed interface ProduitsUiState {
    object Chargement : ProduitsUiState
    data class Succes(val produits: List<Produit>) : ProduitsUiState
    data class Erreur(val message: String) : ProduitsUiState
}""",
        "exempleMin": """// UI observe le ViewModel, ViewModel appelle le Repository
class ProduitsViewModel(private val repository: ProduitRepository) : ViewModel() {
    val uiState = repository.getProduits().stateIn(
        viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList()
    )
}""",
        "explication": [
            ["sealed interface ProduitsUiState", "Permet de modéliser avec une sécurité absolue les 3 états possibles d'un écran : En cours de chargement, Succès avec données, ou Échec avec message."],
            ["Repository", "Point de vérité unique : décide en toute transparence s'il va chercher la donnée dans la base Room ou sur l'API web."],
            ["ViewModel", "Intermédiaire : reçoit les clics de la View, appelle le Repository et met à jour l'UiState."],
            ["View (Compose)", "Couche bête : ne contient aucune logique, ne fait que dessiner l'UiState via un `when (uiState)`."]
        ],
        "exempleReel": """package com.example.app.architecture

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
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

// ══════════════════════════════════════════
// COUCHE 1 : MODEL & REPOSITORY (Données)
// ══════════════════════════════════════════
data class Article(val id: Int, val titre: String, val categorie: String)

class ArticleRepository {
    suspend fun chargerArticles(): List<Article> {
        delay(1200) // Simulation d'une latence réseau
        return listOf(
            Article(1, "Introduction à Jetpack Compose", "Mobile"),
            Article(2, "Architecture MVVM & Clean Architecture", "Architecture"),
            Article(3, "Room et SQLite en Kotlin", "Persistance"),
            Article(4, "Consommer une API REST avec Retrofit", "Réseau")
        )
    }
}

// ══════════════════════════════════════════
// COUCHE 2 : VIEWMODEL & UISTATE (Logique)
// ══════════════════════════════════════════
sealed interface ArticlesUiState {
    object Chargement : ArticlesUiState
    data class Succes(val articles: List<Article>) : ArticlesUiState
    data class Erreur(val erreur: String) : ArticlesUiState
}

class ArticlesViewModel(
    private val repository: ArticleRepository = ArticleRepository()
) : ViewModel() {

    private val _uiState = MutableStateFlow<ArticlesUiState>(ArticlesUiState.Chargement)
    val uiState: StateFlow<ArticlesUiState> = _uiState.asStateFlow()

    init {
        rafraichir()
    }

    fun rafraichir() {
        viewModelScope.launch {
            _uiState.value = ArticlesUiState.Chargement
            try {
                val donnees = repository.chargerArticles()
                _uiState.value = ArticlesUiState.Succes(donnees)
            } catch (e: Exception) {
                _uiState.value = ArticlesUiState.Erreur("Impossible de charger les articles : \${e.localizedMessage}")
            }
        }
    }
}

// ══════════════════════════════════════════
// COUCHE 3 : VIEW COMPOSE (Affichage Pur)
// ══════════════════════════════════════════
@Composable
fun EcranArticlesMVVM(viewModel: ArticlesViewModel = ArticlesViewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            Surface(shadowElevation = 4.dp) {
                Text(
                    text = "Centre de Documentation",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(16.dp)
                )
            }
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentAlignment = Alignment.Center
        ) {
            when (val currentState = state) {
                is ArticlesUiState.Chargement -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator(color = Color(0xFF7F52FF))
                        Spacer(modifier = Modifier.height(12.dp))
                        Text("Chargement des articles...", color = Color.Gray)
                    }
                }
                is ArticlesUiState.Erreur -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(16.dp)) {
                        Text(text = "❌ \${currentState.erreur}", color = MaterialTheme.colorScheme.error)
                        Spacer(modifier = Modifier.height(12.dp))
                        Button(onClick = { viewModel.rafraichir() }) {
                            Text("Réessayer")
                        }
                    }
                }
                is ArticlesUiState.Succes -> {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(currentState.articles, key = { it.id }) { article ->
                            Card(modifier = Modifier.fillMaxWidth()) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Text(article.titre, fontWeight = FontWeight.SemiBold)
                                    Text(article.categorie, color = Color(0xFF7F52FF), style = MaterialTheme.typography.bodySmall)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.0")
}""",
        "resultat": """┌─────────────────────────────────────────────────────┐
│                      VIEW (Compose)                 │
│         Dessine l'UiState (Chargement / Succès)     │
└──────────────────────────┬──────────────────────────┘
                           │ envoie les clics (Events)
                           ▼
┌─────────────────────────────────────────────────────┐
│                    VIEWMODEL                        │
│          Garde l'UiState, lance les coroutines      │
└──────────────────────────┬──────────────────────────┘
                           │ demande les données
                           ▼
┌─────────────────────────────────────────────────────┐
│                    REPOSITORY                       │
│    Choisit entre l'API REST (Retrofit) et Room      │
└─────────────────────────────────────────────────────┘""",
        "params": [
            ["Unidirectional Data Flow (UDF)", "Règle absolue : Les données descendent (State down) du ViewModel vers l'UI, et les événements montent (Events up) de l'UI vers le ViewModel."],
            ["sealed interface UiState", "Empêche tout état incohérent (impossible d'avoir à la fois 'chargement en cours' et 'données affichées')."],
            ["Repository", "Point de vérité unique (Single Source of Truth) masquant la complexité des requêtes SQL et HTTP."],
            ["Separation of Concerns (SoC)", "Chaque classe ne possède qu'une responsabilité précise."]
        ],
        "erreurs": [
            ["L'UI appelle directement une requête Room ou Retrofit", "C'est une violation grave de l'architecture. La vue Compose ne doit JAMAIS savoir d'où proviennent les données. Elle doit uniquement s'adresser à son ViewModel."],
            ["Créer des variables multiples sans sealed interface (ex: var loading, var data, var error)", "Ce patron crée des bugs d'états incohérents (par exemple si loading=true ET error!=null en même temps). Utilise TOUJOURS une `sealed interface UiState` pour modéliser des états mutuellement exclusifs."]
        ],
        "exercice": {
            "enonce": "Dans l'architecture ci-dessus, ajoute un état 'Vide' (object Vide : ArticlesUiState) déclenché lorsque la liste renvoyée par le Repository ne contient aucun élément, et affiche un texte 'Aucun article disponible pour le moment'.",
            "indice": "Dans ArticlesViewModel : if (donnees.isEmpty()) ArticlesUiState.Vide else ArticlesUiState.Succes(donnees). Puis gère 'is ArticlesUiState.Vide' dans le when Compose.",
            "solution": """// Dans la sealed interface :
sealed interface ArticlesUiState {
    object Chargement : ArticlesUiState
    object Vide : ArticlesUiState
    data class Succes(val articles: List<Article>) : ArticlesUiState
    data class Erreur(val erreur: String) : ArticlesUiState
}

// Dans le when de la vue Compose :
is ArticlesUiState.Vide -> {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text("📭 Aucun article disponible pour le moment.", color = Color.Gray)
        Spacer(modifier = Modifier.height(12.dp))
        OutlinedButton(onClick = { viewModel.rafraichir() }) { Text("Actualiser") }
    }
}"""
        },
        "quiz": {
            "q": "Dans l'architecture MVVM préconisée par Google, quelle couche a la responsabilité d'arbitrer entre les données en cache local (Room) et le serveur distant (API Retrofit) ?",
            "options": [
                "Le Repository",
                "Le Composable de l'écran",
                "Le ViewModel",
                "L'Activity principale"
            ],
            "correct": 0,
            "exp": "Le Repository a pour rôle d'agir comme source unique de vérité. C'est lui qui sait s'il doit interroger la base locale SQLite ou l'API réseau, et synchroniser les deux. Le ViewModel se contente de demander les données au Repository sans se soucier de leur provenance."
        },
        "retenir": [
            "MVVM sépare en 3 couches : View (affichage Compose), ViewModel (logique d'écran), Repository (données).",
            "L'UDF (Unidirectional Data Flow) : l'état descend, les événements remontent.",
            "Utilise toujours une `sealed interface UiState` (Chargement, Succès, Erreur).",
            "L'UI n'a jamais accès direct à la base de données ou à Internet."
        ],
        "prereq": ["viewmodel", "state"],
        "suite": ["datastore", "room", "api"]
    },

    "datastore": {
        "id": "datastore",
        "title": "Sauvegarder des Préférences avec DataStore",
        "niveau": 6,
        "level": "mid",
        "duration": "15 min",
        "quoi": "<b>Jetpack DataStore</b> est la solution moderne de stockage de données légères développée par Google pour remplacer définitivement l'ancienne bibliothèque `SharedPreferences`. Construit nativement sur les **Coroutines Kotlin** et les **Flows**, DataStore garantit une écriture asynchrone non-bloquante et une cohérence transactionnelle absolue.",
        "pourquoi": "SharedPreferences présentait deux défauts majeurs : il bloquait le thread principal lors des sauvegardes (provoquant des gels d'écran ANR - Application Not Responding) et n'offrait aucun moyen propre d'écouter les modifications de manière réactive. DataStore résout ces problèmes en exposant un `Flow` réactif et une méthode d'écriture `edit { }` suspendue.",
        "quand": "Pour toutes les préférences utilisateur simples : activer le mode sombre, mémoriser la langue préférée, retenir l'identifiant de session ou savoir si l'utilisateur a déjà vu le tutoriel d'accueil.",
        "syntaxe": """// 1. Déclaration unique du délégué
val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "user_preferences")

// 2. Définition d'une clé typée
val CLE_MODE_SOMBRE = booleanPreferencesKey("mode_sombre")

// 3. Écriture suspendue (Coroutine)
suspend fun sauvegarder(valeur: Boolean) {
    context.dataStore.edit { preferences ->
        preferences[CLE_MODE_SOMBRE] = valeur
    }
}

// 4. Lecture réactive continue (Flow)
val modeSombreFlow: Flow<Boolean> = context.dataStore.data
    .map { preferences -> preferences[CLE_MODE_SOMBRE] ?: false }""",
        "exempleMin": """// Écriture
suspend fun sauverPseudo(context: Context, pseudo: String) {
    context.dataStore.edit { it[stringPreferencesKey("pseudo")] = pseudo }
}

// Lecture
fun lirePseudo(context: Context): Flow<String> =
    context.dataStore.data.map { it[stringPreferencesKey("pseudo")] ?: "Invité" }""",
        "explication": [
            ["preferencesDataStore(name = \"user_preferences\")", "Crée un fichier sur le stockage privé de l'appareil nommé 'user_preferences.preferences_pb'."],
            ["booleanPreferencesKey(\"mode_sombre\")", "Définit une clé typée assurant qu'on ne pourra y stocker qu'un Boolean (évite les erreurs de typage)."],
            ["context.dataStore.edit { ... }", "Fonction `suspend` exécutant l'écriture de manière atomique sur un thread d'arrière-plan."],
            ["context.dataStore.data.map { ... }", "Transforme le flux de préférences en flux d'une valeur précise, mis à jour en temps réel."]
        ],
        "exempleReel": """package com.example.app.preferences

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import java.io.IOException

// 1. Extension contextuelle singleton (obligatoirement au niveau supérieur du fichier)
val Context.parametresDataStore: DataStore<Preferences> by preferencesDataStore(name = "parametres_app")

// 2. Modèle de préférences
data class ParametresUtilisateur(
    val modeSombre: Boolean,
    val notificationsActives: Boolean,
    val nomUtilisateur: String
)

// 3. Repository encapsulant DataStore
class ParametresRepository(private val context: Context) {

    private object Cles {
        val MODE_SOMBRE = booleanPreferencesKey("cle_mode_sombre")
        val NOTIFS = booleanPreferencesKey("cle_notifs")
        val PSEUDO = stringPreferencesKey("cle_pseudo")
    }

    // Lecture réactive sécurisée
    val parametresFlow: Flow<ParametresUtilisateur> = context.parametresDataStore.data
        .catch { exception ->
            if (exception is IOException) emit(emptyPreferences()) else throw exception
        }
        .map { prefs ->
            ParametresUtilisateur(
                modeSombre = prefs[Cles.MODE_SOMBRE] ?: false,
                notificationsActives = prefs[Cles.NOTIFS] ?: true,
                nomUtilisateur = prefs[Cles.PSEUDO] ?: "Développeur"
            )
        }

    suspend fun definirModeSombre(actif: Boolean) {
        context.parametresDataStore.edit { it[Cles.MODE_SOMBRE] = actif }
    }

    suspend fun definirNotifications(actives: Boolean) {
        context.parametresDataStore.edit { it[Cles.NOTIFS] = actives }
    }

    suspend fun definirNom(nom: String) {
        context.parametresDataStore.edit { it[Cles.PSEUDO] = nom }
    }
}

// 4. ViewModel reliant Repository et UI
class ParametresViewModel(private val repository: ParametresRepository) : ViewModel() {

    val uiState: StateFlow<ParametresUtilisateur> = repository.parametresFlow
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = ParametresUtilisateur(false, true, "Chargement...")
        )

    fun changerModeSombre(actif: Boolean) = viewModelScope.launch { repository.definirModeSombre(actif) }
    fun changerNotifications(actives: Boolean) = viewModelScope.launch { repository.definirNotifications(actives) }
    fun changerNom(nom: String) = viewModelScope.launch { repository.definirNom(nom) }
}

// 5. Écran de configuration Compose
@Composable
fun EcranParametres(
    context: Context = LocalContext.current,
    viewModel: ParametresViewModel = remember { ParametresViewModel(ParametresRepository(context)) }
) {
    val params by viewModel.uiState.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Préférences de l'App", fontSize = 22.sp, fontWeight = FontWeight.Bold)

        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                // Option 1 : Mode Sombre
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("Mode Sombre", fontWeight = FontWeight.SemiBold)
                        Text("Activer le thème nuit", style = MaterialTheme.typography.bodySmall)
                    }
                    Switch(
                        checked = params.modeSombre,
                        onCheckedChange = { viewModel.changerModeSombre(it) }
                    )
                }

                Divider()

                // Option 2 : Notifications
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("Notifications", fontWeight = FontWeight.SemiBold)
                        Text("Recevoir les alertes de cours", style = MaterialTheme.typography.bodySmall)
                    }
                    Switch(
                        checked = params.notificationsActives,
                        onCheckedChange = { viewModel.changerNotifications(it) }
                    )
                }

                Divider()

                // Option 3 : Pseudo
                OutlinedTextField(
                    value = params.nomUtilisateur,
                    onValueChange = { viewModel.changerNom(it) },
                    label = { Text("Nom d'utilisateur") },
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }
    }
}""",
        "gradle": """// build.gradle.kts (Module :app)
dependencies {
    implementation("androidx.datastore:datastore-preferences:1.0.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")
}""",
        "resultat": """Écran Paramètres (Compose)
      ↓ (Clic utilisateur sur Switch)
ViewModel.changerModeSombre(true)
      ↓ (Lance coroutine viewModelScope)
ParametresRepository.definirModeSombre(true)
      ↓ (context.dataStore.edit { ... })
Fichier Disque 'parametres_app.preferences_pb' mis à jour !
      ↓ (Le Flow émet la nouvelle valeur)
UI recomposée instantanément : [ ☑ Mode Sombre ]
      ✓ Reste conservé après extinction et réouverture de l'app !""",
        "params": [
            ["preferencesDataStore(name = ...)", "Délégué créant une instance singleton du DataStore liée au Context de l'application."],
            ["booleanPreferencesKey / stringPreferencesKey / intPreferencesKey", "Clés typées évitant les erreurs de casting."],
            ["dataStore.edit { preferences -> ... }", "Méthode d'écriture atomique et asynchrone (suspend function)."],
            ["dataStore.data", "Flux (Flow<Preferences>) émettant les valeurs enregistrées à chaque changement."]
        ],
        "erreurs": [
            ["Crash : IllegalStateException: There are multiple DataStores active for the same file", "Cette erreur classique survient si tu appelles `preferencesDataStore(...)` à l'intérieur d'une classe ou d'une fonction ré-instanciée. Le délégué DOIT être déclaré en top-level (en dehors de toute classe) comme extension : `val Context.dataStore by preferencesDataStore(...)`."],
            ["La valeur n'est pas enregistrée sur le disque", "L'appel `dataStore.edit { }` est une fonction suspendue : si elle n'est pas lancée dans une Coroutine active (ex: `viewModelScope.launch { ... }`), l'opération est abandonnée."]
        ],
        "exercice": {
            "enonce": "Ajoute une clé `intPreferencesKey('compteur_lancements')` pour mémoriser et incrémenter le nombre de fois où l'utilisateur a ouvert l'application.",
            "indice": "Déclare la clé, puis crée `suspend fun incrementerLancements() { dataStore.edit { it[CLE_LANCEMENTS] = (it[CLE_LANCEMENTS] ?: 0) + 1 } }`.",
            "solution": """val CLE_LANCEMENTS = intPreferencesKey("compteur_lancements")

suspend fun incrementerLancements(context: Context) {
    context.parametresDataStore.edit { prefs ->
        val actuel = prefs[CLE_LANCEMENTS] ?: 0
        prefs[CLE_LANCEMENTS] = actuel + 1
    }
}

fun observerLancements(context: Context): Flow<Int> =
    context.parametresDataStore.data.map { it[CLE_LANCEMENTS] ?: 0 }"""
        },
        "quiz": {
            "q": "Pourquoi Jetpack DataStore est-il très supérieur à l'ancienne solution SharedPreferences ?",
            "options": [
                "Il s'exécute de manière asynchrone sans jamais bloquer le thread UI et expose un Flow réactif",
                "Il permet de remplacer complètement une base de données SQL comme Room",
                "Il est capable de stocker des fichiers vidéo de plusieurs giga-octets",
                "Il ne nécessite aucune permission Android"
            ],
            "correct": 0,
            "exp": "SharedPreferences effectuait ses lectures/écritures de façon synchrone en bloquant le thread graphique principal (ce qui provoquait des saccades et des plantages ANR). DataStore est entièrement asynchrone grâce aux coroutines Kotlin et transmet les mises à jour en direct via l'API Flow."
        },
        "retenir": [
            "DataStore remplace SharedPreferences pour les préférences clé-valeur.",
            "Déclare le délégué au niveau supérieur du fichier (`val Context.dataStore by...`).",
            "L'écriture se fait avec `dataStore.edit { }` dans une coroutine.",
            "La lecture s'effectue via un `Flow` réactif encapsulé dans un Repository."
        ],
        "prereq": ["mvvm", "viewmodel"],
        "suite": ["room", "crud"]
    }
}

print("Partie 2 chargée avec succès (4 leçons).")
