# data_pipeline

## Some commands below to setup python 3 env
python3 -m venv data_pipeline_venv
source data_pipeline_venv/bin/activate
pip3 install pyarrow pandas matplotlib ipykernel notebook

## Some commands below to setup local Apache Spark 4.2 environment on WSL2
sudo apt install -y openjdk-21-jdk, Spark 4.0+ uses at least Java 17.0
curl -O https://archive.apache.org/dist/spark/spark-4.2.0/spark-4.2.0-bin-hadoop3.tgz, visit  https://archive.apache.org/dist/spark to see all versions
tar -xvzf spark-4.2.0-bin-hadoop3.tgz, to unpack the archive
sudo mv ./data_pipeline/spark-4.2.0-bin-hadoop3/* ./apache_spark/

Add below variables to bashrc
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export SPARK_HOME=/mnt/c/Users/david/apache_spark
export PATH=$SPARK_HOME/bin:$PATH

Run spark-shell in terminal, should start a scala REPL session if nothing goes wrong
Try access http://localhost:4040, which is the spark UI
