pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "🔹 Building branch: ${env.BRANCH_NAME}"
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

        stage('Branch Specific Validation') {
            steps {
                sh '''
                echo "Running branch-specific checks..."

                if [ "${BRANCH_NAME}" = "feature_Monitor" ]; then
                    echo "✅ feature_Monitor branch detected"
                    test -f monitor_utils.py
                    test -f FEATURE_MONITOR.md
                else
                    echo "✅ main branch detected – skipping feature checks"
                fi
                '''
            }
        }

        stage('Package & Archive') {
            steps {
                sh '''
                tar -czf monitoring-dashboard-${BRANCH_NAME}.tar.gz app.py templates requirements.txt *.py *.md || true
                ls -l
                '''
                archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
