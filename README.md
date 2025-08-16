# 🛡️ S7ENC - Seven-Layer Professional Encryption System

<div align="center">

```
   ███████╗███████╗███████╗███╗   ██╗ ██████╗
   ██╔════╝╚════██║██╔════╝████╗  ██║██╔════╝
   ███████╗    ██╔╝█████╗  ██╔██╗ ██║██║     
   ╚════██║   ██╔╝ ██╔══╝  ██║╚██╗██║██║     
   ███████║   ██║  ███████╗██║ ╚████║╚██████╗
   ╚══════╝   ╚═╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝
```

**stop666two's Python Seven-Layer Encryption Program**

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

🔐 **Military-grade 7-layer encryption** | 🌍 **Full Unicode support** | 📱 **Termux optimized**

[English](#english) | [中文](#中文)

</div>

---

## English

### 🚀 Features

- **🛡️ Seven Independent Encryption Layers**
  - **Layer 1**: Fernet encryption (cryptography library)
  - **Layer 2**: AES-GCM encryption (PyCryptodome library)
  - **Layer 3**: ChaCha20 encryption (PyCryptodome library)
  - **Layer 4**: Salsa20 encryption (PyCryptodome library)
  - **Layer 5**: AES-CBC encryption (cryptography library)
  - **Layer 6**: scrypt + AES encryption (PyCryptodome library)
  - **Layer 7**: HMAC verification + compression (standard library)

- **🌍 Universal Character Support**
  - Full Unicode support (Chinese, Japanese, Korean, Arabic, etc.)
  - Emoji and special symbols support
  - Multi-line text preservation

- **🔒 Advanced Security Features**
  - Independent key derivation for each layer
  - PBKDF2 and scrypt key strengthening
  - HMAC data integrity verification
  - Automatic memory cleanup
  - 20-digit random filenames from π and e constants

- **📱 Cross-Platform Compatibility**
  - Windows, Linux, macOS
  - Android (Termux optimized)
  - Python 3.6+ support

### 📦 Installation

#### Quick Install (Recommended)
```bash
# Clone the repository
git clone https://github.com/stop666two/S7ENC.git
cd S7ENC

# For Termux users (Android)
chmod +x install_deps.sh
./install_deps.sh

# For other platforms
pip install cryptography pycryptodome
```

#### Manual Installation
```bash
# Install dependencies
pip install cryptography pycryptodome

# Run the program
python s7enc.py
```

### 🎯 Usage

1. **Run the program**
   ```bash
   python s7enc.py
   ```

2. **Encrypt text**
   - Choose option 1
   - Enter your encryption key
   - Input text (supports multi-line, end with 'END')
   - Save the 20-digit random number and keep your key safe

3. **Decrypt text**
   - Choose option 2
   - Enter the 20-digit random number
   - Enter your decryption key
   - View the decrypted text

### 🧪 Testing

The program includes comprehensive testing:
```bash
# Run built-in security tests
python s7enc.py
# Choose option 3 for security testing
```

### 🔧 Technical Details

#### Encryption Process
```
Original Text
    ↓
Layer 1: Fernet encryption
    ↓
Layer 2: AES-GCM encryption
    ↓
Layer 3: ChaCha20 encryption
    ↓
Layer 4: Salsa20 encryption
    ↓
Layer 5: AES-CBC encryption
    ↓
Layer 6: scrypt + AES encryption
    ↓
Layer 7: HMAC + compression
    ↓
Final Encrypted Text
```

#### Security Measures
- **Independent Keys**: Each layer uses different derived keys
- **Memory Safety**: Automatic cleanup of sensitive data
- **Data Integrity**: HMAC verification prevents tampering
- **Compression**: Reduces file size while maintaining security

### 📸 Screenshots

```
🛡️ ================================================================
   ███████╗███████╗███████╗███╗   ██╗ ██████╗
   ██╔════╝╚════██║██╔════╝████╗  ██║██╔════╝
   ███████╗    ██╔╝█████╗  ██╔██╗ ██║██║     
   ╚════██║   ██╔╝ ██╔══╝  ██║╚██╗██║██║     
   ███████║   ██║  ███████╗██║ ╚████║╚██████╗
   ╚══════╝   ╚═╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝

    🔐 stop666two's Python Seven-Layer Encryption
    📊 Version: 1.0.0 | 🆓 100% Free & Open Source
    🛡️ 7-layer Professional Encryption | 🧹 Auto Memory Cleanup
================================================================

🎯 Main Menu:
   1️⃣  🔐 Encrypt Text (7-layer Professional Encryption)
   2️⃣  🔓 Decrypt Text (7-layer Professional Decryption)
   3️⃣  🧪 Security Test (Function Verification)
   4️⃣  ℹ️  About Program (Detailed Information)
   5️⃣  🚪 Safe Exit (Auto Cleanup)
```

### ⚠️ Security Notice

- **For Educational Use Only**: This software is for learning and research purposes
- **Keep Keys Safe**: Store your encryption keys securely
- **No Warranty**: Software provided "as is" without any warranty
- **Legal Compliance**: Use in accordance with local laws and regulations

### 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👨‍💻 Author

**stop666two**
- GitHub: [@stop666two](https://github.com/stop666two)

---

## 中文

### 🚀 功能特色

- **🛡️ 七层独立加密系统**
  - **第1层**: Fernet加密 (cryptography库)
  - **第2层**: AES-GCM加密 (PyCryptodome库)
  - **第3层**: ChaCha20加密 (PyCryptodome库)
  - **第4层**: Salsa20加密 (PyCryptodome库)
  - **第5层**: AES-CBC加密 (cryptography库)
  - **第6层**: scrypt+AES加密 (PyCryptodome库)
  - **第7层**: HMAC验证+压缩 (标准库)

- **🌍 全面字符支持**
  - 完整Unicode支持（中文、日文、韩文、阿拉伯文等）
  - 支持emoji表情和特殊符号
  - 保持多行文本格式

- **🔒 高级安全特性**
  - 每层独立密钥派生
  - PBKDF2和scrypt密钥强化
  - HMAC数据完整性验证
  - 自动内存清理
  - 基于π和e常数的20位随机文件名

- **📱 跨平台兼容**
  - Windows, Linux, macOS
  - Android (Termux优化)
  - Python 3.6+ 支持

### 📦 安装方法

#### 快速安装（推荐）
```bash
# 克隆仓库
git clone https://github.com/stop666two/S7ENC.git
cd S7ENC

# Termux用户（安卓）
chmod +x install_deps.sh
./install_deps.sh

# 其他平台
pip install cryptography pycryptodome
```

#### 手动安装
```bash
# 安装依赖
pip install cryptography pycryptodome

# 运行程序
python s7enc.py
```

### 🎯 使用方法

1. **运行程序**
   ```bash
   python s7enc.py
   ```

2. **加密文本**
   - 选择选项1
   - 输入加密密钥
   - 输入文本（支持多行，以'END'结束）
   - 保存20位随机数并妥善保管密钥

3. **解密文本**
   - 选择选项2
   - 输入20位随机数
   - 输入解密密钥
   - 查看解密结果

### 🧪 测试功能

程序包含完整的测试功能：
```bash
# 运行内置安全测试
python s7enc.py
# 选择选项3进行安全测试
```

### 🔧 技术详情

#### 加密流程
```
原始文本
    ↓
第1层: Fernet加密
    ↓
第2层: AES-GCM加密
    ↓
第3层: ChaCha20加密
    ↓
第4层: Salsa20加密
    ↓
第5层: AES-CBC加密
    ↓
第6层: scrypt+AES加密
    ↓
第7层: HMAC+压缩
    ↓
最终加密文本
```

#### 安全措施
- **独立密钥**: 每层使用不同的派生密钥
- **内存安全**: 自动清理敏感数据
- **数据完整性**: HMAC验证防止篡改
- **数据压缩**: 在保持安全的同时减小文件大小

### ⚠️ 安全声明

- **仅供教育使用**: 本软件仅供学习和研究使用
- **妥善保管密钥**: 请安全存储您的加密密钥
- **无质量保证**: 软件按"原样"提供，不提供任何保证
- **合规使用**: 请根据当地法律法规合规使用

### 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📄 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情。

### 👨‍💻 作者

**stop666two**
- GitHub: [@stop666two](https://github.com/stop666two)

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/stop666two/S7ENC?style=social)
![GitHub forks](https://img.shields.io/github/forks/stop666two/S7ENC?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/stop666two/S7ENC?style=social)

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

**如果您觉得这个项目有用，请考虑给它一个星标！**

Made with ❤️ by [stop666two](https://github.com/stop666two)

</div>
