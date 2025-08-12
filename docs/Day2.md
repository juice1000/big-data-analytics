# Tag 2: ML algorithms + Unstructured data processing

---

# Recap:

- Was ist Big Data?
- Was ist ein Data Lake?
- Was ist eine Anekdote für Stream Processing?
- Wie skaliert man Big Data Architekturen?
- Warum ist Apache Spark schneller als MapReduce?
- Was ist der Unterschied zwischen Batch Processing und Stream Processing
- Was ist Databricks?
- Was sind die 5 V’s von Big Data?
- Wann lohnt es sich nicht mehr, SQL zu verwenden?

## Datenqualität und -bereinigung

**Lernziele**

- Datenqualitätsprobleme erkennen
- Techniken zur Bereinigung auswählen und anwenden
- Qualität messbar machen

### Übung - Fehlerhafter Datensatz

**Diskussionsfragen**

- Welche Fehler gibt es? Definiere Kategorien
- Welche Fehler sind in diesem Datensatz am kritischsten?
- Kann man immer alle Ausreißerzeilen löschen?
- Kann man immer alle Zeilen mit undefinierten Werten löschen?
- Kann man immer alle fehlerhafte Zeilen löschen?

| supplier_id | supplier_name | amount | currency | category        | transaction_date         |
| ----------- | ------------- | ------ | -------- | --------------- | ------------------------ |
| 1003        |               |        |          | OFFICE_SUPPLIES | 2023-11-21T19:36:23.867Z |
| 1003        | Alpha GmbH    |        | eur      | office supplies | 2023-11-21T19:36:23.867Z |
| 1004        |               | 796.3  | USD      | office supplies | 2025-01-24T19:36:23.867Z |
| 1001        | Alpha GmbH    |        | eur      |                 | 2023-02-09T19:36:23.867Z |
| 1001        | Gamma Ltd     | 145.66 | USD      |                 | 2023-09-22T19:36:23.867Z |
| 1003        | Alpha GmbH    |        | EUR      |                 | 2025-04-25T19:36:23.867Z |
| 1001        | Alpha GmbH    | 599.3  | USD      | OFFICE_SUPPLIES | 2024-11-03T19:36:23.867Z |
| 9999        |               |        | EUR      | OFFICE_SUPPLIES | 2024-04-07T19:36:23.867Z |
| 1002        | Delta S.A.    | 179.68 |          | OFFICE_SUPPLIES | 2023-10-03T19:36:23.867Z |
| 9999        | Beta AG       |        | EURO     | OFFICE_SUPPLIES | 2023-04-11T19:36:23.867Z |
| 9999        | Gamma Ltd     | 913    |          |                 | 2025-06-29T19:36:23.867Z |
| 1003        | Alpha GmbH    |        |          | office supplies | 2024-01-31T19:36:23.867Z |
| 1004        |               | 33.4   | EUR      |                 | 2024-03-11T19:36:23.867Z |
| 1002        | Delta S.A.    |        |          | OFFICE_SUPPLIES | 2024-10-25T19:36:23.867Z |
| 1001        | Delta S.A.    |        | USD      | Office Supplies | 2025-05-10T19:36:23.867Z |
| 1002        | Alpha GmbH    | 772.12 | EUR      | office supplies | 2024-03-30T19:36:23.867Z |
| 1003        | Alpha GmbH    |        | eur      | office supplies | 2023-10-07T19:36:23.867Z |
| 1002        | Beta AG       |        | USD      | office supplies | 2024-12-25T19:36:23.867Z |
| 1001        | Gamma Ltd     |        | EURO     | office supplies | 2023-06-03T19:36:23.867Z |
| 1002        | Gamma Ltd     | 858.58 | EURO     | OFFICE_SUPPLIES | 2024-11-10T19:36:23.867Z |

---

### Typische Datenqualitätsprobleme (strukturierte Daten)

