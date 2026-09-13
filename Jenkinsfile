pipeline {
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
                bat 'docker push prasheetha06/fake-news-bilstm:latest'
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