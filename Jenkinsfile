pipeline {
    agent any

    environment {
        SONAR_URL = 'http://localhost:9000'
        SONAR_TOKEN = 'sqa_4e13fd27c5304e8d574b23f0f28445775a441073'
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
                python3 -m pip install --upgrade pip
                python3 -m pip install -r app/requirements.txt
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installation des dépendances..."
                sh '''
                pip install --upgrade pip
                pip install -r app/requirements.txt
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
