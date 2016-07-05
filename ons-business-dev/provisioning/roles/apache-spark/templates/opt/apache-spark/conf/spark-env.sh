export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:{{apache_hadoop_home}}/lib/native

export HADOOP_CONF_DIR={{apache_hadoop_home}}/etc/hadoop

export SPARK_DIST_CLASSPATH=$({{apache_hadoop_home}}/bin/hadoop classpath)
