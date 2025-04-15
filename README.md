# Ứng dụng Lập kế hoạch Chuyến đi

## Giới thiệu

Ứng dụng này sử dụng kiến trúc đa tác nhân (multi-agent) với ADK và giao thức A2A. Các agent (được viết bằng FastAPI) giao tiếp với nhau để xây dựng một kế hoạch chuyến đi gồm 1 agent điều phối, 1 agent search internet, 1 agent lên lịch trình tham quan, 1 agent lên kế hoạch ẩm thực và 1 agent đề xuất chỗ ở. Giao diện người dùng được xây dựng bằng Streamlit. Dùng các model openAI 4o mini, gemini, grok, claude 3.7.

## Cấu trúc dự án

- **agents/**: Chứa các agent riêng biệt:
  - `orchestrator_agent/`: Agent điều phối tổng hợp kết quả từ các agent con.
  - `search_agent/`: Agent tìm kiếm thông tin thực tế (điểm tham quan, nhà hàng, khách sạn).
  - `entertainment_agent/`: Agent lập lịch trình vui chơi.
  - `meal_agent/`: Agent lập kế hoạch ẩm thực.
  - `stay_agent/`: Agent gợi ý chỗ ở.
- **common/**: Mã dùng chung cho giao tiếp A2A và cấu hình.
  - `a2a_server.py`: Server FastAPI cơ bản cho các agent.
  - `a2a_client.py`: Client để giao tiếp giữa các agent.
  - `config.py`: Quản lý cấu hình và biến môi trường.
- **travel_ui.py**: Giao diện frontend (Streamlit).
- **requirements.txt**: Danh sách các thư viện phụ thuộc.
- **.env.template**: Mẫu file cấu hình môi trường.
- **README.md**: Hướng dẫn chạy ứng dụng.

## Hướng dẫn cài đặt và chạy

1. **Tạo môi trường ảo và cài đặt thư viện:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Trên Linux/Mac (Windows: .venv\Scripts\activate)
   pip install -r requirements.txt
   ```

2. **Thiết lập môi trường:**

   ```bash
   # Sao chép file môi trường mẫu
   cp .env.template .env

   # Chỉnh sửa file .env với các thông tin cần thiết:
   # - Thêm API keys cho các dịch vụ (OpenAI, Gemini, Claude)
   # - Điều chỉnh URL các agent nếu cần
   # - Cấu hình các thông số model và ứng dụng
   ```

3. **Chạy các agent (mỗi agent mở 1 terminal riêng):**

   ```bash
   # Chạy Search Agent (port 8001)
   python -m agents.search_agent

   # Chạy Entertainment Agent (port 8002)
   python -m agents.entertainment_agent

   # Chạy Meal Agent (port 8003)
   python -m agents.meal_agent

   # Chạy Stay Agent (port 8004)
   python -m agents.stay_agent

   # Chạy Orchestrator Agent (port 8000)
   python -m agents.orchestrator_agent
   ```

4. **Chạy giao diện người dùng (Streamlit):**

   ```bash
   streamlit run travel_ui.py
   ```

   Mở trình duyệt và truy cập vào địa chỉ hiển thị (thường là http://localhost:8501).

5. **Sử dụng ứng dụng:**
   - Nhập các thông tin chuyến đi: điểm đến, ngày đi/về, số người và chi phí trên mỗi người.
   - Nhấn "Lập kế hoạch" để hệ thống gọi Orchestrator, từ đó gọi lần lượt các agent con.
   - Kết quả (lịch trình, kế hoạch ẩm thực, gợi ý chỗ ở) sẽ được hiển thị trên giao diện Streamlit.

## Biến môi trường

Các biến môi trường quan trọng trong file `.env`:

- **API Keys:**

  - `OPENAI_API_KEY`: API key cho OpenAI
  - `GEMINI_API_KEY`: API key cho Google Gemini
  - `CLAUDE_API_KEY`: API key cho Anthropic Claude
  <!-- - `OLLAMA_API_URL`: URL cho Ollama API (mặc định: http://localhost:11434) -->

- **URL Các Agent:**

  - `ORCHESTRATOR_URL`: URL của agent điều phối
  - `SEARCH_AGENT_URL`: URL của agent tìm kiếm
  - `ENTERTAINMENT_AGENT_URL`: URL của agent lên lịch trình
  - `MEAL_AGENT_URL`: URL của agent kế hoạch ẩm thực
  - `STAY_AGENT_URL`: URL của agent gợi ý chỗ ở

- **Cấu hình Model:**

  - `DEFAULT_MODEL`: Model mặc định (vd: gpt-4)
  - `TEMPERATURE`: Độ sáng tạo của model (0-1)
  - `MAX_TOKENS`: Số token tối đa cho mỗi lần gọi

- **Cài đặt ứng dụng:**
  - `DEBUG`: Chế độ debug (true/false)
  - `LOG_LEVEL`: Mức độ log (DEBUG/INFO/WARNING/ERROR)

## Lưu ý

- Đảm bảo đã cấu hình đúng các API key trong file `.env` trước khi chạy ứng dụng.
- Kiểm tra các port mặc định (8000-8004) không bị chiếm dụng.
- Trong môi trường production, nên thay đổi các URL agent thành địa chỉ thực tế của server.
- Đảm bảo bảo mật file `.env` và không commit nó lên git.

## Kết luận

Mã nguồn trên cung cấp một ví dụ đầy đủ về cách xây dựng ứng dụng lập kế hoạch chuyến đi đa tác nhân sử dụng ADK, A2A, FastAPI và Streamlit. Bạn có thể mở rộng và tích hợp thêm chức năng (ví dụ gọi API tìm kiếm thực, kết nối với các model AI thật) theo nhu cầu thực tế. Nếu có bất kỳ câu hỏi hay cần hỗ trợ thêm, hãy cho tôi biết!

---

<!-- ```
trip_planner/
├── agents/
│   ├── orchestrator_agent/
│   │   ├── __main__.py          # Khởi chạy FastAPI cho orchestrator (port 8000)
│   │   ├── task_manager.py      # Logic gọi các agent con và tổng hợp kết quả
│   │   └── agent.json           # Metadata của orchestrator agent
│   ├── search_agent/
│   │   ├── __main__.py          # Khởi chạy FastAPI cho search agent (port 8001)
│   │   ├── agent_logic.py       # Hàm logic thực hiện “tìm kiếm trên web”
│   │   └── agent.json           # Metadata của search agent
│   ├── entertainment_agent/
│   │   ├── __main__.py          # Khởi chạy FastAPI cho entertainment agent (port 8002)
│   │   ├── agent.py             # Logic lập lịch trình vui chơi
│   │   └── agent.json           # Metadata của entertainment agent
│   ├── meal_agent/
│   │   ├── __main__.py          # Khởi chạy FastAPI cho meal agent (port 8003)
│   │   ├── agent.py             # Logic lập kế hoạch ẩm thực
│   │   └── agent.json           # Metadata của meal agent
│   └── stay_agent/
│       ├── __main__.py          # Khởi chạy FastAPI cho stay agent (port 8004)
│       ├── agent.py             # Logic gợi ý chỗ ở phù hợp
│       └── agent.json           # Metadata của stay agent
├── common/
│   ├── a2a_server.py            # Tạo FastAPI app với endpoint /run cho mỗi agent
│   └── a2a_client.py            # Hàm tiện ích gọi API của các agent khác (A2A client)
├── travel_ui.py                 # Giao diện Streamlit (frontend)
├── requirements.txt             # Danh sách các thư viện cần cài đặt
├── Dockerfile                   # Dockerfile dùng cho toàn bộ dự án
├── docker-compose.yml           # Định nghĩa các service dùng Docker Compose
└── README.md                    # Hướng dẫn triển khai

``` -->
