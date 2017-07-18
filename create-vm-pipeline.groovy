pipeline {
    agent any
    parameters {
        string(name: 'DOM_CNT', defaultValue: '1', description: 'The count of domains which have to be created.')
        string(name: 'DOM_NAME', defaultValue: 'node', description: 'Name prefix for domain/s is/are going to be created.')
        string(name: 'DOM_RAM', defaultValue: '512', description: 'RAM size in MB for the domain.')
        string(name: 'DOM_DISK_SIZE', defaultValue: '5', description: 'Disk size in GB for the domain.')
        string(name: 'DOM_CPU_CNT', defaultValue: '1', description: 'The count of available CPU inside the domain.')
        string(name: 'DOM_OS_IMG', defaultValue: '', description: 'The path or URL where OS image is located.')
        string(name: 'DOM_STORE_PATH', defaultValue: '/var/lib/libvirt/images', description: 'The place where domain image will be created.')
    }
    stages {
        stage('Build') {
            steps {
                echo "Count of Domains: ${params.DOM_CNT}"
                println "Prefix name is: ${params.DOM_NAME}" 
                script {
                    for (int i = 1; i <= params.DOM_CNT.toInteger(); ++i) {
                        echo "Domain with name ${params.DOM_NAME}${i} has been created"
                        sh "/vm/scripts/create_vm.sh ${params.DOM_NAME}${i}"
                    }
                }
            }
        }
    }
}