| Problem        | Beschreibung                                | Beispiel im Banking                                  |
| -------------- | ------------------------------------------- | ---------------------------------------------------- |
| Fehlende Werte | Datenfelder ohne Inhalt                     | Geburtsdatum eines Kunden fehlt                      |
| Outlier        | Extremwerte außerhalb normaler Range        | Überweisung von 1 Mio. € von Privatkonto             |
| Duplikate      | Gleicher Kunde mehrfach erfasst             | „Max Müller“ und „M. Mueller“ als getrennte Einträge |
| Inkonsistenz   | Unterschiedliche Formate oder Schreibweisen | „GER“, „Deutschland“, „DE“                           |

---

### **Qualitätsprobleme von Unstruktierten Daten**

Bsp.: “The quick brown fox jumps over the lazy dog”

- “T\he q\uick brow\n fox ju\mps over the\ laz\y do\g”
- “The 8uick brown fox jumps over the lazy dog”
- 茶色い素早い狐がのんびりした犬を飛び越える
- “NULL”
- [”The quick brown fox jumps over the lazy dog”, “The quick brown fox jumps over the lazy dog”]
- {}

---

- Falscher Dateityp
- Falscher/ defekter Dateiaufbau
- Informationen unsauber
  - Viel unbrauchbare Information
  - Daten korrupt
- Leere Dateien

### Datenbereinigungstechniken

- **Normalisierung:** Einheitliche Datums-, Währungs-, Namensformate
- **Fehlerkorrektur:** IBAN-Checks, Plausibilitätsprüfungen
- **Duplikaterkennung:** Eindeutige IDs, Fuzzy Matching
- **Imputation:** Fehlende Werte ersetzen (Mittelwert, Median, Modell)
- **Outlier-Handling:** Entfernen, Flaggen, getrennt analysieren

---

### Datenqualitätsmetriken

- **Vollständigkeit** – Anteil der gefüllten Felder
- **Genauigkeit** – Abgleich mit Referenzquellen
- **Konsistenz** – Einheitlichkeit über Systeme
- **Aktualität** – Alter der Daten im Analysekontext

---

### **Datenbereinigungsprozess**

**ASCII Diagramm (strukturierte Daten)**

```
[ Rohdaten ]
    ↓
[ Fehlende Werte? ] → Ersetzen / Entfernen
    ↓
[ Ausreißerprüfung ] → Validieren / Korrigieren
    ↓
[ Duplikate? ] → Zusammenführen / Löschen
    ↓
[ Saubere Daten ]

```

**Semi-strukturierte Daten**

```python
[ <JSON> Datei ]
    ↓
[ Datei verarbeitbar ] → Löschen / In Archiv zur Korrektur vorlegen / Code Cleaner
    ↓
[ Wichtige Keys prüfen ] → Logs schreiben / Weiterverarbeitung entscheiden
    ↓
[ Werte überprüfen (Nach ASCII Diagramm) ] → Korrigieren
    ↓
[ Daten strukturieren ]
    ↓
[ Saubere Daten ]
```

**Unstrukturierte Daten**

```python
[ <PDF> Datei ]
    ↓
[ Datei verarbeitbar ] → Löschen / In Archiv zur Korrektur vorlegen
    ↓
[ Daten extrahieren (OCR) ] → Ins Archiv zum Review vorlegen
    ↓
[ Validität prüfen (mit KI oder festen Metriken) ] → Ins Archiv zum Review vorlegen
    ↓
[ Daten strukturieren ]
    ↓
[ Saubere Daten ]
```

### Datenmodellierung

**Lernziele**

- Unterschied zwischen relationaler, dimensionaler und NoSQL-Modellierung verstehen
- Schema-Design für Big Data anwenden

---

### 1. Entity-Relationship-Modell (ERM) – Banking Beispiel

```
[Kunde] 1---N [Konto] 1---N [Transaktion]
[Kunde] 1---N [Produkt]

```

- Kunde kann mehrere Konten haben
- Konto hat viele Transaktionen
- Kunde nutzt mehrere Produkte

---

### 2. Dimensionale Modellierung (Data Warehousing)

- **Star Schema** – Faktentabelle in der Mitte, Dimensionstabellen außen

**Diagramm**

```
       [Dim_Kunde]
            |
[Dim_Zeit] - [Fakt_Transaktion] - [Dim_Produkt]
            |
       [Dim_Filiale]

```

- **Snowflake Schema** – Dimensionen weiter normalisiert

