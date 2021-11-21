# UdaConnect - Conference Connect Project

### Technologies Used
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
* [PostgreSQL](https://www.postgresql.org/) - Relational database
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster
* [Apatche-Kafka](https://kafka.apache.org/) - Open-source distributed message streaming platform.
* [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) - Popular Architecture to create APIs
* [grpc](https://grpc.io/) - Remote procedure calls to enable faster queries over http2.

### Steps of execution

#### 1. Vagrant operations -
Start Vagrant
```bash
$ vagrant up
```

SSH into vagrant to copy the kubernetes config file
```bash
$ vagrant ssh
```

Copy the kube config file that is shown using below command
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml
```

Exit from vagrant using `exit` command

#### 2. Set up Kubernetes

Go to folder `~/.kube/config`.

Create a new `k3s.yaml` file and paste the paste the copied contents.

Run the `kubectl get po` to check if the kubernetes is working fine.

#### 3. Start the application

Run the following commands from project root directory to start the application -

1. `kubectl apply -f deployment/` - Apply deployment folder config and start all the k8s pods
2. `kubectl get pods` - Get all pods created
3. `sh scripts/run_db_command.sh <POD_NAME>` - Seed the database. Replace POD_NAME with the postgres pod name obtained above in point 2.
4. Go to url in your browser to open the application - `http://localhost:30000/`
