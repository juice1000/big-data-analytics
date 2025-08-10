# Tag 1: Big Data fundamentals + Multi-source data integration

## 🎯 **Ziele und Erwartungen der Teilnehmenden**

### **Warum diese Session kritisch ist**

Die Klärung individueller Lernziele bildet das Fundament für einen erfolgreichen Workshop. Bei nur 2 Teilnehmern können wir den Inhalt optimal an die spezifischen Bedürfnisse anpassen.

### **Lernziel-Framework für Banking Analytics**

```
Business Goals → Technical Skills → Practical Application
     ↓                ↓                    ↓
- Fraud Detection   - Spark Mastery    - Real Banking Data
- Customer Insights - ML Algorithms    - Production Pipeline
- Risk Assessment   - LLM Integration  - Cloud Deployment

```

### **Erwartungsmanagement**

- **70% Hands-On:** Direktes Arbeiten mit Code und Daten
- **30% Theorie:** Nur das Wesentliche für das Verständnis
- **Praxisrelevanz:** Jede Übung mit Banking-Kontext
- **Skalierbarkeit:** Von lokaler Entwicklung bis Cloud-Production

---

## 📊 **Grundlagen von Big Data**

### **Die Evolution der Datenlandschaft**

### **Traditionelle Datenverarbeitung (1990er-2000er)**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   OLTP      │    │ Data Warehouse │    │  Reporting  │
│ (Transact.) │ -> │  (Nightly ETL) │ -> │ (Business)  │
└─────────────┘    └─────────────┘    └─────────────┘
   • MB-GB Daten     • Strukturiert      • Batch-Reports
   • Einzelne Server  • Feste Schemas     • Historische Sicht

```

### **Big Data Ära (2010er-heute)**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Multi-Source│    │  Data Lake  │    │ Real-time   │
│ (Streaming) │ -> │ (All Data)  │ -> │ Analytics   │
└─────────────┘    └─────────────┘    └─────────────┘
   • TB-PB Daten     • Alle Formate     • Live Insights
   • Verteilte Sys.  • Schema-on-Read   • Predictive

```

### **Die 5 V's von Big Data - Detaillierte Analyse**

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
• Transaktionsdaten       • JSON APIs                 • E-Mails
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

### **1. Speicherung**

**Problem:** Petabyte-Scale Storage Management

**Traditionelle Limits:**

- **Single Server:** Maximale Festplattenkapazität
- **SAN/NAS:** Kostenexplosion bei großen Datenmengen
- **Backup:** Unmögliche Backup-Zeiten

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

```python
# O(n) - Linear: Akzeptabel bis ~1M Records
for transaction in transactions:
    process(transaction)

# O(n²) - Quadratic: Unmöglich bei Big Data
for t1 in transactions:
    for t2 in transactions:
        compare(t1, t2)  # 1M × 1M = 1 Trillion operations!

# O(log n) - Distributed: Big Data Solution
spark.sql("SELECT * FROM transactions WHERE suspicious = true")

```

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

**Distributed Quality Checks:**

```python
# Spark: 1,000,000 records/second (1000x faster)
df.filter(col("amount") > 0)\
  .filter(col("currency").isin(["EUR", "USD", "GBP"]))\
  .filter(col("timestamp").isNotNull())

```

### **Chancen und Potenziale von Big Data**

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

```
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
│ 1. Disk-based: Slow I/O between jobs   │
│ 2. Batch-only: No real-time processing │
│ 3. Complex: Multi-step jobs difficult  │
│ 4. No Interactive: Each query from disk│
└─────────────────────────────────────────┘

Spark Solutions:
┌─────────────────────────────────────────┐
│ 1. In-Memory: 10-100x faster          │
│ 2. Unified: Batch + Stream + ML       │
│ 3. Simple: High-level APIs             │
│ 4. Interactive: REPL for exploration   │
└─────────────────────────────────────────┘

```

### **Hive & Pig: SQL-ähnliche Abfragesprachen**

**Apache Hive:**

```sql
-- Hive: SQL-on-Hadoop
CREATE TABLE transactions (
    transaction_id STRING,
    customer_id STRING,
    amount DECIMAL(10,2),
    timestamp TIMESTAMP,
    merchant STRING
) STORED AS PARQUET;

-- Complex Analytics Query
SELECT
    customer_id,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_amount,
    STDDEV(amount) as amount_volatility
FROM transactions
WHERE timestamp >= '2024-01-01'
GROUP BY customer_id
HAVING COUNT(*) > 100;

```

**Apache Pig:**

