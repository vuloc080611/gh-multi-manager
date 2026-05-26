# 🚀 gh-multi-manager

> Quản lý hàng loạt GitHub repository từ command line – tiết kiệm hàng giờ đồng hồ mỗi tuần.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![tests](https://github.com/YOUR_USERNAME/gh-multi-manager/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/gh-multi-manager/actions/workflows/test.yml)

## ✨ Tính năng

- **Clone hàng loạt** tất cả repo của bạn (hoặc của tổ chức) chỉ với một lệnh.
- **Pull, commit, push** đồng loạt trên nhiều repo – hỗ trợ xử lý bất đồng bộ (nhanh hơn 5-10 lần).
- **Tạo branch mới** trên tất cả repo chỉ trong 2 giây.
- **Xem trạng thái** (dirty/clean, ahead/behind, nhánh hiện tại) dưới dạng bảng đẹp.
- **Tích hợp GitHub token** – an toàn, không lưu mật khẩu.
- **CI/CD sẵn sàng** – có GitHub Actions test tự động mỗi khi push.

## 📦 Cài đặt

```bash
# 1. Clone repo này về máy bạn (sẽ tự clone, nhưng bạn cần tạo token trước)
git clone https://github.com/YOUR_USERNAME/gh-multi-manager.git
cd gh-multi-manager

# 2. Cài đặt (khuyến nghị dùng virtual environment)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .

# 3. Set GitHub token (tạo tại https://github.com/settings/tokens, cần quyền repo)
export GITHUB_TOKEN=ghp_your_token_here   # Linux/Mac
# set GITHUB_TOKEN=ghp_your_token_here    # Windows cmd
