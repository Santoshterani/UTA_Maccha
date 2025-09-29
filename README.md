# 🍵 Uta Maccha – Online Food Ordering Platform  

**Uta Maccha** is a full-stack web application built with **Django** that allows customers to browse restaurant menus, add items to cart, place secure orders with Razorpay integration, and track past orders. Restaurants can manage menus and update order statuses in real time.  

---

## ✨ Features  

### 👩‍💻 Customer Features
- Browse restaurants and their menus  
- Add items to cart (with images & prices)  
- Secure checkout with Razorpay payment gateway  
- View order summary with receipt-style UI  
- Track past orders with images & status updates  
- Reorder previous orders in one click  

### 🏪 Restaurant Features
- Manage restaurant profile and menus  
- Add/update food items with images & prices  
- Track incoming orders  
- Update order status (Pending → Preparing → Completed/Cancelled)  

### ⚙️ System Features
- Glassmorphism + dark gradient **modern UI**  
- Session-based cart system  
- Order history with **unique Order IDs & timestamps**  
- Integrated **payment gateway** (Razorpay)  
- Django ORM models for Restaurant, Customer, Item, Cart, Order  

---

## 🛠 Tech Stack  

- **Backend:** Django, Python  
- **Frontend:** HTML, CSS (Glassmorphism + Dark Gradient UI)  
- **Database:** SQLite (default, can be swapped with PostgreSQL/MySQL)  
- **Payment Gateway:** Razorpay  
- **Version Control:** Git & GitHub  

---

## 📂 Project Structure  

<img width="382" height="640" alt="image" src="https://github.com/user-attachments/assets/9b020f91-94d1-4cfe-bb57-d2978d56d317" />

## ⚡ Installation & Setup  

1. Clone the repository:  
   ```bash
   git clone https://github.com/<your-username>/Uta_Maccha.git
   cd Uta_Maccha

2. Create a virtual environment & activate:

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


3. Install dependencies:

pip install -r requirements.txt


4. Apply migrations:

python manage.py migrate


5. Create a superuser (for admin/restaurant):

python manage.py createsuperuser


6. Run the server:

python manage.py runserver


7. Open in browser:

http://127.0.0.1:8000/


Admin dashboard interface:<img width="757" height="552" alt="image" src="https://github.com/user-attachments/assets/f5652fe3-3d32-43e0-8aad-8588bd3c5036" />

Customer dashboard:<img width="1874" height="448" alt="image" src="https://github.com/user-attachments/assets/9bb41037-fc7d-4ef3-8d0d-fc973479a3e2" />


   
