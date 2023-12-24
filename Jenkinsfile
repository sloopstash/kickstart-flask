pipeline {
  agent any
  parameters {
    choice(
      name:'test_environment',choices:['qab','qaa'],description:'Testing environment'
    )
  }
  environment {
    TEST_ENVIRONMENT=params.test_environment.toUpperCase()
  }
  stages {
    stage('CI: Download sources') {
      steps {
        sh(
          script:'git clone https://github.com/sloopstash/kickstart-docker.git kickstart-docker',
          returnStatus:true
        )
        sh(
          script:'git clone https://github.com/sloopstash/kickstart-ansible.git kickstart-ansible',
          returnStatus:true
        )
      }
    }
stage('CI: Sonarqube quality check') {
      when {branch 'feature'}
      steps {
      echo "sonar quality check is completed"
      }
    }
    stage('CI: Build OCI images') {
      steps {
        dir('kickstart-docker') {
          sh 'sudo docker image build -t sloopstash/base:v1.1.1 -f image/base/1.1.1/amazon-linux-2.dockerfile image/base/1.1.1/context'
          sh 'sudo docker image build -t sloopstash/nginx:v1.14.0 -f image/nginx/1.14.0/amazon-linux-2.dockerfile image/nginx/1.14.0/context'
          sh 'sudo docker image build -t sloopstash/python:v2.7 -f image/python/2.7/amazon-linux-2.dockerfile image/python/2.7/context'
          sh 'sudo docker image build -t sloopstash/redis:v4.0.9 -f image/redis/4.0.9/amazon-linux-2.dockerfile image/redis/4.0.9/context'
        }
      }
    }
    stage('CI: Bootstrap testing environment') {
       when{ branch 'qa'}
      steps {
        dir('kickstart-docker') {
          sh "sudo docker compose -f compose/crm.yml --env-file compose/${TEST_ENVIRONMENT}.env -p sloopstash-${params.test_environment}-crm up -d"
          sh "sudo docker container exec sloopstash-${params.test_environment}-crm-app-1 pip install pytest"
        }
      }
    }
    stage('CI: Execute test cases') {
       when{ branch 'qa'}
      environment {
        APP_SOURCE='/opt/app/source'
      }
      steps {
        sh "sudo docker container exec --workdir ${APP_SOURCE} sloopstash-${params.test_environment}-crm-app-1 pytest --junitxml=reports.xml script/test/main.py"
      }
      post {
        // always {
        //   junit 'reports.xml'
        // }
        success {
          input 'App testing has been successful. Do you want to proceed deployment in staging environment?'
        }
      }
    }
    stage('CD: Bootstrap staging environment') {
       when{ branch 'staging'}
      steps {
        dir('kickstart-ansible') {
          sh 'sudo docker compose -f docker/compose/crm.yml --env-file docker/compose/STG.env -p sloopstash-stg-crm up -d --scale app=3 --scale nginx=2'
        }
      }
    }
    stage('CD: Execute deployment') {
      when{ branch 'staging'}
      steps {
        dir('kickstart-ansible') {
          ansiblePlaybook(
            credentialsId:'ansible-node-ssh',
            playbook:'playbook/redis.yml',
            inventory:'inventory/stg',
            tags:'setup,configure,stop,start'
          )
          ansiblePlaybook(
            credentialsId:'ansible-node-ssh',
            playbook:'playbook/crm/app.yml',
            inventory:'inventory/stg',
            tags:'setup,update,configure,stop,start',
            limit:'sloopstash-stg-crm-app-1'
          )
          ansiblePlaybook(
            credentialsId:'ansible-node-ssh',
            playbook:'playbook/nginx.yml',
            inventory:'inventory/stg',
            tags:'setup,update,configure,stop,start',
            limit:'sloopstash-stg-crm-nginx-1'
          )
        }
      }
      post {
        success {
          input 'Deployment has been successful. Do you want to proceed deployment in production environment?'
        }
      }
    }
  }
  // post {
    // always {
    //   dir('kickstart-docker') {
    //     sh "sudo docker compose -f compose/crm.yml --env-file compose/${TEST_ENVIRONMENT}.env -p sloopstash-${params.test_environment}-crm down"
    //   }
    //   dir('kickstart-ansible') {
    //     sh 'sudo docker compose -f docker/compose/crm.yml --env-file docker/compose/STG.env -p sloopstash-stg-crm down'
    //   }
    //   emailext(
    //     subject:'Jenkins: ${env.JOB_NAME} - ${currentBuild.currentResult}',
    //     body:'${env.BUILD_NUMBER} ${env.JOB_NAME} execution ${currentBuild.currentResult}.\n Know more at ${env.BUILD_URL}.',
    //     recipientProviders:[[$class:'DevelopersRecipientProvider'],[$class:'RequesterRecipientProvider']]
    //   )
    // }
  //   success {
  //     cleanWs(
  //       deleteDirs:true,
  //       disableDeferredWipeout:true
  //     )
  //   }
  // }
}
