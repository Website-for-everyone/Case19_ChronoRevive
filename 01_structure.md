# АРХИТЕКТУРА И СПЕЦИФИКАЦИЯ ПРОЕКТА: CHRONOREVIVE

> **Проект:** ChronoRevive — Ателье реставрации винтажных часов и сложной механики  
> **Клиент / Заказчик:** ChronoRevive Haute Horlogerie Atelier (@chronorevive_atelier)  
> **Чек проекта:** 190,000 ₽ | **Срок:** 14 дней (Дедлайн: 2026-11-25)  
> **Дедлайн MVP (80%):** 2026-11-22  
> **Тип договора:** Договор СМЗ с ИП (Чек «Мой Налог»)

---

## 🛠 Технологический стек
- **Frontend / UI:** Vanilla JS, HTML5 Canvas 2D Horological Simulation, CSS3 Haute Horlogerie Aesthetic (Royal Navy `#0B132B`, Brushed Steel `#C0C0C0`, Rose Gold `#B76E79`, Warm Ivory `#FAF9F6`)
- **Интерактивные модули:** 
  - Анимированный швейцарский анкерный спуск (Swiss Lever Escapement) с симуляцией частоты полуколебаний (18,000 – 36,000 пк/час) и тикающим звуком
  - Макро-слайдер реставрации «До / После» (Corroded Vintage vs Restored Mirror Finish)
  - Онлайн-портал трекинга стадий реставрации по номеру заказа (`CR-8492`)
  - Форма экспресс-оценки стоимости реставрации по фото
- **Backend / Web API:** Python 3.12, FastAPI, Uvicorn, Pydantic v2
- **Telegram Bot:** Python 3.12, Aiogram 3.x, FSM Прием фото повреждений, Авто-вердикт мастера, Трекинг статуса заказа
- **Хранилище данных:** In-Memory Horological Database & Appraisal Dispatcher

---

## 🏛 Архитектурная схема
```
[ Владелец раритетных часов / Коллекционер ] 
          │ 
          ├──────────────► [ Веб-интерфейс ChronoRevive (Порт 3019) ]
          │                  - Анимированный анкерный спуск (Canvas Escapement)
          │                  - Макро-сравнение реставрации До / После
          │                  - Форма онлайн-оценки по фото механизма
          │                  - Трекер этапов ремонта (CR-8492)
          │                  - REST API /api/showcase-models, /api/track-order/{id}, /api/appraisal-request
          │
          └──────────────► [ Telegram-бот @ChronoReviveBot ]
                             - Прием фото поломки и циферблата
                             - Автоматический расчет предварительной сметы
                             - Быстрый трекинг заказа (/track CR-8492)
                             - Диспетчер лидов в @Idrisov_prod
```

---

## 🔐 Переменные окружения (.env.example)
```env
BOT_TOKEN=8217851677:AAHN34TMuC1P4e6SppuazFN8BIiLHa_RyIc
TELEGRAM_OWNER_ID=1387913438
TELEGRAM_OWNER_USERNAME=@Idrisov_prod
PORT=3019
API_PORT=8019
WEBHOOK_URL=http://localhost:8019/webhook
```

---

## 🔗 Ресурсы и ссылки
- **Порт Web/API:** `3019` (Web UI), `8019` (API)
- **Telegram Bot:** `@ChronoReviveBot`
- **Код проекта:** `C:\Users\danie\OneDrive\Desktop\Idrisov\Idrisov_OS\01_Business\Projects\Case19_ChronoRevive\`