```python
              [Dim_Kunde]
                  |
           [Dim_Kundenregion]
                  |
              [Dim_Land]
                  |
[Dim_Zeit] - [Fakt_Transaktion] - [Dim_Produkt] - [Dim_Produktkategorie] - [Dim_Produkttyp]
                  |
              [Dim_Filiale] - [Dim_Filialregion] - [Dim_Land]
```

### 3. NoSQL-Datenmodellierung (mit Beispielen)

- **Key-Value:** Schneller Zugriff (Kundennummer → Kundendaten)
- **Document Model:** Vollständiges Kundenprofil als JSON
- **Wide Column Stores:** Zeitreihen (Kontostände pro Tag)

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/image.png)

---

### 4. Big Data Schema Design

- **Sharding:** Horizontale Aufteilung (Regionen, Kundengruppen)

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/image%201.png)

- **Replikation:** Mehrfachspeicherung für Ausfallsicherheit

---

**Diskussionsfragen**

- Wann ist Star Schema besser als Snowflake?
- Welche NoSQL-Struktur passt für Betrugserkennung in Echtzeit?

---

# Grundlagen Datenanalyse-Algorithmen

**Lernziele**

- Clustering verstehen
- K-means und hierarchisches Clustering kennen
- Business-Interpretation anwenden

---

## Clustering

- Ziel: Ähnliche Datenpunkte gruppieren ohne vorgegebene Labels
- **K-means Prozess**

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/image%202.png)

```
[Datensätze]
   ↓
[Wähle k Zentren]
   ↓
[Ordne Punkte dem nächsten Zentrum zu]
   ↓
[Neuberechnung Zentren]
   ↓
[Wiederholen bis stabil]

```

- **Hierarchisches Clustering:** Baumstruktur (Dendrogramm)

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/405c4096-add4-4478-be5d-cde5df4c7de8.png)

Mehr Clustering Methoden…

https://www.kdnuggets.com/unveiling-hidden-patterns-an-introduction-to-hierarchical-clustering

## Banking-Anwendung

- Frage: Welche Möglichkeiten bieten Clustering Methoden im Banking-Sektor?

---

**Diskussionsfragen**

- Wie wählt man k in K-means?
- Wann ist Clustering besser als Klassifikation?

---

## Klassifizierungsalgorithmen

---

### Logistic Regression

Binäre Klassifikation (Fraud / kein Fraud)

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/ca77a3d3-1399-4ed9-9863-a61413c37538.png)

**Modellbewertung**

- **Precision** – Anteil korrekter positiver Vorhersagen
- **Recall** – Anteil erkannter positiver Fälle
- **F1-Score** – Balance aus Precision und Recall

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/image%203.png)

- **ROC-AUC**

[Classification: ROC and AUC  |  Machine Learning  |  Google for Developers](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc)

---

## Regressionsanalyse

**Lernziele**

- Lineare und logistische Regression verstehen
- Modellbewertung anwenden

---

### 1. Lineare Regression

- Vorhersage kontinuierlicher Werte
- Banking: Customer Lifetime Value (CLV)

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/7157e307-1bf2-47e9-b355-74e84eaeccb5.png)

- **Modellbewertung**
  - **MSE (Mean Squared Error)** – mittlerer quadratischer Fehler, stark empfindlich gegenüber Ausreißern.
  - **RMSE (Root Mean Squared Error)** – Quadratwurzel von MSE, gleiche Einheit wie Zielvariable.
  - **MAE (Mean Absolute Error)** – mittlerer absoluter Fehler, robuster gegen Ausreißer.
  - **R² (Bestimmtheitsmaß)** – erklärt, wie viel Varianz im Ziel durch das Modell erklärt wird (1 = perfekt, 0 = nichts erklärt).

---

**Diskussionsfragen**

- Wann ist ein hoher Recall wichtiger als hohe Precision?
- Banking-Beispiel: Betrugserkennung vs. Marketingkampagne

## Machine Learning Algorithmen

### 1. Decision Tree

- Regeln → Entscheidungen → Klassen
- Einfach interpretierbar

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/image%204.png)

### 2. Random Forest

- Ensemble vieler Bäume
- Robust gegen Overfitting

