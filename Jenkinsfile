pipeline {
    agent any 

    stages {
        stage('Build Frontend') {
            agent {
                docker { image 'node:lts-alpine' }
            }
            steps {
                dir('frontend') {
                    sh 'rm -rf node_modules package-lock.json'
                    sh 'npm cache clean --force'
                    sh 'npm install --prefix . --cache ./.npm-cache'
                    sh 'npm run build -- --configuration=production'
                }
            }
        }
        stage('Build Backend') {
            agent {
                docker { image 'python:3.9-slim-buster' }
            }
            steps {
                dir('backend') {
                    sh 'python -m venv venv'
                    sh '. venv/bin/activate && pip install -r requirements.txt && pip install -r requirements-dev.txt'
                }
            }
        }
        stage('Test Backend') {
            agent {
                docker { image 'python:3.9-slim-buster' }
            }
            steps {
                dir('backend') {
                    sh '. venv/bin/activate && python -m pytest -v'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d --build'
            }
        }
    }
}
