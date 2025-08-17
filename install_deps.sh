#!/bin/bash
# =================================================================
# S7ENC Termux 依赖安装脚本
# 作者: stop666two
# 开源地址：https://github.com/stop666two/S7ENC
# 版本: 1.0.0
# 描述: 自动安装S7ENC七层加密系统所需的所有依赖
# 兼容: sh/bash/dash等Shell环境
# =================================================================

# 检测Shell类型并设置兼容模式
if [ -n "$BASH_VERSION" ]; then
    # Bash环境
    set -euo pipefail
else
    # 其他Shell环境（如dash）
    set -e
fi

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 显示横幅
show_banner() {
    clear
    echo -e "${PURPLE}"
    echo "=================================================================="
    echo "   ███████╗███████╗███████╗███╗   ██╗ ██████╗"
    echo "   ██╔════╝╚════██║██╔════╝████╗  ██║██╔════╝"
    echo "   ███████╗    ██╔╝█████╗  ██╔██╗ ██║██║     "
    echo "   ╚════██║   ██╔╝ ██╔══╝  ██║╚██╗██║██║     "
    echo "   ███████║   ██║  ███████╗██║ ╚████║╚██████╗"
    echo "   ╚══════╝   ╚═╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝"
    echo ""
    echo "           Termux 依赖自动安装脚本"
    echo "              版本: 1.0.0"
    echo "             作者: stop666two"
    echo " 开源地址：https://github.com/stop666two/S7ENC"
    echo "=================================================================="
    echo -e "${NC}"
    echo -e "${WHITE}🛡️ 七层专业加密系统依赖安装${NC}"
    echo -e "${WHITE}🔐 包含: cryptography + pycryptodome${NC}"
    echo -e "${WHITE}📱 适用: Termux Android 环境${NC}"
    echo -e "${WHITE}🚀 特性: 阿里云镜像源加速${NC}"
    echo ""
}

# 检查网络连接
check_network() {
    log_step "检查网络连接..."
    if ping -c 1 mirrors.aliyun.com &> /dev/null; then
        log_success "网络连接正常"
        return 0
    else
        log_error "网络连接失败，请检查网络设置"
        exit 1
    fi
}

# 检查Termux环境
check_termux() {
    log_step "检查Termux环境..."
    if [ -z "$PREFIX" ]; then
        log_error "未检测到Termux环境，请在Termux中运行此脚本"
        exit 1
    fi
    log_success "Termux环境检查通过"
}

# 备份原始源
backup_sources() {
    log_step "备份原始软件源..."
    if [ -f "$PREFIX/etc/apt/sources.list" ]; then
        cp "$PREFIX/etc/apt/sources.list" "$PREFIX/etc/apt/sources.list.backup.$(date +%Y%m%d_%H%M%S)"
        log_success "原始软件源已备份"
    else
        log_warning "未找到原始软件源文件"
    fi
}

# 更换镜像源（支持多个高速源）
change_mirror() {
    log_step "更换为高速镜像源..."
    
    # 创建新的sources.list，使用多个高速镜像源
    cat > "$PREFIX/etc/apt/sources.list" << EOF
# 清华大学镜像源（推荐）
deb https://mirrors.tuna.tsinghua.edu.cn/termux/termux-packages-24/ stable main

# 阿里云镜像源（备用）
# deb https://mirrors.aliyun.com/termux/termux-packages-24/ stable main

# 中科大镜像源（备用）
# deb https://mirrors.ustc.edu.cn/termux/termux-packages-24/ stable main

# 华为云镜像源（备用）
# deb https://mirrors.huaweicloud.com/termux/termux-packages-24/ stable main
EOF
    
    if [ $? -eq 0 ]; then
        log_success "清华大学高速镜像源配置完成"
    else
        log_error "镜像源配置失败"
        exit 1
    fi
    
    # 配置APT加速选项
    log_info "配置APT下载加速选项..."
    cat > "$PREFIX/etc/apt/apt.conf.d/99termux-speed" << EOF
# 并发下载配置
Acquire::Queue-Mode "host";
Acquire::Retries "3";
Acquire::http::Timeout "30";
Acquire::https::Timeout "30";

# 并发连接数
Acquire::http::Pipeline-Depth "5";
Acquire::https::Pipeline-Depth "5";

# 下载速度优化
Acquire::http::No-Cache true;
Acquire::BrokenProxy true;
EOF
    
    log_success "APT下载加速配置完成"
}

