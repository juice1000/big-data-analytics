# Big Data Analytics Workshop - Lab Exercises

## 🎯 Workshop Overview

This repository contains hands-on lab exercises for the "Big Data Analytics im Banking" workshop. The labs are designed to provide practical experience with big data technologies, focusing on banking use cases.

## 📚 Lab Structure

### Lab 01: Big Data Fundamentals

**Duration:** 90 minutes  
**Focus:** Understanding the 5 V's of Big Data with practical examples

- **01_data_volume_demonstration.ipynb** - Working with large datasets
- **02_data_variety_formats.ipynb** - Handling structured, semi-structured, and unstructured data
- **03_data_quality_assessment.ipynb** - Data quality validation and profiling

### Lab 02: Apache Spark Introduction

**Duration:** 120 minutes  
**Focus:** Spark fundamentals and SQL operations

- **01_spark_setup_and_basics.ipynb** - Spark session, RDDs, and DataFrames
- **02_spark_sql_operations.ipynb** - SQL queries on distributed data
- **03_spark_performance_optimization.ipynb** - Caching and performance tuning

### Lab 03: Banking Fraud Detection

**Duration:** 150 minutes  
**Focus:** Real-time fraud detection using big data

- **01_fraud_data_exploration.ipynb** - Banking transaction analysis
- **02_fraud_detection_rules.ipynb** - Rule-based detection systems
- **03_ml_fraud_detection.ipynb** - Machine learning models for fraud detection

### Lab 04: Customer Analytics & Segmentation

**Duration:** 120 minutes  
**Focus:** Customer insights through big data analytics

- **01_customer_segmentation.ipynb** - K-means clustering for customer segments
- **02_behavioral_analytics.ipynb** - Customer behavior pattern analysis
- **03_personalization_engine.ipynb** - Recommendation systems

### Lab 05: Data Integration & ETL

**Duration:** 90 minutes  
**Focus:** Data pipeline construction and management

- **01_data_ingestion_batch.ipynb** - Batch ETL processes
- **02_data_quality_monitoring.ipynb** - Quality checks and monitoring
- **03_schema_evolution.ipynb** - Handling changing data schemas

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Java 8 or higher (for Spark)
- Minimum 8GB RAM recommended

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd big-data-analytics
   ```

2. **Create virtual environment**

   ```bash
   python -m venv bigdata_workshop
   source bigdata_workshop/bin/activate  # Linux/Mac
   # bigdata_workshop\Scripts\activate   # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start Jupyter**

   ```bash
   jupyter notebook
   ```

5. **Verify Spark installation**
   ```python
   from pyspark.sql import SparkSession
   spark = SparkSession.builder.appName("Test").getOrCreate()
   print("Spark version:", spark.version)
   ```

## 📊 Datasets

The workshop uses synthetic banking datasets that are GDPR-compliant:

- **Banking Transactions:** 1M+ synthetic transaction records
- **Customer Data:** 100K synthetic customer profiles
- **Market Data:** Historical financial market indicators
- **External APIs:** Mock data for external integrations

All datasets are generated using the Faker library to ensure privacy compliance.

## 🛠 Technology Stack

- **Apache Spark 3.5** - Distributed computing engine
- **PySpark** - Python API for Spark
- **Pandas** - Data manipulation and analysis
- **Jupyter Notebooks** - Interactive development environment
- **Matplotlib/Seaborn/Plotly** - Data visualization
- **Scikit-learn** - Machine learning algorithms

## 📋 Learning Outcomes

After completing these labs, participants will be able to:

1. **Understand Big Data Fundamentals**

   - Explain the 5 V's of Big Data with practical examples
   - Identify data quality issues and implement validation strategies
   - Work with multiple data formats and sources

2. **Master Apache Spark**

   - Create and manipulate Spark DataFrames
   - Write complex SQL queries for distributed data
   - Optimize Spark applications for performance

3. **Implement Banking Analytics**

   - Build fraud detection systems using ML algorithms
   - Perform customer segmentation and behavioral analysis
   - Create real-time analytics pipelines

4. **Design Data Integration Solutions**
   - Implement robust ETL processes
   - Handle schema evolution and data quality monitoring
   - Integrate multiple data sources effectively

## 🔧 Troubleshooting

### Common Issues

**Spark Session Issues:**

```python
# If you encounter memory issues
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

**Java Version Issues:**

```bash
# Check Java version
java -version
# Should show Java 8 or higher
```

**Memory Optimization:**

```bash
# Set environment variables
export SPARK_DRIVER_MEMORY=4g
export SPARK_EXECUTOR_MEMORY=2g
```

## 📞 Support

For technical support during the workshop:

- Check the troubleshooting section above
- Review Spark documentation: https://spark.apache.org/docs/latest/
- Ask questions during the hands-on sessions

## 📝 Notes

- All code examples are tested with Python 3.8+ and Spark 3.5
- Notebooks include detailed explanations and business context
- Each lab builds upon previous concepts progressively
- Real-world banking scenarios are used throughout

---

**Happy Learning! 🎓**
