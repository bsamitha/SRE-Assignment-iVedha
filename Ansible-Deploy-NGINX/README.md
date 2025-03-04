🚀 NGINX Deployment with HTTPS using Ansible
This project contains an Ansible playbook that automates the deployment of an NGINX web server on an Ubuntu server, 
configures HTTPS using a self-signed SSL certificate, and ensures the service is set to restart automatically if it crashes.

✅ Requirements
Ansible installed on your local or source machine.
SSH access to the target Ubuntu server.

⚙️ Inventory Configuration (hosts.yml)
Define your target servers
🔄 Replace server_ip with the actual IP address of your server with respective env.

🚀 How to Run
Install Ansible (if not already installed):
sudo apt update
sudo apt install ansible -y

Run the playbook:
ansible-playbook -i hosts.yml main.yml --ask-pass -e env=non-prod

⚙️ Define a CI/CD pipeline to run the Ansible playbook