# 测试镜像源速度并选择最快的
test_mirror_speed() {
    log_step "测试镜像源速度，选择最快的源..."
    
    # 定义镜像源列表
    MIRRORS="
https://mirrors.tuna.tsinghua.edu.cn/termux/termux-packages-24/
https://mirrors.ustc.edu.cn/termux/termux-packages-24/
https://mirrors.aliyun.com/termux/termux-packages-24/
https://mirrors.huaweicloud.com/termux/termux-packages-24/
"
    
    FASTEST_MIRROR=""
    FASTEST_TIME=999999
    
    for mirror in $MIRRORS; do
        log_info "测试镜像源: $mirror"
        
        # 使用curl测试下载速度
        if command -v curl >/dev/null 2>&1; then
            time_taken=$(curl -o /dev/null -s -w '%{time_total}' --connect-timeout 10 --max-time 30 "${mirror}dists/stable/Release" 2>/dev/null || echo "999999")
        else
            # 如果没有curl，使用wget
            start_time=$(date +%s)
            if wget -q --timeout=10 --tries=1 -O /dev/null "${mirror}dists/stable/Release" 2>/dev/null; then
                end_time=$(date +%s)
                time_taken=$((end_time - start_time))
            else
                time_taken=999999
            fi
        fi
        
        # 转换为整数比较
        time_int=$(echo "$time_taken" | cut -d. -f1)
        if [ "$time_int" -lt "$FASTEST_TIME" ] && [ "$time_int" -lt "10" ]; then
            FASTEST_TIME=$time_int
            FASTEST_MIRROR=$mirror
        fi
        
        log_info "响应时间: ${time_taken}秒"
    done
    
    if [ -n "$FASTEST_MIRROR" ]; then
        log_success "选择最快镜像源: $FASTEST_MIRROR"
        
        # 使用最快的镜像源
        cat > "$PREFIX/etc/apt/sources.list" << EOF
# 自动选择的最快镜像源
deb ${FASTEST_MIRROR} stable main
EOF
    else
        log_warning "所有镜像源测试失败，使用默认清华源"
        cat > "$PREFIX/etc/apt/sources.list" << EOF
# 清华大学镜像源（默认）
deb https://mirrors.tuna.tsinghua.edu.cn/termux/termux-packages-24/ stable main
EOF
    fi
}

# 更新包管理器
update_packages() {
    log_step "更新包管理器和已安装包..."
    
    # 清理包缓存
    pkg clean
    
    # 更新包列表
    if pkg update -y; then
        log_success "包列表更新完成"
    else
        log_error "包列表更新失败"
        exit 1
    fi
    
    # 升级已安装包
    log_info "开始升级已安装的包..."
    if pkg upgrade -y; then
        log_success "包升级完成"
    else
        log_warning "包升级过程中有警告，继续安装..."
    fi
}

# 安装基础工具
install_basic_tools() {
    log_step "安装Python和基础开发工具..."
    
    log_info "安装 python..."
    if pkg install python -y; then
        log_success "python 安装成功"
    else
        log_error "python 安装失败"
        exit 1
    fi
    
    log_info "安装 python-pip..."
    if pkg install python-pip -y; then
        log_success "python-pip 安装成功"
    else
        log_error "python-pip 安装失败"
        exit 1
    fi
    
    log_info "安装 clang..."
    if pkg install clang -y; then
        log_success "clang 安装成功"
    else
        log_error "clang 安装失败"
        exit 1
    fi
    
    log_info "安装 make..."
    if pkg install make -y; then
        log_success "make 安装成功"
    else
        log_error "make 安装失败"
        exit 1
    fi
    
    log_info "安装 cmake..."
    if pkg install cmake -y; then
        log_success "cmake 安装成功"
    else
        log_error "cmake 安装失败"
        exit 1
    fi
    
    log_info "安装 rust..."
    if pkg install rust -y; then
        log_success "rust 安装成功"
    else
        log_error "rust 安装失败"
        exit 1
    fi
    
    log_info "安装 pkg-config..."
    if pkg install pkg-config -y; then
        log_success "pkg-config 安装成功"
    else
        log_warning "pkg-config 安装失败，继续..."
    fi
}