```
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

### **Apache Spark: Die moderne Big Data Engine**

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

### **Spark SQL: Verteiltes SQL**

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

### **Cloud Platforms für Big Data**

### **GCP Databricks: Unified Analytics Platform**

**Databricks Architektur:**

```
┌─────────────────────────────────────────────────────┐
│                Databricks Workspace                │
├─────────────────────────────────────────────────────┤
│ Notebooks │ Jobs │ Models │ SQL │ Dashboards       │
├─────────────────────────────────────────────────────┤
│            Apache Spark Runtime                     │
├─────────────────────────────────────────────────────┤
│              GCP Infrastructure                     │
│  Compute Engine │ Cloud Storage │ BigQuery         │
└─────────────────────────────────────────────────────┘

```

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

# BigQuery Integration
spark = SparkSession.builder \
    .appName("Banking Analytics") \
    .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-latest.jar") \
    .getOrCreate()

# Read from BigQuery
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

### **Vertex AI für LLM Integration**

**Google's AI Platform für Banking Analytics**

```python
# Vertex AI + LLM für Transaction Analysis
from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel

# Initialize Vertex AI
aiplatform.init(project="banking-analytics", location="us-central1")

# Load PaLM model
model = TextGenerationModel.from_pretrained("text-bison@001")

# Analyze transaction descriptions
def analyze_transaction_text(description):
    prompt = f"""
    Analyze this banking transaction description for fraud indicators:
    Transaction: "{description}"

    Consider:
    - Unusual merchant names
    - Suspicious transaction patterns
    - Geographic inconsistencies

    Provide a fraud risk score (0-100) and explanation.
    """

    response = model.predict(
        prompt=prompt,
        temperature=0.1,
        max_output_tokens=256
    )

    return response.text

# Apply to transaction stream
transactions_with_ai = spark_df.withColumn(
    "ai_fraud_analysis",
    udf(analyze_transaction_text)(col("description"))
)

```

---

## 🏦 **Banking-Spezifische Big Data Anwendungen**

### **Fraud Detection mit Big Data**

### **Traditional vs. Big Data Approach**

```
Traditional Fraud Detection:
┌─────────────────────────────────────────┐
│ • Rule-based (if amount > €5000...)     │
│ • Batch processing (daily updates)      │
│ • Limited features (transaction only)   │
│ • High false positives (>30%)          │
│ • 24-48 hour detection delay           │
└─────────────────────────────────────────┘

Big Data Fraud Detection:
┌─────────────────────────────────────────┐
│ • ML-based (complex pattern detection)  │
│ • Real-time processing (<100ms)         │
│ • Multi-modal (transaction + behavior)  │
│ • Low false positives (<5%)            │
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

### **Customer Analytics & Segmentation**

### **Traditional Segmentation**

```sql
-- Simple demographic segmentation
SELECT
    CASE
        WHEN age < 25 THEN 'Young'
        WHEN age < 45 THEN 'Middle'
        ELSE 'Senior'
    END as age_group,
    COUNT(*) as customer_count
FROM customers
GROUP BY age_group;

```

### **Big Data Behavioral Segmentation**

```python
# Advanced behavioral segmentation with Spark MLlib
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler

# Create feature vectors
feature_cols = [
    "avg_transaction_amount", "transaction_frequency",
    "product_diversity", "digital_engagement_score",
    "customer_service_interactions", "account_balance_volatility"
]

assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
customer_features = assembler.transform(customer_data)

# Apply K-means clustering
kmeans = KMeans(k=8, featuresCol="features", predictionCol="segment")
model = kmeans.fit(customer_features)

# Generate segments
segmented_customers = model.transform(customer_features)

# Business interpretation
segment_profiles = segmented_customers.groupBy("segment").agg(
    avg("avg_transaction_amount").alias("avg_spend"),
    avg("transaction_frequency").alias("frequency"),
    avg("product_diversity").alias("products"),
    count("*").alias("customer_count")
)

```

### **Portfolio Optimization mit Big Data**

### **Risk Assessment at Scale**

