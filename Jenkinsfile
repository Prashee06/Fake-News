pipeline {

    environment {
        KUBECONFIG = 'C:\\ProgramData\\Jenkins\\.kube\\config'
    }

    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t fake-news-bilstm .'
            }
        }

        stage('Tag Docker Image') {
            steps {
                bat 'docker tag fake-news-bilstm prasheetha06/fake-news-bilstm:latest'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    bat '''
                        echo %DOCKER_PASSWORD% | docker login -u %DOCKER_USERNAME% --password-stdin
                        docker push prasheetha06/fake-news-bilstm:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Check Kubernetes') {
            steps {
                bat 'kubectl config current-context'
                bat 'kubectl get nodes'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Fake News Detection CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}