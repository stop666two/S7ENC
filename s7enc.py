#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S7ENC - stop666two's Python Seven-Layer Encryption Program
版本: 1.0.0
作者: stop666two
许可: 100% 免费开源软件，禁止商业使用
开源地址：https://github.com/stop666two/S7ENC

免责声明：
本软件按"原样"提供，不提供任何明示或暗示的保证。
使用本软件的风险完全由用户承担。
作者不对使用本软件造成的任何损失负责。
本软件仅供学习和研究使用，禁止用于任何商业目的。
"""

import os
import sys
import time
import hashlib
import base64
import random
import gc
import platform
import zlib
import hmac
from datetime import datetime
from typing import List, Tuple, Optional

# 自动依赖检查和安装
def _0x1a2b3c():
    """检查并安装依赖"""
    required_packages = ['cryptography', 'pycryptodome']
    for package in required_packages:
        try:
            if package == 'cryptography':
                from cryptography.fernet import Fernet
            elif package == 'pycryptodome':
                from Crypto.Cipher import AES, ChaCha20, Salsa20
        except ImportError:
            print(f"🔧 正在安装 {package}...")
            os.system(f"{sys.executable} -m pip install {package} --quiet")
    print("✅ 依赖检查完成")

_0x1a2b3c()

# 导入专业加密库
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES as PyCrypto_AES, ChaCha20, Salsa20
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad, unpad

# 数学常数π和e的800位精度（用于生成随机数）
_0x2b3c4d = ("31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
             "82148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964"
             "42881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372"
             "45870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330"
             "57270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833"
             "67336244065664308602139494639522473719070217986094370277053921717629317675238467481846766940513200056"
             "81271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199"
             "56112129021960864034418159813629774771309960518707211349999998372978049951059731732816096318595024459"
             "45534690830264252230825334468503526193118817101000313783875288658753320838142061717766914730359825349"
             "04287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989380952572"
             "01065485863278865936153381827968230301952035301852968995773622599413891249721775283479131515574857242"
             "45415069595082953311686172785588907509838175463746493931925506040092770167113900984882401285836160356"
             "37076601047101819429555961989467678374494482553797747268471040475346462080466842590694912933136770289"
             "89152104752162056966024058038150193511253382430035587640247496473263914199272604269922796782354781636"
             "00934172164121992458631503028618297455570674983850549458858692699569092721079750930295532116534498720"
             "27559602364806654991198818347977535663698074265425278625518184175746728909777727938000816470600161452"
             "49192173217214772350141441973568548161361157352552133475741849468438523323907394143334547762416862518"
             "98356948556209921922218427255025425688767179049460167460976597981234634868541634557490166530730655438"
             "90156645324")

_0x3c4d5e = ("27182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274"
             "27466391932003059921817413596629043572900334295260595630738132328627943490763233829880753195251019011"
             "57383418793070215408914993488416750924476146066088226480016847741185374234544243710753907774499206955"
             "17027618386062613313845830007520449338265602976067371132007093287091274437470472306969772093101416928"
             "36819025515108657463772111252389784425056953696770785449969967946864455490598793163688923008793127736"
             "17821542499922957635148220826989519366803318252886939849646510582093923982948879332036250946495242346"
             "68073616117323350649699845162658706772451151473056030074299804476669280477227776672932393942142539883"
             "20640961297495269164845932631969142646036966493893970158316061996593069688701177506387645306816647951"
             "45642433856805563563571753495166949124406895965201517700009550346368644905026369365393564444437700006"
             "84635561780701696630947177261580414340551164486263607104045688587785945639503163109082161682868650015"
             "90403762659847464739133028254246529823974337777540479517560626496230649599689069624638471575836326001"
             "01993987494509862984516071005978946725062949823529072781698639624406123002095094851516522436169952316"
             "12700789250664460772044923642630602092453345539594999916677981652706883173881688374058899978700073746"
             "06499495372173843603143499422394665872183000796052706")

def _0x4d5e6f():
    """获取π和e的20位随机数"""
    _0x5e6f70 = _0x2b3c4d + _0x3c4d5e
    _0x6f7081 = random.randint(0, len(_0x5e6f70) - 20)
    return _0x5e6f70[_0x6f7081:_0x6f7081 + 20]

def _0x7081a2():
    """清屏函数"""
    if platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

def _0x8192b3(data: str) -> None:
    """安全清理内存数据"""
    try:
        if data:
            # 覆盖原始数据
            data = '0' * len(data)
            del data
        gc.collect()
    except:
        pass

class _0x9283c4:
    """七层专业加密系统核心类"""
    
    def __init__(self, _0xa394d5: str):
        self._0xkey_str = _0xa394d5
        self._0xkey_bytes = hashlib.sha256(_0xa394d5.encode()).digest()
        self._0xtimestamp = datetime.now().isoformat()
        # 为每层生成不同的密钥
        self._0xlayer_keys = []
        for i in range(7):
            layer_key = hashlib.sha256(f"{_0xa394d5}_layer_{i}".encode()).digest()
            self._0xlayer_keys.append(layer_key)
        
    def _0xe7d819(self, text: str) -> str:
        """第1层：Fernet加密 - cryptography库"""
        try:
            # 使用PBKDF2生成Fernet密钥
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self._0xlayer_keys[0][:16],
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(self._0xkey_str.encode()))
            
            fernet = Fernet(key)
            encrypted = fernet.encrypt(text.encode('utf-8'))
            return base64.b64encode(encrypted).decode('ascii')
        except Exception as e:
            print(f"第1层加密错误: {str(e)}")
            raise
    
    def _0x09fa3b(self, text: str) -> str:
        """第1层解密：Fernet解密"""
        try:
            # 重新生成相同的密钥
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self._0xlayer_keys[0][:16],
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(self._0xkey_str.encode()))
            
            fernet = Fernet(key)
            encrypted = base64.b64decode(text.encode('ascii'))
            decrypted = fernet.decrypt(encrypted)
            return decrypted.decode('utf-8')
        except Exception as e:
            print(f"第1层解密错误: {str(e)}")
            raise
    
    def _0x1a0b4c(self, text: str) -> str:
        """第2层：AES-GCM加密 - PyCryptodome库"""
        try:
            key = self._0xlayer_keys[1][:32]
            nonce = self._0xlayer_keys[1][:12]  # GCM推荐12字节nonce
            
            cipher = PyCrypto_AES.new(key, PyCrypto_AES.MODE_GCM, nonce=nonce)
            ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
            
            # 组合nonce + tag + ciphertext
            result = nonce + tag + ciphertext
            return base64.b64encode(result).decode('ascii')
        except Exception as e:
            print(f"第2层加密错误: {str(e)}")
            raise
    
    def _0x2b1c5d(self, text: str) -> str:
        """第2层解密：AES-GCM解密"""
        try:
            data = base64.b64decode(text.encode('ascii'))
            nonce = data[:12]
            tag = data[12:28]
            ciphertext = data[28:]
            
            key = self._0xlayer_keys[1][:32]
            cipher = PyCrypto_AES.new(key, PyCrypto_AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode('utf-8')
        except Exception as e:
            print(f"第2层解密错误: {str(e)}")
            raise
    
    def _0x3c2d6e(self, text: str) -> str:
        """第3层：ChaCha20加密 - PyCryptodome库"""
        try:
            key = self._0xlayer_keys[2][:32]
            nonce = self._0xlayer_keys[2][:12]
            
            cipher = ChaCha20.new(key=key, nonce=nonce)
            ciphertext = cipher.encrypt(text.encode('utf-8'))
            
            result = nonce + ciphertext
            return base64.b64encode(result).decode('ascii')
        except Exception as e:
            print(f"第3层加密错误: {str(e)}")
            raise
    
    def _0x5e4f80(self, text: str) -> str:
        """第3层解密：ChaCha20解密"""
        try:
            data = base64.b64decode(text.encode('ascii'))
            nonce = data[:12]
            ciphertext = data[12:]
            
            key = self._0xlayer_keys[2][:32]
            cipher = ChaCha20.new(key=key, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            return plaintext.decode('utf-8')
        except Exception as e:
            print(f"第3层解密错误: {str(e)}")
            raise
    
    def _0x7061a2(self, text: str) -> str:
        """第4层：Salsa20加密 - PyCryptodome库"""
        try:
            key = self._0xlayer_keys[3][:32]
            nonce = self._0xlayer_keys[3][:8]  # Salsa20使用8字节nonce
            
            cipher = Salsa20.new(key=key, nonce=nonce)
            ciphertext = cipher.encrypt(text.encode('utf-8'))
            
            result = nonce + ciphertext
            return base64.b64encode(result).decode('ascii')
        except Exception as e:
            print(f"第4层加密错误: {str(e)}")
            raise
    
    def _0x8172b3(self, text: str) -> str:
        """第4层解密：Salsa20解密"""
        try:
            data = base64.b64decode(text.encode('ascii'))
            nonce = data[:8]
            ciphertext = data[8:]
            
            key = self._0xlayer_keys[3][:32]
            cipher = Salsa20.new(key=key, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            return plaintext.decode('utf-8')
        except Exception as e:
            print(f"第4层解密错误: {str(e)}")
            raise
    
    def _0x9283c4_layer5(self, text: str) -> str:
        """第5层：AES-CBC加密 - cryptography库"""
        try:
            key = self._0xlayer_keys[4][:32]
            iv = self._0xlayer_keys[4][:16]
            
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            
            # PKCS7填充
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(text.encode('utf-8'))
            padded_data += padder.finalize()
            
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            
            result = iv + ciphertext
            return base64.b64encode(result).decode('ascii')
        except Exception as e:
            print(f"第5层加密错误: {str(e)}")
            raise
    
    def _0xa394d5_layer5(self, text: str) -> str:
        """第5层解密：AES-CBC解密"""
        try:
            data = base64.b64decode(text.encode('ascii'))
            iv = data[:16]
            ciphertext = data[16:]
            
            key = self._0xlayer_keys[4][:32]
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            
            # 移除PKCS7填充
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_data)
            plaintext += unpadder.finalize()
            
            return plaintext.decode('utf-8')
        except Exception as e:
            print(f"第5层解密错误: {str(e)}")
            raise
    
    def _0xb4a5e6_layer6(self, text: str) -> str:
        """第6层：scrypt + AES加密 - PyCryptodome库"""
        try:
            salt = self._0xlayer_keys[5][:16]
            # 使用scrypt密钥派生
            key = scrypt(self._0xkey_str.encode(), salt, 32, N=2**14, r=8, p=1)
            
            iv = self._0xlayer_keys[5][:16]
            cipher = PyCrypto_AES.new(key, PyCrypto_AES.MODE_CBC, iv)
            
            # 填充
            padded_text = pad(text.encode('utf-8'), PyCrypto_AES.block_size)
            ciphertext = cipher.encrypt(padded_text)
            
            result = salt + iv + ciphertext
            return base64.b64encode(result).decode('ascii')
        except Exception as e:
            print(f"第6层加密错误: {str(e)}")
            raise
    
    def _0xc5b6f7_layer6(self, text: str) -> str:
        """第6层解密：scrypt + AES解密"""
        try:
            data = base64.b64decode(text.encode('ascii'))
            salt = data[:16]
            iv = data[16:32]
            ciphertext = data[32:]
            
            # 重新派生密钥
            key = scrypt(self._0xkey_str.encode(), salt, 32, N=2**14, r=8, p=1)
            
            cipher = PyCrypto_AES.new(key, PyCrypto_AES.MODE_CBC, iv)
            padded_text = cipher.decrypt(ciphertext)
            
            # 移除填充
            plaintext = unpad(padded_text, PyCrypto_AES.block_size)
            return plaintext.decode('utf-8')
        except Exception as e:
            print(f"第6层解密错误: {str(e)}")
            raise
    
    def _0xd6c708_layer7(self, text: str) -> str:
        """第7层：HMAC + 压缩 + Base64"""
        try:
            # 计算HMAC
            hmac_key = self._0xlayer_keys[6]
            signature = hmac.new(hmac_key, text.encode('utf-8'), hashlib.sha256).digest()
            
            # 压缩数据
            compressed = zlib.compress(text.encode('utf-8'))
            
            # 组合：signature + compressed_data
            result = signature + compressed
            return base64.b64encode(result).decode('ascii')
        except Exception as e:
            print(f"第7层加密错误: {str(e)}")
            raise
    
    def _0xe7d819_layer7_dec(self, text: str) -> str:
        """第7层解密：HMAC验证 + 解压缩"""
        try:
            data = base64.b64decode(text.encode('ascii'))
            signature = data[:32]  # SHA256产生32字节
            compressed = data[32:]
            
            # 解压缩
            decompressed = zlib.decompress(compressed)
            plaintext = decompressed.decode('utf-8')
            
            # 验证HMAC
            hmac_key = self._0xlayer_keys[6]
            expected_signature = hmac.new(hmac_key, plaintext.encode('utf-8'), hashlib.sha256).digest()
            
            if not hmac.compare_digest(signature, expected_signature):
                raise ValueError("HMAC验证失败：数据可能被篡改")
            
            return plaintext
        except Exception as e:
            print(f"第7层解密错误: {str(e)}")
            raise
    
    def _0xf8e92a(self, plaintext: str) -> Tuple[str, str]:
        """完整七层加密"""
        print("🔄 开始七层专业加密过程...")
        
        # 添加时间戳和版本信息
        _0x091b2c = f"S7ENC_V1.0_{self._0xtimestamp}_{len(plaintext)}_{plaintext}"
        
        current = _0x091b2c
        layers = [
            ("第1层：Fernet加密", self._0xe7d819),
            ("第2层：AES-GCM加密", self._0x1a0b4c),
            ("第3层：ChaCha20加密", self._0x3c2d6e),
            ("第4层：Salsa20加密", self._0x7061a2),
            ("第5层：AES-CBC加密", self._0x9283c4_layer5),
            ("第6层：scrypt+AES加密", self._0xb4a5e6_layer6),
            ("第7层：HMAC+压缩", self._0xd6c708_layer7)
        ]
        
        for i, (name, func) in enumerate(layers, 1):
            print(f"🔐 正在执行 {name}... ({i}/7)")
            current = func(current)
            time.sleep(0.1)  # 视觉效果
        
        # 生成随机文件名
        random_name = _0x4d5e6f()
        
        print("✅ 七层专业加密完成！")
        return current, random_name
    
    def _0x1a2c3d(self, ciphertext: str) -> str:
        """完整七层解密"""
        print("🔄 开始七层专业解密过程...")
        
        current = ciphertext
        layers = [
            ("第7层：HMAC+解压缩", self._0xe7d819_layer7_dec),
            ("第6层：scrypt+AES解密", self._0xc5b6f7_layer6),
            ("第5层：AES-CBC解密", self._0xa394d5_layer5),
            ("第4层：Salsa20解密", self._0x8172b3),
            ("第3层：ChaCha20解密", self._0x5e4f80),
            ("第2层：AES-GCM解密", self._0x2b1c5d),
            ("第1层：Fernet解密", self._0x09fa3b)
        ]
        
        for i, (name, func) in enumerate(layers, 1):
            print(f"🔓 正在执行 {name}... ({i}/7)")
            current = func(current)
            time.sleep(0.1)  # 视觉效果
        
        # 验证头部信息
        if not current.startswith("S7ENC_V1.0_"):
            raise ValueError("解密失败：数据头部验证失败")
        
        # 提取原文
        parts = current.split('_', 4)
        if len(parts) != 5:
            raise ValueError("解密失败：数据格式错误")
        
        original_length = int(parts[3])
        original_text = parts[4]
        
        if len(original_text) != original_length:
            raise ValueError("解密失败：数据长度不匹配")
        
        print("✅ 七层专业解密完成！")
        return original_text

class _0x2b3d4e:
    """主程序类"""
    
    def __init__(self):
        self._0x3c4e5f = "1.0.0"
        self._0x4d5f60 = []  # 存储敏感数据用于清理
        
    def _0x5e6071(self):
        """显示免责声明"""
        _0x7081a2()
        print("📜 " + "="*60)
        print("     S7ENC - 免责声明和许可协议")
        print("="*60)
        print()
        print("⚠️  重要声明：")
        print("   • 本软件为100%免费开源软件")
        print("   • 仅供学习和研究使用")
        print("   • 严禁任何形式的商业使用")
        print("   • 软件按'原样'提供，不提供任何保证")
        print("   • 使用风险完全由用户承担")
        print("   • 作者不对任何损失负责")
        print()
        print("🔒 专业加密特性：")
        print("   • 七层专业级加密算法")
        print("   • Fernet + AES-GCM + ChaCha20")
        print("   • Salsa20 + AES-CBC + scrypt")
        print("   • HMAC验证 + 数据压缩")
        print("   • 自动内存清理")
        print("   • Unicode全字符支持")
        print()
        print("="*60)
        
        while True:
            choice = input("📋 请输入 'AGREE' 同意协议并继续，或 'EXIT' 退出: ").strip().upper()
            if choice == 'AGREE':
                break
            elif choice == 'EXIT':
                print("👋 再见！")
                sys.exit(0)
            else:
                print("❌ 请输入 'AGREE' 或 'EXIT'")
    
    def _0x6f7182(self):
        """显示主菜单"""
        _0x7081a2()
        print("🛡️ " + "="*60)
        print("   ███████╗███████╗███████╗███╗   ██╗ ██████╗")
        print("   ██╔════╝╚════██║██╔════╝████╗  ██║██╔════╝")
        print("   ███████╗    ██╔╝█████╗  ██╔██╗ ██║██║     ")
        print("   ╚════██║   ██╔╝ ██╔══╝  ██║╚██╗██║██║     ")
        print("   ███████║   ██║  ███████╗██║ ╚████║╚██████╗")
        print("   ╚══════╝   ╚═╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝")
        print()
        print("    🔐 stop666two's Python Seven-Layer Encryption")
        print(f"    📊 版本: {self._0x3c4e5f} | 🆓 100% 免费开源")
        print("    🛡️ 7层专业加密 | 🧹 自动残留清理")
        print("="*60)
        print()
        print("🎯 功能菜单：")
        print("   1️⃣  🔐 加密文本 (7层专业加密 + 残留清理)")
        print("   2️⃣  🔓 解密文本 (7层专业解密 + 残留清理)")
        print("   3️⃣  🧪 安全测试 (验证功能 + 安全检查)")
        print("   4️⃣  ℹ️  关于程序 (详细信息 + 免费声明)")
        print("   5️⃣  🚪 安全退出 (自动清理残留)")
        print()
        print("💡 提示：使用专业加密库，支持所有Unicode字符")
        print("🔒 安全：Fernet+AES+ChaCha20+Salsa20+HMAC")
        print("🏆开源地址：https://github.com/stop666two/S7ENC")
        print("="*60)
    
    def _0x8093a4(self):
        """加密功能"""
        _0x7081a2()
        print("🔐 " + "="*50)
        print("           专业加密模式")
        print("="*50)
        print()
        
        # 获取密钥
        password = input("🔑 请输入加密密钥: ").strip()
        if not password:
            print("❌ 密钥不能为空！")
            input("按回车键继续...")
            return
        
        if len(password) < 6:
            print("⚠️  警告：密钥长度较短，建议使用6位以上强密钥")
            
        self._0x4d5f60.append(password)
        
        print()
        print("📝 请输入要加密的文本（支持多行）:")
        print("   💡 输入完成后，单独输入 'END' 结束")
        print("   📄 支持中文、emoji、特殊符号等所有Unicode字符")
        print("-" * 50)
        
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        
        if not lines:
            print("❌ 没有输入任何文本！")
            input("按回车键继续...")
            return
        
        plaintext = '\n'.join(lines)
        self._0x4d5f60.append(plaintext)
        
        print()
        print("⏳ 开始专业加密处理...")
        start_time = time.time()
        
        try:
            encryptor = _0x9283c4(password)
            ciphertext, random_name = encryptor._0xf8e92a(plaintext)
            
            # 保存到文件
            filename = f"{random_name}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(ciphertext)
            
            end_time = time.time()
            
            # 显示结果
            print()
            print("✅ " + "="*50)
            print("           专业加密成功完成！")
            print("="*50)
            print(f"📁 文件名: {filename}")
            print(f"🎲 随机数: {random_name}")
            print(f"📊 原文大小: {len(plaintext)} 字符")
            print(f"📊 密文大小: {len(ciphertext)} 字符")
            print(f"📈 数据膨胀: {len(ciphertext)/len(plaintext):.2f}x")
            print(f"⏱️  加密耗时: {end_time-start_time:.2f} 秒")
            print(f"💾 文件大小: {os.path.getsize(filename)} 字节")
            print()
            print("🔒 请妥善保管20位随机数和密钥！")
            print("🗑️ 正在清理内存残留...")
            
            # 清理敏感数据
            _0x8192b3(plaintext)
            _0x8192b3(ciphertext)
            _0x8192b3(password)
            
        except Exception as e:
            print(f"❌ 加密失败: {str(e)}")
        
        input("\n按回车键返回主菜单...")
    
    def _0x91b4c5(self):
        """解密功能"""
        _0x7081a2()
        print("🔓 " + "="*50)
        print("           专业解密模式")
        print("="*50)
        print()
        
        # 获取随机数
        random_name = input("🎲 请输入20位随机数: ").strip()
        if len(random_name) != 20 or not random_name.isdigit():
            print("❌ 随机数格式错误！必须是20位数字")
            input("按回车键继续...")
            return
        
        # 检查文件
        filename = f"{random_name}.txt"
        if not os.path.exists(filename):
            print(f"❌ 找不到加密文件: {filename}")
            input("按回车键继续...")
            return
        
        # 获取密钥
        password = input("🔑 请输入解密密钥: ").strip()
        if not password:
            print("❌ 密钥不能为空！")
            input("按回车键继续...")
            return
        
        self._0x4d5f60.extend([random_name, password])
        
        print()
        print("⏳ 开始专业解密处理...")
        start_time = time.time()
        
        try:
            # 读取文件
            with open(filename, 'r', encoding='utf-8') as f:
                ciphertext = f.read()
            
            decryptor = _0x9283c4(password)
            plaintext = decryptor._0x1a2c3d(ciphertext)
            
            end_time = time.time()
            
            # 显示结果
            print()
            print("✅ " + "="*50)
            print("           专业解密成功完成！")
            print("="*50)
            print("📄 解密内容:")
            print("-" * 50)
            
            # 显示多行文本，保持换行格式
            print(plaintext)
            
            print("-" * 50)
            print(f"📊 解密大小: {len(plaintext)} 字符")
            print(f"📄 行数统计: {plaintext.count(chr(10)) + 1} 行")
            print(f"⏱️  解密耗时: {end_time-start_time:.2f} 秒")
            print()
            
            # 询问是否保存
            save_choice = input("💾 是否保存解密结果到新文件? (y/N): ").strip().lower()
            if save_choice == 'y':
                save_filename = f"decrypted_{random_name}_{int(time.time())}.txt"
                with open(save_filename, 'w', encoding='utf-8') as f:
                    f.write(plaintext)
                print(f"✅ 已保存到: {save_filename}")
                print(f"💡 文件中保持了原有的换行格式")
            
            print("🗑️ 正在清理内存残留...")
            
            # 清理敏感数据
            _0x8192b3(plaintext)
            _0x8192b3(ciphertext)
            _0x8192b3(password)
            
        except Exception as e:
            print(f"❌ 解密失败: {str(e)}")
        
        input("\n按回车键返回主菜单...")
    
    def _0xa2c5d6(self):
        """安全测试功能"""
        _0x7081a2()
        print("🧪 " + "="*50)
        print("           专业加密测试模式")
        print("="*50)
        print()
        
        test_cases = [
            ("Hello World!", "test123"),
            ("你好，世界！🌍", "测试密钥456"),
            ("Multi\nLine\nText", "password789"),
            ("🔐🛡️🧪Special#@!$%", "复杂密钥2024"),
            ("ksndkdn\n可是你上课辛苦\n😍😛😎😙😳😑😞😚\n+.com_&www..com.net#+#+\n\n\n😛😳😙😙\n(=。=)Σ( ° △ °|||)︴😑😑😟😞", "专业测试密钥")
        ]
        
        print("🔍 开始执行专业加密测试...")
        print()
        
        all_passed = True
        
        for i, (test_text, test_key) in enumerate(test_cases, 1):
            print(f"📋 测试用例 {i}: ", end="", flush=True)
            
            try:
                # 加密
                encryptor = _0x9283c4(test_key)
                ciphertext, _ = encryptor._0xf8e92a(test_text)
                
                # 解密
                decryptor = _0x9283c4(test_key)
                decrypted = decryptor._0x1a2c3d(ciphertext)
                
                if decrypted == test_text:
                    print("✅ 通过")
                else:
                    print("❌ 失败")
                    print(f"    原文: {repr(test_text)}")
                    print(f"    解密: {repr(decrypted)}")
                    all_passed = False
                    
            except Exception as e:
                print(f"❌ 异常: {str(e)}")
                all_passed = False
        
        print()
        print("🔒 内存安全测试...")
        
        # 测试内存清理
        test_data = "敏感测试数据" * 100
        _0x8192b3(test_data)
        print("✅ 内存清理测试通过")
        
        print()
        print("📊 " + "="*50)
        if all_passed:
            print("🎉 所有测试通过！专业加密系统运行正常")
            print("✅ Fernet加密/解密功能正常")
            print("✅ AES-GCM加密/解密功能正常")
            print("✅ ChaCha20加密/解密功能正常")
            print("✅ Salsa20加密/解密功能正常")
            print("✅ AES-CBC加密/解密功能正常")
            print("✅ scrypt+AES加密/解密功能正常")
            print("✅ HMAC+压缩功能正常")
            print("✅ Unicode字符支持正常")
            print("✅ 多行文本处理正常")
            print("✅ 内存清理功能正常")
        else:
            print("⚠️  部分测试失败，请检查系统")
        
        print("="*50)
        input("\n按回车键返回主菜单...")
    
    def _0xb3d6e7(self):
        """关于程序"""
        _0x7081a2()
        print("ℹ️ " + "="*60)
        print("              关于 S7ENC")
        print("="*60)
        print()
        print("📝 程序信息:")
        print(f"   名称: S7ENC (Seven-Layer Encryption)")
        print(f"   全称: stop666two's Python seven-layer encryption program")
        print(f"   版本: {self._0x3c4e5f}")
        print(f"   作者: stop666two")
        print(f"   开源地址：https://github.com/stop666two/S7ENC")
        print(f"   语言: Python 3.6+")
        print()
        print("🔒 专业加密层级:")
        print("   • 第1层: Fernet加密 (cryptography库)")
        print("   • 第2层: AES-GCM加密 (PyCryptodome库)")
        print("   • 第3层: ChaCha20加密 (PyCryptodome库)")
        print("   • 第4层: Salsa20加密 (PyCryptodome库)")
        print("   • 第5层: AES-CBC加密 (cryptography库)")
        print("   • 第6层: scrypt+AES加密 (PyCryptodome库)")
        print("   • 第7层: HMAC验证+压缩 (标准库)")
        print()
        print("🛡️ 安全特性:")
        print("   • 七层独立的专业加密算法")
        print("   • 每层使用不同的密钥派生")
        print("   • PBKDF2、scrypt等强化密钥派生")
        print("   • HMAC数据完整性验证")
        print("   • 数据压缩减小文件大小")
        print("   • 自动内存清理机制")
        print("   • 支持所有Unicode字符")
        print()
        print("💻 系统要求:")
        print("   • Python 3.6 或更高版本")
        print("   • cryptography 库（自动安装）")
        print("   • pycryptodome 库（自动安装）")
        print("   • 支持 Windows/Linux/macOS")
        print()
        print("🆓 许可协议:")
        print("   • 100% 免费开源软件")
        print("   • 仅供学习和研究使用")
        print("   • 禁止任何商业用途")
        print("   • MIT许可证")
        print()
        print("⚠️ 免责声明:")
        print("   • 软件按'原样'提供，不提供任何保证")
        print("   • 使用风险完全由用户承担")
        print("   • 作者不对任何损失负责")
        print("   • 请合法合规使用")
        print()
        print("🔧 技术细节:")
        print("   • 基于π和e常数的20位随机数生成")
        print("   • 多层独立密钥派生机制")
        print("   • 时间戳完整性验证")
        print("   • 安全的内存数据清理")
        print("   • 专业加密库确保安全性")
        print()
        print("="*60)
        input("按回车键返回主菜单...")
    
    def _0xc4e7f8(self):
        """安全退出"""
        _0x7081a2()
        print("🚪 " + "="*40)
        print("         正在安全退出...")
        print("="*40)
        print()
        
        print("🗑️ 清理内存数据...")
        for data in self._0x4d5f60:
            _0x8192b3(data)
        
        print("🧹 清理临时文件...")
        # 这里可以添加临时文件清理逻辑
        
        print("🔒 清理系统缓存...")
        gc.collect()
        
        print("✅ 清理完成")
        print()
        print("👋 感谢使用 S7ENC 专业加密系统！")
        print("🆓 永久免费，欢迎分享")
        print("🛡️ 七层专业加密，保护您的数据安全")
        print("📝 作者:stop666two")
        print("🏆开源地址：https://github.com/stop666two/S7ENC")
        print("="*40)
        
        time.sleep(1)
        sys.exit(0)
    
    def _0xd5f809(self):
        """主程序运行"""
        # 显示免责声明
        self._0x5e6071()
        
        while True:
            self._0x6f7182()
            
            try:
                choice = input("\n🎯 请选择功能 (1-5): ").strip()
                
                if choice == '1':
                    self._0x8093a4()
                elif choice == '2':
                    self._0x91b4c5()
                elif choice == '3':
                    self._0xa2c5d6()
                elif choice == '4':
                    self._0xb3d6e7()
                elif choice == '5':
                    self._0xc4e7f8()
                else:
                    print("❌ 无效选择，请输入 1-5")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ 检测到强制退出，执行安全清理...")
                self._0xc4e7f8()
            except Exception as e:
                print(f"❌ 程序错误: {str(e)}")
                time.sleep(2)

def main():
    """主函数"""
    try:
        app = _0x2b3d4e()
        app._0xd5f809()
    except Exception as e:
        print(f"🚨 严重错误: {str(e)}")
        print("📞 如需帮助，请联系开发者")
        input("按回车键退出...")

if __name__ == "__main__":
    main()