```python
# Portfolio risk calculation with distributed computing
def calculate_var_at_risk(portfolio_data, confidence_level=0.95):
    """
    Value at Risk calculation for large portfolios
    Using Monte Carlo simulation on Spark
    """

    # Generate random scenarios (10M simulations)
    scenarios = spark.range(10000000).select(
        (rand() * 2 - 1).alias("market_shock"),
        (rand() * 0.5).alias("credit_shock"),
        (rand() * 0.3).alias("operational_shock")
    )

    # Apply shocks to portfolio
    portfolio_scenarios = portfolio_data.crossJoin(scenarios).select(
        "*",
        (col("position_value") *
         (1 + col("market_shock") * col("beta") +
          col("credit_shock") * col("credit_risk") +
          col("operational_shock") * 0.1)).alias("shocked_value")
    )

    # Calculate portfolio P&L for each scenario
    portfolio_pnl = portfolio_scenarios.groupBy("market_shock", "credit_shock", "operational_shock").agg(
        sum("shocked_value").alias("total_portfolio_value")
    ).withColumn(
        "portfolio_pnl",
        col("total_portfolio_value") - sum("position_value")
    )

    # Calculate VaR
    var_threshold = portfolio_pnl.approxQuantile("portfolio_pnl", [1 - confidence_level], 0.01)[0]

    return var_threshold

```

---

## 📁 **Datenbeschaffung und -integration**

### **Datenquellen im Banking-Kontext**

### **Interne Datenquellen**

```
┌─────────────────────────────────────────────────────┐
│                  Core Banking System                │
├─────────────────────────────────────────────────────┤
│ • Transaktionsdaten (Payment Processing)           │
│ • Kundenstammdaten (CRM)                          │
│ • Kontoinformationen (Account Management)          │
│ • Kredithistorie (Risk Management)                 │
│ • Produktportfolio (Product Database)              │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                 Digital Channels                    │
├─────────────────────────────────────────────────────┤
│ • Mobile Banking Logs                              │
│ • Online Banking Clickstreams                      │
│ • ATM Transaction Logs                             │
│ • Call Center Interactions                         │
│ • Chat/Support Communications                      │
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

### **Datenextraktion Strategien**

### **1. Batch ETL für Historical Data**

```python
# Daily batch ETL für Transaktionsdaten
from pyspark.sql import SparkSession
from datetime import datetime, timedelta

