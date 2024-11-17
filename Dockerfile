# Python asosli tasvirni o'rnatish
FROM python:3.10-slim

# Ish katalogini o'rnatish
WORKDIR /usr/src/app

# Kutubxonalarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# watchmedo (watchdog) ni o'rnatish
RUN pip install watchdog

# Ilova kodini nusxalash
COPY . .

# Ilovani ishga tushirish uchun
CMD ["python", "-u", "app.py"]
