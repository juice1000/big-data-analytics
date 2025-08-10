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
