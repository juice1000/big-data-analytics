# Tag 1: Big Data fundamentals + Multi-source data integration

---

## 🎯 **Ziele und Erwartungen der Teilnehmenden**

### **Lernziel-Framework für Banking Analytics**

```
Business Goals → Technical Skills → Practical Application
     ↓                ↓                    ↓
- Fraud Detection   - Spark Mastery    - Real Banking Data
- Customer Insights - ML Algorithms    - Production Pipeline
- Risk Assessment   - LLM Integration  - Cloud Deployment

```

### **Erwartungsmanagement**

- **Praxisrelevanz:** Jede Übung mit Banking-Kontext
- **Skalierbarkeit:** Von lokaler Entwicklung bis Cloud-Production

---

## 📊 **Grundlagen von Big Data**

### **Die Evolution der Datenlandschaft**

### **Traditionelle Datenverarbeitung (1990er-2000er)**

```
┌─────────────┐    ┌────────────────┐    ┌─────────────┐
│   OLTP      │    │ Data Warehouse │    │  Reporting  │
│ (Transact.) │ -> │  (Nightly ETL) │ -> │ (Business)  │
└─────────────┘    └────────────────┘    └─────────────┘
   • MB-GB Daten     • Strukturiert      • Batch-Reports
   • Einzelne Server • Feste Schemas     • Historische Sicht

```

OTLP = Online Transaction Processing (executing a large number of small, concurrent transactions, typically in real-time)

OLTP = Online Transaction Processing - das System, das Ihre täglichen Bankgeschäfte wie Überweisungen und Kontostände in Echtzeit verarbeitet. Denken Sie an das System, das läuft, wenn Sie eine Karte in den Geldautomaten stecken.

Data Warehouse = Ein zentraler Speicherort für bereinigte, strukturierte Daten aus verschiedenen Quellen. Stellen Sie sich vor wie eine gut organisierte Bibliothek, wo alle Bücher (Daten) katalogisiert und an festen Plätzen stehen.

ETL = Extract, Transform, Load - der traditionelle Prozess zur Datenverarbeitung:
• Extract: Daten aus verschiedenen Quellen sammeln
• Transform: Daten bereinigen und in das gewünschte Format bringen
• Load: Bereinigte Daten in das Data Warehouse laden

### **Big Data Ära (2010er-heute)**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Multi-Source│    │  Data Lake  │    │ Real-time   │
│ (Streaming) │ -> │ (All Data)  │ -> │ Analytics   │
└─────────────┘    └─────────────┘    └─────────────┘
   • TB-PB Daten     • Alle Formate     • Live Insights
   • Verteilte Sys.  • Schema-on-Read   • Predictive

```

Data Lake = Ein riesiger Speicher für Daten in ihrem ursprünglichen Format. Stellen Sie sich vor wie ein großer See, in den verschiedene Flüsse (Datenquellen) münden. Die Daten werden erst später strukturiert, wenn man sie braucht.

Schema-on-Read = Die Struktur wird erst beim Lesen der Daten festgelegt, nicht beim Speichern. Das ist wie ein flexibles Lagersystem - Sie können verschiedene Gegenstände einlagern und später entscheiden, wie Sie sie sortieren möchten.

## **🎓 Grundlegende Begriffe einfach erklärt**

Bevor wir in die technischen Details eintauchen, klären wir die wichtigsten Begriffe mit einfachen Analogien:

### **📖 Big Data Glossar**

- Data Warehouse = Eine gut organisierte Bibliothek, wo alle Bücher (Daten) katalogisiert und an festen Plätzen stehen. Perfekt für geplante Recherche, aber unflexibel für spontane Fragen.
- Data Lake = Ein riesiger Speicher für Daten in ihrem ursprünglichen Format. Wie ein großer See, in den verschiedene Flüsse (Datenquellen) münden. Die Daten werden erst später strukturiert, wenn man sie braucht.
- ETL (Extract, Transform, Load) = Traditioneller Prozess: Daten sammeln → bereinigen → in Warehouse laden. Wie Bücher sortieren, bevor sie ins Regal kommen.
- Schema-on-Read vs Schema-on-Write = Bei Schema-on-Write definieren Sie die Struktur beim Speichern (wie vorgedruckte Formulare). Bei Schema-on-Read entscheiden Sie erst beim Lesen, wie Sie die Daten interpretieren (wie leere Notizblätter, die Sie später unterschiedlich verwenden).
- Verteilte Systeme = Statt einem großen Computer nutzen Sie viele kleine Computer zusammen. Wie ein Orchester: Jeder Musiker spielt seinen Teil, zusammen entsteht die Symphonie.

### **🏦 Banking-spezifische Begriffe**

- OLTP (Online Transaction Processing) = Das System für tägliche Bankgeschäfte wie Überweisungen und Kontostände. Optimiert für viele kleine, schnelle Transaktionen - wie ein Supermarkt-Kassensystem.
- OLAP (Online Analytical Processing) = Das System für Analysen und Berichte. Optimiert für komplexe Fragen über große Datenmengen - wie ein Forschungslabor.
- Fraud Detection = Betrugserkennung. Systeme, die verdächtige Transaktionen in Echtzeit identifizieren - wie ein digitaler Detektiv, der 24/7 auf Verdächtiges achtet.
- Risk Assessment = Risikobewertung. Berechnung der Wahrscheinlichkeit, dass ein Kredit nicht zurückgezahlt wird - wie ein digitaler Wahrsager für Kreditentscheidungen.

### **Die 5 V's von Big Data**

Beschreiben Charakteristiken, die Big Data innehat.

![image.png](Tag%201%20Big%20Data%20fundamentals%20+%20Multi-source%20data%20in%2024a7a6147595806a8bfeec3805da3e08/image.png)

### **1. Volume (Datenmenge)**

**Problem:** Exponentielles Datenwachstum

**Banking-Beispiele:**

- **Deutsche Bank:** ~1 Milliarde Transaktionen/Tag
- **PayPal:** 19 Millionen Transaktionen/Tag
- **Visa:** 65.000 Transaktionen/Sekunde

**Technische Herausforderungen:**

```python
# Traditionelle Limits
pandas_limit = "~8GB RAM Limit"
single_machine = "Vertical Scaling Costs"

# Big Data Lösung
spark_distributed = "Horizontal Scaling"
cloud_elastic = "Pay-as-you-scale"

