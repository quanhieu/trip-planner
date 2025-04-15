# Prompt: Xây dựng AI Agent với khả năng tìm kiếm web và tạo câu trả lời thông minh

Bạn là một AI Agent thông minh có khả năng tìm kiếm thông tin trên internet và tạo câu trả lời chất lượng cao dựa trên thông tin thu thập được. Hãy thực hiện các bước sau để tìm kiếm và tạo câu trả lời cho truy vấn của người dùng:

## Bước 1: Tìm kiếm thông tin sử dụng Google Custom Search API

Đầu tiên, bạn cần tìm kiếm thông tin liên quan đến truy vấn của người dùng bằng Google Custom Search API:

1. Phân tích truy vấn của người dùng để xác định từ khóa chính và thông tin cần tìm kiếm
2. Sử dụng Google Custom Search API để thực hiện tìm kiếm với các tham số sau:

   - API Key: [YOUR_API_KEY]
   - Search Engine ID: [YOUR_SEARCH_ENGINE_ID]
   - Truy vấn tìm kiếm: [Truy vấn của người dùng]
   - Số lượng kết quả: 10 (hoặc tùy chỉnh)
   - Các tham số bổ sung (nếu cần): dateRestrict, fileType, siteSearch...

3. Xử lý kết quả tìm kiếm để trích xuất thông tin quan trọng:
   - Tiêu đề trang web
   - URL
   - Đoạn trích (snippet)
   - Thời gian xuất bản (nếu có)

## Bước 2: Kết hợp LLM với kết quả tìm kiếm

Sau khi có kết quả tìm kiếm, hãy tổng hợp và phân tích thông tin để tạo câu trả lời chất lượng cao:

1. Tạo prompt cho LLM bao gồm:

   - Truy vấn gốc của người dùng
   - Thông tin từ kết quả tìm kiếm (đã được xử lý và định dạng)
   - Hướng dẫn về cách tổng hợp thông tin và tạo câu trả lời

2. Yêu cầu LLM:
   - Tổng hợp thông tin từ nhiều nguồn
   - Đảm bảo tính chính xác và cập nhật của thông tin
   - Cung cấp câu trả lời toàn diện và có cấu trúc
   - Trích dẫn nguồn thông tin (nếu cần)
   - Tránh tạo ra thông tin không có trong kết quả tìm kiếm

## Bước 3: Sử dụng Google ADK (Agent Development Kit)

Để xây dựng một AI Agent mạnh mẽ hơn, hãy tích hợp Google ADK:

1. Cài đặt Google ADK:

   ```python
   pip install google-adk
   ```

2. Thiết lập môi trường:

   ```python
   # Thiết lập API key trong file .env
   GOOGLE_API_KEY=YOUR_API_KEY_HERE
   GOOGLE_GENAI_USE_VERTEXAI=0
   ```

3. Tạo Agent với công cụ tìm kiếm:

   ```python
   from google.adk import Agent, Tool
   from google.adk.tools import google_search

   # Tạo agent với công cụ tìm kiếm Google
   agent = Agent(
       tools=[google_search.GoogleSearchTool()]
   )

   # Sử dụng agent để tạo câu trả lời
   response = agent.generate(query)
   ```

4. Tận dụng các tính năng của ADK:
   - Điều phối linh hoạt (Sequential, Parallel, Loop)
   - Kiến trúc đa agent
   - Hệ sinh thái công cụ phong phú
   - Khả năng triển khai và đánh giá

## Bước 4: Triển khai RAG (Retrieval-Augmented Generation)

Để cải thiện chất lượng câu trả lời, hãy triển khai mô hình RAG:

1. Chuẩn bị dữ liệu:

   - Làm sạch và sắp xếp dữ liệu từ kết quả tìm kiếm
   - Loại bỏ thông tin trùng lặp, lỗi thời hoặc không liên quan
   - Tổ chức thông tin theo mức độ liên quan và độ tin cậy

2. Tạo vector nhúng:

   - Chuyển đổi văn bản thành vector nhúng để hỗ trợ tìm kiếm ngữ nghĩa
   - Sử dụng mô hình nhúng phù hợp (ví dụ: OpenAI embeddings, SentenceTransformers)

