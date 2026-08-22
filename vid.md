# 🎬 DAYFLOW HRMS — Demo Video Script

## Before Recording

```bash
# Run this FIRST in your terminal:
python3 seed_demo.py
# Then start Odoo:
odoo -d your_db
```

Open your browser to `http://localhost:8069`

---

## Step 1: Sign Up (show the form)

| Action | Details |
|--------|---------|
| **URL** | `http://localhost:8069/web/signup` |
| **What to fill** | Email: `newuser@dayflow.demo`, Password: `test1234`, Employee ID: `EMP99`, Role: `Employee` |
| **Click** | "Sign Up" |
| **Say** | *"New employees self-register with their Employee ID and role — HR or Employee. Email verification is sent automatically."* |
| **Show** | The signup form with Employee ID and Role dropdown |

> ⚠️ Don't try to log in as the new user — just show the form works, then move on.

---

## Step 2: Employee Dashboard

| Action | Details |
|--------|---------|
| **URL** | `http://localhost:8069/web/login` |
| **Login** | `emp1@dayflow.demo` / `emp123` |
| **You land on** | `http://localhost:8069/dayflow/dashboard` (auto) |
| **What to show** | 3 cards: **Attendance: Present** (green), **Leave: 1 Pending**, **Payroll: ₹48,000** |
| **Say** | *"Each employee sees a personalized dashboard with live attendance status, pending leave count, and their latest salary — all computed from Odoo's database in real time."* |
| **Show** | Point to each card one by one. Hover over the green "Present" badge. |

---

## Step 3: Check Attendance

| Action | Details |
|--------|---------|
| **Click** | "Dayflow" menu in top bar → "My Attendance" |
| **URL** | `http://localhost:8069/web#action=dayflow_hrms.action_dayflow_my_attendance` |
| **What to show** | List with Employee One, check-in 9:00 AM, check-out 6:00 PM |
| **Say** | *"Attendance is tracked daily with check-in and check-out times."* |
| **Show** | The attendance list row showing today's record |

---

## Step 4: Apply Leave

| Action | Details |
|--------|---------|
| **Click** | "Dayflow" → "Apply / My Leave" |
| **URL** | `http://localhost:8069/web#action=dayflow_hrms.action_dayflow_my_leave` |
| **Click** | "New" button (top-left) |
| **What to fill** | Description: `Team outing`, Start Date: pick next Monday, End Date: pick next Tuesday |
| **Click** | "Save" |
| **What to show** | Leave appears with **"Pending"** state badge (yellow) |
| **Say** | *"Employees can apply for leave directly. It enters a pending state awaiting HR approval."* |
| **Show** | The yellow "Pending" badge on the leave record |

---

## Step 5: Switch to HR

| Action | Details |
|--------|---------|
| **Click** | Avatar (top-right) → "Log out" |
| **URL** | `http://localhost:8069/web/login` |
| **Login** | `hr@dayflow.demo` / `hr123` |
| **Click** | "Dayflow" → "Dashboard" |
| **URL** | `http://localhost:8069/dayflow/dashboard` |
| **What to show** | Greeting: "Good morning, Demo HR Admin 👋" with purple **"HR view"** badge, Employee table with 4 rows |
| **Say** | *"HR sees a consolidated view of all employees — their attendance status, pending requests, and can drill into any employee's profile."* |
| **Show** | Point to the employee table — each row has colored attendance pills + pending leave count |

---

## Step 6: Approve Leave

| Action | Details |
|--------|---------|
| **Click** | "Dayflow" → "Leave Approvals" |
| **URL** | `http://localhost:8069/web#action=dayflow_hrms.action_dayflow_leave_approvals` |
| **What to show** | Employee One's "Family function" leave (Pending) |
| **Click** | On the row to open the leave request |
| **Click** | "Approve" button (top of form) |
| **What to show** | State badge changes from **"Pending"** (yellow) → **"Approved"** (green) |
| **Say** | *"HR can review and approve or reject leave requests with a single click."* |
| **Show** | The color change from yellow to green |

---

## Step 7: View Payroll (HR)

| Action | Details |
|--------|---------|
| **Click** | "Dayflow" → "Payroll" |
| **URL** | `http://localhost:8069/web#action=dayflow_hrms.action_payroll` |
| **What to show** | List of all 4 employees with columns |
| **Click** | Employee One's row to open form |
| **What to show** | Form view: Basic ₹45,000, Allowances ₹5,000, Deductions ₹2,000, Net ₹48,000 |
| **Say** | *"Payroll is fully computed — HR can edit the salary structure and net salary recalculates automatically. Basic salary plus allowances minus deductions equals net salary."* |
| **Show** | Point to each field. Optionally edit Basic Salary to show net updates live. |

---

## Step 8: Employee Payroll (Read-Only)

| Action | Details |
|--------|---------|
| **Click** | Avatar → "Log out" |
| **URL** | `http://localhost:8069/web/login` |
| **Login** | `emp2@dayflow.demo` / `emp123` |
| **Click** | "Dayflow" → "Payroll" |
| **URL** | `http://localhost:8069/web#action=dayflow_hrms.action_payroll` |
| **What to show** | Same payroll list but **no "New" button** — can only view, not edit |
| **Say** | *"Employees see their own payroll as read-only — they can view but not edit their salary structure. HR has full control."* |
| **Show** | Click on a row — form opens in read-only mode, no edit/save buttons |

---

## 📋 Quick Copy-Paste URLs

| Step | Endpoint |
|------|----------|
| Signup | `http://localhost:8069/web/signup` |
| Login | `http://localhost:8069/web/login` |
| Dashboard | `http://localhost:8069/dayflow/dashboard` |
| My Attendance | `http://localhost:8069/web#action=dayflow_hrms.action_dayflow_my_attendance` |
| Apply Leave | `http://localhost:8069/web#action=dayflow_hrms.action_dayflow_my_leave` |
| Leave Approvals | `http://localhost:8069/web#action=dayflow_hrms.action_dayflow_leave_approvals` |
| Payroll | `http://localhost:8069/web#action=dayflow_hrms.action_payroll` |

---

## ⏱️ Time Check

| Step | Duration | Running Total |
|------|----------|---------------|
| Step 1 | ~30 sec | 0:30 |
| Step 2 | ~30 sec | 1:00 |
| Step 3 | ~20 sec | 1:20 |
| Step 4 | ~30 sec | 1:50 |
| Step 5 | ~20 sec | 2:10 |
| Step 6 | ~30 sec | 2:40 |
| Step 7 | ~30 sec | 3:10 |
| Step 8 | ~20 sec | **3:30** |

**Total: ~3.5 minutes** ✅