```

Stellen Sie sich vor: Wenn Sie mit Excel arbeiten, werden alle Daten in den Arbeitsspeicher (RAM) Ihres Computers geladen. Moderne Computer haben oft 8-16GB RAM, was bedeutet, dass Sie maximal 2-3GB an Daten verarbeiten können.

Bei Big Data haben wir aber Datensätze, die 1000x größer sind! Da müssen wir die Daten auf viele Computer verteilen - so wie ein großes Lager, das auf mehrere Gebäude aufgeteilt wird.

Cloud-Elastic = Sie zahlen nur für die Rechenleistung, die Sie gerade brauchen. Wie bei einem Taxi - Sie zahlen nur für die gefahrenen Kilometer, nicht für das ganze Auto.

Pandas = Eine Python-Bibliothek für Datenanalyse, die in den Arbeitsspeicher (RAM) eines einzelnen Computers geladen wird. Bei 8GB RAM sind etwa 2-3GB für Daten verfügbar - das reicht für kleine bis mittlere Datasets.

Vertical Scaling (Vertikal skalieren) = Den Computer stärker machen: Mehr RAM, schnellere CPU, größere Festplatte. Wird schnell sehr teuer.

Horizontal Scaling (Horizontal skalieren) = Mehr Computer verwenden: Statt einem 32GB-Computer nutzen Sie vier 8GB-Computer zusammen. Günstiger und flexibler.

### **2. Velocity (Geschwindigkeit)**

**Problem:** Real-time Verarbeitung wird zur Geschäftsanforderung

**Banking Real-time Requirements:**

- **Fraud Detection:** < 100ms Entscheidung
- **Credit Approval:** < 5 Sekunden
- **Market Trading:** < 1ms (High-Frequency Trading)
- **Mobile Banking:** < 200ms Response

**Architektur-Implikationen:**

```
Batch Processing    vs.    Stream Processing
┌─────────────┐           ┌─────────────┐
│Data arrives │           │Data arrives │
│in batches   │           │continuously │
│             │           │             │
│Process every│           │Process in   │
│X hours      │           │real-time    │
│             │           │             │
│High latency │           │Low latency  │
└─────────────┘           └─────────────┘

```

### **3. Variety (Vielfalt)**

**Problem:** Daten kommen in verschiedenen Formaten

**Banking Data Sources:**

```
Strukturiert (20%):        Semi-strukturiert (30%):    Unstrukturiert (50%):
• Transaktionsdaten      • JSON APIs                 • E-Mails
• Kundenstammdaten       • XML Nachrichten           • Chat-Logs
• Kontostände            • Log-Dateien               • Dokumente
• Kredithistorie         • Web-Clickstreams          • Audio-Calls

```

**Schema Evolution Challenge:**

```sql
-- Traditional: Schema-on-Write
CREATE TABLE transactions (
    id INTEGER,
    amount DECIMAL(10,2),
    currency CHAR(3)
);

-- Big Data: Schema-on-Read
-- Flexibel: Neue Felder ohne Schema-Änderung
{
  "id": 123,
  "amount": 99.99,
  "currency": "EUR",
  "metadata": {...}  // Neue Felder jederzeit möglich
}

```

### **4. Veracity (Wahrhaftigkeit)**

**Problem:** Datenqualität variiert stark

**Banking Data Quality Issues:**

- **Incomplete Data:** 15-20% fehlende Werte in Customer Data
- **Inconsistent Formats:** Datum, Währung, Namen
- **Duplicate Records:** 5-10% bei Kundenzusammenführungen
- **Outdated Information:** Adressen, Telefonnummern

**Quality Impact on Business:**

```
Schlechte Datenqualität → Falsche Insights → Schlechte Entscheidungen

Beispiel: Credit Scoring
• 30% fehlerhafte Einkommensdaten
• 15% veraltete Beschäftigungsinformationen
→ 25% falsche Kreditentscheidungen
→ €50M jährlicher Verlust (Großbank)

```

### **5. Value (Wert)**

**Problem:** Nur ein Bruchteil der Daten ist wertvoll

**Banking Value Extraction:**

```
Raw Data (100%) → Processed (30%) → Insights (5%) → Action (1%)

Beispiel: Fraud Detection
• 1M tägliche Transaktionen
• 10,000 verdächtige Muster
• 100 echte Betrugsfälle
• 50 verhinderte Verluste = €500,000 täglich gerettete Summe

```

### **Herausforderungen bei der Big Data Verarbeitung**

- **Speicherung:** Ein Server kann maximal 100TB speichern
- **Geschwindigkeit:** Ein Computer prüft 10.000 Datensätze/Sekunde
- **Flexibilität:** Schema-Änderungen dauern Monate
- **Kosten:** Stärkere Hardware wird exponentiell teurer

Lösungen:

- **Verteilte Speicherung:** 1000 Server mit je 100TB = 100PB
- **Parallele Verarbeitung:** 1000 Computer prüfen 10M Datensätze/Sekunde
- **Schema-on-Read:** Struktur beim Lesen bestimmen
- **Horizontal Skalierung:** Mehr günstige Computer statt teure Hardware

### **1. Speicherung**

**Problem:** Petabyte-Scale Storage Management

**Traditionelle Limits:**

- **Single Server:** Maximale Festplattenkapazität
- **SAN/NAS Architekturen:** Kostenexplosion bei großen Datenmengen
- **Backup:** Unmögliche Backup-Zeiten

SAN = Storage Area Network (unabhängiges Speichernetzwerk, wird über Switch)

![image.png](Tag%201%20Big%20Data%20fundamentals%20+%20Multi-source%20data%20in%2024a7a6147595806a8bfeec3805da3e08/image%201.png)

NAS = Network Attached Storage (Teil des Netzwerkes)

![image.png](Tag%201%20Big%20Data%20fundamentals%20+%20Multi-source%20data%20in%2024a7a6147595806a8bfeec3805da3e08/image%202.png)

DAS = Direct Attached Storage (z.B. an den PC)

![image.png](Tag%201%20Big%20Data%20fundamentals%20+%20Multi-source%20data%20in%2024a7a6147595806a8bfeec3805da3e08/image%203.png)

**Big Data Lösung:**

```
Distributed File Systems (HDFS)
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Node 1  │ │ Node 2  │ │ Node 3  │ │ Node 4  │
│ 10TB    │ │ 10TB    │ │ 10TB    │ │ 10TB    │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
    │           │           │           │
    └───────────┼───────────┼───────────┘
                │           │
        Replicated Data (3x Copy)

