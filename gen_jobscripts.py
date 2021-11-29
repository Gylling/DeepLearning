types = ["plr"]
games = [
    "starpilot",
    "coinrun",
    "jumper"
]
error_functions = ["GAEMag", "OneStep", "GAE"]


for type in types:
    for game in games:
        for err in range(3):
            name = f"{type}-{game}-{error_functions[err]}"
            text = f"""
#!/bin/sh
mkdir logs/{name}

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J {name}
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/{name}/%J.out
#BSUB -e logs/{name}/%J.err

echo "Running {name}"
python3 {type}.py 1 {err} {game}"""
            with open(f"jobscripts/{name}.sh", "w") as f:
                f.write(text)