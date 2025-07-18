# Contrats API - Plateforme Ebook Étudiant

## Données Mock à Remplacer

### Frontend Mock Data (`/app/frontend/src/data/mock.js`)
- **mockEbook** : Contenu complet de l'ebook avec chapitres, descriptions, contenu détaillé
- **Témoignages** : Avis d'étudiants sur la page d'accueil
- **Statistiques** : Nombre d'étudiants aidés, taux de réussite, etc.

## APIs à Implémenter

### 1. API Génération PDF
**POST /api/generate-pdf**
- **Description** : Génère un PDF complet de l'ebook
- **Input** : Aucun (utilise le contenu stocké)
- **Output** : 
  ```json
  {
    "success": true,
    "download_url": "/api/download-pdf/{token}",
    "filename": "comment-faire-1000-euros-en-1-mois.pdf"
  }
  ```

### 2. API Téléchargement PDF
**GET /api/download-pdf/{token}**
- **Description** : Télécharge le PDF généré
- **Input** : Token de téléchargement
- **Output** : Fichier PDF en binary

### 3. API Contenu Ebook
**GET /api/ebook/content**
- **Description** : Récupère le contenu complet de l'ebook
- **Output** : Structure identique à mockEbook

### 4. API Statistiques
**GET /api/stats**
- **Description** : Récupère les statistiques de la plateforme
- **Output** :
  ```json
  {
    "students_helped": 15000,
    "success_rate": 85,
    "avg_time_to_results": 30
  }
  ```

### 5. API Témoignages
**GET /api/testimonials**
- **Description** : Récupère les témoignages d'étudiants
- **Output** :
  ```json
  [
    {
      "name": "Marie L.",
      "role": "Étudiante en Commerce",
      "content": "J'ai réussi à gagner 1200€...",
      "rating": 5
    }
  ]
  ```

### 6. API Tracking des Téléchargements
**POST /api/track-download**
- **Description** : Enregistre les téléchargements pour les statistiques
- **Input** :
  ```json
  {
    "user_info": {
      "user_agent": "string",
      "ip": "string",
      "timestamp": "datetime"
    }
  }
  ```

## Modèles de Données

### EbookContent
```python
class EbookContent(BaseModel):
    title: str
    subtitle: str
    author: str
    pages: int
    chapters: List[Chapter]

class Chapter(BaseModel):
    title: str
    description: str
    content: List[Section]

class Section(BaseModel):
    subtitle: str
    text: List[str]
    tips: Optional[str] = None
```

### DownloadTracking
```python
class DownloadTracking(BaseModel):
    id: str
    timestamp: datetime
    user_agent: str
    ip_address: str
    filename: str
```

### Statistics
```python
class Statistics(BaseModel):
    students_helped: int
    success_rate: int
    avg_time_to_results: int
    total_downloads: int
```

## Intégration Frontend-Backend

### Remplacement des Mocks
1. **Home.js** : Remplacer les données hardcodées par des appels API
2. **Preview.js** : Récupérer le contenu via API au lieu de mock.js
3. **Téléchargement PDF** : Remplacer l'alerte mock par un vrai téléchargement

### Appels API à Implémenter
1. `useEffect` pour charger le contenu de l'ebook
2. `useEffect` pour charger les statistiques
3. `useEffect` pour charger les témoignages
4. Fonction `handleDownload` pour générer et télécharger le PDF

## Fonctionnalités Techniques

### Génération PDF
- Utiliser `reportlab` ou `weasyprint` pour générer des PDFs de qualité
- Mise en page professionnelle avec table des matières
- Formatage du texte avec styles et hiérarchie
- Ajout de métadonnées (titre, auteur, etc.)

### Système de Tokens
- Génération de tokens temporaires pour les téléchargements
- Expiration des tokens après 24h
- Sécurisation des téléchargements

### Base de Données
- Collection `ebook_content` : Contenu de l'ebook
- Collection `download_tracking` : Suivi des téléchargements
- Collection `statistics` : Statistiques de la plateforme
- Collection `testimonials` : Témoignages clients

## Sécurité et Performance

### Limitations
- Rate limiting sur la génération PDF (max 5 par IP/heure)
- Validation des inputs
- Sanitization du contenu

### Cache
- Cache Redis pour les PDFs générés
- Cache des statistiques (refresh toutes les heures)
- Cache du contenu de l'ebook

## Déploiement

### Variables d'Environnement
- `PDF_STORAGE_PATH` : Chemin de stockage des PDFs
- `PDF_EXPIRY_HOURS` : Durée de vie des PDFs (défaut: 24h)
- `MAX_PDF_GENERATION_PER_HOUR` : Limite de génération par heure

### Fichiers Statiques
- Dossier `/static/pdfs/` pour le stockage temporaire
- Nettoyage automatique des fichiers expirés