3. Truy xuất thông tin:

   - Khi nhận được truy vấn, tìm kiếm các đoạn văn bản liên quan nhất
   - Kết hợp tìm kiếm dựa trên từ khóa (BM25) và tìm kiếm ngữ nghĩa (vector search)

4. Tạo câu trả lời:
   - Kết hợp truy vấn gốc và thông tin truy xuất được vào prompt cho LLM
   - Yêu cầu LLM tổng hợp thông tin và tạo câu trả lời có cấu trúc, dễ hiểu
   - Đảm bảo câu trả lời dựa trên thông tin đã truy xuất, tránh "ảo giác"

## Bước 5: Đánh giá và cải thiện

Sau khi tạo câu trả lời, hãy đánh giá chất lượng và thực hiện các cải tiến:

1. Kiểm tra tính chính xác:

   - Đảm bảo thông tin trong câu trả lời khớp với nguồn dữ liệu
   - Xác minh rằng không có thông tin sai lệch hoặc lỗi thời

2. Đánh giá tính toàn diện:

   - Câu trả lời có bao gồm tất cả các khía cạnh quan trọng của truy vấn không?
   - Có thiếu thông tin quan trọng nào không?

3. Cải thiện định dạng và cấu trúc:

   - Tổ chức câu trả lời thành các phần logic
   - Sử dụng định dạng phù hợp (đánh dấu, danh sách, bảng) để tăng khả năng đọc

4. Cung cấp nguồn thông tin:
   - Trích dẫn nguồn cho thông tin quan trọng
   - Cung cấp liên kết đến nguồn gốc nếu người dùng muốn tìm hiểu thêm

## Lưu ý quan trọng

- Đảm bảo tôn trọng giới hạn API và quản lý chi phí
- Xử lý thông tin nhạy cảm một cách an toàn và có đạo đức
- Cập nhật thường xuyên các công cụ và mô hình để đảm bảo hiệu suất tốt nhất
- Theo dõi phản hồi của người dùng để cải thiện liên tục

---

# Tích hợp Giao thức Agent2Agent (A2A) vào Hệ thống AI

## Kiến trúc A2A

A2A được xây dựng dựa trên hai loại agent chính:

1. **Client Agent**: Agent khởi tạo yêu cầu và giao nhiệm vụ[4]
2. **Remote Agent**: Agent nhận nhiệm vụ, thực thi và gửi kết quả hoặc cập nhật trạng thái lại cho Client Agent[4]

Ngoài ra, A2A tích hợp các khả năng sau:

- **Capability Discovery**: Agent đăng ký khả năng thông qua "Agent Card"[4]
- **Task Management**: Quản lý vòng đời của các tác vụ[4]
- **Collaboration**: Hỗ trợ trao đổi thông tin giữa các agent[4]
- **User Experience Negotiation**: Cho phép các agent thương lượng định dạng nội dung khi giao tiếp[4]

## Tích hợp A2A bằng Python

### 1. Cài đặt thư viện Python A2A

Bạn có thể sử dụng thư viện Python A2A để dễ dàng tích hợp giao thức này:

```python
# Cài đặt thư viện
pip install python-a2a
```

### 2. Tạo một A2A Agent Server đơn giản

```python
from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server

class EchoAgent(A2AServer):
    """Agent đơn giản phản hồi lại tin nhắn với tiền tố."""
    def handle_message(self, message):
        if message.content.type == "text":
            return Message(
                content=TextContent(text=f"Echo: {message.content.text}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

# Chạy server
if __name__ == "__main__":
    agent = EchoAgent()
    run_server(agent, host="0.0.0.0", port=5000)
```

### 3. Gửi tin nhắn đến A2A Agent

```python
from python_a2a import A2AClient, Message, TextContent, MessageRole
from python_a2a.utils import pretty_print_message

# Tạo client kết nối đến agent tương thích A2A
client = A2AClient("http://localhost:5000/a2a")

# Tạo tin nhắn đơn giản
message = Message(
    content=TextContent(text="Hello, A2A!"),
    role=MessageRole.USER
)

# Gửi tin nhắn và nhận phản hồi
response = client.send_message(message)

# Hiển thị phản hồi
pretty_print_message(response)
```

### 4. Tạo Agent sử dụng LLM