### 3. SVM (Support-Vector Machine)

- Finded eine **Grenzlinie** (bei 2D) oder **Hyper­ebene** (bei mehr Dimensionen), die die Klassen **maximal trennt**.
- „Support Vectors“ sind die Datenpunkte, die dieser Grenze am nächsten liegen - sie bestimmen ihre Lage.
- Gut für komplexe Grenzen

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/image%205.png)

**Typische Anwendungen:**

- Spam-Erkennung
- Gesichtserkennung
- Krankheitserkennung in medizinischen Daten
- Bilderkennung bei wenigen Trainingsdaten

## Unstructured Data Analytics

**Lernziele**

- Text- und Dokumentenverarbeitung verstehen
- Sentiment Analysis anwenden

---

### 1. Text Data Processing

- **Kundenkommunikation analysieren**
  Verarbeitung und Auswertung von E-Mails, Chatlogs und Social-Media-Nachrichten, um Kundenbedürfnisse und -anliegen besser zu verstehen.
  Beispiele:
  - Automatische Klassifizierung von Anfragen (z. B. Support, Beschwerde, Feedback)
  - Erkennung von wiederkehrenden Themen und Problemen
  - Priorisierung dringender Kundenanliegen
- **Transaktionsbeschreibungen durchsuchen**
  Extraktion relevanter Informationen aus Freitextfeldern in Konto- oder Zahlungsinformationen.
  Beispiele:
  - Zuordnung von Transaktionen zu Kategorien (Miete, Einkauf, Reisen)
  - Identifizierung von Händlern und Zahlungsplattformen
  - Erkennung untypischer Beschreibungen als Hinweis auf Betrug
- **Sentiment Analysis für Kundenstimmung**
  Erkennung der Stimmungslage in Kundenfeedback oder Supportgesprächen.
  Beispiele:
  - Positiv/neutral/negativ-Klassifizierung
  - Trends im Zeitverlauf verfolgen, um Kampagnenerfolg oder Servicequalität zu messen
  - Automatische Eskalation bei negativem Feedback

---

### 2. Document Processing

- **PDFs parsen (Verträge, Kontoauszüge)**
  Extraktion strukturierter Daten aus unstrukturierten Dokumenten.
  Beispiele:
  - Automatische Extraktion von Vertragsdetails wie Laufzeit, Gebühren, Kündigungsfristen
  - Verarbeitung von Kontoauszügen zur Transaktionsanalyse
  - Validierung von Dokumentinhalten gegen interne Systeme
- **E-Mail-Analyse für Supportoptimierung**
  Strukturierung und Auswertung von E-Mail-Inhalten zur Effizienzsteigerung im Kundenservice.
  Beispiele:
  - Erkennung und Tagging von Standardanfragen
  - Automatisierte Antwortvorschläge für häufige Fragen
  - Analyse von Bearbeitungszeiten und Antwortqualität

### 3. Image Processing

- **Bilder vorverarbeiten (Fotos, Scans)**
  Vorbereitung von Bilddaten zur Verbesserung der Qualität und Extraktion relevanter Informationen.
  Beispiele:
  - Rauschreduzierung und Schärfung für bessere Erkennungsergebnisse
  - Zuschneiden und Skalieren auf einheitliche Formate
  - Farbanpassung und Kontrastoptimierung für konsistente Bildqualität
- **Objekterkennung und Segmentierung**
  Identifizierung und Abgrenzung relevanter Objekte innerhalb eines Bildes.
  Beispiele:
  - Erkennung von Produkten in Lagerfotos zur Bestandskontrolle
  - Segmentierung von medizinischen Aufnahmen zur Analyse bestimmter Gewebearten
  - Zählen und Klassifizieren von Objekten in Produktionslinien
- **Texterkennung (OCR)**
  Automatische Erfassung von Textinhalten aus Bildern.
  Beispiele:
  - Extraktion von Text aus eingescannten Formularen
  - Erkennung von Beschriftungen und Nummernschildern
  - Digitalisierung handschriftlicher Notizen
- **Bildklassifikation**
  Automatisierte Zuordnung von Bildern zu vordefinierten Kategorien.
  Beispiele:
  - Sortieren von Produktbildern in E-Commerce-Kataloge
  - Erkennen von defekten Produkten in der Qualitätskontrolle
  - Einordnung von Satellitenbildern nach Landnutzung
