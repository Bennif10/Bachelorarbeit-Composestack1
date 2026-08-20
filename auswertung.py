import csv

data = {}

with open('neuvector_load.csv', mode='r') as f:
    reader = csv.reader(f)
    for row in reader:
        if not row or len(row) < 5:
            continue
        
        container = row[1].strip()
        try:
            cpu = float(row[2].replace('%', '').strip())
            mem_pct = float(row[4].replace('%', '').strip())
        except ValueError:
            continue
        
        if container not in data:
            data[container] = {'cpu': [], 'mem': []}
        
        data[container]['cpu'].append(cpu)
        data[container]['mem'].append(mem_pct)

# Tabellenkopf mit ausreichend Spaltenbreite (30 Zeichen für Name)
print(f"{'Container':<30} | {'Avg CPU %':<10} | {'Max CPU %':<10} | {'Avg Mem %':<10} | {'Max Mem %':<10}")
print("-" * 80)

for container, metrics in data.items():
    avg_cpu = sum(metrics['cpu']) / len(metrics['cpu']) if metrics['cpu'] else 0
    max_cpu = max(metrics['cpu']) if metrics['cpu'] else 0
    avg_mem = sum(metrics['mem']) / len(metrics['mem']) if metrics['mem'] else 0
    max_mem = max(metrics['mem']) if metrics['mem'] else 0
    
    print(f"{container:<30} | {avg_cpu:<10.2f} | {max_cpu:<10.2f} | {avg_mem:<10.2f} | {max_mem:<10.2f}")
