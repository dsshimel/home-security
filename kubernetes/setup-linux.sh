# Install kubeadm, kubectl, and kubelet based on the instructions at the following link:
# https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl

sudo apt-get update

# apt-transport-https may be a dummy package; if so, you can skip that package
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# If the directory `/etc/apt/keyrings` does not exist, it should be created before the curl command
# Check if directory /etc/apt/keyrings exists
if [ ! -d "/etc/apt/keyrings" ]; then
  echo "Directory /etc/apt/keyrings does not exist"
  echo "Creating directory /etc/apt/keyrings"
  sudo mkdir -p -m 755 /etc/apt/keyrings
fi

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Enable the kubelet service before running kubeadm
sudo systemctl enable --now kubelet

# TODO: Finish the setup/startup script