```

### **2. Verarbeitungsgeschwindigkeit**

**Problem:** Traditionelle Algorithmen skalieren nicht

**Complexity Analysis:**

**Denken Sie an Algorithmus-Effizienz wie beim Aufräumen einer Bibliothek:**

• **Linear (O(n)):** Sie schauen jedes Buch einzeln durch - bei 1 Million Büchern schauen Sie 1 Million mal
• **Quadratisch (O(n²)):** Sie vergleichen jedes Buch mit jedem anderen - bei 1 Million Büchern sind das 1 Billion Vergleiche! Das dauert ewig.
• **Logarithmisch (O(log n)):** Sie nutzen ein intelligentes Ordnungssystem - selbst bei 1 Million Büchern brauchen Sie nur 20 Schritte

**Big Data Lösung:** Statt einen Bibliothekar alle Bücher durchsuchen zu lassen, teilen Sie die Arbeit auf 1000 Bibliothekare auf. Jeder sucht nur 1000 Bücher durch - parallel und viel schneller!

### **3. Datenqualität bei Scale**

**Problem:** Quality Checks werden zum Bottleneck

**Traditional Quality Checks:**

```python
# Single-threaded: 10,000 records/second
def validate_record(record):
    check_completeness(record)
    check_format(record)
    check_business_rules(record)
    return is_valid

# Time für 1B records: 100,000 seconds (28 hours!)

```

**Stellen Sie sich vor: Ein Sicherheitsbeamter überprüft jeden Besucher einzeln**

Traditionelle Datenqualität ist wie ein einzelner Sicherheitsbeamter, der jeden Besucher eines riesigen Konzerts einzeln überprüft. Bei 10.000 Besuchern schafft er vielleicht 1000 pro Stunde - das dauert 10 Stunden!

**Big Data Lösung: 100 Sicherheitsbeamte arbeiten parallel**

Spark ist wie 100 Sicherheitsbeamte, die gleichzeitig arbeiten. Jeder überprüft 100 Besucher - das dauert nur 6 Minuten! So kann Spark 1 Million Datensätze pro Sekunde überprüfen, während ein traditionelles System nur 10.000 schafft.

**Distributed Quality Checks:**

```python
# Spark: 1,000,000 records/second (1000x faster)
df.filter(col("amount") > 0)\
  .filter(col("currency").isin(["EUR", "USD", "GBP"]))\
  .filter(col("timestamp").isNotNull())

```

## **Chancen und Potenziale von Big Data**

### **1. Erkenntnisgewinn durch Skalierung**

**Statistical Power durch größere Samples:**

```
Sample Size Impact auf Confidence:
┌──────────────┬─────────────┬──────────────┐
│ Sample Size  │ Margin Error│ Confidence   │
├──────────────┼─────────────┼──────────────┤
│ 1,000        │ ±3.1%       │ 95%          │
│ 10,000       │ ±1.0%       │ 95%          │
│ 1,000,000    │ ±0.1%       │ 95%          │
│ 100,000,000  │ ±0.01%      │ 95%          │
└──────────────┴─────────────┴──────────────┘

```

**Banking Insights Examples:**

- **Micro-Segmentation:** 10,000 Customer segments statt 10
- **Real-time Patterns:** Fraud detection in Millisekunden
- **Predictive Accuracy:** 95% Genauigkeit bei Kreditausfällen

### **2. Verbesserte Entscheidungsfindung**

**From Reactive to Predictive:**

```
Traditional Banking          Big Data Banking
┌─────────────────┐         ┌─────────────────┐
│ Historical      │   →     │ Predictive      │
│ Analysis        │         │ Analytics       │
│                 │         │                 │
│ "What happened?"│         │ "What will      │
│                 │         │  happen?"       │
│                 │         │                 │
│ Monthly Reports │         │ Real-time       │
│                 │         │ Dashboards      │
└─────────────────┘         └─────────────────┘

```

**Decision Speed Impact:**

- **Credit Decisions:** 2 Wochen → 2 Minuten
- **Fraud Detection:** 24 Stunden → 100 Millisekunden
- **Market Response:** 1 Woche → Real-time

### **3. Personalisierte Dienstleistungen**

**Hyper-Personalization durch Big Data:**

```python
# Traditional: Segment-based
if customer.age > 65:
    offer_pension_products()

# Big Data: Individual-based
if customer.spending_pattern.matches("young_family") and \
   customer.savings_rate > 0.15 and \
   customer.location.near("good_schools"):
    offer_education_savings_plan()

```

---

## 🏗️ **Big Data-Technologien und -Plattformen**

### **Hadoop-Ökosystem: Die Foundation**

**Stellen Sie sich Hadoop wie ein riesiges Lager vor:**

- **HDFS (Hadoop Distributed File System)** = Das Lagersystem selbst. Statt einem riesigen Lagerhaus haben Sie 1000 kleine Lagerhallen, die alle miteinander verbunden sind. Wenn eine abbrennt, haben Sie die Waren trotzdem noch in 2 anderen Hallen (automatische Sicherheitskopien).
- **MapReduce** = Die Arbeiter im Lager. Jeder Arbeiter bekommt einen kleinen Teil der Aufgabe (Map), dann werden alle Ergebnisse zusammengefügt (Reduce). Wie eine Inventur: 1000 Arbeiter zählen je ein Regal, dann wird alles zusammengerechnet.
- **YARN** = Der Lagerverwalter. Er entscheidet, welcher Arbeiter welche Aufgabe bekommt und sorgt dafür, dass alles effizient läuft.

### **Hadoop Architektur Overview**

```
┌─────────────────────────────────────────────────────┐
│                Hadoop Ecosystem                     │
├─────────────────────────────────────────────────────┤
│ Applications: Hive, Pig, Mahout, HBase, Flume     │
├─────────────────────────────────────────────────────┤
│ Processing: MapReduce, Spark, Tez                  │
├─────────────────────────────────────────────────────┤
│ Resource Management: YARN                           │
├─────────────────────────────────────────────────────┤
│ Storage: HDFS (Hadoop Distributed File System)     │
└─────────────────────────────────────────────────────┘

