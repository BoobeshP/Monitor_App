pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install OS Dependencies') {
            steps {
                sh '''
                sudo apt update
                sudo apt install -y python3.10-venv python3-pip
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv ${VENV}
                . ${VENV}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Health Check Test') {
            steps {
                sh '''
                . ${VENV}/bin/activate
                python -c "import app; print('App import successful')"
                '''
            }
        }

        stage('Package & Archive Application ✅') {
            steps {
                sh '''
                tar -czf monitoring-dashboard.tar.gz app.py templates requirements.txt
                ls -l monitoring-dashboard.tar.gz
                '''
                archiveArtifacts artifacts: 'monitoring-dashboard.tar.gz', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Monitoring Dashboard CI successful"
        }
        failure {
            echo "❌ Pipeline failed"
        }
        always {
            cleanWs()
        }
    }
}
