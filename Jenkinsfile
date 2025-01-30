#!groovy
pipeline {
    agent any

    stages {
        stage('Cleanup') {
            steps {
                echo 'Cleaning up existing Containers and Images'
                sh 'docker rm -f $(docker ps -aq) || true'
                sh 'docker rmi -f $(docker images -q) || true'  
                sh 'docker ps -a'
                sh 'docker images'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t pyapp-image .'  
                sh 'docker network create jenkinsnetwork || true' 
            }
        }
        stage('Run') {
            steps {
                sh 'docker run -d --name pythonapp --network jenkinsnetwork pyapp-image'
                sh 'docker run -d --name nginx --network jenkinsnetwork -p 80:80 -v ${WORKSPACE}/nginx.conf:/etc/nginx/nginx.conf nginx:latest'
            }
        }
        stage('Test') {
            steps {
                sh 'curl -f http://localhost:5500 || echo "Test failed"' 
                sh 'curl -f http://localhost:80 || echo "Nginx test failed"'
            }
        }
    }
}

