# Tag 2: ML algorithms + Unstructured data processing

##

### Datenqualität und -bereinigung

**Lernziele**

- Datenqualitätsprobleme erkennen
- Techniken zur Bereinigung auswählen und anwenden
- Qualität messbar machen

---

### 1. Typische Datenqualitätsprobleme

| Problem        | Beschreibung                                | Beispiel im Banking                                  |
| -------------- | ------------------------------------------- | ---------------------------------------------------- |
| Fehlende Werte | Datenfelder ohne Inhalt                     | Geburtsdatum eines Kunden fehlt                      |
| Ausreißer      | Extremwerte außerhalb normaler Range        | Überweisung von 1 Mio. € von Privatkonto             |
| Duplikate      | Gleicher Kunde mehrfach erfasst             | „Max Müller“ und „M. Mueller“ als getrennte Einträge |
| Inkonsistenz   | Unterschiedliche Formate oder Schreibweisen | „GER“, „Deutschland“, „DE“                           |

---

### 2. Datenbereinigungstechniken

- **Normalisierung:** Einheitliche Datums-, Währungs-, Namensformate
- **Fehlerkorrektur:** IBAN-Checks, Plausibilitätsprüfungen
- **Duplikaterkennung:** Eindeutige IDs, Fuzzy Matching
- **Imputation:** Fehlende Werte ersetzen (Mittelwert, Median, Modell)
- **Outlier-Handling:** Entfernen, Flaggen, getrennt analysieren

---

### 3. Datenqualitätsmetriken

- **Vollständigkeit** – Anteil der gefüllten Felder
- **Genauigkeit** – Abgleich mit Referenzquellen
- **Konsistenz** – Einheitlichkeit über Systeme
- **Aktualität** – Alter der Daten im Analysekontext

---

**ASCII Diagramm – Datenbereinigungsprozess**

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

---

**Didaktische Tipps**

- Zeige echten (anonymisierten) Bank-Datensatz mit Fehlern
- Lass Teilnehmer gemeinsam bereinigen

**Diskussionsfragen**

- Welche Fehler sind im Bankensektor am kritischsten?
- Kann man immer alle Ausreißer löschen?

---

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

### 2. Dimensionale Modellierung

- **Star Schema** – Faktentabelle in der Mitte, Dimensionstabellen außen
- **Snowflake Schema** – Dimensionen weiter normalisiert

**Diagramm**

```
       [Dim_Kunde]
            |
[Dim_Zeit] - [Fakt_Transaktion] - [Dim_Produkt]
            |
       [Dim_Filiale]

```

---

### 3. NoSQL-Datenmodellierung

- **Key-Value:** Schneller Zugriff (Kundennummer → Kundendaten)
- **Document Model:** Vollständiges Kundenprofil als JSON
- **Wide Column Stores:** Zeitreihen (Kontostände pro Tag)

---

### 4. Big Data Schema Design

- **Sharding:** Horizontale Aufteilung (Regionen, Kundengruppen)
- **Replikation:** Mehrfachspeicherung für Ausfallsicherheit

---

**Diskussionsfragen**

- Wann ist Star Schema besser als Snowflake?
- Welche NoSQL-Struktur passt für Betrugserkennung in Echtzeit?

---

### Grundlagen Datenanalyse-Algorithmen

**Lernziele**

- Clustering verstehen
- K-means und hierarchisches Clustering kennen
- Business-Interpretation anwenden

---

### 1. Clustering

- Ziel: Ähnliche Datenpunkte gruppieren ohne vorgegebene Labels
- **K-means Prozess**

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

---

### 2. Banking-Anwendung

- Kundensegmentierung nach Umsatz & Risiko
- Gezielte Marketingkampagnen

---

**Diskussionsfragen**

- Wie wählt man k in K-means?
- Wann ist Clustering besser als Klassifikation?

---

### Klassifizierungsalgorithmen

**Lernziele**

- Entscheidungsbaum, Random Forest, SVM verstehen
- Anwendungen in Fraud Detection

---

### 1. Entscheidungsbaum

- Regeln → Entscheidungen → Klassen
- Einfach interpretierbar

### 2. Random Forest

- Ensemble vieler Bäume
- Robust gegen Overfitting

### 3. SVM

- Findet optimale Trennlinie (Hyperplane)
- Gut für komplexe Grenzen

---

**Banking-Beispiel**

- Klassifikation: Verdächtig vs. legitim
- Betrugserkennung anhand Transaktionsmustern

---

**Diskussionsfragen**

- Wann ist Interpretierbarkeit wichtiger als Genauigkeit?
- Nachteile von SVM bei Big Data?

---

## Regressionsanalyse

**Lernziele**

- Lineare und logistische Regression verstehen
- Modellbewertung anwenden

---

### 1. Lineare Regression

- Vorhersage kontinuierlicher Werte
- Banking: Customer Lifetime Value (CLV)

### 2. Logistische Regression

- Binäre Klassifikation (Fraud / kein Fraud)

### 3. Modellbewertung

- **Precision** – Anteil korrekter positiver Vorhersagen
- **Recall** – Anteil erkannter positiver Fälle
- **F1-Score** – Balance aus Precision und Recall

---

**Diskussionsfragen**

- Wann ist ein hoher Recall wichtiger als hohe Precision?
- Banking-Beispiel: Betrugserkennung vs. Marketingkampagne

---

### Unstructured Data Analytics

**Lernziele**

- Text- und Dokumentenverarbeitung verstehen
- Sentiment Analysis anwenden

---

### 1. Text Data Processing

- Kundenkommunikation analysieren (E-Mails, Chatlogs)
- Transaktionsbeschreibungen durchsuchen
- Sentiment Analysis für Kundenstimmung

### 2. Document Processing

- PDFs parsen (Verträge, Kontoauszüge)
- E-Mail-Analyse für Supportoptimierung

### 3. Banking-Anwendung

- Textbasierte Betrugserkennung (verdächtige Betreffzeilen, Formulierungen)

---

**Diskussionsfragen**

- Welche unstrukturierten Datenquellen sind im Banking besonders wertvoll?
- Wie können wir Textdaten mit Transaktionsdaten kombinieren?

---

### Data Visualization & Pandas Deep-Dive

**Lernziele**

- Fortgeschrittene Pandas-Techniken anwenden
- Interaktive Dashboards erstellen

---

### 1. Pandas Advanced

- Zeitreihenanalyse (Umsatz pro Monat)
- Statistische Methoden (Varianz, Korrelation)
- Integration mit Spark DataFrames

### 2. Matplotlib/Seaborn

- Statistische Diagramme (Boxplot, Scatterplot)

### 3. Streamlit Dashboards

- Interaktive KPIs (z. B. Kreditausfallrate, Umsatz pro Segment)

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