```python
import os
from python_a2a import OpenAIA2AServer, run_server

# Tạo agent sử dụng OpenAI
agent = OpenAIA2AServer(
    api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-4",
    system_prompt="You are a helpful AI assistant specialized in explaining complex topics simply."
)

# Chạy server
if __name__ == "__main__":
    run_server(agent, host="0.0.0.0", port=5000)
```

### 5. Xây dựng Agent Chain cho tác vụ phức tạp

```python
from python_a2a import A2AClient, Message, TextContent, MessageRole

# Kết nối đến các agent chuyên biệt
weather_agent = A2AClient("http://localhost:5001/a2a")
planning_agent = A2AClient("http://localhost:5002/a2a")

def plan_trip(location):
    """Kết nối nhiều agent để lập kế hoạch chuyến đi."""
    # Bước 1: Lấy thông tin thời tiết
    weather_message = Message(
        content=TextContent(text=f"What's the weather forecast for {location}?"),
        role=MessageRole.USER
    )
    weather_response = weather_agent.send_message(weather_message)

    # Bước 2: Sử dụng dữ liệu thời tiết để tạo kế hoạch chuyến đi
    planning_message = Message(
        content=TextContent(
            text=f"I'm planning a trip to {location}. Weather forecast: {weather_response.content.text}"
            f"Please suggest activities and packing recommendations."
        ),
        role=MessageRole.USER
    )
    planning_response = planning_agent.send_message(planning_message)

    return planning_response.content.text

# Sử dụng các agent đã kết nối
trip_plan = plan_trip("Tokyo")
print(trip_plan)
```

## Tích hợp A2A với FastAPI

Để xây dựng một hệ thống đa agent có thể mở rộng, bạn có thể tích hợp A2A với FastAPI:

### 1. Tạo file server A2A chung

```python
# common/a2a_server.py
from fastapi import FastAPI
import uvicorn

def create_app(agent):
    app = FastAPI()

    @app.post("/run")
    async def run(payload: dict):
        return await agent.execute(payload)

    return app
```

### 2. Tạo các agent chuyên biệt

Mỗi agent nên có cấu trúc tương tự:

```
agents/
├── host_agent/
│   ├── agent.py
│   ├── task_manager.py
│   ├── __main__.py
│   └── .well-known/
│       └── agent.json
├── flight_agent/
├── stay_agent/
└── activities_agent/
```

Mỗi agent sử dụng `google.adk.agents.Agent`, một wrapper mô hình LLM, và `Runner` để thực thi[6].

### 3. Tạo một hệ thống đa agent

Ví dụ về hệ thống đa agent cho ứng dụng lập kế hoạch du lịch:

```python
# Trong host_agent/task_manager.py
import httpx

class TaskManager:
    def __init__(self):
        self.flight_agent_url = "http://localhost:5001/run"
        self.stay_agent_url = "http://localhost:5002/run"
        self.activities_agent_url = "http://localhost:5003/run"

    async def execute(self, travel_request):
        # Gọi flight_agent
        async with httpx.AsyncClient() as client:
            flight_response = await client.post(
                self.flight_agent_url,
                json=travel_request
            )
            flight_data = flight_response.json()

        # Gọi stay_agent
        async with httpx.AsyncClient() as client:
            stay_response = await client.post(
                self.stay_agent_url,
                json=travel_request
            )
            stay_data = stay_response.json()

        # Gọi activities_agent
        async with httpx.AsyncClient() as client:
            activities_response = await client.post(
                self.activities_agent_url,
                json=travel_request
            )
            activities_data = activities_response.json()

        # Tổng hợp kết quả
        return {
            "flights": flight_data,
            "accommodations": stay_data,
            "activities": activities_data
        }
```

## Tích hợp A2A với Google ADK

Google's Agent Development Kit (ADK) là một framework mã nguồn mở được thiết kế để đơn giản hóa quy trình phát triển agent end-to-end[1]. ADK hỗ trợ việc cấu trúc các hệ thống đa agent thông qua các khái niệm phân cấp như agent cha (parent_agent) và agent con (sub_agents)[1].

### 1. Cài đặt ADK

```bash
pip install google-adk
```

### 2. Thiết lập môi trường

```bash
# Thiết lập API key trong file .env
GOOGLE_API_KEY=YOUR_API_KEY_HERE
GOOGLE_GENAI_USE_VERTEXAI=0
```

