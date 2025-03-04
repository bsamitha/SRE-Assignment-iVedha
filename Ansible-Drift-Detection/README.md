🚀 NGINX Deployment with HTTPS using Ansible
This Ansible playbook helps to detect and optionally remediate infrastructure drift by checking if installed software versions on remote servers match the expected baseline.

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
ansible-playbook -i hosts.yml main.yml --ask-pass -e env=non-prod -e software=python3 -e version=3.8.10

⚙️ Define a CI/CD pipeline to run the Ansible playbook