import pandas as pd, matplotlib.pyplot as plt, json

def read_jsonl(path) -> pd.DataFrame:
    lines = []
    with open(path, "r") as f:
        lines = f.read().splitlines()
    line_dicts = [json.loads(line) for line in lines]
    return pd.DataFrame(line_dicts)

if __name__ == "__main__":
    data = read_jsonl("data/example_history.jsonl")
    
    plt.title("Progresso por geração.")
    
    plt.plot("generation", "best_fitness", data=data, label="melhor progresso")
    plt.xlabel("geração"); plt.ylabel("fitness")
    
    plt.plot("generation", "average_fitness", linestyle="--", data=data, label="progresso médio")
    plt.xlabel("geração"); plt.ylabel("fitness")
    
    plt.legend()    
    plt.show()