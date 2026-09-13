pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'python test_image_analyzer.py'
            }
        }

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