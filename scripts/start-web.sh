#!/bin/bash

if [[ $NODE_ID == "1" ]]; then
    echo "==== init mongodb ===="
    # echo -e "use admin\nrs.initiate({_id: 'mongorepl', members:[{_id: 0, host: 'node1:27017'}]})" | mongo -host node1:27017
    # echo 'db.createUser({user: "admin", pwd: "123456", roles: [{ role: "userAdminAnyDatabase", db: "admin"}]})' | mongo -host mongorepl/node1:27017
    echo -e "use admin\nrs.initiate({_id: 'mongorepl', members:[{_id: 0, host: 'node1:27017'}, {_id: 1, host: 'node2:27017'}, {_id: 2, host: 'node3:27017'}, {_id: 3, host: 'node4:27017'}]})" | mongo -host node1:27017
    echo 'db.createUser({user: "admin", pwd: "123456jj4j", roles: [{ role: "userAdminAnyDatabase", db: "admin"}]})' | mongo -host mongorepl/node1:27017,node2:27017,node3:27017,node4:27017
fi

if [[ $NODE_ID == "1" ]]; then
    echo "==== update spark files and datasets ===="
    (cd $SPARK_HOME/jars/; zip -q /tmp/spark_jars.zip *)
    hdfs dfs -mkdir -p /home
    hdfs dfs -put /tmp/spark_jars.zip /home/
    # hdfs dfs -put /usr/local/mongo-spark-connector_2.12-3.0.0.jar /home/hadoop/spark_jars/
    rm /tmp/spark_jars.zip

    hdfs dfs -put $PROJECT_ROOT/data/$DATASET/ratings.csv /home/
fi

if [[ $NODE_ID == "1" ]]; then
    echo "==== build & start backend ===="
    cd $PROJECT_ROOT
    python -m venv venv
    source venv/bin/activate
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    pip install wheel
    pip install -r requirements.txt

    cd $PROJECT_ROOT/backend
    rm -rf movie_rcmd/migrations/0*
    python manage.py makemigrations
    python manage.py migrate
    python manage.py import ../data/$DATASET
    uwsgi --ini uwsgi.ini

    echo "==== start crontab ===="
    crond
    echo -e 'i*/10   *    *    *    *    bash /root/rcmd_project/backend/run_rcmd.sh >/tmp/run_rcmd.log 2>&1\x1B:wq' | crontab -e

    echo "==== start rcmd_stats ===="
    nohup bash run_stats.sh &
fi

if [[ $NODE_ID == "1" ]]; then
    echo "==== build frontend ===="
    cd $PROJECT_ROOT/frontend
    YARN=/usr/local/lib/node_modules/yarn/bin/yarn
    $YARN config set registry 'https://registry.npm.taobao.org/'
    $YARN
    $YARN build
fi

if [[ $NODE_ID == "1" ]]; then
    echo "==== start nginx ===="
    nginx
fi