### 3. Tạo Agent với ADK và A2A

```python
from google.adk import Agent, Tool
from google.adk.tools import google_search

# Tạo agent với công cụ tìm kiếm Google
agent = Agent(
    tools=[google_search.GoogleSearchTool()]
)

# Tích hợp với FastAPI
@app.post("/agent/search")
async def agent_search(search_terms: SearchTerms):
    response = await agent.generate(search_terms.query)
    return {"response": response}
```

### 4. Tích hợp ADK với FastAPI

```python
import os
import sys
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from dotenv import load_dotenv

# Thiết lập đường dẫn
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AGENT_DIR = BASE_DIR

# Thiết lập đường dẫn DB cho sessions
SESSION_DB_URL = f"sqlite:///{os.path.join(BASE_DIR, 'sessions.db')}"

# Tạo ứng dụng FastAPI sử dụng helper của ADK
app: FastAPI = get_fast_api_app(
    agent_dir=AGENT_DIR,
    session_db_url=SESSION_DB_URL,
    allow_origins=["*"],  # Trong môi trường production, hãy giới hạn điều này
    web=True  # Bật ADK Web UI
)

# Thêm endpoint tùy chỉnh
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/agent-info")
async def agent_info():
    """Cung cấp thông tin về agent"""
    from multi_tool_agent import root_agent
    return {
        "agent_name": root_agent.name,
        "description": root_agent.description,
        "model": root_agent.model,
        "tools": [t.__name__ for t in root_agent.tools]
    }

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9999,
        reload=False
    )
```

## Triển khai RAG (Retrieval-Augmented Generation)

Để cải thiện chất lượng câu trả lời, bạn có thể triển khai mô hình RAG:

```python
from fastapi import FastAPI, Depends
from langchain.retrievers import WebSearchRetriever
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

app = FastAPI()

# Khởi tạo retriever và LLM
def get_retriever():
    return WebSearchRetriever()

def get_llm():
    return OpenAI(temperature=0)

@app.post("/rag_search")
async def rag_search(
    search_terms: SearchTerms,
    retriever = Depends(get_retriever),
    llm = Depends(get_llm)
):
    # Tạo chuỗi RAG
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )

    # Thực hiện tìm kiếm và tạo câu trả lời
    result = qa_chain.run(search_terms.query)

    return {"response": result}
```

## Ví dụ về luồng giao tiếp A2A

A2A không chỉ là việc gửi tin nhắn giữa các agent, mà còn cho phép ủy thác nhiệm vụ, cộng tác giải quyết vấn đề, và điều phối các quy trình phức tạp. Dưới đây là một số ví dụ:

### Quy trình tuyển dụng

Một người quản lý tuyển dụng có thể yêu cầu agent chính tìm kiếm ứng viên phù hợp. Agent chính sẽ sử dụng A2A để giao tiếp và ủy thác nhiệm vụ cho các agent chuyên biệt khác:

- Agent tìm nguồn ứng viên
- Agent lên lịch phỏng vấn
- Agent kiểm tra lý lịch[1]

### Sửa chữa ô tô

Người dùng báo cáo sự cố cho agent dịch vụ khách hàng. Agent này sử dụng A2A để tương tác với người dùng hoặc các agent khác trong quá trình chẩn đoán và xây dựng kế hoạch hành động để giải quyết vấn đề[1].

## Lưu ý quan trọng

1. **API Key và Xác thực**: Đảm bảo bạn đã thiết lập API key cho các dịch vụ và LLM.

2. **Xử lý bất đồng bộ**: Sử dụng `async/await` trong FastAPI để xử lý nhiều yêu cầu đồng thời.

3. **Lưu trữ lịch sử trò chuyện**: Sử dụng cơ sở dữ liệu để lưu trữ lịch sử trò chuyện.

4. **Tối ưu hóa hiệu suất**: Cân nhắc việc lưu vào bộ nhớ đệm kết quả để cải thiện thời gian phản hồi.

5. **Bảo mật**: Đảm bảo bạn không chia sẻ API key công khai và nên lưu trữ chúng trong biến môi trường.

Với các phương pháp trên, bạn có thể xây dựng một hệ thống đa agent mạnh mẽ có khả năng giao tiếp và phối hợp hiệu quả thông qua giao thức A2A của Google.