```

### **HDFS (Hadoop Distributed File System)**

**Das verteilte Dateisystem für Big Data**

**Kernprinzipien:**

```
1. Massive Skalierung:
   • Designed für Petabytes
   • Commodity Hardware
   • Linear scaling

2. Fault Tolerance:
   • Automatische Replikation (3x default)
   • Self-healing bei Node-Ausfällen
   • No Single Point of Failure

3. High Throughput:
   • Optimiert für große Files (>64MB)
   • Sequential Access Pattern
   • Bandwidth over Latency

```

**HDFS Architektur:**

```
                ┌─────────────┐
                │ NameNode    │ ← Metadaten Master
                │ (Master)    │   (Filesystem Namespace)
                └─────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
 ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
 │ DataNode 1  │ │ DataNode 2  │ │ DataNode 3  │
 │             │ │             │ │             │
 │ Block A-1   │ │ Block A-2   │ │ Block A-3   │
 │ Block B-1   │ │ Block B-2   │ │ Block C-1   │
 │ Block C-2   │ │ Block C-3   │ │ Block B-3   │
 └─────────────┘ └─────────────┘ └─────────────┘

```

**Banking Use Case:**

```python
# Speicherung von 5 Jahren Transaktionsdaten
# 1 Milliarde Transaktionen/Tag × 365 Tage × 5 Jahre = 1.8 Trillion Records
# @ 200 Bytes/Record = 360 TB Raw Data

hdfs_storage = {
    "raw_transactions": "120 TB",
    "processed_data": "90 TB",
    "ml_features": "60 TB",
    "models_backups": "30 TB",
    "total_with_replication": "900 TB"  # 3x replication
}

```

### **MapReduce-Programmierung**

**Das ursprüngliche Big Data Processing Model**

**MapReduce Paradigma:**

```python
Input → MAP → Shuffle & Sort → REDUCE → Output

Beispiel: Fraud Detection Count
Input: [transaction1, transaction2, ..., transactionN]

MAP Phase:
transaction1 → ("fraud", 1) if is_suspicious(transaction1) else ("normal", 1)
transaction2 → ("fraud", 1) if is_suspicious(transaction2) else ("normal", 1)

REDUCE Phase:
("fraud", [1,1,1,...]) → ("fraud", total_count)
("normal", [1,1,1,...]) → ("normal", total_count)

```

**MapReduce Limitations (Warum Spark besser ist):**

```
MapReduce Problems:
┌─────────────────────────────────────────┐
│ 1. Disk-based: Slow I/O between jobs    │
│ 2. Batch-only: No real-time processing  │
│ 3. Complex: Multi-step jobs difficult   │
│ 4. No Interactive: Each query from disk │
└─────────────────────────────────────────┘

Spark Solutions:
┌────────────────────────────────────────────────┐
│ 1. In-Memory: 10-100x faster                   │
│ 2. Unified: Batch + Stream + ML                │
│ 3. Simple: High-level APIs                     │
│ 4. Interactive: REPL (Read-Evaluate-Print-Loop)│
└────────────────────────────────────────────────┘

```

## **Apache Spark: Die moderne Big Data Engine**

### **🎆 Apache Spark: Unified Framework**

*Data Collection → Cleaning → Analysis → Feature Engineering → 
Model Training → Evaluation & Validation → Serving*

**Spark ist wie ein modernes Hochleistungs-Logistikzentrum:**

- **In-Memory Computing** = Statt jedes Paket zwischenzulagern, behalten die Arbeiter alles im Kopf (Arbeitsspeicher). 10-100x schneller als ständiges Hin- und Herräumen.
- **Unified Analytics** = Ein System für alles: normale Lagerarbeit, Echtzeitüberwachung, Qualitätskontrolle und Vorhersagen. Früher brauchten Sie 4 verschiedene Systeme.
- **Spark SQL** = Sie können mit normaler Sprache (SQL) fragen: 'Zeig mir alle roten Produkte aus 2024' statt komplizierte Arbeitsbefehle zu geben.
- **Spark Streaming** = Überwachung in Echtzeit. Jedes neue Paket wird sofort registriert und verarbeitet, nicht erst am Ende des Tages.

### **Warum Spark MapReduce ablöst**

**Performance Comparison:**

```
Benchmark: 100GB Daten sortieren

MapReduce:    1600 Sekunden
Spark (Disk): 200 Sekunden  (8x schneller)
Spark (Memory): 23 Sekunden (70x schneller)

Iterative ML Algorithm (10 Iterations):
MapReduce:    30 Minuten (jede Iteration from disk)
Spark:        2 Minuten (data cached in memory)

```

### Best of Both Worlds

Eine Kombination aus beidem ist auch möglich

```python
                   +---------------------------+
                   |        Clients            |
                   |  (Spark jobs / Notebooks) |
                   +-------------+-------------+
                                 |
                                 v
+---------------------------------------------------------------+
|                        Resource Layer                         |
|                    (YARN / Kubernetes*)                       |
|   Schedulers allocate executors & containers for Spark jobs   |
+---------------------------+-----------------------------------+
                            |
                            v
+---------------------------------------------------------------+
|                         Compute Layer                         |
|                         Apache Spark                          |
|  - Spark SQL / DataFrames  - MLlib  - Structured Streaming    |
|  - Executors run close to data (data locality)                |
+---------------------------+-----------------------------------+
                            |
                            v
+---------------------------------------------------------------+
|                         Storage Layer                         |
|     HDFS  (or Ozone / S3-compatible object storage**)         |
|  - Parquet / ORC / Avro files                                 |
|  - Replication & fault-tolerance                              |
+---------------------------+-----------------------------------+
                            |
                            v
+---------------------------------------------------------------+
|                      Metastore & Tables                       |
|        Apache Hive Metastore (Glue OK too)                    |
|  - External tables over Parquet/ORC in HDFS                   |
|  - Accessed via Spark SQL (Hive catalog)                      |
+---------------------------+-----------------------------------+
                            |
                            v
+---------------------------------------------------------------+
|                     NoSQL / Serving (optional)                |
|        HBase / Cassandra / Elasticsearch                      |
|  - Low-latency lookups / serving layer                        |
+---------------------------------------------------------------+
```

### **Spark Core Concepts**

**1. In-Memory Computing:**

```
Traditional MapReduce:          Apache Spark:
┌─────┐                        ┌─────┐
│ Job1│ → Disk → ┌─────┐       │ Job1│ ↘
└─────┘          │ Job2│       └─────┘  ┌────────┐
                 └─────┘                │ Memory │
                      ↓                 └────────┘
              Disk → ┌─────┐                 ↗
                     │ Job3│       ┌─────┐ ↗
                     └─────┘       │ Job2│
                                   └─────┘

