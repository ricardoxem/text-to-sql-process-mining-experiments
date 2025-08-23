import matplotlib.pyplot as plt

def plot_and_save_graph_results(data, data1, data2, data3, file, categories, x_pos, x_positions, ax_text_pos, ax1_text_pos, ay_ticks, ay_ticks1, hspace, legend_anchor, fig_size, metric_label):
    fig, (ax, ax1, ax2, ax3) = plt.subplots(4,1, figsize=fig_size)
    
    categories_qtd = len(categories)
    labels = ['GPT-3.5 Turbo - OpenAI Repr.', 'GPT-3.5 Turbo - Code Repr.', 
              'Gemini-1.0 - OpenAI Repr.', 'Gemini-1.0 - Code Repr.',
              'Llama3-8B - OpenAI Repr.', 'Llama3-8B - Code Repr.']

    colors = ['#66BB6A', '#4CAF50',  # Vibrant Green, Medium Green
              '#FFA726', '#FF9800',  # Vibrant Orange, Medium Orange
              '#42A5F5', '#2196F3']  # Vibrant Blue, Medium Blue
    bar_width = 0.3
    
    colors = colors * categories_qtd
        
    # Create first bar chart
    #ax.bar(x_pos, data, width=bar_width, color=colors, label=labels*categories_qtd)
    
    # Plot bars
    bars = []
    for i, category in enumerate(labels*categories_qtd):
        bar = ax.bar(x_pos[i], data[i], width=bar_width, color=colors[i])
        bars.append(bar)
    
    ax.grid(color='#D3D3D3', linestyle='--', linewidth=0.15)

    for i, counts, in enumerate(data):
        ax.text(x_pos[i], data[i] + 2, counts, ha='center', fontsize=8)

    # Set y-axis control ticks
    ax.set_yticks(ay_ticks)
    ax.tick_params(axis='y', labelsize=20)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(categories, fontsize=20)

    # Add title and labels
    # Add labels and title
    ax.set_ylabel(metric_label, fontsize=20)
    ax.text(0, ax_text_pos, "zero-shot", fontsize=20,  weight='bold')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


    # Add legend
    ax.legend(bars, ncol=3, bbox_to_anchor=legend_anchor, frameon=False, labels=labels, fontsize=16)
    
    # Create second bar chart
    ax1.bar(x_pos, data1, width=bar_width, color=colors)
    ax1.grid(color='#D3D3D3', linestyle='--', linewidth=0.15)

    for i, counts, in enumerate(data1):
        ax1.text(x_pos[i], data1[i] + 2, counts, ha='center', fontsize=8)
    
    # Set y-axis control ticks
    ax1.set_yticks(ay_ticks1)
    ax1.tick_params(axis='y', labelsize=20)
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(categories, fontsize=20)

    # Add title and labels
    # Add labels and title
    ax1.set_ylabel(metric_label, fontsize=20)
    ax1.text(0, ax1_text_pos, "one-shot", fontsize=20,  weight='bold')

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)  
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)

    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.subplots_adjust(hspace)
    plt.savefig(file, format='png', bbox_inches='tight')

    # Create third bar chart
    ax2.bar(x_pos, data2, width=bar_width, color=colors)
    ax2.grid(color='#D3D3D3', linestyle='--', linewidth=0.15)

    for i, counts, in enumerate(data2):
        ax2.text(x_pos[i], data2[i] + 2, counts, ha='center', fontsize=8)
    
    # Set y-axis control ticks
    ax2.set_yticks(ay_ticks1)
    ax2.tick_params(axis='y', labelsize=20)
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(categories, fontsize=20)

    # Add title and labels
    # Add labels and title
    ax2.set_ylabel(metric_label, fontsize=20)
    ax2.text(0, ax1_text_pos, "three-shot", fontsize=20,  weight='bold')

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)  
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)

    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.subplots_adjust(hspace)
    plt.savefig(file, format='png', bbox_inches='tight')

    # Create four bar chart
    ax3.bar(x_pos, data3, width=bar_width, color=colors)
    ax3.grid(color='#D3D3D3', linestyle='--', linewidth=0.15)

    for i, counts, in enumerate(data3):
        ax3.text(x_pos[i], data3[i] + 2, counts, ha='center', fontsize=8)
    
    # Set y-axis control ticks
    ax3.set_yticks(ay_ticks1)
    ax3.tick_params(axis='y', labelsize=20)
    ax3.set_xticks(x_positions)
    ax3.set_xticklabels(categories, fontsize=20)

    # Add title and labels
    # Add labels and title
    ax3.set_ylabel(metric_label, fontsize=20)
    ax3.text(0, ax1_text_pos, "five-shot", fontsize=20,  weight='bold')

    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)  
    ax3.spines['bottom'].set_visible(False)
    ax3.spines['left'].set_visible(False)

    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.subplots_adjust(hspace)
    plt.savefig(file, format='png', bbox_inches='tight')