- **Visuelle Ähnlichkeitssuche**
  Finden ähnlicher Bilder in großen Datenbeständen.
  Beispiele:
  - Identifizieren von Plagiaten in Bilddatenbanken
  - Empfehlung ähnlicher Produkte im Onlinehandel
  - Erkennen von Duplikaten oder Varianten eines Bildes

---

```python
               ┌────────────────────────────────┐
               │        Ingestion               │
               │  (E-Mails, PDFs, Transaktionen)│
               └───────────────┬────────────────┘
                               │
                      ┌────────▼────────┐
                      │    BRONZE       │
                      │   (Rohdaten)    │
                      └───┬─────┬───────┘
                          │     │
         ┌────────────────┘     └─────────────────┐
         │                                        │
┌────────▼────────┐                       ┌───────▼────────┐
│ Text-Pipeline   │                       │ Dokumente      │
│ (NLP)           │                       │ (PDF/OCR)      │
├─────────────────┤                       ├────────────────┤
│ Normalisierung  │                       │ OCR & Parsing  │
│ (PII, Sprache)  │                       │ (Tabellen)     │
│ → NLP Labeling  │                       │ Feldextraktion │
│ (Intent, Sent., │                       │ (Regeln + LLM) │
│  Entities)      │                       │ Validierung    │
│ → Indexierung   │                       │ (Referenzen)   │
│ (OpenSearch,    │                       └───────┬────────┘
│  pgvector)      │                               │
└────────┬────────┘                               │
         │                                        │
         │             ┌──────────────────────────▼────────────┐
         └────────────►│               SILBER                  │
                       │      (bereinigte, angereicherte       │
                       │               Daten)                  │
                       └───────────────┬───────────┬───────────┘
                                       │           │
                                       │           │
                               ┌───────▼───────┐   │
                               │  Features     │   │
                               │ (Geo, Zeit,   │   │
                               │Text, Historie)│   │
                               └───────┬───────┘   │
                                       │           │
                              ┌────────▼─────────┐ │
                              │  Betrugserkennung│ │
                              │ (Regeln + ML)    │ │
                              └────────┬─────────┘ │
                                       │           │
                              ┌────────▼─────────┐ │
                              │   Aktionen       │ │
                              │ (Block, Step-Up, │ │
                              │   Case)          │ │
                              └────────┬─────────┘ │
                                       │           │
                          ┌────────────▼───────────▼───┐
                          │            GOLD            │
                          │ (Features, Scores, Indizes)│
                          └────────────────────────────┘
```

---

**Diskussionsfragen**

- Welche unstrukturierten Datenquellen sind im Banking besonders wertvoll?
- Wie können wir Textdaten mit Transaktionsdaten kombinieren?
- Welche Big Data Typen könnten noch vorkommen? Wie können wir diese bearbeiten?

---

## Data Visualization

**Lernziele**

- Fortgeschrittene Pandas-Techniken kennenlernen
- Interaktive Dashboards erstellen

---

### 1. Pandas Advanced

- Zeitreihenanalyse (Umsatz pro Monat)
- Statistische Methoden (Varianz, Korrelation)
- Integration mit Spark DataFrames

### 2. Matplotlib/Seaborn

- Statistische Diagramme (Boxplot, Scatterplot)

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/image%206.png)

### 3. Streamlit Dashboards

- Interaktive KPIs (z. B. Kreditausfallrate, Umsatz pro Segment)

![image.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/image%207.png)

---

**Datenfluss zur Visualisierung**

```
[Datenerfassung]
   ↓
[Datenbereinigung]
   ↓
[Analyse in Pandas/Spark]
   ↓
[Visualisierung in Matplotlib/Streamlit]

```

## Beispiel einer Big Data Architektur (Fraud Detection)

![Screenshot 2025-08-12 at 13.45.45.png](Tag%202%20ML%20algorithms%20+%20Unstructured%20data%20processing%2024a7a614759580cfaaf2ed5d071082c4/Screenshot_2025-08-12_at_13.45.45.png)