```

Spark ist ein Lazy-Excecution Framework.

**2. Unified Analytics Platform:**

```
┌─────────────────────────────────────────────────────┐
│                Spark Applications                   │
├─────────────────────────────────────────────────────┤
│ Spark SQL │ Streaming │ MLlib │ GraphX │ R/Python   │
├─────────────────────────────────────────────────────┤
│              Spark Core Engine                      │
│         (RDDs, DAG Scheduler, Memory Mgmt)          │
├─────────────────────────────────────────────────────┤
│           Cluster Resource Manager                  │
│      (YARN, Mesos, Kubernetes, Standalone)         │
└─────────────────────────────────────────────────────┘

```

### Programmiersprachen mit Spark

![Screenshot 2025-08-10 at 18.52.48.png](Tag%201%20Big%20Data%20fundamentals%20+%20Multi-source%20data%20in%2024a7a6147595806a8bfeec3805da3e08/Screenshot_2025-08-10_at_18.52.48.png)

### Spark-Integrationen

![Screenshot 2025-08-10 at 18.49.04.png](Tag%201%20Big%20Data%20fundamentals%20+%20Multi-source%20data%20in%2024a7a6147595806a8bfeec3805da3e08/Screenshot_2025-08-10_at_18.49.04.png)

### **Spark SQL: Distributed SQL**

**SQL-Interface für Big Data**

```python
# Spark SQL Example: Banking Fraud Analysis
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

# Load banking data
transactions = spark.read.parquet("hdfs://banking/transactions/")

# Register as SQL table
transactions.createOrReplaceTempView("transactions")

# Complex fraud detection query
fraud_patterns = spark.sql("""
    SELECT
        customer_id,
        COUNT(*) as transaction_count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount,
        STDDEV(amount) as amount_volatility,
        COUNT(DISTINCT merchant) as unique_merchants,
        COUNT(DISTINCT HOUR(timestamp)) as active_hours
    FROM transactions
    WHERE date(timestamp) = current_date()
    GROUP BY customer_id
    HAVING
        transaction_count > 50 OR
        amount_volatility > 1000 OR
        unique_merchants > 20
    ORDER BY amount_volatility DESC
""")

```

**Apache Pig:**

ETL Pipelines auf semi/unstructured Daten

```sql
-- Pig Latin: Dataflow Language
transactions = LOAD 'hdfs://transactions.csv' USING PigStorage(',')
    AS (id:chararray, customer:chararray, amount:double, timestamp:chararray);

filtered = FILTER transactions BY amount > 1000.0;
grouped = GROUP filtered BY customer;
aggregated = FOREACH grouped GENERATE
    group AS customer,
    COUNT(filtered) AS high_value_count;

STORE aggregated INTO 'hdfs://high_value_customers';

```

### **Spark Streaming: Real-time Processing**

**Micro-Batch Architecture für Low-Latency**

```python
# Spark Streaming: Real-time Fraud Detection
from pyspark.streaming import StreamingContext

# Create streaming context (2 second batches)
ssc = StreamingContext(spark.sparkContext, 2)

# Connect to Kafka stream
kafka_stream = KafkaUtils.createStream(ssc,
    zkQuorum="localhost:2181",
    groupId="fraud-detection",
    topics={"transactions": 1})

# Process each micro-batch
def process_transactions(time, rdd):
    if not rdd.isEmpty():
        # Convert to DataFrame
        df = spark.read.json(rdd)

        # Apply fraud detection model
        predictions = fraud_model.transform(df)

        # Filter high-risk transactions
        high_risk = predictions.filter(col("fraud_probability") > 0.8)

        # Send alerts
        high_risk.foreach(send_fraud_alert)

kafka_stream.foreachRDD(process_transactions)
ssc.start()
ssc.awaitTermination()

```

### **Apache Flink: Stream-First Processing**

### **Flink vs. Spark Streaming**

```
┌─────────────────┬─────────────────┬─────────────────┐
│     Aspect      │ Spark Streaming │ Apache Flink    │
├─────────────────┼─────────────────┼─────────────────┤
│ Processing Model│ Micro-batches   │ True Streaming  │
│ Latency         │ 0.5-2 seconds   │ <100ms          │
│ Throughput      │ Very High       │ High            │
│ Exactly-once    │ Yes             │ Yes             │
│ Complex Events  │ Limited         │ Excellent (CEP) │
│ Windowing       │ Good            │ Very Advanced   │
│ Ecosystem       │ Mature          │ Growing         │
└─────────────────┴─────────────────┴─────────────────┘

```

**Flink Banking Use Case:**

```java
// Flink: Real-time Transaction Monitoring
DataStream<Transaction> transactions = env
    .addSource(new KafkaSource<>("transactions"))
    .keyBy(Transaction::getCustomerId)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(new TransactionAggregator())
    .filter(new FraudDetectionFilter());

transactions.addSink(new AlertSink());

```

## **🎆 Cloud-Plattformen für Big Data**

Moderne Banken nutzen Cloud-Plattformen, um Big Data zu verarbeiten. Das ist wie der Umzug von einem eigenen Rechenzentrum in ein hochmodernes, geteiltes Datacenter:

### **☁️ Google Cloud + Databricks: Das Power-Duo**

- **Google Cloud Platform** = Das Rechenzentrum. Unbegrenzte Rechenleistung und Speicherplatz, den Sie nach Bedarf mieten.
- **Databricks** = Die Entwicklungsumgebung. Ein modernes Labor, wo Data Scientists und Entwickler zusammenarbeiten können.
- **BigQuery** = Der Hochgeschwindigkeits-Abfrage-Service. Stellen Sie Fragen an Milliarden von Datensätzen und bekommen Antworten in Sekunden.
- **Vertex AI** = Die Künstliche Intelligenz. Wie ein sehr kluger Assistent, der Muster in Daten erkennt und Vorhersagen macht.

### **GCP Databricks: Unified Analytics Platform**

**Databricks Architektur:**

```
┌─────────────────────────────────────────────────────┐
│                Databricks Workspace                 │
├─────────────────────────────────────────────────────┤
│ Notebooks │ Jobs │ Models │ SQL │ Dashboards        │
├─────────────────────────────────────────────────────┤
│            Apache Spark Runtime                     │
├─────────────────────────────────────────────────────┤
│              GCP Infrastructure                     │
│  Compute Engine │ Cloud Storage │ BigQuery          │
└─────────────────────────────────────────────────────┘

