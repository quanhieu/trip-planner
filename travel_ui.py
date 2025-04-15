# travel_ui.py
import streamlit as st
import requests
import datetime

st.title("Ứng dụng Lập Kế hoạch Chuyến đi")

# Form nhập liệu
with st.form(key='trip_form'):
    destination = st.text_input("Đi chơi đâu?", "Đà Nẵng")
    start_date = st.date_input("Ngày đi", datetime.date.today())
    end_date = st.date_input("Ngày về", datetime.date.today() + datetime.timedelta(days=3))
    num_people = st.number_input("Tổng số người đi", min_value=1, value=2)
    budget_per_person = st.number_input("Chi phí trên mỗi người (VND)", min_value=100000, value=500000, step=100000)
    submit_button = st.form_submit_button(label='Lập kế hoạch')

if submit_button:
    payload = {
        "destination": destination,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "num_people": num_people,
        "budget_per_person": budget_per_person
    }
    st.info("Đang xây dựng kế hoạch, vui lòng chờ...")
    try:
        # Gọi Orchestrator Agent (port 8000)
        response = requests.post("http://localhost:8000/run", json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        st.success("Kế hoạch của bạn đã sẵn sàng!")
        
        st.subheader("Lịch trình:")
        itinerary = result.get("itinerary", [])
        if itinerary:
            for day in itinerary:
                st.write(f"**Day {day.get('day', '')}:**")
                for activity in day.get("activities", []):
                    st.write(f"- *{activity.get('time', '')}*: {activity.get('activity', '')}")
        else:
            st.write("Không có lịch trình chi tiết.")
        
        st.subheader("Kế hoạch Ẩm thực:")
        meals = result.get("meals", [])
        if meals:
            for meal in meals:
                st.write(f"**Day {meal.get('day', '')}:** Trưa - {meal.get('lunch', '')} | Tối - {meal.get('dinner', '')}")
        else:
            st.write("Không có kế hoạch ẩm thực chi tiết.")
        
        st.subheader("Đề xuất Chỗ ở:")
        stays = result.get("stays", {})
        if stays:
            st.write(f"- **Tên**: {stays.get('name', '')}")
            st.write(f"- **Giá/đêm**: {stays.get('price_per_night', '')} VND")
            st.write(f"- **Ghi chú**: {stays.get('note', '')}")
        else:
            st.write("Không có đề xuất chỗ ở.")
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {str(e)}")
