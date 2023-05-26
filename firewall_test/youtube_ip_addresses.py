def list_youtube_ip():
    youtube_ip = []
    for i in range(232, 240):
        for j in range(0, 256):
            youtube_ip.append(f'199.223.{i}.{j}')
    for i in range(160, 176):
        for j in range(0, 256):
            youtube_ip.append(f'207.223.{i}.{j}')
    for i in range(152, 156):
        for j in range(0, 256):
            youtube_ip.append(f'208.65.{i}.{j}')
    for i in range(224, 256):
        for j in range(0, 256):
            youtube_ip.append(f'208.117.{i}.{j}')
    for i in range(128, 256):
        for j in range(0, 256):
            youtube_ip.append(f'209.85.{i}.{j}')
    for i in range(192, 224):
        for j in range(0, 256):
            youtube_ip.append(f'216.58.{i}.{j}')
    for i in range(32,64):
        for j in range(0, 256):
            youtube_ip.append(f'216.239.{i}.{j}')
    return youtube_ip

if __name__ == "__main__":
    youtube_ip = list_youtube_ip()
    with open('commands.txt', 'w') as f:
        for ip in youtube_ip:
            f.write(f'table_add MyIngress.dst_ip_drop MyIngress.drop {ip}/32 => ')
            f.write('\n')
    f.close()