# 安装系统依赖库
install_system_deps() {
    log_step "安装系统依赖库..."
    
    log_info "安装 openssl..."
    if pkg install openssl -y; then
        log_success "openssl 安装成功"
    else
        log_warning "openssl 安装失败，继续..."
    fi
    
    log_info "安装 openssl-dev..."
    if pkg install openssl-dev -y; then
        log_success "openssl-dev 安装成功"
    else
        log_warning "openssl-dev 安装失败，继续..."
    fi
    
    log_info "安装 libffi..."
    if pkg install libffi -y; then
        log_success "libffi 安装成功"
    else
        log_warning "libffi 安装失败，继续..."
    fi
    
    log_info "安装 libffi-dev..."
    if pkg install libffi-dev -y; then
        log_success "libffi-dev 安装成功"
    else
        log_warning "libffi-dev 安装失败，继续..."
    fi
    
    log_info "安装 libjpeg-turbo..."
    if pkg install libjpeg-turbo -y; then
        log_success "libjpeg-turbo 安装成功"
    else
        log_warning "libjpeg-turbo 安装失败，继续..."
    fi
    
    log_info "安装 libpng..."
    if pkg install libpng -y; then
        log_success "libpng 安装成功"
    else
        log_warning "libpng 安装失败，继续..."
    fi
    
    log_info "安装 zlib..."
    if pkg install zlib -y; then
        log_success "zlib 安装成功"
    else
        log_warning "zlib 安装失败，继续..."
    fi
    
    log_info "安装 zlib-dev..."
    if pkg install zlib-dev -y; then
        log_success "zlib-dev 安装成功"
    else
        log_warning "zlib-dev 安装失败，继续..."
    fi
    
    log_info "安装 libxml2..."
    if pkg install libxml2 -y; then
        log_success "libxml2 安装成功"
    else
        log_warning "libxml2 安装失败，继续..."
    fi
    
    log_info "安装 libxml2-dev..."
    if pkg install libxml2-dev -y; then
        log_success "libxml2-dev 安装成功"
    else
        log_warning "libxml2-dev 安装失败，继续..."
    fi
    
    log_info "安装 libxslt..."
    if pkg install libxslt -y; then
        log_success "libxslt 安装成功"
    else
        log_warning "libxslt 安装失败，继续..."
    fi
    
    log_info "安装 libxslt-dev..."
    if pkg install libxslt-dev -y; then
        log_success "libxslt-dev 安装成功"
    else
        log_warning "libxslt-dev 安装失败，继续..."
    fi
}

# 配置Python包源（多源加速）
configure_pip() {
    log_step "配置Python包管理器高速镜像源..."
    
    # 创建pip配置目录
    mkdir -p ~/.config/pip
    
    # 配置pip使用多个高速镜像，自动选择最快的
    cat > ~/.config/pip/pip.conf << EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/
extra-index-url = 
    https://mirrors.aliyun.com/pypi/simple/
    https://pypi.mirrors.ustc.edu.cn/simple/
    https://mirrors.huaweicloud.com/repository/pypi/simple/
trusted-host = 
    pypi.tuna.tsinghua.edu.cn
    mirrors.aliyun.com
    pypi.mirrors.ustc.edu.cn
    mirrors.huaweicloud.com
timeout = 60
retries = 3

[install]
trusted-host = 
    pypi.tuna.tsinghua.edu.cn
    mirrors.aliyun.com
    pypi.mirrors.ustc.edu.cn
    mirrors.huaweicloud.com
EOF
    
    if [ $? -eq 0 ]; then
        log_success "pip高速镜像源配置完成"
    else
        log_error "pip镜像源配置失败"
        exit 1
    fi
    
    # 升级pip
    log_info "升级pip到最新版本..."
    if python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/; then
        log_success "pip升级完成"
    else
        log_warning "pip升级失败，继续使用当前版本"
    fi
}