def plot_and_save_graph_results_by_model(data, file):
       
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))  # 1 row, 4 columns
    fig.text(0.25, 1.05, 'Exact Match Accuracy (EM)', ha='center', va='center', fontsize=16)
    fig.text(0.75, 1.05, 'Execution Accuracy (EX)', ha='center', va='center', fontsize=16)

    x_values = [0, 1, 3, 5]    
    # Plot for EM data
    for key, value in data['EM']['PT'].items():
        axes[0].plot(x_values, value, marker='o', label=key)

    for key, value in data['EM']['EN'].items():
        axes[1].plot(x_values, value, marker='o', label=key)

    # Plot for EX data
    for key, value in data['EX']['PT'].items():
        axes[2].plot(x_values, value, marker='o', label=key)

    for key, value in data['EX']['EN'].items():
        axes[3].plot(x_values, value, marker='o', label=key)

    # Config default
    axes[0].set_title('Portuguese')
    axes[1].set_title('English')
    axes[2].set_title('Portuguese')
    axes[3].set_title('English')
    for i in range(0, 4):
        axes[i].set_yticks(range(0, 110, 20))
        axes[i].set_xlabel('Shots', fontsize=12)
        axes[i].set_xticks([0, 1, 3, 5])
        axes[i].tick_params(axis='y', labelsize=12)
        axes[i].tick_params(axis='x', labelsize=12)
        axes[i].grid(color='gray', linestyle='--', linewidth=0.5)

    bars = []
    axes[0].set_ylabel('Percentage (%)', fontsize=12)
    #axes[1][0].set_ylabel('Percentage (%)', fontsize=12)
    #legend_anchor = (0.0, 0.0)
    #axes[1].legend(bars, ncol=3, loc='upper center', bbox_to_anchor=(1.0, 1.15), frameon=False, 
    #    labels=data['EX']['PT'].keys(), fontsize=10)

    # ---- Central legend for the whole figure ----
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc='lower center',        # place legend at the center-bottom
        bbox_to_anchor=(0.5, 1.0),  # adjust position (x=0.5 center, y=-0.05 below plots)
        ncol=4,                    # number of columns in legend
        frameon=False,
        fontsize=10
    )
  

    plt.tight_layout()  # Adjust layout to prevent overlapping
    #plt.subplots_adjust(hspace=0.4) 
    plt.savefig(file, format='png', bbox_inches='tight', dpi=300)

def plot_and_save_graph_results_no_hardness(data, file):
       
    fig, axes = plt.subplots(1, 2, figsize=(10, 6))  # 1 row, 2 columns
    fig.text(0.22, 0.89, 'Execution Accuracy (EX)', ha='center', va='center', fontsize=16)

    x_values = [0, 1, 3, 5]    
    
    # Plot for EX data
    for key, value in data['EX']['PT'].items():
        axes[0].plot(x_values, value, marker='o', label=key)

    for key, value in data['EX']['EN'].items():
        axes[1].plot(x_values, value, marker='o', label=key)

    # Config default
    axes[0].set_title('Portuguese')
    axes[1].set_title('English')
    for i in range(0, 2):
        axes[i].set_yticks(range(0, 110, 20))
        axes[i].set_xlabel('Shots', fontsize=12)
        axes[i].set_xticks([0, 1, 3, 5])
        axes[i].tick_params(axis='y', labelsize=12)
        axes[i].tick_params(axis='x', labelsize=12)
        axes[i].grid(color='gray', linestyle='--', linewidth=0.5)

    bars = []
    axes[0].set_ylabel('Percentage (%)', fontsize=12)
    axes[1].legend(bars, ncol=3, bbox_to_anchor=(1.0, 1.35), frameon=False, 
        labels=data['EX']['PT'].keys(), fontsize=8)
  

    plt.tight_layout()  # Adjust layout to prevent overlapping
    plt.savefig(file, format='png', bbox_inches='tight', dpi=300)