```

### Databricks - Unified Analytics Platform

![image.png](Tag%201%20Big%20Data%20fundamentals%20+%20Multi-source%20data%20in%2024a7a6147595806a8bfeec3805da3e08/image%204.png)

**Key Databricks Features:**

- **Collaborative Notebooks:** Multi-language (Python, Scala, SQL, R)
- **Auto-scaling Clusters:** Pay-per-use compute
- **MLflow Integration:** ML lifecycle management
- **Delta Lake:** ACID transactions for data lakes
- **Security:** Enterprise-grade access controls

### **Google Cloud Integration**

```python
# Databricks + GCP Services Integration
from pyspark.sql import SparkSession

# Session Initialization
spark = SparkSession.builder \
    .appName("Banking Analytics") \
    .getOrCreate()

# Read directly from BigQuery
transactions = spark.read \
    .format("bigquery") \
    .option("table", "banking-project.transactions.daily") \
    .load()

# Process with Spark
fraud_scores = transactions \
    .select("customer_id", "amount", "merchant") \
    .groupBy("customer_id") \
    .agg({"amount": "avg", "merchant": "count"})

# Write back to BigQuery
fraud_scores.write \
    .format("bigquery") \
    .option("table", "banking-project.analytics.fraud_scores") \
    .mode("overwrite") \
    .save()

```

## 🏦 **Banking-Spezifische Big Data Anwendungen**

### **Fraud Detection mit Big Data**

**Traditionell:** Ein Bankmitarbeiter überprüft morgens die Transaktionen vom Vortag. Betrüger haben 24 Stunden Vorsprung.

**Big Data:** Ein intelligentes System analysiert jede Transaktion in Echtzeit:

- **Ist das normal für diesen Kunden?** (Verhaltensanalyse)
- **Passt der Ort zur gewohnten Route?** (Geo-Analyse)
- **Gibt es ähnliche Betrugsmuster?** (Machine Learning)
- **Entscheidung in <100ms:** Transaktion genehmigen oder blockieren

### **Traditional vs. Big Data Approach**

```
Traditional Fraud Detection:
┌─────────────────────────────────────────┐
│ • Rule-based (if amount > €5000...)     │
│ • Batch processing (daily updates)      │
│ • Limited features (transaction only)   │
│ • High false positives (>30%)           │
│ • 24-48 hour detection delay            │
└─────────────────────────────────────────┘

Big Data Fraud Detection:
┌─────────────────────────────────────────┐
│ • ML-based (complex pattern detection)  │
│ • Real-time processing (<100ms)         │
│ • Multi-modal (transaction + behavior)  │
│ • Low false positives (<5%)             │
│ • Immediate detection & blocking        │
└─────────────────────────────────────────┘

```

### **Multi-Layer Fraud Detection Architecture**

```
Layer 1: Real-time Rules (< 10ms)
├─ Amount limits
├─ Geographic checks
└─ Merchant validation

Layer 2: ML Scoring (< 100ms)
├─ Behavior patterns
├─ Network analysis
└─ Anomaly detection

Layer 3: Deep Analysis (< 1s)
├─ Text analysis (LLM)
├─ Cross-reference external data
└─ Human expert review queue

```

## 📁 **Datenbeschaffung und -integration**

### **Interne Datenquellen**

```
┌─────────────────────────────────────────────────────┐
│                  Core Banking System                │
├─────────────────────────────────────────────────────┤
│ • Transaktionsdaten (Payment Processing)            │
│ • Kundenstammdaten (CRM)                            │
│ • Kontoinformationen (Account Management)           │
│ • Kredithistorie (Risk Management)                  │
│ • Produktportfolio (Product Database)               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                 Digital Channels                    │
├─────────────────────────────────────────────────────┤
│ • Mobile Banking Logs                               │
│ • Online Banking Clickstreams                       │
│ • ATM Transaction Logs                              │
│ • Call Center Interactions                          │
│ • Chat/Support Communications                       │
└─────────────────────────────────────────────────────┘

```

### **Externe Datenquellen**

```python
# External Data Integration für Enhanced Analytics
external_data_sources = {
    "market_data": {
        "provider": "Bloomberg/Reuters",
        "frequency": "real_time",
        "data_types": ["stock_prices", "fx_rates", "interest_rates"],
        "volume": "1M records/day"
    },
    "credit_bureaus": {
        "provider": "Schufa/Experian",
        "frequency": "on_demand",
        "data_types": ["credit_scores", "payment_history"],
        "volume": "100K requests/day"
    },
    "economic_indicators": {
        "provider": "Government APIs",
        "frequency": "monthly",
        "data_types": ["inflation", "unemployment", "gdp"],
        "volume": "1K indicators"
    },
    "social_sentiment": {
        "provider": "Social Media APIs",
        "frequency": "hourly",
        "data_types": ["brand_mentions", "sentiment_scores"],
        "volume": "50K mentions/day"
    }
}

