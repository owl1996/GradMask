import subprocess
from concurrent.futures import ThreadPoolExecutor
import itertools
import os

# Liste de tes commandes sous forme de strings
baseline_train_epochs = {
    "cifar10": 100,
    "cifar100": 100,
    "tiny-imagenet": 1,
    "svhn": 200,
    "imagenet": 90,
    "imagenet100": 90
}

base_script = "python -u mlflow_forget.py"

dataset = ["cifar10", "cifar100"]
unlearn = ["NGPlus", "mask_NGPlus", "mix_NGPlus", "SRL", "mask_SRL", "mix_SRL", "SalUn", "FT"]
unlearn_epochs = ["1", "2", "3", "5", "10"]
beta = ["0.85", "0.9", "0.95"]
quantile = ["0.3", "0.4", "0.5", "0.6"]
# archs = ["vgg16_bn", "resnet18"]
archs = ["resnet18", "vgg16_bn"]
seeds = ["0", "1", "2", "3", "4"]

commands = [base_script
            + " --save_dir ./results/" + _dataset
            + " --mask ./results/" + _dataset + "/" + _seed + _arch + "_ep" + str(baseline_train_epochs[_dataset]) + "model_SA_best.pth.tar"
            + " --unlearn " + _unlearn
            + " --unlearn_epochs " + _unlearn_epochs
            + " --unlearn_lr 0.1"
            + " --data ./data"
            + " --dataset " + _dataset
            + " --seed " + _seed
            + " --arch " + _arch
            + " --epochs " + str(baseline_train_epochs[_dataset])
            for (_dataset, _unlearn, _unlearn_epochs, _seed, _arch) in itertools.product(dataset, unlearn, unlearn_epochs, seeds, archs) 
]

new_commands = []
for command in commands:
    if ("SRL" in command) or ("SalUn" in command) or ("NGPlus" in command):
        commands.remove(command)
        for _beta in beta:
            new_command = command + " --beta " + _beta
            if ("SalUn" in command) or ("mix" in command):
                for _quantile in quantile:
                    new_command_ = new_command + " --quantile " + _quantile
                    new_commands.append(new_command_)
            else:
                new_commands.append(new_command)
    else:
        new_commands.append(command)
    
# print(new_commands)

base_commands = ["python -u main_baseline.py"
            + " --save_dir ./results/" + _dataset
            + " --arch " + _arch
            + " --data ./data"
            + " --dataset " + _dataset
            + " --seed " + _seed
            + " --epochs " + str(baseline_train_epochs[_dataset])
            for (_arch, _dataset, _seed) in itertools.product(archs, dataset, seeds)]

ideal_commands = ["python -u mlflow_forget.py"
            + " --save_dir ./results/" + _dataset
            + " --unlearn ideal"
            + " --unlearn_epochs " + str(baseline_train_epochs[_dataset])
            + " --unlearn_lr 0.1"
            + " --data ./data"
            + " --dataset " + _dataset
            + " --seed " + _seed
            + " --arch " + _arch
            + " --epochs " + str(baseline_train_epochs[_dataset])
            for (_arch, _dataset, _seed) in itertools.product(archs, dataset, seeds)
            if "ideal" + "_uep" + str(baseline_train_epochs[_dataset]) + "_s" + _seed + _arch + "_ep" + str(baseline_train_epochs[_dataset]) + "checkpoint.pth.tar" not in os.listdir("./results/" + _dataset)]

commands = base_commands + ideal_commands + new_commands

# print(ideal_commands)

def run_command(cmd):
    """Exécute une commande et gère les erreurs"""
    try:
        print(f"Démarrage: {cmd}")
        result = subprocess.run(
            cmd.split(), 
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Succès: {cmd}\nSortie:\n{result.stdout[:200]}...")  # Affiche les 200 premiers caractères
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur dans {cmd}\nCode: {e.returncode}\nErreur: {e.stderr[:200]}...")
        return False
    except Exception as e:
        print(f"Exception inattendue: {str(e)}")
        return False

# Exécution parallèle (ajuster max_workers selon ton CPU)
with ThreadPoolExecutor(max_workers=1) as executor:
    results = executor.map(run_command, commands)

# Vérification finale
if all(results):
    print(f"\nToutes les {len(commands)} commandes ont réussi !")
else:
    print("\nCertaines commandes ont échoué, vérifie les logs ci-dessus.")
