pipeline {
    agent any
    parameters {
        string(name: 'VM_CNT', defaultValue: '1', description: 'The count of VMs which have to be created.')
        string(name: 'VM_NAME', defaultValue: 'node', description: 'Name prefix for VM node/s is/are going to be created.')
        string(name: 'VM_RAM', defaultValue: '512', description: 'RAM size in MB for the VM.')
        string(name: 'VM_DISK_SIZE', defaultValue: '5', description: 'Disk size in GB for the VM.')
        string(name: 'VM_CPU_CNT', defaultValue: '1', description: 'The count of available CPU inside the node.')
        string(name: 'VM_OS_IMG', defaultValue: '', description: 'The path or URL where OS image is located.')
        string(name: 'VM_STORE_PATH', defaultValue: '/var/lib/libvirt/images', description: 'The the where VM image will be created.')
    }
    stages {
        stage('Build') {
            steps {
                echo "Count of VM: ${params.VM_CNT}"
                println "Prefix name is: ${params.VM_NAME}" 
                script {
                    for (int i = 1; i <= params.VM_CNT.toInteger(); ++i) {
                        echo "VM node with name ${params.VM_NAME}${i} has been created"
                        sh "/vm/scripts/create_vm.sh ${params.VM_NAME}${i}"
                    }
                }
            }
        }
    }
}