def daily_transaction_etl(spark, processing_date):
    """
    Extract yesterday's transactions and load into data lake
    """

    # Extract from core banking database
    yesterday = processing_date - timedelta(days=1)

    transactions = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:oracle:thin:@banking-db:1521:PROD") \
        .option("dbtable", f"""
            (SELECT * FROM transactions
             WHERE transaction_date = '{yesterday.strftime('%Y-%m-%d')}')
        """) \
        .option("user", "etl_user") \
        .option("password", "etl_password") \
        .load()

    # Transform: Add derived fields
    enriched_transactions = transactions \
        .withColumn("transaction_hour", hour("transaction_timestamp")) \
        .withColumn("is_weekend", dayofweek("transaction_date").isin([1, 7])) \
        .withColumn("amount_category",
                   when(col("amount") < 10, "micro")
                   .when(col("amount") < 100, "small")
                   .when(col("amount") < 1000, "medium")
                   .otherwise("large"))

    # Load to data lake (partitioned by date)
    enriched_transactions.write \
        .mode("overwrite") \
        .partitionBy("transaction_date") \
        .parquet(f"gs://banking-datalake/transactions/year={yesterday.year}/month={yesterday.month}")

    return f"Processed {enriched_transactions.count()} transactions for {yesterday}"

```

### **2. Real-time Streaming für Live Data**

```python
# Kafka-based real-time ingestion
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Define transaction schema
transaction_schema = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("amount", DecimalType(10,2), True),
    StructField("merchant", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("channel", StringType(), True)
])

# Read streaming data from Kafka
streaming_transactions = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "banking-kafka:9092") \
    .option("subscribe", "live-transactions") \
    .load() \
    .select(from_json(col("value").cast("string"), transaction_schema).alias("data")) \
    .select("data.*")

# Real-time fraud scoring
fraud_scored_stream = streaming_transactions \
    .withColumn("fraud_score",
               when(col("amount") > 5000, 0.8)
               .when(col("channel") == "ATM", 0.3)
               .otherwise(0.1)) \
    .withColumn("risk_level",
               when(col("fraud_score") > 0.7, "HIGH")
               .when(col("fraud_score") > 0.3, "MEDIUM")
               .otherwise("LOW"))

# Write to multiple sinks
query = fraud_scored_stream.writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, epoch: [
        df.write.format("delta").mode("append").save("gs://fraud-detection/live-scores"),
        df.filter(col("risk_level") == "HIGH").write.format("kafka")
          .option("kafka.bootstrap.servers", "alert-kafka:9092")
          .option("topic", "fraud-alerts").save()
    ]) \
    .start()

```

### **3. API Integration für External Data**

```python
# External API data integration
import requests
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

class ExternalDataIntegrator:
    def __init__(self, spark):
        self.spark = spark

    def fetch_market_data(self, symbols, date_range):
        """
        Fetch market data from external APIs
        """
        def fetch_symbol_data(symbol):
            response = requests.get(
                f"https://api.marketdata.com/v1/stocks/{symbol}/quotes",
                params={
                    "from": date_range["start"],
                    "to": date_range["end"],
                    "token": "market_api_token"
                }
            )
            return response.json()

        # Parallel API calls
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(fetch_symbol_data, symbols))

        # Convert to Spark DataFrame
        market_df = self.spark.createDataFrame(
            pd.DataFrame([item for sublist in results for item in sublist])
        )

        return market_df

    def enrich_transactions_with_market_data(self, transactions_df):
        """
        Enrich transactions with market context
        """
        # Get relevant market data
        market_data = self.fetch_market_data(
            symbols=["^GDAXI", "EURUSD=X"],
            date_range={"start": "2024-01-01", "end": "2024-12-31"}
        )

        # Join transactions with market data
        enriched = transactions_df.join(
            market_data.select("date", "market_volatility", "market_sentiment"),
            transactions_df.transaction_date == market_data.date,
            "left"
        )

        return enriched

```

### **Datenintegration Herausforderungen**

### **1. Schema Evolution Management**

```python
# Schema evolution handling mit Delta Lake
from delta.tables import DeltaTable

def handle_schema_evolution(new_data_df, target_table_path):
    """
    Gracefully handle schema changes in banking data
    """

    if DeltaTable.isDeltaTable(spark, target_table_path):
        # Table exists - check for schema evolution
        existing_table = DeltaTable.forPath(spark, target_table_path)

        # Schema comparison
        existing_schema = existing_table.toDF().schema
        new_schema = new_data_df.schema

        # Add new columns if they don't exist
        for field in new_schema.fields:
            if field.name not in [f.name for f in existing_schema.fields]:
                existing_table.toDF().withColumn(field.name, lit(None).cast(field.dataType))

        # Merge with schema evolution
        existing_table.alias("existing").merge(
            new_data_df.alias("new"),
            "existing.transaction_id = new.transaction_id"
        ).whenMatchedUpdateAll() \
         .whenNotMatchedInsertAll() \
         .execute()
    else:
        # First load - create table
        new_data_df.write.format("delta").save(target_table_path)

```

### **2. Data Quality Across Sources**

```python
# Multi-source data quality validation
class DataQualityValidator:

    def __init__(self, spark):
        self.spark = spark
        self.quality_rules = {
            "transactions": {
                "completeness": ["transaction_id", "customer_id", "amount"],
                "validity": {
                    "amount": "amount > 0 AND amount < 1000000",
                    "currency": "currency IN ('EUR', 'USD', 'GBP')",
                    "timestamp": "timestamp IS NOT NULL"
                },
                "uniqueness": ["transaction_id"]
            },
            "customers": {
                "completeness": ["customer_id", "email"],
                "validity": {
                    "email": "email RLIKE '^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}",
                    "birth_date": "birth_date < current_date() AND birth_date > '1900-01-01'"
                },
                "uniqueness": ["customer_id", "email"]
            }
        }

    def validate_dataset(self, df, dataset_type):
        """
        Comprehensive data quality validation
        """
        rules = self.quality_rules.get(dataset_type, {})
        quality_report = {}

        # Completeness checks
        for column in rules.get("completeness", []):
            null_count = df.filter(col(column).isNull()).count()
            total_count = df.count()
            quality_report[f"{column}_completeness"] = 1 - (null_count / total_count)

        # Validity checks
        for column, condition in rules.get("validity", {}).items():
            valid_count = df.filter(condition).count()
            total_count = df.count()
            quality_report[f"{column}_validity"] = valid_count / total_count

        # Uniqueness checks
        for column in rules.get("uniqueness", []):
            unique_count = df.select(column).distinct().count()
            total_count = df.count()
            quality_report[f"{column}_uniqueness"] = unique_count / total_count

        return quality_report

    def create_quality_dashboard(self, quality_reports):
        """
        Generate data quality monitoring dashboard
        """
        quality_df = self.spark.createDataFrame([
            (dataset, metric, score, datetime.now())
            for dataset, metrics in quality_reports.items()
            for metric, score in metrics.items()
        ], ["dataset", "metric", "quality_score", "timestamp"])

        # Save for monitoring dashboard
        quality_df.write.mode("append").saveAsTable("data_quality.monitoring")

        return quality_df

```

---

## 🔧 **Hands-On Vorbereitung**

### **Environment Setup Checkliste**

### **Local Development Setup**

```bash
# 1. Python Environment
python -m venv bigdata_workshop
source bigdata_workshop/bin/activate  # Linux/Mac
# bigdata_workshop\Scripts\activate   # Windows

# 2. Core Packages Installation
pip install --upgrade pip
pip install pyspark==3.5.0
pip install pandas numpy matplotlib seaborn plotly
pip install jupyter notebook ipython
pip install requests beautifulsoup4 lxml

# 3. Java Installation Verification
java -version  # Should show Java 17+
echo $JAVA_HOME  # Should point to Java installation

# 4. Spark Installation Test
python -c "from pyspark.sql import SparkSession; print('Spark import successful')"

# 5. Memory Configuration
export SPARK_DRIVER_MEMORY=4g
export SPARK_EXECUTOR_MEMORY=2g

```

### **Data Download and Verification**

```python
# Data integrity verification script
import os
import hashlib
import requests
from pathlib import Path

def download_workshop_data():
    """
    Download and verify workshop datasets
    """

    datasets = {
        "banking_transactions_1M.csv": {
            "url": "https://workshop-data.example.com/transactions_1M.csv",
            "size_mb": 200,
            "checksum": "a1b2c3d4e5f6..."
        },
        "banking_transactions_5M.csv": {
            "url": "https://workshop-data.example.com/transactions_5M.csv",
            "size_mb": 1000,
            "checksum": "f6e5d4c3b2a1..."
        },
        "customer_data.csv": {
            "url": "https://workshop-data.example.com/customers.csv",
            "size_mb": 50,
            "checksum": "1a2b3c4d5e6f..."
        }
    }

    data_dir = Path("workshop_data")
    data_dir.mkdir(exist_ok=True)

    for filename, info in datasets.items():
        file_path = data_dir / filename

        if not file_path.exists():
            print(f"Downloading {filename}...")
            response = requests.get(info["url"], stream=True)

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Verify file integrity
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        if file_hash == info["checksum"]:
            print(f"✅ {filename} verified successfully")
        else:
            print(f"❌ {filename} checksum mismatch - please re-download")

    print("Data download complete!")

if __name__ == "__main__":
    download_workshop_data()

```

### **Banking Dataset Overview**

### **Synthetische Datensätze (GDPR-konform)**

```python
# Dataset schemas and sample data
banking_schemas = {
    "transactions": {
        "schema": [
            ("transaction_id", "string"),
            ("customer_id", "string"),
            ("amount", "decimal(10,2)"),
            ("currency", "string"),
            ("merchant", "string"),
            ("merchant_category", "string"),
            ("transaction_type", "string"),
            ("channel", "string"),
            ("timestamp", "timestamp"),
            ("location_country", "string"),
            ("location_city", "string"),
            ("is_weekend", "boolean"),
            ("description", "string")
        ],
        "sample_data": {
            "transaction_id": "TXN_2024_000001",
            "customer_id": "CUST_12345",
            "amount": 45.67,
            "currency": "EUR",
            "merchant": "REWE Supermarket",
            "merchant_category": "Grocery",
            "transaction_type": "purchase",
            "channel": "card",
            "timestamp": "2024-08-09 14:23:15",
            "location_country": "DE",
            "location_city": "Frankfurt",
            "is_weekend": False,
            "description": "Weekly grocery shopping"
        },
        "volume": "5M records",
        "time_range": "2019-2024"
    },

    "customers": {
        "schema": [
            ("customer_id", "string"),
            ("age", "integer"),
            ("gender", "string"),
            ("income_bracket", "string"),
            ("city", "string"),
            ("country", "string"),
            ("account_type", "string"),
            ("registration_date", "date"),
            ("credit_score", "integer"),
            ("email", "string"),
            ("phone", "string"),
            ("preferred_channel", "string")
        ],
        "sample_data": {
            "customer_id": "CUST_12345",
            "age": 34,
            "gender": "F",
            "income_bracket": "50k-75k",
            "city": "Frankfurt",
            "country": "DE",
            "account_type": "premium",
            "registration_date": "2020-03-15",
            "credit_score": 750,
            "email": "customer@example.com",
            "phone": "+49-xxx-xxxxxxx",
            "preferred_channel": "mobile"
        },
        "volume": "100K records"
    }
}

```

Diese umfassende theoretische Grundlage bietet das notwendige Fundament für den praktischen Workshop-Tag 1 und kann direkt für Präsentationen und Dokumentation verwendet werden.
