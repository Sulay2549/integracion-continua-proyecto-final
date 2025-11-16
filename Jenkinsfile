pipeline {
    agent any 

    stages {
        stage('Build Frontend') {
            agent {
                docker { image 'node:lts-alpine' }
            }
            steps {
                dir('frontend') {
                    sh 'npm cache clean --force'
                    sh 'npm install --prefix . --cache ./.npm-cache'
                    sh 'npm run build -- --configuration=production'
                }
            }
        }
        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'python -m venv venv'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Building and deploying Docker images...'
                script {
                    // Construir y desplegar Frontend Docker
                    dir('Frontend') {
                        sh 'docker build -t frontend-app .'
                    }
                    // Construir y desplegar Backend Docker
                    dir('Backend') {
                        sh 'docker build -t backend-app .'
                    }
                    // Desplegar (ejecutar) ambas imágenes
                    sh 'docker-compose down || true' // Detener contenedores existentes si los hay
                    sh 'docker-compose up -d' // Iniciar contenedores en modo detached
                }
            }
        }
    }
}
