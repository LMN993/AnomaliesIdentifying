import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import re


# Функция для группировки файлов по числам в названиях
def group_files_by_number(data):
    file_groups = defaultdict(lambda: {"not_black_hole": [], "black_hole": []})

    for row in data:
        file_name, sender_receiver_id, packet_count = row
        number = int(re.search(r'\d+', file_name).group())

        if "not_black_hole" in file_name:
            file_groups[number]["not_black_hole"].append((sender_receiver_id, int(packet_count)))
        elif "black_hole" in file_name:
            file_groups[number]["black_hole"].append((sender_receiver_id, int(packet_count)))

    return file_groups


# Чтение данных из CSV-файла
filename = "results.csv"
with open(filename, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    data = [row for row in reader]

file_groups = group_files_by_number(data)

# Построение и отображение объединенных графиков с двумя столбцами разных цветов
for number, file_group in file_groups.items():
    fig, ax = plt.subplots(figsize=(16, 10))
    width = 0.4
    offset = width

    all_sender_receiver_ids = set()
    for j, (file_type, file_data) in enumerate(file_group.items()):
        if file_data:
            sender_receiver_ids, packet_counts = zip(*file_data)
            all_sender_receiver_ids.update(sender_receiver_ids)
    all_sender_receiver_ids = sorted(list(all_sender_receiver_ids))

    for j, (file_type, file_data) in enumerate(file_group.items()):
        if file_data:
            sender_receiver_ids, packet_counts = zip(*file_data)
            d = {}
            for k in range(len(sender_receiver_ids)):
                d[sender_receiver_ids[k]] = packet_counts[k]
            for s in all_sender_receiver_ids:
                if s not in d.keys():
                    d[s] = 0
            pc = [d[s] for s in all_sender_receiver_ids]
            x = [i + (j * offset) for i in range(len(all_sender_receiver_ids))]
            #print(f"{sender_receiver_ids} - {packet_counts}")
            ax.bar(x, pc, width=width, alpha=0.6, label=file_type.capitalize())


    ax.set_title(f'Сравнение файлов not_black_hole-{number}-0.pcap и black_hole-{number}-0.pcap', fontsize=12)
    ax.set_xlabel("IР отправителя и получателя", fontsize=10)
    ax.set_ylabel("Количество пакетов", fontsize=10)
    ax.set_xticks([i + width / 2 for i in range(len(all_sender_receiver_ids))])
    ax.set_xticklabels(all_sender_receiver_ids, rotation=10, fontsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.legend()

    plt.show()

