pipeline {
    agent any

    environment {
        SONAR_URL = 'http://localhost:9000'
        SONAR_TOKEN = 'sqa_0efceaee176c2f4597209d9290c145bb473d8c9c'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Clonage du dépôt..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installation des dépendances..."
                sh '''
                python3 -m venv ./app/
                ls ./app/bin/
                pip3 install -r app/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Exécution des tests unitaires..."
                sh '''
                cd app
                pytest --junitxml=results.xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo "Analyse statique avec SonarQube..."
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=secure-project \
                      -Dsonar.sources=app \
                      -Dsonar.host.url=$SONAR_URL \
                      -Dsonar.login=$SONAR_TOKEN
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo "Vérification des résultats de l'analyse..."
                script {
                    def qualityGate = waitForQualityGate()
                    if (qualityGate.status != 'OK') {
                        error "Quality Gate non validé. Analyse échouée."
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Archivage des résultats de tests..."
            archiveArtifacts artifacts: '**/results.xml', allowEmptyArchive: true
            junit 'app/results.xml'
        }
    }
}
