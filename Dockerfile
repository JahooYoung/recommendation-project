FROM centos:8
LABEL Yangjh  jahoo@pku.edu.cn

LABEL Discription="Movie Recommendation Project" version="1.0"

# 安装必备的软件包
RUN yum -y install dnf yum-utils net-tools openssh-server openssh-clients \
        which less python3 python3-devel gcc zip
COPY ./configs/repos/* /etc/yum.repos.d/
RUN yum install -y nginx mongodb-org
RUN dnf module install -y nodejs:12
RUN yum clean all

RUN ln /usr/bin/python3 /usr/bin/python
RUN npm install -g yarn

EXPOSE 22
EXPOSE 8000
EXPOSE 8080

# 配置SSH免密登录
RUN ssh-keygen -q -t rsa -b 2048 -f /etc/ssh/ssh_host_rsa_key -N ''
RUN ssh-keygen -q -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N ''
RUN ssh-keygen -q -t dsa -f /etc/ssh/ssh_host_ed25519_key  -N ''
RUN ssh-keygen -f /root/.ssh/id_rsa -N ''
RUN touch /root/.ssh/authorized_keys
RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
RUN echo "root:ss123jj4j" | chpasswd
COPY ./configs/ssh_config /etc/ssh/ssh_config

# JDK 增加JAVA_HOME环境变量
ADD ./tools/jdk-8u271-linux-x64.tar.gz /usr/local/
ENV JAVA_HOME /usr/local/jdk1.8.0_271
ENV JRE_HOME=$JAVA_HOME/jre
ENV CLASSPATH .:$JAVA_HOME/lib:$JRE_HOME/lib
# ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

# Hadoop
ADD ./tools/hadoop-3.2.1.tar.gz /usr/local
ENV HADOOP_HOME /usr/local/hadoop-3.2.1
COPY ./configs/hadoop/* $HADOOP_HOME/etc/hadoop/
COPY ./tools/sbin/* $HADOOP_HOME/sbin/
RUN mkdir -p /data/hadoop/dfs/{data,name,journal} && \
    mkdir -p /data/hadoop/tmp && \
    mkdir -p $HADOOP_HOME/logs
# RUN chmod 700 $HADOOP_HOME/sbin/*.sh
# RUN chmod 700 $HADOOP_HOME/*.sh $HADOOP_HOME/sbin/*.sh

# Spark
# ADD ./tools/spark-3.0.1-bin-hadoop3.2.tgz /usr/local
# ENV SPARK_HOME /usr/local/spark-3.0.1-bin-hadoop3.2
ADD ./tools/spark-2.4.7-bin-hadoop2.7.tgz /usr/local
ENV SPARK_HOME /usr/local/spark-2.4.7-bin-hadoop2.7
ENV HADOOP_CONF_DIR $HADOOP_HOME/etc/hadoop
COPY ./tools/*.jar $SPARK_HOME/jars/

# Zookeeper
ADD ./tools/apache-zookeeper-3.6.2-bin.tar.gz /usr/local
ENV ZOOKEEPER_HOME /usr/local/apache-zookeeper-3.6.2-bin
COPY ./configs/zoo.cfg $ZOOKEEPER_HOME/conf/zoo.cfg
RUN mkdir -p /usr/local/apache-zookeeper-3.6.2-bin/{data,logs}

# Scala
ADD ./tools/scala-2.11.12.tgz /usr/local
ENV SCALA_HOME /usr/local/scala-2.11.12

#将环境变量添加到系统变量中
ENV PATH $SCALA_HOME/bin:$ZOOKEEPER_HOME/bin:$SPARK_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin:$PATH

# MongoDB
RUN mkdir -p /data/mongodb/db
COPY ./configs/mongodb.conf /data/mongodb/

# nginx
COPY ./configs/nginx.conf /etc/nginx/

ENV PROJECT_ROOT /root/rcmd_project

# 数据集等文件
RUN mkdir -p $PROJECT_ROOT/data
COPY ./ml-latest-small.zip /tmp/
RUN unzip /tmp/ml-latest-small.zip -d $PROJECT_ROOT/data/
RUN rm /tmp/ml-latest-small.zip

# 前端和后端文件
RUN mkdir -p $PROJECT_ROOT
COPY ./frontend $PROJECT_ROOT/frontend
COPY ./backend $PROJECT_ROOT/backend
COPY ./requirements.txt $PROJECT_ROOT/

# 启动脚本
COPY ./scripts/* /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh $HADOOP_HOME/sbin/*.sh

#启动容器时执行的脚本文件
# CMD ["/usr/sbin/sshd","-D"]