# 安装Python加密库（优化版）
install_crypto_libs() {
    log_step "安装Python加密库（高速下载）..."
    
    # 清理pip缓存
    log_info "清理pip缓存..."
    python -m pip cache purge
    
    # 设置环境变量
    export CARGO_BUILD_TARGET="$(rustc -Vv | grep host | cut -d' ' -f2)" 2>/dev/null || true
    export PYO3_CROSS_LIB_DIR="$PREFIX/lib"
    
    # 使用清华源安装cryptography
    log_info "安装 cryptography 库（使用清华大学镜像）..."
    log_info "⏳ 这可能需要几分钟时间，请耐心等待..."
    
    # 尝试多个镜像源安装cryptography
    CRYPTO_INSTALLED=false
    
    # 清华源
    if ! $CRYPTO_INSTALLED; then
        log_info "尝试清华大学镜像源..."
        if python -m pip install cryptography -i https://pypi.tuna.tsinghua.edu.cn/simple/ --no-cache-dir --timeout 60; then
            log_success "cryptography 安装成功（清华源）"
            CRYPTO_INSTALLED=true
        fi
    fi
    
    # 中科大源
    if ! $CRYPTO_INSTALLED; then
        log_info "尝试中科大镜像源..."
        if python -m pip install cryptography -i https://pypi.mirrors.ustc.edu.cn/simple/ --no-cache-dir --timeout 60; then
            log_success "cryptography 安装成功（中科大源）"
            CRYPTO_INSTALLED=true
        fi
    fi
    
    # 阿里源
    if ! $CRYPTO_INSTALLED; then
        log_info "尝试阿里云镜像源..."
        if python -m pip install cryptography -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir --timeout 60; then
            log_success "cryptography 安装成功（阿里源）"
            CRYPTO_INSTALLED=true
        fi
    fi
    
    # 预编译版本
    if ! $CRYPTO_INSTALLED; then
        log_warning "尝试预编译版本..."
        if python -m pip install --only-binary=all cryptography -i https://pypi.tuna.tsinghua.edu.cn/simple/; then
            log_success "cryptography 预编译版本安装成功"
            CRYPTO_INSTALLED=true
        fi
    fi
    
    if ! $CRYPTO_INSTALLED; then
        log_error "cryptography 安装失败"
        exit 1
    fi
    
    # 安装pycryptodome（多源尝试）
    log_info "安装 pycryptodome 库..."
    PYCRYPTO_INSTALLED=false
    
    # 清华源
    if ! $PYCRYPTO_INSTALLED; then
        log_info "尝试清华大学镜像源..."
        if python -m pip install pycryptodome -i https://pypi.tuna.tsinghua.edu.cn/simple/ --no-cache-dir --timeout 60; then
            log_success "pycryptodome 安装成功（清华源）"
            PYCRYPTO_INSTALLED=true
        fi
    fi
    
    # 中科大源
    if ! $PYCRYPTO_INSTALLED; then
        log_info "尝试中科大镜像源..."
        if python -m pip install pycryptodome -i https://pypi.mirrors.ustc.edu.cn/simple/ --no-cache-dir --timeout 60; then
            log_success "pycryptodome 安装成功（中科大源）"
            PYCRYPTO_INSTALLED=true
        fi
    fi
    
    # 阿里源
    if ! $PYCRYPTO_INSTALLED; then
        log_info "尝试阿里云镜像源..."
        if python -m pip install pycryptodome -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir --timeout 60; then
            log_success "pycryptodome 安装成功（阿里源）"
            PYCRYPTO_INSTALLED=true
        fi
    fi
    
    if ! $PYCRYPTO_INSTALLED; then
        log_error "pycryptodome 安装失败"
        exit 1
    fi
}

# 验证安装
verify_installation() {
    log_step "验证安装结果..."
    
    # 验证cryptography
    log_info "验证 cryptography..."
    if python -c "from cryptography.fernet import Fernet; from cryptography.hazmat.primitives.ciphers import Cipher; print('cryptography 验证成功')" 2>/dev/null; then
        log_success "✅ cryptography 验证通过"
    else
        log_error "❌ cryptography 验证失败"
        exit 1
    fi
    
    # 验证pycryptodome
    log_info "验证 pycryptodome..."
    if python -c "from Crypto.Cipher import AES, ChaCha20, Salsa20; print('pycryptodome 验证成功')" 2>/dev/null; then
        log_success "✅ pycryptodome 验证通过"
    else
        log_error "❌ pycryptodome 验证失败"
        exit 1
    fi
    
    # 显示版本信息
    log_info "已安装库的版本信息:"
    echo "----------------------------------------"
    python -c "import cryptography; print(f'cryptography: {cryptography.__version__}')" 2>/dev/null || echo "cryptography: 版本获取失败"
    python -c "import Crypto; print(f'pycryptodome: {Crypto.__version__}')" 2>/dev/null || echo "pycryptodome: 版本获取失败"
    echo "----------------------------------------"
}

