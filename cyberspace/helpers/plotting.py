import matplotlib.pyplot as plt

def plot_incidence_response_states(df):
        

    plt.figure(figsize=(10,6))

    ir_columns = [
        "Normal",
        "Detected",
        "Contained",
        "Eradicated",
        "Recovered",
    ]

    for col in ir_columns:
        plt.plot(df.index, df[col], linewidth=2, label=col)

    plt.title("Incident Response State Distribution")
    plt.xlabel("Simulation Step")
    plt.ylabel("Number of Personas")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_security_metrics(df):
    plt.figure(figsize=(10,6))

    security_columns = [
        "Compromised",
        "Discovered",
        "Persistence",
        "C2",
        "DataCollected",
        "Monitoring",
    ]

    for col in security_columns:
        plt.plot(df.index, df[col], linewidth=2, label=col)

    plt.title("Cybersecurity Metrics Over Time")
    plt.xlabel("Simulation Step")
    plt.ylabel("Number of Personas")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

def individual_plots(df):

    metrics = [
        "Compromised",
        "Discovered",
        "Persistence",
        "C2",
        "DataCollected",
        "Monitoring",
        "Normal",
        "Detected",
        "Contained",
        "Eradicated",
        "Recovered",
    ]

    for metric in metrics:

        plt.figure(figsize=(7,4))

        plt.plot(df.index, df[metric], linewidth=2)

        plt.title(metric)
        plt.xlabel("Simulation Step")
        plt.ylabel("Number of Personas")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

def dashboard(df):
    fig, axes = plt.subplots(3, 4, figsize=(16, 10))

    metrics = [
        "Compromised",
        "Discovered",
        "Persistence",
        "C2",
        "DataCollected",
        "Monitoring",
        "Normal",
        "Detected",
        "Contained",
        "Eradicated",
        "Recovered",
    ]

    axes = axes.flatten()

    for i, metric in enumerate(metrics):
        axes[i].plot(df.index, df[metric], linewidth=2)
        axes[i].set_title(metric)
        axes[i].set_xlabel("Step")
        axes[i].set_ylabel("Count")
        axes[i].grid(True)

    # Hide unused subplot (12th)
    for j in range(len(metrics), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()