```

## **Datenextraktion Strategien**

In der Banking-Welt müssen wir verschiedene Datenextraktionsansätze verstehen, da nicht alle Daten gleich behandelt werden können. Hier sind die drei Hauptstrategien:

### **1. Batch ETL für Historical Data**

Warum Batch ETL?

- Große Datenmengen verarbeiten (TB-Level)
- Komplexe Transformationen mit hoher Rechenleistung
- Zeitkritikalität nicht gegeben (täglich, wöchentlich)
- Kostenoptimierung durch Off-Peak-Verarbeitung

Banking-Beispiel für Batch ETL:

Tägliche Verarbeitung von Transaktionsdaten:

Schritt 1: Extract (22:00 Uhr)
• Alle Transaktionen des Tages aus Core Banking System
• Kundenstammdaten-Updates
• Wechselkurs-Snapshots
• Merchant-Kategorisierungen

Schritt 2: Transform (22:30-04:00 Uhr)
• Datenbereinigung (Duplikate, Formate)
• Anreicherung mit externen Daten
• Fraud-Score-Berechnung (historisch)
• Customer-Segmentierung
• Compliance-Checks

Schritt 3: Load (04:00-05:00 Uhr)
• Data Warehouse Update
• Analytische Datenbankbefüllung
• Dashboard-Datenmart Refresh

Typische Batch-Größen im Banking:

- Transaktionen: 1-10 Millionen Records/Tag
- Datenvolumen: 100GB-2TB/Tag
- Verarbeitungszeit: 4-6 Stunden
- Parallelität: 50-200 Spark Executors

### **2. Real-time Streaming für Live Data**

Wann brauchen wir Real-time?

- Fraud Detection: Transaktion muss in <100ms bewertet werden
- Risk Monitoring: Portfoliowerte ändern sich sekundär
- Customer Experience: Sofortige Empfehlungen
- Regulatory Compliance: Sofortige Meldungen

Streaming-Architektur im Banking:

ATM/POS → Kafka → Spark Streaming → Fraud Engine → Sofortige Entscheidung
    ↓           ↓           ↓              ↓              ↓
  <1ms      <10ms      <50ms         <30ms         <100ms

Parallele Verarbeitung:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│         Transaction       │→ │             Kafka             │→│           Multiple          │
│             Stream          │    │             Topics            │    │       Consumers        │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                           ┌──────┼──────┐                     │
                           │                │                │                     ▼
              ┌────▼──┐ ┌─▼──┐ ┌─▼──┐   ┌──────────┐
              │      Fraud    │ │  Risk  │ │    Rec  │   │      Database     │
              │    Engine    │ │ Mgmt│ │  Eng   │   │      Updates       │
              └───────┘  └────┘ └────┘    └──────────┘

Streaming vs. Batch Entscheidungsmatrix:

Streaming wählen, wenn:
• Latenz < 1 Sekunde erforderlich
• Daten kontinuierlich ankommen
• Sofortige Aktionen nötig (Alerts, Blocking)
• Event-driven Architecture

Batch wählen, wenn:
• Komplexe Joins zwischen großen Datensätzen
• Historische Analysen über Jahre
• Kostenoptimierung wichtig
• Verarbeitungszeit > 1 Stunde akzeptabel

### **3. API Integration für External Data**

Warum APIs kritisch für Banking sind:

- Regulatorische Anforderungen (Open Banking, PSD2)
- Real-time Marktdaten für Trading
- Kreditscoring mit externen Datenquellen
- KYC/AML-Compliance Checks

Typische Banking API-Integrations-Szenarien:

Szenario 1: Kreditprüfung in Echtzeit
┌───────────┐    ┌────────────────┐    ┌────────────────┐
│ Kunde     │ → │ Bank System   │ → │ Multiple APIs   │
│ Antrag    │    │ (Spark Job)   │    │ (Parallel)      │
└───────────┘    └────────────────┘    └────────────────┘
                                              │
                               ┌──────────┼──────────┐
                               │          │          │
                         ┌────▼──┐ ┌─▼──┐ ┌─▼────┐
                         │Schufa │ │BaFin│ │Social│
                         │ API   │ │ API │ │ Data │
                         └───────┘ └─────┘ └──────┘
                             │       │       │
                             ▼       ▼       ▼
                         ┌─────────────────────────┐
                         │   ML-Model für Credit   │
                         │   Scoring (< 3 Sek)     │
                         └─────────────────────────┘

API-Integration Herausforderungen:

- Rate Limiting: APIs haben oft Beschränkungen (z.B. 1000 Calls/Minute)
- Authentication: OAuth, API Keys, Zertifikate verwalten
- Error Handling: Netzwerkfehler, Timeouts, Service-Downtimes
- Data Consistency: Verschiedene APIs liefern unterschiedliche Formate
- Kosten: Pay-per-call Models können teuer werden

### **Datenintegration Herausforderungen**

Selbst mit den besten Extraktionsstrategien stehen wir vor zwei grundlegenden Herausforderungen:

### **1. Schema Evolution Management**

Das Problem: Datenstrukturen ändern sich ständig

Warum Schema Evolution in Banking kritisch ist:

- Regulatorische Änderungen: Neue Compliance-Felder (z.B. DSGVO, Basel III)
- Produktinnovationen: Neue Bankprodukte brauchen neue Datenfelder
- API-Updates: Externe Datenanbieter ändern ihre Strukturen
- System-Upgrades: Core Banking Systeme werden modernisiert

Schema Evolution Beispiel - Banking Transaction Table:

Version 1.0 (2020):
• transaction_id
• customer_id
• amount
• currency
• timestamp

Version 2.0 (2021 - DSGVO):
+ privacy_consent_flag
+ data_retention_date
+ anonymization_level

Version 3.0 (2022 - Open Banking):
+ third_party_provider_id
+ consent_scope
+ api_version

Version 4.0 (2024 - ESG Compliance):
+ carbon_footprint_score
+ sustainable_investment_flag
+ esg_rating

Das Problem: Wie behandeln wir alte Daten mit neuen Schemas?

Lösungsansätze für Schema Evolution:

- Schema Registry: Zentrale Versionierung aller Schemas (Confluent Schema Registry)
- Delta Lake: ACID-Transaktionen für Schema-Änderungen
- Backwards Compatibility: Neue Felder als optional mit Default-Werten
- Data Versioning: Separate Pipelines für verschiedene Schema-Versionen

### Praktisches Beispiel: Schema Evolution Workflow

Schritt 1: Schema-Änderung erkennen
┌──────────────────────────────┐
│ Neues Feld: esg_rating      │
│ Typ: INTEGER               │
│ Default: NULL              │
│ Required: false            │
└──────────────────────────────┘

Schritt 2: Schema Registry Update
• Version 4.0 registrieren
• Backward Compatibility prüfen
• Consumer benachrichtigen

Schritt 3: Graduelle Migration
• Neue Daten: Schema 4.0
• Alte Daten: Schema 1.0-3.0 (NULL-Werte für neue Felder)
• Queries: Beide Versionen unterstützen

### **2. Data Quality Across Sources**

Das Problem: Jede Datenquelle hat ihre eigenen Qualitätsstandards

Multi-Source Data Quality Herausforderungen:

Banking Data Quality Matrix (typische Probleme):

┌──────────────────┼────────────────┼──────────────────┐
│ Datenquelle      │ Typical Issues   │ Quality Score    │
├──────────────────┼────────────────┼──────────────────┤
│ Core Banking     │ 5% Duplicates    │ 95% (Excellent)  │
│ Mobile App       │ 10% Missing      │ 85% (Good)       │
│ Web Portal       │ 15% Inconsistent │ 80% (Fair)       │
│ ATM Logs         │ 20% Format Issues│ 75% (Poor)       │
│ External APIs    │ 30% Stale Data   │ 60% (Critical)   │
│ Social Media     │ 50% Unreliable   │ 40% (Unusable)   │
└──────────────────┴────────────────┴──────────────────┘

Spezifische Qualitätsprobleme nach Quelle:

Core Banking System (95% Quality):
• Sehr hohe Genauigkeit
• Vollständige Transaktionsdaten
• Problem: Legacy-Formate, langsame Updates

Mobile/Web Channels (80-85% Quality):
• Real-time Daten
• Gute User Experience Metriken
• Problem: Unvollständige Sessions, Device-Unterschiede

External APIs (60% Quality):
• Wertvolle Anreicherung
• Aktuelle Marktdaten
• Problem: Rate Limits, Ausfallzeiten, verschiedene Formate

Data Quality Management Strategien:

1. Source-Level Quality Gates (Präventive Maßnahmen):

- Input Validation: Daten sofort bei Eingabe prüfen
- API Contracts: Klare SLAs mit externen Anbietern
- Real-time Monitoring: Sofortige Alerts bei Qualitätsabfall

2. Processing-Level Quality Control (Reaktive Maßnahmen):

- Data Profiling: Automatische Erkennung von Anomalien
- Cross-Source Validation: Daten zwischen Quellen abgleichen
- Machine Learning Quality Scoring: Automatische Qualitätsbewertung

3. Unified Data Quality Framework:

┌─────────────────────────────────────────────────────┐
│            Data Quality Monitoring Dashboard           │
├─────────────────────────────────────────────────────┤
│ Source        Quality Score    Last Updated   Status │
├─────────────────────────────────────────────────────┤
│ Core Banking  95%             2min ago       🟢     │
│ Mobile App    87%             5min ago       🟢     │
│ Web Portal    78%             1min ago       🟡     │
│ External API  45%             15min ago      🔴     │
└─────────────────────────────────────────────────────┘

Praktische Workshop-Übung: Data Quality Assessment

Im Workshop werden wir folgende praktische Übungen durchführen:

- Batch ETL: Historische Transaktionsdaten mit Spark verarbeiten
- Streaming: Live-Simulation von Kreditkarten-Transaktionen
- API Integration: Externe Wechselkurse in Echtzeit abrufen
- Schema Evolution: Neue Compliance-Felder hinzufügen ohne Downtime
- Quality Monitoring: Automatische Erkennung von Datenqualitätsproblemen

## **🔄 Datenbeschaffung und -integration verstehen**

In der Banking-Welt kommen Daten aus vielen verschiedenen Quellen. Stellen Sie sich vor, Sie müssen ein vollständiges Bild eines Kunden erstellen:

### **🎯 Datenqualität: Das A und O**

Schlechte Datenqualität ist wie ein kaputtes Navigationsgerät - es führt Sie in die falsche Richtung, egal wie gut Ihr Auto ist.

****Die 6 Dimensionen der Datenqualität:****

- **Vollständigkeit** = Sind alle Puzzle-Teile da? (Wie vollständig ist ein Kundenprofil?)
- **Genauigkeit** = Stimmen die Informationen? (Ist die E-Mail-Adresse korrekt?)
- **Konsistenz** = Sagen alle Quellen dasselbe? (Heißt der Kunde überall gleich?)
- **Aktualität** = Sind die Daten frisch genug? (Ist die Adresse noch aktuell?)
- **Gültigkeit** = Erfüllen Daten die Geschäftsregeln? (Ist das Geburtsdatum realistisch?)
- **Eindeutigkeit** = Gibt es Duplikate? (Existiert derselbe Kunde mehrfach?)

## **🎩 Mehr Banking-Use Cases in der Praxis**

Schauen wir uns konkrete Beispiele an, wie Big Data das Banking verändert hat:

### **📊 Kreditentscheidungen: Der intelligente Berater**

**Traditionell:** Kreditantrag → Manuelle Prüfung → 2 Wochen warten → Entscheidung

**Big Data:** Automatische Analyse in 2 Minuten:

- **Finanzhistorie:** Wie zuverlässig war der Kunde bisher?
- **Verhaltensanalyse:** Wie verwaltet er sein Geld?
- **Externe Faktoren:** Wie stabil ist sein Job/Branche?
- **Resultat:** 95% Genauigkeit bei Ausfallprognosen

### **🎛️ Personalisierte Angebote: Der persönliche Bankberater**

**Traditionell:** Alle Kunden bekommen dieselben Standard-Angebote per Post.

**Big Data:** Jeder Kunde bekommt maßgeschneiderte Angebote:

- **Junge Familie mit steigendem Einkommen** → Bauspardarlehen-Angebot
- **Student mit regelmäßigen Einzahlungen** → Investmentfonds-Angebot
- **Senior mit hohen Ersparnissen** → Altersvorsorge-Optimierung

## **🌈 Zusammenfassung: Die Big Data Revolution**

**Tag 1 hat gezeigt, wie sich die Datenwelt fundamental verändert hat:**

- **Von klein zu riesig:** MB → Petabytes (das Millionenfache)
- **Von langsam zu sofort:** Tägliche Berichte → Echtzeit-Entscheidungen
- **Von starr zu flexibel:** Feste Schemas → Beliebige Datenformate
- **Von teuer zu erschwinglich:** Spezialhardware → Cloud-Services

**Die wichtigsten Erkenntnisse:**

- **Big Data ist kein Hype** - es löst echte Geschäftsprobleme
- **Technologie ist Mittel zum Zweck** - der Fokus liegt auf Mehrwert für Kunden
- **Datenqualität ist entscheidend** - schlechte Daten führen zu schlechten Entscheidungen
- **Integration ist komplex** - aber die Tools werden immer

## Databricks Tutorial

File Upload oder Daten aus verschiedenen Quellen beziehen

![Screenshot 2025-08-11 at 15.26.20.png](Tag%201%20Big%20Data%20fundamentals%20+%20Multi-source%20data%20in%2024a7a6147595806a8bfeec3805da3e08/Screenshot_2025-08-11_at_15.26.20.png)