# 显示完成信息
show_completion() {
    echo ""
    echo -e "${GREEN}=================================================================="
    echo -e "🎉 S7ENC 依赖安装完成！"
    echo -e "=================================================================="
    echo -e "${NC}"
    echo -e "${WHITE}✅ 安装成功的组件:${NC}"
    echo -e "   📦 阿里云镜像源"
    echo -e "   🐍 Python 解释器"
    echo -e "   🔧 开发工具链"
    echo -e "   📚 系统依赖库"
    echo -e "   🔐 cryptography 加密库"
    echo -e "   🛡️ pycryptodome 加密库"
    echo ""
    echo -e "${WHITE}🚀 下一步:${NC}"
    echo -e "   1. 下载 S7ENC 加密程序(开源地址：https://github.com/stop666two/S7ENC)"
    echo -e "   2. 运行: ${CYAN}python s7enc.py${NC}"
    echo -e "   3. 享受七层专业加密服务！"
    echo ""
    echo -e "${WHITE}💡 提示:${NC}"
    echo -e "   • 程序支持中文、emoji等所有Unicode字符"
    echo -e "   • 文件名使用π和e常数生成的20位随机数"
    echo -e "   • 七层加密提供军用级安全保护"
    echo ""
    echo -e "${YELLOW}⚠️ 免责声明:${NC}"
    echo -e "   本软件仅供学习研究使用，请合法合规使用"
    echo ""
    log_success "安装脚本执行完成！"
}

# 错误处理函数
handle_error() {
    local exit_code=$?
    echo ""
    log_error "安装过程中发生错误（退出码: $exit_code）"
    echo ""
    echo -e "${YELLOW}🔧 故障排除建议:${NC}"
    echo -e "   1. 检查网络连接是否稳定"
    echo -e "   2. 确保Termux应用是最新版本"
    echo -e "   3. 重新运行此脚本"
    echo -e "   4. 手动执行失败的命令进行调试"
    echo ""
    echo -e "${CYAN}📞 获取帮助:${NC}"
    echo -e "   如需技术支持，请联系开发者"
    echo ""
    exit $exit_code
}

# 用户确认函数
user_confirm() {
    echo ""
    echo -e "${YELLOW}📋 即将安装以下组件:${NC}"
    echo -e "   • 阿里云镜像源（加速下载）"
    echo -e "   • Python 开发环境"
    echo -e "   • 系统依赖库"
    echo -e "   • cryptography 加密库"
    echo -e "   • pycryptodome 加密库"
    echo ""
    echo -e "${YELLOW}⏱️ 预计安装时间: 10~25分钟${NC}"
    echo -e "${YELLOW}📱 所需存储空间: ~200MB${NC}"
    echo ""
    printf "🤔 是否继续安装？[Y/n]: "
    read -r REPLY
    echo ""
    if [ "$REPLY" = "n" ] || [ "$REPLY" = "N" ]; then
        log_info "用户取消安装"
        exit 0
    fi
}

# 主函数
main() {
    # 设置错误处理 - 兼容不同Shell
    if [ -n "$BASH_VERSION" ]; then
        trap handle_error ERR
        set -e
    else
        set -e
    fi
    
    # 显示横幅
    show_banner
    
    # 用户确认
    user_confirm
    
    # 执行安装步骤
    log_info "开始执行S7ENC依赖安装...(开源地址：https://github.com/stop666two/S7ENC)"
    echo ""
    
    check_network
    check_termux
    backup_sources
    test_mirror_speed  # 新增：测试并选择最快镜像源
    update_packages
    install_basic_tools
    install_system_deps
    configure_pip
    install_crypto_libs
    verify_installation
    
    # 显示完成信息
    show_completion
}

# 运行主函数
main "$@"